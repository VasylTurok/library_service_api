from rest_framework import viewsets
from drf_spectacular.utils import OpenApiParameter, extend_schema
from books_service.models import Book
from books_service.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=str,
                description="Filter by title. Example: ?title=Some title"
            ),
            OpenApiParameter(
                "author",
                type=str,
                description="Filter by author. Example: ?author=Some author"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
