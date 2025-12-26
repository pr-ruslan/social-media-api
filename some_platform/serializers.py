from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from some_platform.models import (
    UserProfile,
)

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    phone_number = PhoneNumberField()
    class Meta:
        model = UserProfile
        fields = ('url', 'date_of_birth', 'phone_number', 'gender', 'image')
        readonly_fields = ('url', 'image')
