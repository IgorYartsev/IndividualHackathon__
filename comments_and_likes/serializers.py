from rest_framework import serializers
from .models import Comment,Like



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Comment
        fields = ('id','body','user','movie')

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Like
        fields =('user',)