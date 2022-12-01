from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentRetrieveSerializer


class PaymentViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            return queryset.filter(borrowing__user=self.request.user.id)

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentRetrieveSerializer

        return PaymentSerializer
