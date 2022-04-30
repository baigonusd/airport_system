from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class Email:
    def __init__(self, email):
        self.email = email

    def send_verification_email(self, token):
        try:
            send_mail(
                subject="Верификация почтового ящика на портале Airport System",
                message="Пройдите по данной ссылке чтобы верифицировать данный почтовый ящик: {}".format(
                    settings.FRONTEND_URL + "validate-email/?t=" + token.key
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.email],
                html_message="Пройдите по данной ссылке чтобы верифицировать данный почтовый ящик: {}".format(
                    settings.FRONTEND_URL + "validate-email/?t=" + token.key
                ),
            )
            return True
        except SMTPException:
            raise Exception("SMTP exception")
