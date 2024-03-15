from django.core.validators import RegexValidator
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from advertisement.models import Advertisement
from rest_framework import viewsets, mixins
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


phone_regex = RegexValidator(
        regex=r"^\+(?:99361|99362|99363|99364|99365|99371)\d{6}$",
        message="Phone number must be entered in the format +99361-->65XXXXXX or +99371XXXXXX, where XXXXXXX is the 7-digit subscriber number."
    )


def validate_image(image):
    max_width = 1024
    max_height = 768
    width, height = get_image_dimensions(image)
    
    if width > max_width or height > max_height:
        raise ValidationError("Image dimensions exceed allowed limits: %(width)sx%(height)s. Maximum allowed: %(max_width)sx%(max_height)s." % {
            'width': width,
            'height': height,
            'max_width': max_width,
            'max_height': max_height,
        })
    

class HomeAdvertisementView(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Advertisement.objects.filter(is_active=True)
    serializer_class = HomeAdvertisementsSerializers
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser,FormParser]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)