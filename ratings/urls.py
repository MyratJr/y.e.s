from . import views
from django.urls import path


urlpatterns = [
    path('rate_user', views.RateUserView().as_view(), name='rate-user'),
]