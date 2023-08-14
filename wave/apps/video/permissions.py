from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from wave.apps.users.models import User


class CanCreateVideo(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        user: User = request.user
        if request.method not in SAFE_METHODS:
            return user.has_permission()
        return True
