from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email", "avatar", "banner_image", "experience", "address", "summary")}),
        (("Contact"), {"fields": ("web", "tiktok", "instagram", "imo", "phone")}),
        (("Points"), {"fields": ["rate_point", "rate_point_total", "point_counter", "view_counter", "like_counter"]}),
        (
            ("Permissions"),
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
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
        (("Personal info"), {"fields": ("email", "phone_number")}),
    )