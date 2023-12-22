from rest_framework import viewsets
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListOrRetrieveSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("user", "book")
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("user", "book")
        if not self.request.user.is_staff:
            queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return BorrowingListOrRetrieveSerializer
        return self.serializer_class
