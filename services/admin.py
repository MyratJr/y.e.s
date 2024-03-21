from django.contrib import admin
from .models import *
from django.utils.html import format_html
from ehyzmat.settings import MEDIA_URL

class PropertyVideoInline(admin.StackedInline):
    model = ServiceGalleryImage


admin.site.register(Service_Category)


@admin.register(Service)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'place', 'public', 'get_new_icon']
    inlines = [PropertyVideoInline]
    def get_new_icon(self, obj):
        if obj.is_new:
            return format_html('<img src="{}" width="45" height="45" style="position:fixed; margin-top:-1%">'.format(MEDIA_URL + 'service/service_images/new.gif'))
        else:
            return ''