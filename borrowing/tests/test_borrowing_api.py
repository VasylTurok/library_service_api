from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from books_service.models import Book
from borrowing.models import Borrowing


class BorrowingAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",

        )
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverChoices.SOFT,
            inventory=5,
            daily_fee="9.99"
        )

        Borrowing.objects.create(
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timedelta(days=14),
            book=self.book,
            user=self.user
        )

    def test_list_borrowings(self):
        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_borrowing(self):
        url = reverse("borrowing:borrowing-list")
        data = {
            "expected_return_date": (timezone.now() + timedelta(days=14)).date(),
            "book": self.book.id,
            "user": self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_return_book(self):
        borrowing = Borrowing.objects.get(id=1)
        url = reverse("borrowing:return-book", kwargs={"pk": borrowing.id})
        response = self.client.post(url, {"pk": borrowing.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_book_nonexistent_borrowing(self):
        url = reverse("borrowing:return-book", kwargs={"pk": 999})
        response = self.client.post(url, {"pk": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_return_book_already_returned(self):
        borrowing = Borrowing.objects.get(id=1)
        borrowing.actual_return_date = timezone.now().date()
        borrowing.save()
        url = reverse("borrowing:return-book", kwargs={"pk": borrowing.id})
        response = self.client.post(url, {"pk": borrowing.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
