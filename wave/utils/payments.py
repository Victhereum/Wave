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


# Example usage:
# if __name__ == "__main__":
#     # Replace 'YOUR_API_KEY' with your actual API key from Moyasar
#     api_key = "YOUR_API_KEY"
#     api = MoyasarAPIWrapper()

#     # Create a payment
# payment_data = {
#     "amount": 10000,  # amount in Saudi Riyals (Halalas) in cents
#     "description": "Test Payment",
#     "source_type": "creditcard",
#     "source_data": {
#         "name": "John Doe",
#         "number": "4111111111111111",
#         "cvc": "123",
#         "month": "01",
#         "year": "2025",
#     },
# }
#     response = api.create_payment(**payment_data)
#     print("Payment created:", response)

#     # Retrieve a payment
#     payment_id = response["id"]
#     payment_info = api.get_payment(payment_id)
#     print("Payment details:", payment_info)

#     # Refund a payment (optional)
#     refund_response = api.refund_payment(payment_id, amount=5000)  # Refunding half of the payment amount
#     print("Refund response:", refund_response)

# payment_data = {
#         "amount": 10000,  # amount in Saudi Riyals (Halalas) in cents
#         "description": "Test Payment",
#         "source_type": "creditcard",
#         "source_data": {
#             "name": "John Doe",
#             "number": "4111111111111111",
#             "cvc": "123",
#             "month": "01",
#             "year": "2025",
#         },
#     }
# response = api.create_payment(**payment_data)
# print("Payment created:", response)
# moyasar.api_key = API_KEY

# response = Create(data=payment_data)
# print("Payment created:", response.create(data=payment_data))
