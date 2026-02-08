from rest_framework.routers import DefaultRouter
from django.urls import path, include

from some_platform.views import (UserProfileViewSet,
    PostViewSet,)

router = DefaultRouter()
router.register(
    r"profile",
    UserProfileViewSet,
    basename="profile"
)
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "some_platform"