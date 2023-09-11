from datetime import timedelta

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request

from wave.apps.users.models import User
from wave.apps.video.models import Video
from wave.utils.enums import FreeModeChoices
from wave.utils.media import MediaHelper

ACCESS_STRUCTURE: dict = settings.ACCESS_STRUCTURE


def __access_structure(type) -> tuple:
    access = ACCESS_STRUCTURE.get(type)
    return access.get("COUNT"), access.get("LENGTH")


def access_control(request: Request):
    fs = FileSystemStorage()
    media = request.FILES.get("media")
    filename = fs.save(media.name, media)
    file_path = fs.path(filename)
    video_duration_str = MediaHelper.get_video_duration(file_path)

    video_duration = timedelta(seconds=video_duration_str).total_seconds()
    fs.delete(filename)
    user: User = request.user

    if settings.TESTING:
        return True

    if user.free_mode_status == FreeModeChoices.ACTIVE:
        trial_count, trial_limit = __access_structure("TRIAL")
        if video_duration > trial_limit:
            raise PermissionDenied(
                detail="The duration of this video is longer than the required limit, kindly upgrade to a paid plan"
            )
        trial_video_count = Video.objects.filter(user=user, created_at__date=now().date()).count()
        if trial_video_count >= trial_count:
            raise PermissionDenied(detail="You have exhausted the number of free trials")
        return True

    if user.has_active_subscription():
        paid_count, paid_limit = __access_structure("PAID")
        if video_duration > paid_limit:
            raise PermissionDenied(
                detail="The duration of this video is longer than your current plan limit, kindly upgrade your plan"
            )
        paid_video_count = Video.objects.filter(user=user, created_at__date=now().date()).count()
        if paid_video_count >= paid_count:
            raise PermissionDenied(
                detail="You have exhausted the number of videos for this plan, kindly renew your plan"
            )
        return True
    raise PermissionDenied("You need to subscribe to a paid plan to use this feature")
