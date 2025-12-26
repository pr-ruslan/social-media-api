from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from rest_framework.response import Response
from rest_framework import status

from some_platform.models import UserProfile
from some_platform.serializers import (
    UserProfileSerializer,
    UserProfileLogoUploadSerializer,
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