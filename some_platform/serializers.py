from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from some_platform.models import (
    UserProfile,
    Hashtag,
    Post,
    Comment,
    Like,
)


class UserProfileSerializer(serializers.ModelSerializer):
    # Read-only fields from related User model
    username = serializers.ReadOnlyField(source="user.username")
    email = serializers.ReadOnlyField(source="user.email")
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")

    # Human-readable gender label
    gender_display = serializers.CharField(
        source="get_gender_display",
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "phone_number",
            "gender",
            "gender_display",
            "logo",
        ]

    def validate_date_of_birth(self, value):
        from datetime import date

        if value and value > date.today():
            raise serializers.ValidationError(
                _("Date of birth cannot be in the future.")
            )
        return value



class UserProfileLogoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["logo"]

    def validate_logo(self, value):
        max_size = 2 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                _("Logo file size must be under 2MB.")
            )
        return value


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ["id", "name",]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.email")
    hashtags = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Hashtag.objects.all(),
        many=True,
        required=False,
    )
    class Meta:
        model = Post
        fields = ["id",
                  "title",
                  "body",
                  "author",
                  "created_at",
                  "hashtags"]
        read_only_fields = ["id", "created_at",]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.email")
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
    )

    class Meta:
        model = Comment
        fields = ["id",
                  "author",
                  "post",
                  "body",
                  "created_at",]
        read_only_fields = ["id", "created_at",]
