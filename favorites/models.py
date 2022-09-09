from django.db import models

from films.models import Movie
from account.models import CustomUser

class Favorites(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='favorites')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='favorites')
    class Meta:
        unique_together = ['movie','user']
