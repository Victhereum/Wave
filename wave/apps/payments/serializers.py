from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from wave.apps.payments.models import Payments
from wave.utils.enums import CardSourceType, CurrencyChoices, PaymentPlans


class PaymentSerializers:
    class CreatePayment(serializers.Serializer):
        currency = serializers.CharField(required=False, write_only=True)
        source: CardSourceType = serializers.JSONField(required=True)
        plan = serializers.ChoiceField(choices=PaymentPlans.choices, required=True)

        @extend_schema_field(CardSourceType)
        def get_source(self, obj) -> CardSourceType:
            return obj["source"]

    class GetPayment(serializers.ModelSerializer):
        class Meta:
            model = Payments
            fields = ("id", "plan", "status")

    class FetchPayment(serializers.ModelSerializer):
        metadata = serializers.ReadOnlyField()

        class Meta:
            model = Payments
            fields = ("id", "plan", "status", "metadata")

    class CardType(serializers.Serializer):
        number = serializers.CharField(required=True)

        class Meta:
            fields = ("number",)

    class CurrencySchema(serializers.Serializer):
        value = serializers.ChoiceField(choices=[x[0] for x in CurrencyChoices.choices])
        label = serializers.ChoiceField(choices=[x[1] for x in CurrencyChoices.choices])

    class CardTypeResponseSchema(serializers.Serializer):
        value = serializers.ChoiceField(choices=[x[0] for x in CurrencyChoices.choices])
        label = serializers.ChoiceField(choices=[x[1] for x in CurrencyChoices.choices])
        icon = serializers.ChoiceField(choices=[x[1] for x in CurrencyChoices.choices])
