from . import views
from django.urls import path


urlpatterns = [
    path('user_ratings/<int:pk>', views.User_CommentsAPIView().as_view(), name='user_rates'),
    path('user_ratings', views.Leave_CommentAPIView().as_view(), name='leave_comment'),
]