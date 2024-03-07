# from . import views
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter


# router=DefaultRouter()
# router.register('service', views.ServicesListAPIView, basename='service-categories-list')


# urlpatterns = [
#     path('service-categories/', include(router.urls)),
#     path('service_gallery_image/', views.Service_Gallery_ImagesAPIView.as_view(), name='service-gallery-images'),
#     path('home/', views.HomeDataView.as_view(), name='home-datas'),
#     path('categories_list/', views.All_CategoriesAPIView.as_view(), name='categories'),
#     path('like_service/<int:pk>', views.LikeServiceAPIView.as_view(), name='like-user'),
#     path('filter-service', views.FilterServiceList.as_view(), name='filter_service'),
# ]
