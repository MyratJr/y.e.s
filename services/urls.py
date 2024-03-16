from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('services-view', views.Services_View, basename='services_view')


urlpatterns = [
    path('', include(router.urls)),
    path('service-gallery/', views.Service_Gallery_ImagesView.as_view(), name='service_gallery'),
    path('service-gallery-destroy/<int:id>/', views.Service_Gallery_DestroyView.as_view(), name='service_gallery_destroy'),
    path('service-categories/', views.All_CategoriesAPIView.as_view(), name='service_categories'),
    path('like-service/<int:id>/', views.LikeServiceAPIView.as_view(), name='like_user'),
    path('filter-service/', views.FilterServiceList.as_view(), name='filter_service'),
    path('home-services/', views.HomeServicesView.as_view({'get': 'list'}), name='home_services'),
    path('home-service-categories/', views.HomeServiceCategoriesView.as_view({'get': 'list'}), name='home_service_categories'),
    path('likes-to-service/', views.LikesToServiceView.as_view(), name='likes_to_service'),
    path('service-likes-from/', views.ServiceLikesFromUsersView.as_view(), name='service_likes_from')    ]