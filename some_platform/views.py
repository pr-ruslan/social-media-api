from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from some_platform.models import (UserProfile,
                                  Post,
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
from some_platform.permissions import IsAdminOrSelfOrReadOnly
from some_platform.mixins import LikableViewSetMixin


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

    @extend_schema(
        summary="Get current user's profile",
        responses=UserProfileSerializer,
    )
    @action(detail=False, methods=["get"])
    def me(self, request):
        profile = request.user.userprofile
        serializer = self.get_serializer(profile)

        return Response(serializer.data)

    def perform_create(self, serializer):
        if hasattr(self.request.user, "userprofile"):
            raise ValidationError("Profile already exists.")
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Upload profile logo",
        request=UserProfileLogoUploadSerializer,
        responses=UserProfileSerializer,
    )
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


class PostViewSet(LikableViewSetMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelfOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="following",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Return posts from users the current user follows (true/false)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
