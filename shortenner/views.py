from rest_framework import viewsets
from rest_framework import permissions
from .serializers import URLSerializer, UserSerializer
from hashlib import md5
from rest_framework.decorators import action
from .models import URL
from django.contrib.auth.models import User
from .utils import generate_short_url
from rest_framework.response import Response
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from rest_framework.throttling import UserRateThrottle
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.email = request.data['email']
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'status': 'deleted'})

    def perform_create(self, serializer):
        serializer.save()

    def showurls(self, request, *args, **kwargs):
        instance = self.get_object()
        urls = URL.objects.filter(user=instance)
        serializer = URLSerializer(urls, many=True)
        return Response(serializer.data)



class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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



    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)    
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

    def destroy(self, request, *args, **kwargs):
        if URL.objects.filter(id=kwargs['pk'], user=request.user).exists():
            return Response({'error': 'You can not delete this url'})
        else:
            return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['GET'])
    def redirect(self, request, shorted):
        instance = URL.objects.get(shorted=shorted)
        print('origin',instance.origin)
        return redirect(instance.origin)

