from typing import Literal, Self

import auto_prefetch
from django.db import models
from django.utils.timezone import now, timedelta

from wave.apps.video.models import Caption
from wave.utils.enums import (
    PaymentStatus,
    SubscriptionPlanDurationChoices,
    SubscriptionPlans,
    SubscriptionPriviledges,
    SubscriptionStatus,
)
from wave.utils.models import UIDTimeBasedModel
from wave.utils.payments import MoyasarAPIWrapper

payment = MoyasarAPIWrapper()


class SubscriptionPriviledge(UIDTimeBasedModel):
    description = models.TextField()
    priviledge = models.CharField(max_length=250, choices=SubscriptionPriviledges.choices, null=True)

    @classmethod
    def create_default(cls):
        for priviledge in SubscriptionPriviledges.choices:
            cls.objects.get_or_create(
                priviledge=priviledge[0],
                description=priviledge[1],
            )


class SubscriptionPlan(UIDTimeBasedModel):
    name = models.CharField(max_length=15, choices=SubscriptionPlans.choices, default=SubscriptionPlans.BASIC)
    type = models.CharField(
        max_length=15,
        choices=SubscriptionPlanDurationChoices.choices,
        default=SubscriptionPlanDurationChoices.ONE_MONTH,
    )
    description = models.TextField(help_text="The description of the plan")
    priviledges: "SubscriptionPriviledge" = models.ManyToManyField(
        "payments.SubscriptionPriviledge", related_name="plans"
    )
    slots = models.IntegerField(default=int)
    """Number of media that can be subtitled in this plan"""
    max_duration = models.DurationField(default=timedelta(seconds=1).total_seconds())
    """The maximum length of the media"""
    price = models.FloatField(default=float)
    duration = models.DurationField(default=timedelta(seconds=1).total_seconds())
    """The duration for custom plans only"""

    def __str__(self) -> str:
        return self.name

    def first(self):
        return self

    @classmethod
    def create_free(cls: Self) -> models.QuerySet["SubscriptionPlan"]:
        free_plans = cls.objects.filter(name=SubscriptionPlans.FREE).order_by("-created_at")
        if not free_plans.exists():
            cls.objects.create(
                name=SubscriptionPlans.FREE,
                type=SubscriptionPlanDurationChoices.DEFAULT,
                description="Free plan",
                slots=2,
                media_length=timedelta(seconds=15).total_seconds(),
            )
        return free_plans

    @classmethod
    def create_basic(cls) -> models.QuerySet["SubscriptionPlan"]:
        plans = cls.objects.filter(name=SubscriptionPlans.BASIC)
        if not plans.exists():
            return cls.objects.create(
                name=SubscriptionPlans.BASIC,
                type=SubscriptionPlanDurationChoices.ONE_MONTH,
                description="Basic plan",
                slots=10,
                media_length=timedelta(minutes=30).total_seconds(),
            )
        return plans

    @classmethod
    def create_premium(cls) -> models.QuerySet["SubscriptionPlan"]:
        plans = cls.objects.filter(name=SubscriptionPlans.PREMIUM)
        if not plans.exists():
            return cls.objects.create(
                name=SubscriptionPlans.PREMIUM,
                type=SubscriptionPlanDurationChoices.ONE_MONTH,
                description="Premium plan",
                slots=100,
                media_length=timedelta(minutes=30).total_seconds(),
            )
        return plans

    @classmethod
    def create_and_get_default_plan(
        cls,
        plan: Literal[
            SubscriptionPlans.FREE, SubscriptionPlans.BASIC, SubscriptionPlans.PREMIUM
        ] = SubscriptionPlans.FREE,
    ) -> "SubscriptionPlan":
        default_plans = {
            SubscriptionPlans.FREE: cls.create_basic(),
            SubscriptionPlans.FREE: cls.create_free(),
            SubscriptionPlans.FREE: cls.create_premium(),
        }
        return default_plans[plan]


class Subscriptions(UIDTimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", on_delete=models.CASCADE, related_name="subscriptions")
    plan: "SubscriptionPlan" = auto_prefetch.ForeignKey(
        "payments.SubscriptionPlan", on_delete=models.CASCADE, related_name="payment_plans"
    )

    @property
    def metadata(self) -> dict:
        if self.id:
            return payment.get_payment(self.id)
        return {}

    @property
    def status(self) -> str:
        if self.metadata:
            return self.metadata.get("status", None)

        return PaymentStatus.INITIATED

    @property
    def days_left(self) -> int:
        if self.plan.name == SubscriptionPlans.CUSTOM:
            used_days = now() - self.created_at
            if remaining_days := timedelta(seconds=self.plan.duration - used_days.total_seconds).days < 0:
                return 0
            return remaining_days
        return None

    @property
    def videos_left(self) -> int:
        if self.plan.name != SubscriptionPlans.CUSTOM:
            return self.plan.slots - self.captions_during_subscription.count()

    @property
    def captions_during_subscription(self) -> models.QuerySet["Caption"]:
        return self.user.videos.filter(created_at__gte=self.created_at)

    @property
    def subscription_status(
        self,
    ) -> Literal[SubscriptionStatus.ACTIVE, SubscriptionStatus.EXPIRED]:
        """
        If the payment is for a custom plan, then check by duration alloted
        else check by number of videos subtitled
        """
        if self.plan.name == SubscriptionPlans.CUSTOM:
            used_days = now() - self.created_at
            if used_days.total_seconds() >= self.plan.duration:
                return SubscriptionStatus.EXPIRED
            if self.captions_during_subscription.count() >= self.plan.slots:
                return SubscriptionStatus.EXPIRED
            return SubscriptionStatus.ACTIVE
        else:
            if self.captions_during_subscription.count() >= self.plan.slots:
                return SubscriptionStatus.EXPIRED
            return SubscriptionStatus.ACTIVE

    @property
    def has_expired(self) -> bool:
        if self.subscription_status == SubscriptionStatus.ACTIVE:
            return False
        return True
