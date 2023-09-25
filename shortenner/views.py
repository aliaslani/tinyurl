from rest_framework import viewsets
from .serializers import URLSerializer
from hashlib import md5
from rest_framework.decorators import action
from . models import URL
from .utils import generate_short_url
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.throttling import UserRateThrottle

class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        user = self.request.user
        origin = serializer.validated_data['origin']
        if origin:
            shorted = generate_short_url(serializer.validated_data['origin'])
            serializer.save(user=user, shorted=shorted)
        else:
            serializer.save(user=user)
    
        
    def get_queryset(self):
        return URL.objects.filter(user=self.request.user)



    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.origin = instance.origin.replace('http://', '')
        instance.origin = instance.origin.replace('https://', '')
        instance.origin = 'http://' + instance.origin
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.origin = request.data['origin']
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def redirect(self, request, shorted):
        instance = URL.objects.get(shorted=shorted)
        print('origin',instance.origin)
        return redirect(instance.origin)

