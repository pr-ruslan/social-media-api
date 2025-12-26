from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


User = get_user_model()


def upload_to(instance, filename):
    return 'user_profile_image/{}/{}'.format(instance.user_id, filename)


class Hashtag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return f"#{self.name}"


class Post(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(
        Hashtag,
        related_name="posts",
        blank=True
    )


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author}"


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author} on  {self.post.title}"


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        "content_type",
        "object_id"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content_type", "object_id")

    def __str__(self):
        return f"{self.user} likes {self.content_object}"


class UserProfile(models.Model):
    GENDER_UNKNOWN = 'U'
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = (
        (GENDER_UNKNOWN, _('unknown')),
        (GENDER_MALE, _('male')),
        (GENDER_FEMALE, _('female')),
    )

    user = models.OneToOneField(User, primary_key=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    phone_number = PhoneNumberField(_('phone number'), blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    image = models.ImageField(_('image'), blank=True, null=True, upload_to=upload_to)

    def __str__(self):
        return f'{self.user.username} Profile'
