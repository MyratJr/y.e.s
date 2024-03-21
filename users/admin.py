from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Şahsy maglumat"), {"fields": ("first_name", "last_name", "email", "avatar", "banner_image", "experience", "address", "summary")}),
        (("Kontakt"), {"fields": ("web", "tiktok", "instagram", "imo", "phone")}),
        (("Ballar"), {"fields": ["rate_point", "rate_point_total", "point_counter", "view_counter", "like_counter"]}),
        (
            ("Rugsatlar"),
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
        (("Möhüm seneler"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
        (("Şahsy maglumat"), {"fields": ("email", "phone")}),
    )
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user == obj