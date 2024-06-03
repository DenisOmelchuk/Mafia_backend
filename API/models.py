from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, null=True, unique=True)
    avatar = models.ImageField(null=True, blank=False)
    friends = models.ManyToManyField('self', blank=True, related_name='friends')
    friends_request_received = models.ManyToManyField('self', blank=True, related_name='friend_requests_received')
    friends_request_sent = models.ManyToManyField('self', blank=True, related_name='friend_requests_sent')

    REQUIRED_FIELDS = ['avatar']

    def __str__(self):
        return self.username


class RoomMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=1000)
    channel = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.username} in {self.channel}"

