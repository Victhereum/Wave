from typing import Literal, Self

import auto_prefetch
from django.db import models
from django.utils.timezone import now, timedelta

from wave.apps.video.models import Video
from wave.utils.enums import (
    PaymentPlanDurationChoices,
    PaymentPlans,
    PaymentPriviledges,
    PaymentStatus,
    PaymentSubscriptionStatus,
)
from wave.utils.models import UIDTimeBasedModel
from wave.utils.payments import MoyasarAPIWrapper

payment = MoyasarAPIWrapper()


class PaymentPriviledge(UIDTimeBasedModel):
    description = models.TextField()
    priviledge = models.CharField(max_length=250, choices=PaymentPriviledges.choices, null=True)

    @classmethod
    def create_default(cls):
        for priviledge in PaymentPriviledges.choices:
            cls.objects.get_or_create(
                priviledge=priviledge[0],
                description=priviledge[1],
            )


class PaymentPlan(UIDTimeBasedModel):
    name = models.CharField(max_length=15, choices=PaymentPlans.choices, default=PaymentPlans.BASIC)
    type = models.CharField(
        max_length=15, choices=PaymentPlanDurationChoices.choices, default=PaymentPlanDurationChoices.ONE_MONTH
    )
    description = models.TextField(help_text="The description of the plan")
    priviledges: "PaymentPriviledge" = models.ManyToManyField("payments.PaymentPriviledge", related_name="plans")
    media_allowed = models.IntegerField(default=int)
    """Number of media that can be subtitled in this plan"""
    media_length = models.DurationField(default=timedelta(seconds=1).total_seconds())
    """The length of the media"""
    price = models.FloatField(default=float)
    duration = models.DurationField(default=timedelta(seconds=1).total_seconds())
    """The duration for custom plans only"""

    def __str__(self) -> str:
        return self.name

    def first(self):
        return self

    @classmethod
    def create_free(cls: Self) -> models.QuerySet["PaymentPlan"]:
        free_plans = cls.objects.filter(name=PaymentPlans.FREE).order_by("-created_at")
        if not free_plans.exists():
            cls.objects.create(
                name=PaymentPlans.FREE,
                type=PaymentPlanDurationChoices.DEFAULT,
                description="Free plan",
                media_allowed=2,
                media_length=timedelta(seconds=15).total_seconds(),
            )
        return free_plans

    @classmethod
    def create_basic(cls) -> models.QuerySet["PaymentPlan"]:
        plans = cls.objects.filter(name=PaymentPlans.BASIC)
        if not plans.exists():
            return cls.objects.create(
                name=PaymentPlans.BASIC,
                type=PaymentPlanDurationChoices.ONE_MONTH,
                description="Basic plan",
                media_allowed=10,
                media_length=timedelta(minutes=30).total_seconds(),
            )
        return plans

    @classmethod
    def create_premium(cls) -> models.QuerySet["PaymentPlan"]:
        plans = cls.objects.filter(name=PaymentPlans.PREMIUM)
        if not plans.exists():
            return cls.objects.create(
                name=PaymentPlans.PREMIUM,
                type=PaymentPlanDurationChoices.ONE_MONTH,
                description="Premium plan",
                media_allowed=100,
                media_length=timedelta(minutes=30).total_seconds(),
            )
        return plans

    @classmethod
    def create_and_get_default_plan(
        cls, plan: Literal[PaymentPlans.FREE, PaymentPlans.BASIC, PaymentPlans.PREMIUM] = PaymentPlans.FREE
    ) -> "PaymentPlan":
        default_plans = {
            PaymentPlans.FREE: cls.create_basic(),
            PaymentPlans.FREE: cls.create_free(),
            PaymentPlans.FREE: cls.create_premium(),
        }
        return default_plans[plan]


class Payments(UIDTimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", on_delete=models.CASCADE, related_name="user_payments")
    plan: "PaymentPlan" = auto_prefetch.ForeignKey(
        "payments.PaymentPlan", on_delete=models.CASCADE, related_name="payment_plans"
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
        if self.plan.name == PaymentPlans.CUSTOM:
            used_days = now() - self.created_at
            if remaining_days := timedelta(seconds=self.plan.duration - used_days.total_seconds).days < 0:
                return 0
            return remaining_days
        return None

    @property
    def videos_left(self) -> int:
        if self.plan.name != PaymentPlans.CUSTOM:
            return self.plan.media_allowed - self.videos_during_subscription.count()

    @property
    def videos_during_subscription(self) -> models.QuerySet["Video"]:
        return self.user.videos.filter(created_at__gte=self.created_at)

    @property
    def subscription_status(self) -> Literal[PaymentSubscriptionStatus.ACTIVE, PaymentSubscriptionStatus.EXPIRED]:
        """
        If the payment is for a custom plan, then check by duration alloted
        else check by number of videos subtitled
        """
        if self.plan.name == PaymentPlans.CUSTOM:
            used_days = now() - self.created_at
            if used_days.total_seconds() >= self.plan.duration:
                return PaymentSubscriptionStatus.EXPIRED
            return PaymentSubscriptionStatus.ACTIVE
        else:
            if self.videos_during_subscription.count() >= self.plan.media_allowed:
                return PaymentSubscriptionStatus.EXPIRED
            return PaymentSubscriptionStatus.ACTIVE

    @property
    def has_expired(self) -> bool:
        if self.subscription_status == PaymentSubscriptionStatus.ACTIVE:
            return False
        return True


# class PaymentPlansModel(UIDTimeBasedModel):
#     name = models.CharField(max_length=10, choices=PaymentPlans.choices, unique=True)
#     amount = models.PositiveIntegerField()
#     description = models.TextField(null=True)
