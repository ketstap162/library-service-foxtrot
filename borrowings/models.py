import datetime
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import CheckConstraint, Q
from django.db.models.functions import Now

from books.models import Book


def calculate_expected_return_date(borrow_days: int) -> datetime:
    """Calculates the date on which book has to be returned without any penalties"""
    current_date = datetime.date.today()
    return current_date + datetime.timedelta(days=borrow_days)


class Borrowing(models.Model):
    BORROW_TERM = 14
    EXPIRED_DATA_PRICE_FACTOR = 2

    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(
        null=True,
        default=calculate_expected_return_date(borrow_days=BORROW_TERM),
    )
    actual_return_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )

    @property
    def is_returned(self) -> bool:
        return bool(self.actual_return_date)

    @property
    def price(self) -> Decimal:
        """Return borrowing price or -1 if book is not returned"""
        if self.is_returned is False:
            return Decimal("-1")

        days = (self.borrow_date - self.actual_return_date).days

        price = self.book.daily_fee * days

        if days > 14:
            price *= self.EXPIRED_DATA_PRICE_FACTOR

        return price
        
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(borrow_date__lte=Now()),
                name="Borrow date must be less than or equal today"
            ),
            CheckConstraint(
                check=Q(expected_return_date__gt=Now()),
                name="Expected return date must be greater than or equal today"
            ),
            CheckConstraint(
                check=Q(actual_return_date__gte=Now()),
                name="Actual return date must be greater than or equal today"
            ),
        ]

    def __str__(self) -> str:
        return f"Book {self.book.title} was borrowed at: {self.borrow_date}. Return date: {self.expected_return_date}"
