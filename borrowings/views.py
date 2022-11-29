from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingCreateSerializer,
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("user", "book")
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = self.queryset
            users = self.request.query_params.get("user_id")

            if users:
                users_ids = self.params_to_ints(users)
                queryset = queryset.filter(user__id__in=users_ids)

        else:
            queryset = Borrowing.objects.filter(user=self.request.user)

        borrowed = self.request.query_params.get("is_active")

        if borrowed:
            queryset = queryset.filter(actual_return_date__isnull=True)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingRetrieveSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
