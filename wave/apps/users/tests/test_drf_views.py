import pytest
from rest_framework.test import APIRequestFactory

from wave.apps.users.api.views import UserViewSet
from wave.apps.users.models import User


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore

        assert response.data["id"] == user.id
