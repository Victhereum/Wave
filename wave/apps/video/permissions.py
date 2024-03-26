from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from wave.utils.functions import access_control


class CanCreateCaption(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method not in SAFE_METHODS:
            return access_control(request)
        return True
