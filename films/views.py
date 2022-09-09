from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404


from .models import Movie
from .serializers import MovieSerializers,MovieDetailSerializers,MovieCreateSerializers
from comments_and_likes.serializers import CommentSerializer,LikeSerializer
from comments_and_likes.models import Like
from rating.serializers import RatingSerializer
from favorites.models import Favorites
from my_movies.tasks import sending_message_task
from .services import open_file

class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 1000

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category',)
    search_fields = ('title','year','country',)
    pagination_class = StandartResultPagination

    def create(self, request):
        serializer =MovieCreateSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sending_message_task.delay()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

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
        Like.objects.create(movie=movie, user=request.user)
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
    @action(['GET', 'POST'], detail=True)
    def rating(self, request, pk=None):
        movie = self.get_object()
        if request.method =='GET':
            ratings =  movie.ratings.all()
            serializer = RatingSerializer(ratings, many=True).data
            return Response(serializer, status = 200)
        data = request.data
        serializer = RatingSerializer(data = data, context={'request':request, 'movie':movie})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    @action(['POST'], detail=True, )
    def favorite(self, request, pk):
        movie = self.get_object()
        if request.user.favorites.filter(movie=movie).exists():
            request.user.favorites.filter(movie=movie).delete()
            return Response('Убрали из избранных', status=204)
        Favorites.objects.create(movie=movie, user=request.user)
        return Response('Добавлено в избранные!', status=201)



def get_list_video(request):
    return render(request, 'video_hosting/home.html', {'video_list': Movie.objects.all()})


def get_video(request, pk: int):
    _video = get_object_or_404(Movie, id=pk)
    return render(request, "video_hosting/video.html", {"video": _video})


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response