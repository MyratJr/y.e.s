from django.contrib import admin
from .models import Advertisement


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'is_active', 'expired_date', 'date_created')
    fields = ('title', 'image', 'is_active', 'expired_date')
    readonly_fields = ('date_created',)


admin.site.register(Advertisement, AdvertisementAdmin)