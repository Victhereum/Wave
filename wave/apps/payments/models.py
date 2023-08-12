import auto_prefetch
from django.db import models

from wave.utils.choices import PaymentPlans
from wave.utils.models import UIDTimeBasedModel
from wave.utils.payments import MoyasarAPIWrapper

payment = MoyasarAPIWrapper()


class Payments(UIDTimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", on_delete=models.CASCADE, related_name="user_payments")
    plan = models.CharField(max_length=15, choices=PaymentPlans.choices, default=PaymentPlans.MONTHLY)

    @property
    def metadata(self):
        if self.id:
            return payment.get_payment(self.id)
        return {}

    @property
    def status(self):
        if self.metadata:
            return self.metadata.get("status", None)

        return None
