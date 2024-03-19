from django.urls import path
from . import views


urlpatterns = [
    path('post_otp/', views.OTPView.as_view(), name='otp'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('list-phones', views.ListPhoneNumbersView.as_view(), name='list_phones')
]