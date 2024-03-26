from django.contrib import admin

from wave.apps.payments.models import Subscriptions


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status")
    list_filter = ("plan",)
    search_fields = ("user__name", "user__phone_no")
    readonly_fields = ("user", "plan", "status", "metadata")

    def has_add_permission(self, request):
        return False  # Disable adding new payments from admin

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("user")

    @admin.display(description="User Phone")
    def user_phone(self, obj: Subscriptions):
        return obj.user.phone_no if obj.user else None
