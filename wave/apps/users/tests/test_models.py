from wave.apps.users.models import User


def test_user_get_absolute_url(user: User):
    print(user.get_absolute_url())
    assert user.get_absolute_url() == f"/api/v1/users/{user.id}/"
