from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("user", "media_path", "was_captioned")
    list_filter = ("user", "was_captioned")
    search_fields = ("user__phone_no", "user__phone_no", "media_path")
    readonly_fields = ("user", "media_path", "was_captioned", "captions")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("user")

    @admin.display(description="User Phone")
    def user_phone(self, obj):
        return obj.user.phone_no if obj.user else None
