from django.contrib import admin
from .models import *


class PropertyVideoInline(admin.StackedInline):
    model = ServiceGalleryImage


admin.site.register(Service_Category)
admin.site.register(ServiceGalleryImage)


@admin.register(Service)
class CarAdmin(admin.ModelAdmin):
    inlines = [PropertyVideoInline]