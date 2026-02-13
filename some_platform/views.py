from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.exceptions import ValidationError

from some_platform.models import (UserProfile,
                                  Post,
                                  Like,
                                  Comment)
from user.models import Follow
from some_platform.serializers import (
    UserProfileSerializer,
    UserProfileLogoUploadSerializer,
    PostSerializer,
    CommentSerializer,
)
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class IsAdminOrSelfOrReadOnly(BasePermission):
    """
    Object-level permission:
    - Admins have full access
    - Users can act on their own object
    - Read-only requests are allowed for everyone
    """
    def has_object_permission(self, request, view, obj):
        # Always allow safe methods
        if request.method in SAFE_METHODS:
            return True

        # Admins can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Normal user can act only on their own object
        # For UserProfile, obj.user is the owner
        return hasattr(obj, "user") and obj.user == request.user


class UserProfileViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelfOrReadOnly]
    queryset = UserProfile.objects.all().select_related("user")
    filter_backends = [SearchFilter, DjangoFilterBackend,]

    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
    ]

    filterset_fields = ["gender"]

    @action(detail=False, methods=["get",])
    def me(self, request):
        profile = request.user.userprofile
        serializer = self.get_serializer(profile)

        return Response(serializer.data)

    def perform_create(self, serializer):
        if hasattr(self.request.user, "userprofile"):
            raise ValidationError("Profile already exists.")
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


class LikableViewSetMixin:
    @action(
        detail=True,
        methods=["post"],
        url_path="like"
    )
    def like(self, request, pk=None):
        obj = self.get_object()
        user = request.user

        content_type = ContentType.objects.get_for_model(obj)

        like, created = Like.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=obj.id,
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
        obj = self.get_object()
        user = request.user
        content_type = ContentType.objects.get_for_model(obj)

        deleted, _ = Like.objects.filter(
            user=user,
            content_type=content_type,
            object_id=obj.id,
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


class PostViewSet(LikableViewSetMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelfOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = {
        "author": ["exact"],
        "hashtags__name": ["exact"],
    }

    search_fields = ["title", "body"]

    def get_queryset(self):
        queryset = (
            Post.objects
            .select_related("author")
            .prefetch_related("hashtags")
        )

        following = self.request.query_params.get("following")

        if following == "true":
            user = self.request.user

            queryset = queryset.filter(
                Q(author=user) |
                Q(author__in=Follow.objects.filter(
                    follower=user
                ).values("following_id"))
            )

        return queryset


class CommentViewSet(LikableViewSetMixin, ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelfOrReadOnly]

    def get_queryset(self):
        return (
            Comment.objects
            .select_related("author", "post")
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

