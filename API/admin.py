from django.contrib import admin
from .models import CustomUser, FriendRequest, GameRoom

admin.site.register(GameRoom)
admin.site.register(CustomUser)
admin.site.register(FriendRequest)
