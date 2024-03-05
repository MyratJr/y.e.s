from django.urls import path
from . import views

urlpatterns = [
    path('regions/', views.SnippetList.as_view(), name='regions-list'),
]