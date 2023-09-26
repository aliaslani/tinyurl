
from rest_framework import routers, serializers, viewsets
from .views import URLViewSet
from django.urls import path, include
from django.contrib.auth.models import User
from .views import UserViewSet





router = routers.DefaultRouter()
router.register('urls', URLViewSet,basename="urls")

urlpatterns = [
    path('', include(router.urls)),
    path('redirect/<str:shorted>/',URLViewSet.as_view({'get': 'redirect'})),
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
