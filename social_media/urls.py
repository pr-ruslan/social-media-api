from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # auth urls
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),

    # api urls
    path("api/", include("user.urls")),
    path('api/some_platform/', include("some_platform.urls", namespace="some_platform"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
