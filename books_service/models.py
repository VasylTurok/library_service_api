from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(max_length=63, unique=True)
    author = models.CharField(max_length=63)
    cover = models.CharField(
        choices=CoverChoices,
        max_length=4,
        default=CoverChoices.SOFT
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title", ]
