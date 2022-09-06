from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response

from .models import Movie
from .serializers import MovieSerializers,MovieDetailSerializers


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieSerializers
        return MovieDetailSerializers

    def get_permissions(self):
        if self.action == 'list' or 'detail':
            permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        else:
            permission_classes = (permissions.IsAdminUser,)
        return [permission() for permission in permission_classes]

