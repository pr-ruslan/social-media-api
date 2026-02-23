from rest_framework import serializers

from user.models import CustomUser, Follow


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email"]
