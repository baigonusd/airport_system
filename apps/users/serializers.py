import re
from smtplib import SMTPException

import jwt
from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from .models import User, Passenger

from utils.sms import SMS
from utils.email import Email


# User Sign Up
class UserSignupSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mobile_phone = serializers.CharField(required=True)
    number_of_doc = serializers.CharField(required=True, max_length=9)
    iin = serializers.CharField(required=True, max_length=12)
    gender = serializers.IntegerField(required=True)
    password = serializers.CharField(write_only=True)
    role = serializers.IntegerField()
    scan_udv = serializers.ImageField(use_url=True)

    def validate(self, data):
        if Passenger.objects.filter(number_of_doc=data["number_of_doc"]):
            raise exceptions.ValidationError(
                "User with this document has already exist."
            )
        if Passenger.objects.filter(iin=data["iin"]):
            raise exceptions.ValidationError("User with this IIN has already exist.")
        if Passenger.objects.filter(mobile_phone=data["mobile_phone"]):
            raise exceptions.ValidationError(
                "User with this mobile phone has already exist."
            )
        if Passenger.objects.filter(user__email=data["email"]):
            raise exceptions.ValidationError("User with this email has already exist.")
        if data["role"] != 4:
            raise exceptions.ValidationError("Role is restricted.")
        return data

    def __send_verification_code(self, user):
        sms = SMS(user.passenger_profile.mobile_phone)
        return sms.send_msg(login=True)

    @transaction.atomic
    def create(self, validated_data):
        user = {
            "email": validated_data["email"],
            "password": validated_data["password"],
            "name": validated_data["name"],
            "surname": validated_data["surname"],
            "role": validated_data.get("role"),
        }

        user_created = get_user_model().objects.create_user(**user)
        user_created.passenger_profile.mobile_phone = validated_data["mobile_phone"]
        user_created.passenger_profile.gender = validated_data["gender"]
        user_created.passenger_profile.number_of_doc = validated_data["number_of_doc"]
        user_created.passenger_profile.iin = validated_data["iin"]
        user_created.passenger_profile.scan_udv = validated_data["scan_udv"]
        user_created.passenger_profile.save()

        # sent = self.__send_verification_code(user_created)

        # if sent:
        #     return user_created
        # else:
        #     raise exceptions.ValidationError("Unable to send verification code.")

        return user_created


class SmsActivationSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(required=True)
    code = serializers.CharField(max_length=4, required=True)


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self, instance):
        return get_profile_serializer(instance)

    class Meta:
        model = get_user_model()
        fields = ("email", "name", "surname", "role", "profile")
        read_only_fields = ("__all__",)


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("mobile_phone", "valid_number")
        read_only_fields = ("__all__",)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    mobile_phone = serializers.CharField(required=False)
    password = serializers.CharField()

    def authenticate(self, **kwargs):
        email = kwargs.get("email")
        mobile_phone = kwargs.get("mobile_phone")
        password = kwargs["password"]
        try:
            if email:
                user = User.objects.get(email=email)
                if user.check_password(password) is True:
                    return user
            elif mobile_phone:
                try:
                    user_profile = Passenger.objects.get(mobile_phone=mobile_phone)
                except Passenger.DoesNotExist:
                    # user_profile = Passenger.objects.get(
                    #     mobile_phone=mobile_phone
                    # )
                    return None
                if user_profile.user.check_password(password) is True:
                    return user_profile.user
            else:
                return None
        except User.DoesNotExist:
            return None

    def validate(self, data):
        user = self.authenticate(**data)
        if user and user.is_active:
            return user
        raise exceptions.AuthenticationFailed()


class UserUpdateSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    is_valid_email = serializers.BooleanField(required=False)
    password = serializers.CharField(required=False, allow_null=True)
    old_password = serializers.CharField(required=False, allow_null=True)

    def validate_mobile_phone(self, value):
        if value and not re.match("^\+77[0-9]{9}$", value):
            raise serializers.ValidationError("Неверный формат номера телефона")

        return value

    def create(self, validated_data):
        email = validated_data.get("email")
        sent = self.verify_email(email)
        return email, sent

    def update(self, instance, validated_data):
        """
        Если ошибку дает, значит не обновилась таблица с ролями
        Нужно подправить модельку
        """

        if "mobile_phone" in validated_data:
            if instance.role == 4:
                try:
                    Passenger.objects.exclude(user=instance).get(
                        mobile_phone=validated_data["mobile_phone"]
                    )
                    raise serializers.ValidationError(
                        "Номера телефона уже используется"
                    )
                except Passenger.DoesNotExist:
                    return None
        if validated_data.get("password") and validated_data.get("old_password"):
            if instance.check_password(validated_data.get("old_password")):
                instance.set_password(validated_data.get("password"))
            else:
                raise serializers.ValidationError("Неверный пароль")
        if validated_data.get("email"):
            if validated_data.get("is_valid_email") is True and validated_data.get(
                "email"
            ):
                if (
                    instance.is_valid_email is True
                    and instance.email == validated_data.get("email")
                ):
                    raise serializers.ValidationError(
                        "Пользователь уже подтвердил свой email"
                    )
                elif (
                    instance.is_valid_email is False
                    and instance.email == validated_data.get("email")
                ):
                    instance.is_valid_email = True
                else:
                    raise serializers.ValidationError("Неверный email")
            if validated_data.get("is_valid_email") is False:
                raise serializers.ValidationError(
                    "Валидность email не может установлена в отрицательное значение кроме системы"
                )

            else:
                instance.email = validated_data.get("email")
        instance.save()
        return instance

    def verify_email(self, email):
        try:
            user = User.objects.get(email=email)
            if user.is_valid_email:
                raise serializers.ValidationError("Данный email уже верифицирован")
            else:
                token = Token.objects.get_or_create(user=user)
                mail = Email(user.email)
                sent = mail.send_verification_email(token.key)
                if sent:
                    return True
                else:
                    raise SMTPException("Ошибка отправки письма")
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден")


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=False)
    mobile_phone = serializers.CharField(max_length=20, required=False)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32, required=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


def get_profile_serializer(*args, **kwargs):
    user = args[0]
    if user.role == 4:
        return PassengerSerializer(user.passenger_profile).data
