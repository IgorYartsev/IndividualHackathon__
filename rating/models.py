from django.db import models
from films.models import Movie
from django.contrib.auth import get_user_model

User = get_user_model()

class Mark():
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    marks  =((one, 'Too bad!'),
             (two, 'Bad!'),
             (three, 'Normal!'),
             (four, 'Good!'),
             (five, 'Excelent!'))


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=Mark.marks)
    create_at = models.DateTimeField(auto_now_add=True)
