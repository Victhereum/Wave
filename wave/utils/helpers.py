from django.conf import settings
from django.utils.timezone import datetime


class GenerateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + settings.SECRET_KEY
