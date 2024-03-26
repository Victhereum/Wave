from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from wave.apps.payments.models import SubscriptionPlan, SubscriptionPriviledge, Subscriptions
from wave.utils.enums import CardSourceType, CurrencyChoices, SubscriptionPlans


class SubscriptionSerializers:
    class CreateSubscription(serializers.Serializer):
        currency = serializers.CharField(required=False, write_only=True)
        source: CardSourceType = serializers.JSONField(required=True)
        plan = serializers.ChoiceField(choices=SubscriptionPlans.choices, required=True)

        @extend_schema_field(CardSourceType)
        def get_source(self, obj) -> CardSourceType:
            return obj["source"]

    class GetSubscription(serializers.ModelSerializer):
        class Meta:
            model = Subscriptions
            fields = ("id", "plan", "status")

    class FetchSubscription(serializers.ModelSerializer):
        metadata = serializers.ReadOnlyField()

        class Meta:
            model = Subscriptions
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


class SubscriptionPriviledgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPriviledge
        fields = ("id", "description", "priviledge")


class SubscriptionPlansSerializer(serializers.ModelSerializer):
    priviledges = SubscriptionPriviledgesSerializer(many=True)

    class Meta:
        model = SubscriptionPlan
        fields = ("id", "name", "price", "description", "max_duration", "slots", "type", "priviledges")
