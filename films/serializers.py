from rest_framework import serializers
from django.db.models import Avg


from .models import Movie
from comments_and_likes.serializers import CommentSerializer


class MovieCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('preview','title','year')

    def is_liked(self,movie):
        user = self.context.get('request').user
        return user.liked.filter(movie=movie).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        repr['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        return repr

class MovieDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
    def is_liked(self,movie):
        user = self.context.get('request').user
        return user.liked.filter(movie=movie).exists()
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        repr['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        repr['comments'] = CommentSerializer(instance.comments.all(),many=True).data
        return repr


