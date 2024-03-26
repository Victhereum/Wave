from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from wave.apps.payments.views import SubscriptionViewSet
from wave.apps.users.api.views import UserViewSet
from wave.apps.video.views import CaptionViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("subscriptions", SubscriptionViewSet)
router.register("videos", CaptionViewSet)


app_name = "api"
urlpatterns = router.urls
