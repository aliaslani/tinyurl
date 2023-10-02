from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import UserViewSet, URLViewSet, MyTokenObtainPairSerializer

router = routers.DefaultRouter()
router.register('urls', URLViewSet,basename="urls")
router.register('users', UserViewSet,basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('token/', MyTokenObtainPairSerializer.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
