from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from user.models import Follow


class FollowActionMixin:

    @extend_schema(
        summary="Follow user",
        responses={201: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
    )
    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):

        target = self.get_object()
        follower = request.user

        if target.id == follower.id:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        _, created = Follow.objects.get_or_create(
            follower = follower,
            following = target
        )

        if not created:
            return Response(
                {"detail": "Already following."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "You are now following {}.".format(target.email)},
             status=status.HTTP_201_CREATED
            )

    @extend_schema(
        summary="Unfollow user",
        responses={204: None, 400: OpenApiTypes.OBJECT},
    )
    @follow.mapping.delete
    def unfollow(self, request, pk=None):
        target = self.get_object()
        follower = request.user

        deleted, _  = Follow.objects.filter(
            follower = follower,
            following = target
        ).delete()

        if deleted == 0:
            return Response(
                {"detail": "You are not following this user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
