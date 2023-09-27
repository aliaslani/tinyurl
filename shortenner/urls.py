
from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from django.contrib.auth.models import User
from .views import UserViewSet, URLViewSet





router = routers.DefaultRouter()
router.register('urls', URLViewSet,basename="urls")
router.register('users', UserViewSet,basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('redirect/<str:shorted>/',URLViewSet.as_view({'get': 'redirect'})),
    path('users/<int:pk>/urls/', UserViewSet.as_view({'get': 'showurls'})),
]
