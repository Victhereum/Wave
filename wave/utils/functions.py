from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from rest_framework.request import Request

from wave.apps.users.models import User
from wave.apps.video.models import Video
from wave.utils.choices import FreeModeChoices

ACCESS_STRUCTURE: dict = settings.ACCESS_STRUCTURE


def __access_structure(type) -> tuple:
    access = ACCESS_STRUCTURE.get(type)
    return access.get("COUNT"), access.get("LIMIT")


def access_control(request: Request):
    # FIXME: Add access control, using the new payment system
    video_duration_str = request.data.get("duration", "00:01:30")
    video_duration_parts = video_duration_str.split(":")
    video_duration = timedelta(
        hours=int(video_duration_parts[0]), minutes=int(video_duration_parts[1]), seconds=int(video_duration_parts[2])
    ).seconds

    user: User = request.user

    if user.free_mode_status == FreeModeChoices.ACTIVE:
        trial_count, trial_limit = __access_structure("TRIAL")
        if video_duration > trial_limit:
            return False
        trial_video_count = Video.objects.filter(user=user, created_at__date=now().date()).count()
        if trial_video_count >= trial_count:
            print(trial_video_count)
            return False
        return True

    if user.has_active_subscription():
        paid_count, paid_limit = __access_structure("PAID")
        if video_duration > paid_limit:
            return False
        paid_video_count = Video.objects.filter(user=user, created_at__date=now().date()).count()
        if paid_video_count >= paid_count:
            return False
        return True
