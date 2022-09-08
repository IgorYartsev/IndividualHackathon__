from rest_framework import generics
from .models import Favorites
from .serializers import FavoritesSerializer
from account.permissions import IsAccountOwner

# class FavoritesListViews(generics.ListAPIView):
#     queryset = Favorites.objects.all()
#     serializer_class = FavoritesSerializer
#     permission_classes =(IsAccountOwner,)

