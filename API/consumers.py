import re
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from API.models import CustomUser

gm = CustomUser.objects.get(username='Martin')


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if the user is authenticated
        user = self.scope.get('user')
        if user and user.is_authenticated:
            await self.mark_user_as_online(user)
            # Sanitize the username for the group name
            sanitized_username = re.sub(r'[^a-zA-Z0-9\-\._]', '_', user.username)
            # Construct the group name for the user's notifications
            group_name = f'notifications_{sanitized_username}'
            if not re.match(r'^[a-zA-Z0-9\-\._]+$', group_name):
                await self.close()
                return
            # Add connection to the group
            await self.channel_layer.group_add(group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Remove connection from the group upon disconnection
        user = self.scope.get('user')
        if user and user.is_authenticated:
            await self.mark_user_as_offline(user)
            sanitized_username = re.sub(r'[^a-zA-Z0-9\-._]', '_', user.username)
            room_group_name = f'notifications_{sanitized_username}'
            await self.channel_layer.group_discard(room_group_name, self.channel_name)

    async def friend_request(self, event):
        friend_requests = [
            {
                'username': event.get('username'),
                'avatar': event.get('avatar'),
            }
        ]
        await self.send(text_data=json.dumps({
            'friend_requests': friend_requests
        }))

    @sync_to_async
    def mark_user_as_online(self, user):
        user.is_online = True
        user.save()

    @sync_to_async
    def mark_user_as_offline(self, user):
        user.is_online = False
        user.save()
