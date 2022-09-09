from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    user =serializers.ReadOnlyField(source = 'user.email')
    movie = serializers.ReadOnlyField(source = 'movie.title')
    class Meta:
        model = Rating
        fields = '__all__'

    def create(self , validated_data):
        request =self.context.get('request')
        user = request.user
        movie = self.context.get('movie')
        validated_data['user'] = user
        validated_data['movie'] = movie
        return super().create(validated_data)