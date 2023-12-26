from django.urls import path
from rest_framework import routers

from borrowing.views import BorrowingViewSet, return_book

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)

urlpatterns = [
    path("borrowings/<int:pk>/return/", return_book, name="return-book"),

] + router.urls

app_name = "borrowing"
