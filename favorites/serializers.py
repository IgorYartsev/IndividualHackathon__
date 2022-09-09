from rest_framework import serializers

from .models import Favorites

class FavoritesSerializer(serializers.ModelSerializer):
    movie = serializers.ReadOnlyField(source='movie.title')
    class Meta:
        model = Favorites
        fields = ('movie',)

