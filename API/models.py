from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, null=True, unique=True)
    avatar = models.ImageField(null=True, blank=False)

    REQUIRED_FIELDS = ['avatar']


class RoomMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models)
    token = models.CharField(max_length=1000)
    chanel = models.CharField(max_length=200)

    def __str__(self):
        return self.chanel
