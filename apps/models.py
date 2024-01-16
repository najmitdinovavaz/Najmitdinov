from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField


class Model(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='users/images', blank=True)
    location = models.CharField(max_length=255)
    money_hour = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='users/images')
