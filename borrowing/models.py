import datetime

from django.conf import settings
from django.db import models
from books.models import Book


def calculate_expected_return_date(borrow_days: int) -> datetime:
    """Calculates the date on which book has to be returned without any penalties"""
    current_date = datetime.date.today()
    return current_date + datetime.timedelta(days=borrow_days)


class Borrowing(models.Model):
    BORROW_TERM = 14
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(
        default=calculate_expected_return_date(borrow_days=BORROW_TERM)
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

    def __str__(self) -> str:
        return f"Book {self.book.title} was borrowed at: {self.borrow_date}. Return date: {self.expected_return_date}"
