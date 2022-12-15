from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


class Dishes(models.Model):
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="images", null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    comment = models.CharField(max_length=120, null=True)
    created_date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        unique_together = (
            'user',
            'dish'
        )

# parent model : Movies
# name, year of release, category, director, image
# Review:
# movie-FK: (movies)
# review-CF
# review_date-DF
# user-FK(user)
# rating-PIF
