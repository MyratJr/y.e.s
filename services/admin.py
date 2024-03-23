from django.contrib import admin
from .models import *
from django.utils.html import format_html
from ehyzmat.settings import MEDIA_URL

class PropertyVideoInline(admin.StackedInline):
    model = ServiceGalleryImage

# format_html('<img src="{}" width="30" height="30" style="position:fixed; margin-top:-0.5%">'.format(MEDIA_URL + 'service/service_images/new.png'))
admin.site.register(Service_Category)

from django.utils.translation import gettext_lazy as _

@admin.register(Service)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'place', "yagday"]
    inlines = [PropertyVideoInline]
    
    def yagday(self, obj):
        if obj.status==ServiceVerification.Garashylyar:
            return _("Garaşylýar")
        elif obj.status==ServiceVerification.Showsyz:
            return _("Şowsuz")
        elif obj.status==ServiceVerification.Kabul_Edildi:
            return _("Kabul edildi")
        else:
            return ''