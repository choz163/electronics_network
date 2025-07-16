from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode
from .serializers import NetworkNodeSerializer


class IsActiveStaff(IsAuthenticated):
    """
    Разрешение доступа: только активные (is_active) и штатные (is_staff) пользователи.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_staff


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint для CRUD операций над узлами сети.

    Поддерживает:
    - list/retrieve/create/update/destroy
    - фильтрацию по полю country
    """

    queryset = (
        NetworkNode.objects.all()
        .select_related("supplier")
        .prefetch_related("products")
    )
    serializer_class = NetworkNodeSerializer
    permission_classes = (IsActiveStaff,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("country",)
