from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book
from books.serializers import BookSerializer
from django.test import RequestFactory, TestCase
from books.permisions import IsAdminOrReadOnly
from django.contrib.auth import get_user_model

BOOK_URL = reverse("books:book-list")


def sample_book(**params):
    defaults = {
        "title": "Sample book",
        "author": "Test author",
        "cover": "HARD",
        "inventory": 90,
        "daily_fee": 0.5,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def detail_url(book_id):
    return reverse("books:book-detail", args=[book_id])


class UnauthenticatedBookApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@test.com", "testpass")
        self.client.force_authenticate(self.user)

    def test_list_books(self):
        res = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_detail(self):
        book = sample_book()

        url = detail_url(book.id)
        res = self.client.get(url)

        serializer = BookSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_creat_book_forbidden(self):
        payload = {
            "title": "Sample book",
            "author": "Test author",
            "cover": "HARD",
            "inventory": 90,
            "daily_fee": 0.5,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class IsAdminOrReadOnlyAccessTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create(
            email="admin@admin.com",
            is_staff=True,
        )
        self.non_admin_user = get_user_model().objects.create(email="user@user.com")
        self.factory = RequestFactory()

    def test_admin_user_has_permission(self):
        request = self.factory.delete("/")
        request.user = self.admin_user

        permission_check = IsAdminOrReadOnly()

        permission = permission_check.has_permission(request, None)

        self.assertTrue(permission)

    def test_admin_user_can_perform_safe_method(self):
        request = self.factory.get("/")
        request.user = self.admin_user

        permission_check = IsAdminOrReadOnly()

        permission = permission_check.has_permission(request, None)

        self.assertTrue(permission)

    def test_non_admin_user_has_not_permission(self):
        request = self.factory.delete("/")
        request.user = self.non_admin_user

        permission_check = IsAdminOrReadOnly()

        permission = permission_check.has_permission(request, None)

        self.assertFalse(permission)
