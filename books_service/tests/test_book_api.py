from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from books_service.models import Book


class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",

        )
        self.user.is_staff = True
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "9.99"
        }

        response = self.client.post("/api/books_service/books/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_books(self):
        Book.objects.create(
            title="Book 1",
            author="Author 1",
            cover="SOFT",
            inventory=5,
            daily_fee="12.99"
        )
        Book.objects.create(
            title="Book 2",
            author="Author 2",
            cover="HARD",
            inventory=8,
            daily_fee="14.99"
        )

        response = self.client.get("/api/books_service/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_books_by_title(self):
        Book.objects.create(
            title="Book 1",
            author="Author 1",
            cover="SOFT",
            inventory=5,
            daily_fee="12.99"
        )
        Book.objects.create(
            title="Book 2",
            author="Author 2",
            cover="HARD",
            inventory=8,
            daily_fee="14.99"
        )

        response = self.client.get("/api/books_service/books/", {"title": "Book 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book 1")

    def test_filter_books_by_author(self):
        Book.objects.create(
            title="Book 1",
            author="Author 1",
            cover="SOFT",
            inventory=5,
            daily_fee="12.99"
        )
        Book.objects.create(
            title="Book 2",
            author="Author 2",
            cover="HARD",
            inventory=8,
            daily_fee="14.99"
        )

        response = self.client.get("/api/books_service/books/", {"author": "Author 2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Author 2")

    def test_update_book(self):
        book = Book.objects.create(
            title="Book 1",
            author="Author 1",
            cover="SOFT",
            inventory=5,
            daily_fee="12.99"
        )

        updated_data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "14.99"
        }

        response = self.client.put(f"/api/books_service/books/{book.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")
        self.assertEqual(response.data["author"], "Updated Author")


class UnauthenticatedMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        url = reverse("book:book-list")  # Using 'book-list' as per DRF DefaultRouter
        res = self.client.post(url, data={"title": "Test Book", "author": "Test Author"})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
