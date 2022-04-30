import requests
import random

from django.conf import settings
from django.core.cache import cache


class SMS:

    # url = settings.SMS_PROVIDER_URL
    # params = {
    #     "action": "sendmessage",
    #     "username": settings.SMS_PROVIDER_USERNAME,
    #     "password": settings.SMS_PROVIDER_PASSWORD,
    #     "message:type": "SMS:TEXT",
    #     "originator": "INFO_KAZ",
    # }
    params = {}
    login_message = "Airport System. Ваш код доступа: {}"
    # notif_message = 'MSB.KZ. Вы вошли в систему'

    def __init__(self, user_phone, **kwargs):
        self.params["recipient"] = user_phone

    def gen_code(self):
        return random.randint(1000, 9999)

    def send_activation_code(self, login: bool):
        if self.params.get("recipient") is None:
            return False
        elif login:
            key = "login_" + self.params["recipient"]
            if cache.get(key) is None:
                code = self.gen_code()
                self.params["messagedata"] = self.login_message.format(code)
                try:
                    if self.url == "Test":
                        return True
                    r = requests.get(self.url, params=self.params)
                    cache.set(key, code, settings.SMS_CODE_TTL)
                except requests.exceptions.ConnectionError:
                    raise Exception({"detail": "SMS CONNECTION ERROR"})
            else:
                raise Exception({"detail": "SMS ALREADY SENT"})
            return True
        elif login is False:
            # self.params['messagedata'] = self.notif_message
            return False

        else:
            return False
