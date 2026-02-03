from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from rest_framework.response import Response
from rest_framework import status, generics

from some_platform.models import UserProfile, Post, Like
from some_platform.serializers import (
    UserProfileSerializer,
    UserProfileLogoUploadSerializer,
    PostSerializer,
    CommentSerializer, LikeSerializer
)
from some_platform.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action


class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminOrIsSelf]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user.userprofile

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=["patch", "put"],
        url_path="logo",
        parser_classes=[MultiPartParser, FormParser],
    )
    def upload_logo(self, request):
        """
        Upload or replace user profile logo.
        """
        profile = self.get_object()

        serializer = UserProfileLogoUploadSerializer(
            instance=profile,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            UserProfileSerializer(profile).data,
            status=status.HTTP_200_OK,
        )


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        url_path="like"
    )
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        content_type = ContentType.objects.get_for_model(post)

        like, created = Like.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=post.id,
        )
        if not created:
            return Response(
                {"detail": "Already liked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Post liked."},
            status=status.HTTP_201_CREATED,
        )

    @like.mapping.delete
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(post)

        deleted, _ = Like.objects.filter(
            user=user,
            content_type=content_type,
            object_id=post.id,
        ).delete()

        if deleted == 0:
            return Response(
                {"detail": "Not liked yet."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Post unliked."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]