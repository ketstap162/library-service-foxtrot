import datetime

from borrowings.models import Borrowing


class BorrowingMessages:
    @staticmethod
    def create(borrowing: Borrowing) -> str:
        return (
            "**New borrowing!**\n"
            f"{borrowing.borrow_date}\n"
            f"Book: {borrowing.book.title}\n"
            f"User: {borrowing.user.email}\n"
            f"Expect return: {borrowing.expected_return_date}\n"
        )

    @staticmethod
    def outdated(borrowing: Borrowing) -> str:
        return (
            "**The book has not been returned yet!**\n"
            f"{borrowing.borrow_date}\n"
            f"Book: {borrowing.book.title}\n"
            f"User: {borrowing.user.email}\n"
            f"Expect return: {borrowing.expected_return_date}\n"
            f"Now: {datetime.date.today()}"
        )

    @staticmethod
    def book_return(borrowing: Borrowing) -> str:
        return (
            "**Returned the book!**\n"
            f"{borrowing.borrow_date}\n"
            f"Book: {borrowing.book.title}\n"
            f"User: {borrowing.user.email}\n"
            f"Actual return: {borrowing.actual_return_date}\n"
        )


if __name__ == "__main__":
    BorrowingMessages.create(Borrowing.objects.get(pk=1))
