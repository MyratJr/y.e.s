from django.contrib import admin
from .models import *
from django.utils.html import format_html
from ehyzmat.settings import MEDIA_URL

class PropertyVideoInline(admin.StackedInline):
    model = ServiceGalleryImage


admin.site.register(Service_Category)


@admin.register(Service)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'place', 'public', 'new']
    inlines = [PropertyVideoInline]
    
    def new(self, obj):
        if obj.is_new:
            return format_html('<img src="{}" width="30" height="30" style="position:fixed; margin-top:-0.5%">'.format(MEDIA_URL + 'service/service_images/new.png'))
        else:
            return ''
        
from django.dispatch import receiver
@receiver(psender=CarAdmin)
def set_service_not_new(sender, request, object, **kwargs):
    if object:  # Check if object exists (might be None for list view actions)
        object.is_new = False
        object.save()