from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('services-view', views.Services_View, basename='services_view')


urlpatterns = [
    path('', include(router.urls)),
    path('service_gallery_image/', views.Service_Gallery_ImagesAPIView.as_view(), name='service-gallery-images'),
    path('service_gallery_destroy/', views.Service_Gallery_DestroyView.as_view(), name='service-gallery-destroy'),
    path('home/', views.HomeDataView.as_view(), name='home-datas'),
    path('categories_list/', views.All_CategoriesAPIView.as_view(), name='categories'),
    path('like_service/<int:pk>', views.LikeServiceAPIView.as_view(), name='like-user'),
    path('filter-service', views.FilterServiceList.as_view(), name='filter_service'),
]
