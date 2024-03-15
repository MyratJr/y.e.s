from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('services-view', views.Services_View, basename='services_view')


urlpatterns = [
    path('', include(router.urls)),
    path('service-gallery/', views.Service_Gallery_ImagesView.as_view(), name='service_gallery'),
    path('service_gallery_destroy/<int:pk>/', views.Service_Gallery_DestroyView.as_view(), name='service-gallery-destroy'),
    path('categories_list/', views.All_CategoriesAPIView.as_view(), name='categories'),
    path('like_service/<int:pk>', views.LikeServiceAPIView.as_view(), name='like-user'),
    path('filter-service', views.FilterServiceList.as_view(), name='filter_service'),
    path('home-services', views.HomeServicesView.as_view({'get': 'list'}), name='home_services'),
    path('home-service-categories', views.HomeServiceCategoriesView.as_view({'get': 'list'}), name='home_service_categories'),
    path('home-advertisement', views.HomeAdvertisementView.as_view({'get': 'list'}), name='home_advertisements')
]