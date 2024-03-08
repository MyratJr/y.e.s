from . import views
from django.urls import path


urlpatterns = [
    path('from_rates/<int:pk>', views.RatesFromView().as_view(), name='from-rates'),
    path('rate_user', views.RateUserView().as_view(), name='rate-user'),
]