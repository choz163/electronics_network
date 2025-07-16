"""
Маршрутизация API приложения core.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet

router = DefaultRouter()
router.register(r"nodes", NetworkNodeViewSet, basename="node")

urlpatterns = [
    path("api/", include(router.urls)),
]
