from . import views
from django.urls import path


urlpatterns = [
    path('rate-user', views.RateUserView().as_view(), name='rate_user'),
    path('rates-to', views.RatesToUsersView.as_view(), name='rates_to'),
    path('rates-from', views.RatesFromUsersView.as_view(), name='rates_from'),
]