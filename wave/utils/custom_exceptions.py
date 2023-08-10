from rest_framework import status
from rest_framework.exceptions import APIException


class CustomError:
    class Forbidden(APIException):
        status_code = status.HTTP_403_FORBIDDEN
        default_detail = "forbidden"
        default_code = "forbidden"

    class BadRequest(APIException):
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "bad request"
        default_code = "bad_request"
