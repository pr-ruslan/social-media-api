from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import CustomUserViewSet

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='user')
urlpatterns = [
    path('', include(router.urls)),
]