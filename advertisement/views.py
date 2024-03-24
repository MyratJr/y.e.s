from advertisement.models import Advertisement, AdvertisementChoises
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from rest_framework.response import Response
    

class HomeAdvertisementView(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Advertisement.objects.filter(status=AdvertisementChoises.Kabul_Edildi)
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