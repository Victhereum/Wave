from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("name", "phone_no")}),
        (_("Subscription info"), {"fields": ("free_mode_activated", "free_mode_activated_at", "date_joined")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    list_display = ["name", "phone_no"]
    search_fields = ["name", "phone_no"]
    ordering = ["name", "phone_no"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_no", "password1", "password2"),
            },
        ),
    )
