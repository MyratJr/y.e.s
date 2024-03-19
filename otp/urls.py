from django.urls import path
from . import views


urlpatterns = [
    path('post_otp/', views.OTPView.as_view(), name='otp'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('sms-phone', views.SMSPhoneView.as_view(), name="sms_phone"),
    path('activate-user', views.ActivateUserAPIView.as_view(), name="activate_user"),
]