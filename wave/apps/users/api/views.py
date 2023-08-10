import base64

import pyotp
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime
from knox.models import AuthToken
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, NotFound, PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from wave.apps.users.api.serializers import CreateUserSerializer, GetUserSerializer, OTPSerializer, PhoneSerializer
from wave.apps.users.models import PhoneModel
from wave.utils.custom_exceptions import CustomError
from wave.utils.twillio import send_otp

User = get_user_model()


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


class PhoneNumberView(APIView):
    # authentication_classes = None
    permission_classes = [AllowAny]
    # Get to Create a call for OTP

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
            send_otp(mobile.mobile, otp)
        except Exception as e:
            raise APIException(detail=f"Please try again {e}")
        return Response({"OTP": otp}, status=200)  # Just for demonstration

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
            token = AuthToken.objects.create(user)[1]
            response = {"token": token}
            return Response(response, status=200)
        raise CustomError.BadRequest(detail="Wrong OTP")
