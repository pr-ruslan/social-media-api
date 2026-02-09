from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, F
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser,
                                 on_delete=models.CASCADE,
                                 related_name="following")
    following = models.ForeignKey(CustomUser,
                                  on_delete=models.CASCADE,
                                  related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        indexes = [models.Index(fields=["follower"]),
                   models.Index(fields=["following"])]
        constraints = [
            models.CheckConstraint(
                check=~Q(follower=F("following")),
                name="prevent_self_follow",
            )
        ]

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("You cannot follow yourself!")


