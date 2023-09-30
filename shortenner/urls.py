
from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from django.contrib.auth.models import User
from .views import UserViewSet, URLViewSet, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
      TokenRefreshView,
   )




router = routers.DefaultRouter()
router.register('urls', URLViewSet,basename="urls")
router.register('users', UserViewSet,basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('token/', MyTokenObtainPairSerializer.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
