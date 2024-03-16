from django.contrib import admin
from .models import Advertisement

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'expired_date', 'date_created')
    fields = ('title', 'image', 'is_active', 'expired_date', 'date_created')
    readonly_fields = ('date_created',)