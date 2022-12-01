import datetime

from borrowings.models import Borrowing


class BorrowingMessages:
    @staticmethod
    def create(borrowing: Borrowing) -> str:
        return (
            "** New borrowing! **\n\n"
            f"Date: {borrowing.borrow_date}\n"
            f"Book: {borrowing.book.title}\n"
            f"User: {borrowing.user.email}\n"
            f"Expect return: {borrowing.expected_return_date}\n\n"
            f"#borrowed"
        )

    @staticmethod
    def outdated(borrowing: Borrowing) -> str:
        return (
            "** The book has not been returned yet! **\n\n"
            f"Borrowed: {borrowing.borrow_date}\n"
            f"Book: {borrowing.book.title}\n"
            f"User: {borrowing.user.email}\n"
            f"Expect return: {borrowing.expected_return_date}\n"
            f"Now: {datetime.date.today()}\n\n"
            f"#outdated"
        )

    @staticmethod
    def book_return(borrowing: Borrowing) -> str:
        return (
            "** Returned the book! **\n\n"
            f"Borrowed: {borrowing.borrow_date}\n"
            f"Book: {borrowing.book.title}\n"
            f"User: {borrowing.user.email}\n"
            f"Returned: {borrowing.actual_return_date}\n\n"
            f"#returned"
        )


if __name__ == "__main__":
    BorrowingMessages.create(Borrowing.objects.get(pk=1))
