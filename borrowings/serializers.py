from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.serializers import BookSerializer
from borrowings.models import Borrowing
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

        if book.inventory == 0:
            raise ValidationError(f"Book '{book.title}' is out of stock")

        with transaction.atomic():
            borrowing = Borrowing.objects.create(book=book)

            book.inventory -= 1
            book.save()

        return borrowing


class ReadBorrowSerializer(BorrowingSerializer):
    book = BookSerializer()
