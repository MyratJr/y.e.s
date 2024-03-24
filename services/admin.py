from django.contrib import admin
from .models import *
from django.utils.html import format_html
from ehyzmat.settings import MEDIA_URL


class PropertyVideoInline(admin.StackedInline):
    model = ServiceGalleryImage


# format_html('<img src="{}" width="30" height="30" style="position:fixed; margin-top:-0.5%">'.format(MEDIA_URL + 'service/service_images/new.png'))
admin.site.register(Service_Category)


@admin.register(Service)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'place', "yagday"]
    readonly_fields = ('date_created',)
    inlines = [PropertyVideoInline]
    
    def yagday(self, obj):
        if obj.status==ServiceVerification.Kabul_Edildi:
            return format_html('<b style="color:green;">Kabul edildi</b>')
        elif obj.status==ServiceVerification.Showsyz:
            return format_html('<b style="color:red">Şowsuz</b>')
        elif obj.status==ServiceVerification.Garashylyar:
            return format_html('<b style="color:yellow">Garaşylýar</b>')
        else:
            return ''