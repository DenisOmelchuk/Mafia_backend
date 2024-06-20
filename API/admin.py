from django.contrib import admin
from .models import RoomMember, CustomUser, FriendRequest

admin.site.register(RoomMember)
admin.site.register(CustomUser)
admin.site.register(FriendRequest)
