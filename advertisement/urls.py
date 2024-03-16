from . import views
from django.urls import path


urlpatterns = [
    path('home-advertisements/', views.HomeAdvertisementView.as_view({'get': 'list'}), name='home_advertisements')
]