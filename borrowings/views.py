import datetime

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.response import Response


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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_staff",
                type={"type": "list", "items": {"type": "numbers"}},
                description="Filter by users(ex. ?user_id=1)"
            ),
            OpenApiParameter(
                "borrowed",
                type={"type": "list", "items": {"type": "numbers"}},
                description="Filter by status of book is borrowed(ex. ?is_active=True)"
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
    )
    def return_book(self, request, pk=None):
        borrowing = get_object_or_404(Borrowing, pk=pk)
        if borrowing.is_returned:
            raise ValidationError(
                f"Book '{borrowing.book}' has already been returned."
            )

        borrowing.book.inventory += 1
        borrowing.actual_return_date = datetime.date.today()
        borrowing.save()

        return Response(
            BorrowingSerializer(borrowing).data,
            status=status.HTTP_200_OK
        )
