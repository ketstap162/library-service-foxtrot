from django.urls import path

from borrowings.views import BorrowingCreateView

urlpatterns = [
    path("", BorrowingCreateView.as_view(), name="create")
]

app_name = "borrowings"
