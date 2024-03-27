from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator


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
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Get the limit from the query parameters (with a default)
        limit = int(request.query_params.get('limit', 100))

        # Use Django's Paginator to apply the limit
        paginator = Paginator(queryset, limit)
        page = paginator.get_page(1)

        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)
