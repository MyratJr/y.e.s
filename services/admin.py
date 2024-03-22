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
            return format_html('<img src="{}" width="30" height="30" style="position:fixed;margin-left:0.5%; margin-top:-0.5%">'.format(MEDIA_URL + 'service/service_images/new.png'))
        else:
            return ''
    
    def changeform_view(self, request, object_id=None, form=None, extra_context=None):
        if object_id:
            product = Service.objects.get(pk=object_id)
            product.is_new = True
            product.save()
        return super().changeform_view(request, object_id, form, extra_context)