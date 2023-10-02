from rest_framework import serializers
from .models import URL
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('origin', 'shorted', 'user')
        read_only_fields = ('shorted', 'user')
    user = serializers.StringRelatedField()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_staff', 'groups', 'number_of_urls')
        extra_kwargs = {
            "password": {"write_only": True},
        }

    number_of_urls = serializers.SerializerMethodField(method_name='get_number_of_urls')

    @staticmethod
    def get_number_of_urls(obj):
        return obj.urls.count()

    @staticmethod
    def get_first_name(obj):
        if len(obj.first_name) == 0:
            raise exceptions.ValidationError("First name is required")
        return obj.first_name
