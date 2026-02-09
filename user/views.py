from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet

from user.models import CustomUser, Follow
from user.serializers import CustomUserSerializer


class FollowActionMixin:

    @action(detail=True,
            methods=['post'])
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


class CustomUserViewSet(FollowActionMixin, ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def followers(self, request, pk=None):
        user = self.get_object()
        qs = CustomUser.objects.filter(following__following=user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def following(self, request, pk=None):
        user = self.get_object()
        qs = CustomUser.objects.filter(followers__follower=user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

