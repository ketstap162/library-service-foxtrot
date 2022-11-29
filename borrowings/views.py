from rest_framework import generics

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingCreateSerializer


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.select_related("user", "book")
    serializer_class = BorrowingCreateSerializer

    def perform_create(self, serializer):
        serializer.user = self.request.user
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            return serializer.errors
