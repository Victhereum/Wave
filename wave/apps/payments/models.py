import auto_prefetch
from django.db import models

from wave.utils.enums import PaymentPlans, PaymentStatus
from wave.utils.models import UIDTimeBasedModel
from wave.utils.payments import MoyasarAPIWrapper

payment = MoyasarAPIWrapper()


class Payments(UIDTimeBasedModel):
    user = auto_prefetch.ForeignKey("users.User", on_delete=models.CASCADE, related_name="user_payments")
    plan = models.CharField(max_length=15, choices=PaymentPlans.choices, default=PaymentPlans.BASIC)

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


# class PaymentPlansModel(UIDTimeBasedModel):
#     name = models.CharField(max_length=10, choices=PaymentPlans.choices, unique=True)
#     amount = models.PositiveIntegerField()
#     description = models.TextField(null=True)
