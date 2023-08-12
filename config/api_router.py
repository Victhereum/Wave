from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from wave.apps.payments.views import PaymentViewSet
from wave.apps.users.api.views import UserViewSet
from wave.apps.video.views import VideoViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("payments", PaymentViewSet)
router.register("videos", VideoViewSet)


app_name = "api"
urlpatterns = router.urls
