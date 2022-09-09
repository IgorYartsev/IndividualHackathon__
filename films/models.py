from django.db import models
from category.models import Category
from django.core.validators import FileExtensionValidator


class Movie(models.Model):
    preview = models.ImageField(upload_to='image/')
    title = models.CharField(max_length=100)
    descriptions = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.RESTRICT,related_name='movies')
    year = models.IntegerField()
    country = models.CharField(max_length=100)
    file = models.FileField(upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],default='Some str'
    )


    def __str__(self):
        return f'{self.title} '
