from django.contrib import admin
from .models import *


class PropertyVideoInline(admin.StackedInline):
    model = ServiceGalleryImage


admin.site.register(Service_Category)


@admin.register(Service)
class CarAdmin(admin.ModelAdmin):
    list_display = ['get_new_icon']
    inlines = [PropertyVideoInline]
    def get_new_icon(self, obj):
        if obj.is_new:
            return '<span style="color: green;">&#128187;</span>'
        else:
            return ''