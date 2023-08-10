import random
import pyotp
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from knox.models import AuthToken
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from twilio.rest import Client

# Replace 'your_twilio_account_sid', 'your_twilio_auth_token', and 'your_twilio_phone_number'
twilio_account_sid = 'your_twilio_account_sid'
twilio_auth_token = 'your_twilio_auth_token'
twilio_phone_number = 'your_twilio_phone_number'

User = get_user_model()

class PhoneOTPAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        if not phone_number or not otp:
            return None

        # Verify OTP
        phone_otp = get_object_or_404(PhoneOTP, phone_number=phone_number)
        totp = pyotp.TOTP(phone_otp.otp)
        if not totp.verify(otp):
            raise AuthenticationFailed('Invalid OTP.')

        # OTP verification successful, generate a new token for the user
        user, _ = AuthToken.objects.create(User)
        return user, None
