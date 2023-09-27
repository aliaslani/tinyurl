from rest_framework import serializers
from .models import URL
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        fields = ('origin', 'shorted')
        read_only_fields = ('shorted','user')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name','last_name', 'username', 'password', 'email', 'is_staff', 'groups')