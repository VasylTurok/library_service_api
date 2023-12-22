from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from borrowing.models import Borrowing
from books_service.serializers import BookSerializer
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        Borrowing.validate_borrowing(
            attrs["book"],
            ValidationError
        )
        return data

    def create(self, validated_data):
        with transaction.atomic():
            borrowing = Borrowing.objects.create(**validated_data)
            validated_data["book"].inventory -= 1
            return borrowing


class BorrowingListOrRetrieveSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
