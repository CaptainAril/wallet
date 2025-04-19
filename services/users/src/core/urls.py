from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import StatusView

# Create a router and register our viewset with it.
# router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# router.register(r'status', StatusView, basename='status')

urlpatterns = [
    # path('', include(router.urls))
    path('status/', StatusView.as_view(), name='status'),
]


