from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "borrowing",
            "payment_status",
            "type_status",
            "session_url",
            "session_id",
            "money_to_pay",
        )
        read_only_fields = ("id", "money",)
