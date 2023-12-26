from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Case, When, Value, BooleanField
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import  mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer
)

from borrowing.tasks import notify_borrowing_creation


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Borrowing.objects.select_related("user", "book").annotate(
        is_active=Case(
            When(actual_return_date__isnull=True, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    )
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def perform_create(self, serializer):
        borrowing_instance = serializer.save()

        book_instance = borrowing_instance.book
        book_instance.inventory -= 1
        notify_borrowing_creation.delay(borrowing_instance.id)
        book_instance.save()

        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(user_id=self.request.user.id)

        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")
        if is_active:
            if is_active == "False":
                queryset = queryset.filter(actual_return_date__isnull=False)
            else:
                queryset = queryset.filter(actual_return_date__isnull=True)

        if user_id and self.request.user.is_staff:
            user_ids = self._params_to_ints(user_id)
            queryset = queryset.filter(user__id__in=user_ids)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_active",
                type=bool,
                description="Filter by is_active. "
                            "Use True or False."
                            "Example: ?is_active=True"
            ),
            OpenApiParameter(
                "user_id",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by user ids. Example: ?user_id=1,3"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


def is_admin(user):
    return user.is_staff


@api_view(["POST"])
@user_passes_test(is_admin)
def return_book(request, pk) -> Response:
    try:
        borrowing = Borrowing.objects.get(id=request.data["pk"])
    except Borrowing.DoesNotExist:
        return Response(
            "Borrowing not found",
            status=status.HTTP_404_NOT_FOUND)
    if borrowing.actual_return_date:
        return Response(
            "Failed: Actual return date is missing",
            status=status.HTTP_400_BAD_REQUEST
        )
    borrowing.book.inventory += 1
    borrowing.actual_return_date = datetime.now().date()
    borrowing.save()
    borrowing.book.save()

    return Response("Success", status=status.HTTP_200_OK)
