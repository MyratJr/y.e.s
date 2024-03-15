from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import RegisterAPI, LoginAPI


schema_view = get_schema_view(
    openapi.Info(
        title="Django Sample Application API",
        default_version='v1',
        description="Welcome to the Django Sample Application API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

from django.conf.urls.static import static


urlpatterns = [
    path('api/swaggersalam', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('region/', include('places.urls')),
    path('service/', include('services.urls')),
    path('ratings/', include('ratings.urls')),
    path('otp/', include('otp.urls')),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    # path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('google_oauth2/', include('google_auth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)