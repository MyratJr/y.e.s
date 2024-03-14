from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .models import Service, ServiceGalleryImage, Service_Category
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from ratings.models import View_Service, Like_Service
from rest_framework import viewsets, mixins, generics
from advertisement.models import Advertisement
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *


class Services_View(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser,FormParser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user and request.user.is_authenticated:
            service, created = View_Service.objects.get_or_create(user=request.user, service=instance)
            if created:
                instance.view_counter = instance.view_counter + 1
                instance.save()
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().select_related('user'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Service_Gallery_ImagesAPIView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView,mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]
    queryset = ServiceGalleryImage.objects.all()
    serializer_class = ServiceGalleryImageSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# class Service_Gallery_DestroyView(mixins.DestroyModelMixin, generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser,FormParser]
#     queryset = ServiceGalleryImage.objects.all()

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class HomeDataView(APIView):
    permission_classes= [AllowAny]

    def get(self, request):
        services = Service.objects.all(vip_is_active=True)
        categories = Service_Category.objects.all()
        advertisements = Advertisement.objects.filter(is_active=True)
        services_serializer = HomeServicesSerializers(services, many=True, context={'request': request})
        categories_serializer = HomeCategoriesSerializers(categories, many=True, context={'request': request})
        advertisement_serializer = HomeAdvertisementsSerializers(advertisements, many=True, context={'request': request})
        data = [advertisement_serializer.data, categories_serializer.data, services_serializer.data]
        return Response(data, status=status.HTTP_200_OK)
    

class All_CategoriesAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Service_Category.objects.all()
    serializer_class = HomeCategoriesSerializers
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class LikeServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        liked_service = get_object_or_404(Service, pk=pk)
        user, created = Like_Service.objects.get_or_create(user=request.user,service=liked_service)
        if created:
            liked_service.like_counter += 1
            liked_service.save()
        return Response({"success": True, "likes": liked_service.like_counter})

    
class FilterServiceList(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializers
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__username', 'user__firs_tname', 'name', 'category__name']
    ordering_fields = ["user__rate_point", "experience"]
    filterset_fields = ['category', 'place']