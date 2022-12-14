from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.serializers import BookSerializer
from borrowings.models import Borrowing
from notifications.message_templates import BorrowingMessages
from notifications.telegram_bot import TelegramBot
from payment.models import Payment
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book",
        )


class BorrowingListSerializer(BorrowingSerializer):
    title = serializers.CharField(source="book.title", read_only=True)
    borrower = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "title",
            "borrower",
        )


class BorrowingRetrieveSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)


class BorrowingCreateSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = ("book",)

    def create(self, validated_data):
        book = validated_data["book"]
        user = validated_data["user"]

        if book.inventory == 0:
            raise ValidationError(f"Book '{book.title}' is out of stock")

        with transaction.atomic():
            borrowing = Borrowing.objects.create(book=book, user=user)

            Payment.objects.create(
                payment_status="PENDING",
                money_to_pay=borrowing.book.daily_fee,
                borrowing=borrowing,
                user=borrowing.user_id,
            )

            book.inventory -= 1
            book.save()

            TelegramBot.send_message(
                BorrowingMessages.create(borrowing)
            )

        return borrowing


class ReadBorrowSerializer(BorrowingSerializer):
    book = BookSerializer()
