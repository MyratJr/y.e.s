from django.urls import path, re_path
from . import views


urlpatterns = [
    path('users-list/', views.ListUsersView.as_view(), name='users_list'),
    path('update-user/', views.UpdateUserAPIView.as_view(), name='update_user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('change-forgot-password/', views.ChangeForgotPassword.as_view({'patch': 'partial_update'}), name='change_forgot_password'),
    path('user/<uuid:id>/', views.UserProfileView.as_view(), name='user'),
    path('like-user/<uuid:id>/', views.LikeUserView.as_view(), name='like_user'),
    path('likes-to/', views.LikesToUsersView.as_view(), name='likes_to'),
    path('likes-from/', views.LikesFromUsersView.as_view(), name='likes_from'),
    re_path('^user-services/(?P<id>.+)/$', views.UserServicesView.as_view()),
]