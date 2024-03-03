from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser
from rest_framework import serializers
User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField( write_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'password', 'email', 'referral_code', 'profile_photo', 'bio')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# link_manager/serializers.py

from rest_framework import serializers
from .models import Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [ 'user_id', 'url']
        read_only_fields = ['id']

class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'address', 'gender', 'profile_photo', 'phone_number']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'address', 'gender', 'profile_photo', 'phone_number']