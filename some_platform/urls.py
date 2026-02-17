from rest_framework.routers import DefaultRouter
from django.urls import path, include

from some_platform.views import (UserProfileViewSet,
                                 PostViewSet, CommentViewSet, )

router = DefaultRouter()
router.register(    "profiles", UserProfileViewSet, basename="profile")
router.register("posts", PostViewSet)

router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "some_platform"