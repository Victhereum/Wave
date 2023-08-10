from typing import Any, Dict, Tuple
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import CharField, BooleanField, IntegerField, Model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wave.apps.users.managers import CustomUserManager
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

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.phone_no})

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no

    def delete(self, using: Any = ..., keep_parents: bool = ...) -> Tuple[int, Dict[str, int]]:
        # Delete any reference in the PhoneModel table
        try:
            PhoneModel.objects.get(mobile=self.phone_no).delete()
        except PhoneModel.DoesNotExist:
            pass
        return super().delete(using, keep_parents)


