from rest_framework import viewsets
from rest_framework import permissions
from .serializers import URLSerializer, UserSerializer, MyTokenObtainPairSerializer
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
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView



class MyTokenObtainPairSerializer(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # if 'password' in request.data:
        #     request.data['password'] = instance.set_password(request.data['password'])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'password' in request.data:
            instance.set_password(request.data['password'])
            instance.save()
        self.perform_update(serializer)
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



    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.origin = instance.origin.replace('http://', '')
        instance.origin = instance.origin.replace('https://', '')
        instance.origin = 'http://' + instance.origin
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    @action(detail=True, methods=['GET'],url_path="redirect")
    def redirect(self, request, pk):
        instance = URL.objects.filter(shorted=pk).first()
        print('origin',instance.origin)
        return redirect(instance.origin)

