from django.core.exceptions import ValidationError
from django.db import models

from django.conf import settings
from books_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book,
        related_name="borrowings",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    @staticmethod
    def validate_borrowing(book, error_to_raise):

        if book.inventory <= 0:
            raise error_to_raise(
                {
                    "Book": "Currently, there is no free "
                            f"book with the name '{book.title}'."
                }
            )

    def clean(self):
        Borrowing.validate_borrowing(
            self.book,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        self.book.inventory -= 1
        self.book.save()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.borrow_date} - {self.expected_return_date}"

    class Meta:
        ordering = ["borrow_date", ]
