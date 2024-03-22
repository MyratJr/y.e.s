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
        
    def changeview(self, request, object_id, form_url=None, extra_context=None):
            service = Service.objects.get(pk=object_id)
            service.is_new=False
            service.save()
            return super().changeview(request, object_id, form_url, extra_context)