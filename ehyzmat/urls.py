from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from users.views import RegisterAPI, LoginAPI
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="Y.E.S API",
        default_version='v1',
        description="Welcome to the Y.E.S API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('region/', include('places.urls')),
    path('service/', include('services.urls')),
    path('advertisement/', include('advertisement.urls')),
    path('ratings/', include('ratings.urls')),
    path('otp/', include('otp.urls'), namespace="otp_view"),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterAPI.as_view(), name='register'),
    path('auth/login/', LoginAPI.as_view(), name='login'),
    path('auth/', include('google_auth.urls')),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)