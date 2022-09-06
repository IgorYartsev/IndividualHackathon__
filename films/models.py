from django.db import models
from category.models import Category

class Movie(models.Model):
    preview = models.ImageField(upload_to='media')
    title = models.CharField(max_length=100)
    descriptions = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.RESTRICT,related_name='movies')
    year = models.IntegerField()
    country = models.CharField(max_length=100)
    video = models.FileField(upload_to='media')

    def __str__(self):
        return f'{self.title} '
