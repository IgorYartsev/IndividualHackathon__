from django.db import models
from films.models import Movie
from account.models import CustomUser


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, related_name='comments',on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -> {self.movie} -> {self.created_at}'

class Like(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='liked')
    class Meta:
        unique_together = ['movie','user']