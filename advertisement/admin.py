from django.contrib import admin
from .models import Advertisement, AdvertisementChoises
from django.utils.html import format_html


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'expired_date', 'date_created', 'yagday')
    fields = ('title', 'image', 'status', 'expired_date', 'date_created')
    readonly_fields = ('date_created',)

    def yagday(self, obj):
        if obj.status==AdvertisementChoises.Kabul_Edildi:
            return format_html('<b style="color:green;">Kabul edildi</b>')
        elif obj.status==AdvertisementChoises.Showsyz:
            return format_html('<b style="color:red">Şowsuz</b>')
        elif obj.status==AdvertisementChoises.Garashylyar:
            return format_html('<b style="color:yellow">Garaşylýar</b>')
        else:
            return ''