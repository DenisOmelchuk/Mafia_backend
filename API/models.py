from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, null=True, unique=True)
    avatar = models.ImageField(null=True, blank=False)
    friends = models.ManyToManyField('self', blank=True, related_name='friends')
    is_online = models.BooleanField(default=False)
    role = models.CharField(max_length=15)

    REQUIRED_FIELDS = ['avatar']

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"


class GameRoom(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='hosted_rooms')
    channel = models.CharField(max_length=9, unique=True)
    expected_players_count = models.IntegerField()
    current_players_count = models.IntegerField(default=0)
    is_started = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(CustomUser, related_name='joined_room', blank=True)

    def add_player(self, user):
        self.players.add(user)
        self.current_players_count += 1
        self.save()

    def __str__(self):
        return self.channel
