from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Movie
from .serializers import MovieSerializers,MovieDetailSerializers
from comments_and_likes.serializers import CommentSerializer,LikeSerializer
from comments_and_likes.models import Like


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

    @action(['GET'], detail=True,)
    def comments(self,request,pk):
        movie = self.get_object()
        comments = movie.comments.all()
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data,status=200)

    @action(['POST'], detail=True, )
    def add_to_liked(self, request, pk):
        movie = self.get_object()
        if request.user.liked.filter(movie=movie).exists():
            return Response('Вы уже поставили свой лайк!', status=400)
        Like.objects.create(movie=movie, owner=request.user)
        return Response('Вы поставили лайк', status=201)

    @action(['POST'], detail=True, )
    def remove_from_liked(self, request, pk):
        movie = self.get_object()
        if not request.user.liked.filter(movie=movie).exists():
            return Response('Вы не лайкали этот пост', status=400)
        request.user.liked.filter(movie=movie).delete()
        return Response('Ваш лайк удален!', status=204)

    @action(['GET'], detail=True, )
    def get_likes(self, request, pk):
        movies = self.get_object()
        likes = movies.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=200)
