from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/some_platform', include("some_platform.url", namespace="some_platform"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
