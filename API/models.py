from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, null=True, unique=True)
    avatar = models.ImageField(null=True, blank=False)
    friends = models.ManyToManyField('self', blank=True, related_name='friends')
    is_online = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['avatar']

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"


class RoomMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=1000)
    channel = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.username} in {self.channel}"
