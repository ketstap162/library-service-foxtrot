import uuid

from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = (
        ("PE", "PENDING"),
        ("PA", "PAID"),
    )
    TYPE_CHOICES = (
        ("PA", "PAYMENT"),
        ("FI", "FINE"),
    )

    payment_status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    type_status = models.CharField(max_length=7, choices=TYPE_CHOICES)
    borrowing = models.OneToOneField(to=Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    money_to_pay = models.DecimalField(max_digits=5, decimal_places=2)
