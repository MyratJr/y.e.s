from django.contrib import admin
from .models import *
from django.utils.html import format_html

class PropertyVideoInline(admin.StackedInline):
    model = ServiceGalleryImage


admin.site.register(Service_Category)


@admin.register(Service)
class CarAdmin(admin.ModelAdmin):
    list_display = ['get_new_icon']
    inlines = [PropertyVideoInline]
    def get_new_icon(self, obj):
        if obj.is_new:
            return format_html('<img src="../../otp/new.png">')
        else:
            return ''