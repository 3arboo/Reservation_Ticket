from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
class Movie(models.Model):

    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=10)

class Geust(models.Model):

    name = models.CharField(max_length=10)
    mobile = models.IntegerField(max_length=10)

class Resrvation(models.Model):

    geust = models.ForeignKey(Geust, related_name='resrvation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='resrvation',on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()

@receiver(post_save, sender=User)
def TokenCreat(sender ,instance, created , **kwargs):
    if created:
        Token.objects.create(user =instance)



# Create your models here.
