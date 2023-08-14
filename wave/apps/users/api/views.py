import base64

import pyotp
from django.conf import settings
from django.utils.timezone import datetime
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, NotFound, PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from wave.apps.users.api.serializers import CreateUserSerializer, GetUserSerializer, OTPSerializer, PhoneSerializer
from wave.apps.users.models import PhoneModel, User
from wave.utils.custom_exceptions import CustomError
from wave.utils.twillio import send_otp


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = GetUserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = GetUserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["patch"])
    def free_mode(self, request, *args, **kwargs):
        user: User = request.user

        if not user.free_mode_activated_at:
            user.free_mode_activated = True
            user.free_mode_activated_at = datetime.now()
            user.save()
            return Response(data={"detail": "free mode activated"}, status=status.HTTP_202_ACCEPTED)
        raise PermissionDenied(detail="You have exhausted your 3-day trial period")


class RegistrationAPI(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "detail": GetUserSerializer(user, context=self.get_serializer_context()).data,
            }
        )


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class PhoneNumberView(GenericAPIView):
    # authentication_classes = None
    permission_classes = [AllowAny]

    # Get to Create a call for OTP
    def get_serializer_class(self):
        if self.request.method.lower() == "post":
            return OTPSerializer
        return PhoneSerializer

    def get(self, request, *args, **kwargs):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.get("phone_no", None)
        try:
            user = User.objects.get(phone_no=phone)
        except User.DoesNotExist:
            raise PermissionDenied(detail="User does not exist, kindly create one")
        try:
            mobile = PhoneModel.objects.get(
                mobile=user.phone_no
            )  # if mobile already exists the take this else create New One
        except PhoneModel.DoesNotExist:
            raise PermissionDenied(detail="Phone number does not exist, kindly create an account with it")
        mobile.counter += 1  # Update Counter At every Call
        mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        otp = OTP.at(mobile.counter)
        try:
            if settings.DEBUG:
                return Response({"OTP": otp}, status=200)  # Just for demonstration

            if settings.USE_TWILIO:
                send_otp(mobile.mobile, otp)
                return Response({"detail": "OTP sent"}, status=status.HTTP_200_OK)  # Just for demonstration
            return Response({"OTP": otp}, status=200)  # Just for demonstration
        except Exception as e:
            raise APIException(detail=f"Please try again {e}")

    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.get("phone_no", None)
            otp = serializer.validated_data.get("otp", None)
        try:
            mobile = PhoneModel.objects.get(mobile=phone)
        except PhoneModel.DoesNotExist:
            raise NotFound(detail="User does not exist")  # False Call
        user = User.objects.get(phone_no=phone)

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(otp, mobile.counter):  # Verifying the OTP
            mobile.is_verified = True
            mobile.counter += 1
            mobile.save()
            token = RefreshToken.for_user(user)
            response = {"refresh": str(token), "access": str(token.access_token)}
            return Response(response, status=200)
        raise CustomError.BadRequest(detail="Wrong OTP")
