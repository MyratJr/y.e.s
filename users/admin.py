from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = [
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
    ]

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


    def get_queryset(self, request):
        if not request.user.is_superuser:
            self.fieldsets.pop(3)
            self.fieldsets.pop(4)
            self.fieldsets.pop(5)
            return super().get_queryset(request).filter(id=request.user.id)
        return super().get_queryset(request)