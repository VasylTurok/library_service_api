from celery import shared_task
from django.conf import settings
import requests

from borrowing.models import Borrowing


@shared_task
def send_telegram_notification(message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_NOTIFICATIONS_CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
    }
    response = requests.post(url, data=data)
    return response.json()


@shared_task
def notify_borrowing_creation(borrowing_id):
    borrowing = Borrowing.objects.get(pk=borrowing_id)
    message = (f"New Borrowing Created:\nBook: {borrowing.book.title}\n"
               f"User: {borrowing.user.email}\n"
               f"Borrow Date: {borrowing.borrow_date}\n"
               f"Expected Return Date: {borrowing.expected_return_date}")
    send_telegram_notification.delay(message)
