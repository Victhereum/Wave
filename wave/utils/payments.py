import requests
from django.conf import settings
from rest_framework.exceptions import APIException

API_KEY = settings.MOYASAR_API_KEY


class MoyasarAPIWrapper:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "https://api.moyasar.com"

    def _make_request(self, method, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.request(method, url, json=data, auth=(self.api_key, ""), headers=headers)
        if not response.ok:
            raise APIException(
                {"detail": response.json().get("message", {}), "errors": response.json().get("errors", {})}
            )

        return response.json()

    # Create a payment
    def create_payment(self, amount, currency, description, source, callback_url, metadata: dict):
        data = {
            "amount": amount,
            "source": source,
            "currency": currency,
            "description": description,
            "callback_url": callback_url,
            "metadata": metadata,
        }
        return self._make_request("post", "v1/payments", data)

    # Retrieve a payment
    def get_payment(self, payment_id):
        return self._make_request("get", f"v1/payments/{payment_id}")

    # Refund a payment
    def refund_payment(self, payment_id, amount=None):
        data = {"amount": amount} if amount else None
        return self._make_request("post", f"v1/payments/{payment_id}/refund", data)
