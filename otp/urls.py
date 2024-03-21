from django.urls import path
from . import views


urlpatterns = [
    path('resend-otp-or-forgot-password/', views.ResendOTPORForgotPasswordView.as_view(), name='resend_otp_or_forgot_password'),
    path('sms-phone/', views.SMSPhoneView.as_view(), name="sms_phone"),
    path('activate-user/', views.ActivateUserAPIView.as_view(), name="activate_user"),
]