from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from some_platform.models import Like


class LikableViewSetMixin:
    @extend_schema(
        summary="Like object",
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
    )
    @action(detail=True, methods=["post"], url_path="like")
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

    @extend_schema(
        summary="Unlike object",
        responses={204: None, 400: OpenApiTypes.OBJECT},
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
