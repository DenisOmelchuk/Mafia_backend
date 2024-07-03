import os
import time
from agora_token_builder import RtcTokenBuilder
import string
import random
from .models import GameRoom


def generate_unique_channel_token():
    characters = string.ascii_uppercase + string.digits
    while True:
        token = ''.join(random.choices(characters, k=9))
        if not GameRoom.objects.filter(channel=token).exists():
            return token


def get_agora_token(user_id, channel):
    app_id = "your app_id"
    app_certificate = "your app_certificate"
    channel_name = channel
    uid = user_id
    expiration_time_in_seconds = 4000
    current_time_stamp = int(time.time())
    privilege_expired_ts = current_time_stamp + expiration_time_in_seconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, role, privilege_expired_ts)
    return token
