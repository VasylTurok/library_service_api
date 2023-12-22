from django.db.models import Case, When, Value, BooleanField
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer
)


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


# @api_view(["POST"])
# def return_book(request: Request) -> Response: ? що відправляти
