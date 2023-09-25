from rest_framework import serializers
from .models import URL


class URLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = URL
        fields = ('origin', 'shorted')
        read_only_fields = ('shorted',)

