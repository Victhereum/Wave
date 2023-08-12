from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import BooleanField, CharField, DateTimeField, IntegerField
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from wave.apps.payments.models import Payments
from wave.apps.users.managers import CustomUserManager
from wave.utils.choices import FreeModeChoices, PaymentPlans, PaymentStatus
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

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.phone_no})

    USERNAME_FIELD = "phone_no"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no

    def _last_payment(self) -> Payments:
        payments = self.user_payments
        if payments:
            return payments.first()
        return None

    def _free_mode_status(self) -> str:
        if self.free_mode_activated:
            time_difference: timedelta = now() - self.free_mode_activated_at
            if time_difference.days > 3:
                return FreeModeChoices.EXPIRED
            return FreeModeChoices.ACTIVE
        return FreeModeChoices.NOT_USED

    def _has_active_subscription(self) -> bool:
        # Get the last payment made by this user
        # Differentiate the type
        # If the the type is monthly
        # Get the time difference by month(30 days)
        # If the the type is yearly
        # Get the time difference by year(365 days)
        if self._last_payment():
            last_payment = self._last_payment()
            time_difference: timedelta = now() - last_payment.created_at
            payment_type = last_payment.plan
            # If the last payment status, didn't go through
            # return False
            if last_payment.status != PaymentStatus.PAID:
                return False
            if payment_type == PaymentPlans.MONTHLY:
                if time_difference.days > 30:
                    return False
                return True
            elif payment_type == PaymentPlans.YEARLY:
                if time_difference.days > 365:
                    return False
                return True
            else:
                return False
        return False

    @property
    def has_active_subscription(self):
        return self._has_active_subscription

    @property
    def free_mode_status(self):
        return self._free_mode_status()

    @property
    def can_download(self) -> bool:
        if self._free_mode_status() == FreeModeChoices.ACTIVE:
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
