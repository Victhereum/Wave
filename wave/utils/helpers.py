from django.utils.timezone import datetime
from django.conf import settings
class GenerateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + settings.SECRET_KEY
