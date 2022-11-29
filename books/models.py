from django.db import models


class Book(models.Model):
    COVER_CHOICES = (
        ("H", "HARD"),
        ("S", "SOFT"),
    )

    title = models.CharField(max_length=255)
    author = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
