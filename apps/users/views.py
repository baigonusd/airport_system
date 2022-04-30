import logging
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User, Passenger

from .serializers import (
    UserSignupSerializer,
    SmsActivationSerializer,
    UserSerializer,
    LoginUserSerializer,
    UserUpdateSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
)


class SignupAPI(generics.GenericAPIView):
    logger = logging.getLogger("autorization")
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        session_id = request.session._get_or_create_session_key()
        email = request.data["email"]
        phone = request.data["mobile_phone"]

        if User.objects.filter(email=email).exists():
            return Response(
                f"User with email {email} already registered.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif User.objects.filter(passenger_profile__mobile_phone=phone).exists():
            return Response(
                f"User with mobile phone {phone} already registered.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # user = User.objects.get(email=serializer.validated_data["email"])
            self.logger.info(
                {
                    "session_id": session_id,
                    "message": "Unverified user with email {} registered".format(email),
                }
            )

            return Response(
                data={"message": f"User {email} is succesfully created"},
                status=status.HTTP_201_CREATED,
            )


class ActivationAPI(generics.GenericAPIView):
    logger = logging.getLogger("authorization")
    permission_classes = [permissions.AllowAny]
    serializer_class = SmsActivationSerializer

    def post(self, request, *args, **kwargs):
        session_id = request.session._get_or_create_session_key()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(
            passenger_profile__mobile_phone=serializer.data["mobile_phone"]
        )
        # key = "login_" + serializer.data["mobile_phone"]
        # if serializer.data["code"] == str(cache.get(key)):
        if serializer.data["code"] == "0000":
            user.is_active = True
            user.passenger_profile.valid_number = True
            user.save()

            self.logger.info(
                {
                    "User": user.id,
                    "session_id": session_id,
                    "message": "User with mobile_phone: {} activated".format(
                        user.passenger_profile.mobile_phone
                    ),
                }
            )
            token, _ = Token.objects.get_or_create(user=user)
            self.logger.info(
                {
                    "User": user.pk,
                    "session_id": session_id,
                    "message": "User with email {} logged in".format(user.email),
                }
            )
            return Response(
                {
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": token.key,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            "Provided code does not match!", status=status.HTTP_400_BAD_REQUEST
        )


class LoginAPI(generics.GenericAPIView):
    logger = logging.getLogger("authorization")
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        session_id = request.session._get_or_create_session_key()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token, _ = Token.objects.get_or_create(user=user)

        self.logger.info(
            {
                "User": user.pk,
                "session_id": session_id,
                "message": "User with email {} logged in".format(user.email),
            }
        )
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": token.key,
            },
            status.HTTP_201_CREATED,
        )


class LogoutAPI(generics.GenericAPIView):
    logger = logging.getLogger("authorization")
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        session_id = request.session._get_or_create_session_key()
        print(request.user)
        self.logger.info(
            {
                "User": request.user,
                "session_id": session_id,
                "message": "User with email {} logout".format(request.user.email),
            }
        )
        request.auth.delete()
        return Response(
            {
                "detail": "Logout OK",
            },
            status.HTTP_201_CREATED,
        )


class UserAPI(generics.GenericAPIView):
    logger = logging.getLogger("authorization")
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer
    serializer_update_class = UserUpdateSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.serializer_class
        else:
            return self.serializer_update_class

    def get(self, request, *args, **kwargs):
        session_id = request.session._get_or_create_session_key()
        self.logger.info(
            {
                "User": request.user,
                "session_id": session_id,
                "message": "Get user ({}) profile data".format(request.user.email),
            }
        )
        return Response(
            {
                "user": UserSerializer(
                    request.user, context=self.get_serializer_context()
                ).data
            },
            status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        session_id = request.session._get_or_create_session_key()
        self.logger.info(
            {
                "User": request.user,
                "session_id": session_id,
                "message": "User ({}) send email verification".format(
                    request.user.email
                ),
            }
        )
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        email, _ = serializer.save()
        if _:
            return Response(
                {"detail": "Email verification to {} sent".format(email)},
                status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Email already verified"}, status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, *args, **kwargs):
        session_id = request.session._get_or_create_session_key()
        self.logger.info(
            {
                "User": request.user,
                "session_id": session_id,
                "message": "Update user ({}) profile data".format(request.user.email),
            }
        )
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    request.user, context=self.get_serializer_context()
                ).data
            },
            status.HTTP_200_OK,
        )


class ForgotPasswordAPI(generics.GenericAPIView):
    logger = logging.getLogger("authorization")
    serializer_post_class = ForgotPasswordSerializer
    serializer_put_class = ResetPasswordSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return self.serializer_post_class
        else:
            return self.serializer_put_class

    def get_permissions(self):
        if self.request.method in [
            "POST",
        ]:
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        session_id = request.session._get_or_create_session_key()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if data.get("email"):
            try:
                user = get_user_model().objects.get(email=data["email"])
            except get_user_model().DoesNotExist:
                return Response(
                    {"detail": "User with this email does not exist"},
                    status.HTTP_404_NOT_FOUND,
                )
        elif data.get("mobile_phone"):
            try:
                user = Passenger.objects.get(mobile_phone=data["mobile_phone"]).user
            except Passenger.DoesNotExist:
                return Response(
                    {"detail": "User with this mobile phone does not exist"},
                    status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"detail": "Email or mobile phone is required"},
                status.HTTP_400_BAD_REQUEST,
            )

        if user.is_active:

            token, _ = Token.objects.get_or_create(user=user)

            self.logger.info(
                {
                    "User": user.pk,
                    "session_id": session_id,
                    "message": "User with email {} forgot password".format(user.email),
                }
            )
            try:
                send_mail(
                    subject="Сброс пароля на платформе Airport System",
                    message="Пройдите по данной ссылке чтобы сбросить пароль: {}".format(
                        settings.FRONTEND_URL + "reset-password/?t=" + token.key
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message="Пройдите по данной ссылке чтобы сбросить пароль: {}".format(
                        settings.FRONTEND_URL + "reset-password/?t=" + token.key
                    ),
                )
                return Response(status=status.HTTP_200_OK)
            except SMTPException:
                return Response(
                    "SMTP exception", status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response({"detail": "User is not active"}, status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        session_id = request.session._get_or_create_session_key()
        self.logger.info(
            {
                "User": request.user,
                "session_id": session_id,
                "message": "Update user ({}) profile data".format(request.user.email),
            }
        )
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    request.user, context=self.get_serializer_context()
                ).data
            },
            status.HTTP_200_OK,
        )
