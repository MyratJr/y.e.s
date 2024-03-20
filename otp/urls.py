from django.urls import path
from . import views


urlpatterns = [
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend_otp'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('sms-phone/', views.SMSPhoneView.as_view(), name="sms_phone"),
    path('activate-user/', views.ActivateUserAPIView.as_view(), name="activate_user"),
]