import datetime

from borrowings.models import Borrowing
from notifications.message_templates import BorrowingMessages
from notifications.telegram_bot import TelegramBot


def daily_expired_borrowings_notification():
    """
    Send notifications about expired
    borrowings into telegram every day
    """

    queryset = Borrowing.objects.filter(
        expected_return_date__lt=datetime.date.today()
    ).filter(
        actual_return_date=None
    )

    print(TelegramBot.CONTACT)
    TelegramBot.send_message(
        BorrowingMessages.outdated_many(queryset)
    )


if __name__ == "__main__":
    daily_expired_borrowings_notification()
