from rest_framework import serializers
from .models import URL
from django.contrib.auth.models import User


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('origin', 'shorted')
        read_only_fields = ('shorted',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')