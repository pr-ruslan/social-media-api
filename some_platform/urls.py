from rest_framework.routers import DefaultRouter
from django.urls import path, include

from some_platform.views import UserProfileViewSet

router = DefaultRouter()
router.register(
    r"profile",
    UserProfileViewSet,
    basename="profile"
)

urlpatterns = [
    path("/", include(router.urls)),
]