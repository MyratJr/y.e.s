from django.urls import path
from .views import *


urlpatterns = [
    path('register', RegisterAPI.as_view(), name='register'),
    path('users-list', ListUsersView.as_view(), name='users_list'),
    path('update-user', UpdateUserAPIView.as_view(), name='update_user'),
    path('login', LoginAPI.as_view(), name='login'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('change-forgot-password', ChangeForgotPassword.as_view({'patch': 'partial_update'}), name='change_forgot_password'),
    path('user/<int:pk>', UserProfileView.as_view(), name='user'),
    path('like-user/<int:pk>', LikeUserView.as_view(), name='like-user'),
    path('likes-to', LikesToUsersView.as_view(), name='likes_to'),
    path('likes-from', LikesFromUsersView.as_view(), name='likes_from'),
    path('likes-to-service', LikesToServiceView.as_view(), name='likes_to_service'),
    path('service-likes-from', ServiceLikesFromUsersView.as_view(), name='service_likes_from'),
    path('user-services/<int:user_id>', UserProfilServicesView.as_view(), name='user_services')
]