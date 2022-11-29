from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing, calculate_expected_return_date


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
        read_only_fields = (
            "id",
            "borrow_date",
            "user",
            "book",
        )


class BorrowingCreateSerializer(BorrowingSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "book",
        )

    def create(self, validated_data):
        book = validated_data["book"]

        if book.inventory == 0:
            raise ValidationError(f"Book '{book.title}' is out of stock")

        with transaction.atomic():
            borrowing = Borrowing.objects.create(book=book)

            book.inventory -= 1
            book.save()

        return borrowing
