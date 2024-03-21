from django.contrib import admin
from .models import *


class PropertyVideoInline(admin.StackedInline):
    model = ServiceGalleryImage


admin.site.register(Service_Category)


@admin.register(Service)
class CarAdmin(admin.ModelAdmin):
    list_display = ('get_new_icon')
    inlines = [PropertyVideoInline]
    def get_new_icon(self, obj):
        if obj.is_new:  # Check if 'is_new' field exists (optional)
            return '<span style="color: green;">&#128187;</span>'  # Green star icon (replace with desired icon)
        else:
            return ''