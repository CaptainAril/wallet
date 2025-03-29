from django.urls import include, path

from .views import HealthCheck

urlpatterns = [
    path('health-check/', HealthCheck.as_view(), name='health-check'),
]
