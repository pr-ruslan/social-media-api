from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_spectacular.utils import extend_schema

from user.models import CustomUser
from user.serializers import CustomUserSerializer
from user.mixins import FollowActionMixin


class CustomUserViewSet(FollowActionMixin, ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get user's followers",
        responses=CustomUserSerializer(many=True),
    )
    @action(detail=True, methods=["get"])
    def followers(self, request, pk=None):
        user = self.get_object()
        qs = CustomUser.objects.filter(following__following=user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get user's followers",
        responses=CustomUserSerializer(many=True),
    )
    @action(detail=True, methods=["get"])
    def following(self, request, pk=None):
        user = self.get_object()
        qs = CustomUser.objects.filter(followers__follower=user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
