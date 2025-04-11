from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserLoginViewSet, UserSignUpViewSet, UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('auth', UserSignUpViewSet, basename='auth-signup')
router.register('auth', UserLoginViewSet, basename='auth-login')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

