from rest_framework import serializers

from wave.apps.payments.models import Payments
from wave.utils.choices import PaymentPlans


class PaymentSerializers:
    class Create(serializers.Serializer):
        currency = serializers.CharField(required=False, write_only=True)
        source = serializers.JSONField(required=True)
        amount = serializers.CharField(required=True)
        plan = serializers.ChoiceField(choices=PaymentPlans.choices, required=True)

        class Meta:
            fields = ("id", "plan", "amount", "currency", "source")

    class Get(serializers.ModelSerializer):
        # status = serializers.ReadOnlyField()

        class Meta:
            model = Payments
            exclude = ("visible", "user")

    class Fetch(serializers.ModelSerializer):
        metadata = serializers.ReadOnlyField()

        class Meta:
            model = Payments
            fields = ("id", "user", "metadata")
