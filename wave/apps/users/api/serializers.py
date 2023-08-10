from djoser.serializers import UserCreateSerializer
from django.db.transaction import atomic

from rest_framework import serializers
from wave.utils.custom_exceptions import CustomError
from wave.apps.users.models import PhoneModel, User
from wave.apps.users.models import User as UserType


class CreateUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    phone_no = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('phone_no', 'name')

    @atomic
    def create(self, validated_data):
        phone, created = PhoneModel.objects.get_or_create(mobile=validated_data["phone_no"])
        if not created:
            raise CustomError.BadRequest(detail="Phone number already exist")
        user = User.objects.create_user(phone_no=phone.mobile, name=validated_data["name"])
        return user

class CustomUserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["phone_no", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

class CustomUserCreateSerializer(UserCreateSerializer):
    re_password = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )
    phone_no = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    def validate(self, attrs):
        re_password = attrs.pop("re_password")
        attrs = super().validate(attrs)
        password = attrs.get("password")
        if password != re_password:
            raise serializers.ValidationError(
                {"error": "The passwords entered do not match."}
            )
        return attrs

    class Meta(UserCreateSerializer.Meta):
        # model = User
        fields = ("phone_no", "name", "password", "re_password")
        extra_kwargs = {
            "re_password": {"write_only": True},
        }

class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "phone_no", "name",)

class PhoneSerializer(serializers.Serializer):
    phone_no = serializers.CharField(required=True)
    class Meta:
        fields = ("phone_no")

class OTPSerializer(serializers.Serializer):
    phone_no = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)
    class Meta:
        fields = ("phone", "otp")

