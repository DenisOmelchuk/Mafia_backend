from django.contrib import admin
from .models import RoomMember, CustomUser

admin.site.register(RoomMember)
admin.site.register(CustomUser)
