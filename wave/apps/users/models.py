from typing import Literal
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import BooleanField, CharField, DateTimeField, IntegerField, QuerySet
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied

from wave.apps.payments.models import SubscriptionPlan, Subscriptions
from wave.apps.users.managers import CustomUserManager
from wave.utils.enums import FreeModeChoices, PaymentStatus, SubscriptionPlans, SubscriptionStatus
from wave.utils.models import UIDTimeBasedModel


def generate_id():
    return uuid4().hex


class PhoneModel(UIDTimeBasedModel):
    mobile = CharField(blank=False, max_length=20, unique=True)

    is_verified = BooleanField(blank=False, default=False)
    counter = IntegerField(default=0, blank=False)

    def __str__(self):
        return str(self.mobile)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Default custom user model for Wave.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    id = CharField(primary_key=True, max_length=120, default=generate_id, unique=True, editable=False)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    phone_no = CharField(_("Phone Number"), unique=True, max_length=25)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    free_mode_activated = BooleanField(default=False)
    free_mode_activated_at = DateTimeField(null=True)
    date_joined = DateTimeField(auto_now_add=True)
    collection_id = CharField(null=True, blank=True, max_length=120)
    subscriptions: QuerySet["Subscriptions"]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("api:user-detail", kwargs={"id": self.pk})

    USERNAME_FIELD = "phone_no"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no

    @property
    def _last_payment(self) -> Subscriptions | None:
        payments: QuerySet[Subscriptions] = self.subscriptions.order_by("-created_at")
        if payments:
            return payments.filter(status=PaymentStatus.PAID).first()
        return None

    def subscribe_to_free_plan(self) -> None:
        if not self.subscriptions.exists():
            free_plan = SubscriptionPlan.create_free().first()
            return Subscriptions.objects.create(user=self, plan=free_plan)

    def _free_mode_status(self) -> str:
        if not self._last_payment:
            # Set the user to the free plan
            return FreeModeChoices.NOT_USED
        else:
            if self._last_payment.has_expired:
                return FreeModeChoices.EXPIRED
            return FreeModeChoices.ACTIVE

    def _has_active_subscription(self) -> bool:
        # Get the last payment made by this user
        # Differentiate the type
        # If the the type is monthly
        # Get the time difference by month(30 days)
        # If the the type is yearly
        # Get the time difference by year(365 days)
        if self._last_payment():
            # time_difference: timedelta = now() - last_payment.created_at
            # payment_type = last_payment.plan
            # If the last payment status, didn't go through
            # return False
            payment_status = self._last_payment().status == PaymentStatus.PAID
            subscription_status = self._last_payment().subscription_status == SubscriptionStatus.ACTIVE
            if payment_status and subscription_status:
                return True
        return False

    @property
    def has_active_subscription(self) -> bool:
        return self._has_active_subscription()

    @property
    def free_mode_status(self) -> Literal[FreeModeChoices.ACTIVE, FreeModeChoices.EXPIRED, FreeModeChoices.NOT_USED]:
        return self._free_mode_status()

    @property
    def can_download(self) -> bool:
        if self.free_mode_status == FreeModeChoices.ACTIVE:
            return True
        elif self._free_mode_status() in [FreeModeChoices.EXPIRED, FreeModeChoices.NOT_USED]:
            # If the user has an active subscription return True
            # Else return False
            return self._has_active_subscription()
        return False

    def delete(self, using=..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        # Delete any reference in the PhoneModel table
        try:
            PhoneModel.objects.get(mobile=self.phone_no).delete()
        except PhoneModel.DoesNotExist:
            pass
        return super().delete(using, keep_parents)

    def has_permission(self) -> bool:
        if not self.can_download:
            raise PermissionDenied(detail="You do not have an active subscription, kindly create a payment plan")
        return True

    @property
    def current_plan(self):
        return self._last_payment().plan

    @property
    def subscription_status(
        self,
    ) -> Literal[SubscriptionStatus.ACTIVE, SubscriptionStatus.EXPIRED]:
        """
        If the payment is for a custom plan, then check by duration alloted
        else check by number of videos subtitled
        """
        if self.current_plan.name == SubscriptionPlans.CUSTOM:
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
