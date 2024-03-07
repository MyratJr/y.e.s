# from knox import views as knox_views
from django.urls import path
from .views import *


urlpatterns = [
    path('api/register', RegisterAPI.as_view(), name='register'),
    path('get-users', GetUsersAPIView.as_view(), name='get_users'),
    path('update-user/<int:pk>', UpdateUserAPIView.as_view(), name='update_user'),
    path('api/login', LoginAPI.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('change-forgot-password/<int:pk>', ChangeForgotPassword.as_view({'patch': 'partial_update'}), name='change_forgot_password'),
    # path('api/logout', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('user/<int:pk>', User_CategoriesAPIView.as_view(), name='user'),
    path('users/<int:pk>', LikeUserAPIView.as_view(), name='like-user'),
    path('get-objects/', LikeToUserView.as_view(), name='get_objects'),
    path('get-my-like/', LikeOfUserView.as_view(), name='get_my_like'),
]