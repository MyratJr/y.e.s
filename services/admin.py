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
    list_display = ['name', 'category', 'place', "status"]
    inlines = [PropertyVideoInline]
    
    def status(self, obj):
        if obj.status==ServiceVerification.Garashylyar:
            return "Garaşylýar"
        elif obj.status==ServiceVerification.Showsyz:
            return "Şowsuz"
        elif obj.status==ServiceVerification.Kabul_Edildi:
            return "Kabul edildi"
        else:
            return ''