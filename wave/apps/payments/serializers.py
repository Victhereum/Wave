from rest_framework import serializers

from wave.apps.payments.models import Payments
from wave.utils.choices import PaymentPlans


class PaymentSerializers:
    class CreatePayment(serializers.Serializer):
        currency = serializers.CharField(required=False, write_only=True)
        source = serializers.JSONField(required=True)
        plan = serializers.ChoiceField(choices=PaymentPlans.choices, required=True)

        class Meta:
            fields = ("plan", "currency", "source")

    class GetPayment(serializers.ModelSerializer):
        status = serializers.ReadOnlyField()

        class Meta:
            model = Payments
            exclude = ("visible", "user", "updated_at")

    class FetchPayment(serializers.ModelSerializer):
        metadata = serializers.ReadOnlyField()

        class Meta:
            model = Payments
            fields = ("id", "user", "metadata")
