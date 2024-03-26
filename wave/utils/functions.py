from datetime import timedelta

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import QuerySet
from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request

from wave.apps.payments.models import SubscriptionPlan
from wave.apps.users.models import User
from wave.apps.video.models import Caption
from wave.utils.enums import SubscriptionPlans
from wave.utils.media import MediaHelper

ACCESS_STRUCTURE: dict = settings.ACCESS_STRUCTURE


def __access_structure(type) -> tuple:
    access = ACCESS_STRUCTURE.get(type)
    return access.get("COUNT"), access.get("LENGTH")


def access_control(request: Request):
    fs = FileSystemStorage()
    resource = request.FILES.get("resource")
    filename = fs.save(resource.name, resource)
    file_path = fs.path(filename)
    video_duration_str = MediaHelper.get_video_duration(file_path)

    video_duration = timedelta(seconds=video_duration_str).total_seconds()
    fs.delete(filename)
    user: User = request.user
    user_videos: QuerySet[Caption] = user.videos
    if settings.TESTING:
        return True
    plan: SubscriptionPlan = user.current_plan
    if plan.name == SubscriptionPlans.FREE:
        if video_duration > plan.max_duration:
            raise PermissionDenied(
                detail="The duration of this video is longer than the required limit, kindly upgrade to a paid plan"
            )
        trial_video_count = user_videos.count()
        if trial_video_count >= plan.slots:
            raise PermissionDenied(detail="You have exhausted the number of free trials")
        return True

    if user.has_active_subscription():
        if video_duration > plan.max_duration:
            raise PermissionDenied(
                detail="The duration of this video is longer than your current plan limit, kindly upgrade your plan"
            )
        paid_video_count = Caption.objects.filter(user=user, created_at__date=now().date()).count()
        if paid_video_count >= plan.slots:
            raise PermissionDenied(
                detail="You have exhausted the number of videos for this plan, kindly renew your plan"
            )
        return True
    raise PermissionDenied("You have exhausted your free plan and should subscribe to a paid plan to use this feature")
