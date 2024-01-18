from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated


class GenericViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    protected_views = []
    permissions = [AllowAny]  # Default permission

    def get_permissions(self):
        if self.action in self.protected_views:
            return [permission() for permission in self.permissions]
        return [AllowAny()]
