from rest_framework import serializers
from API.models import RoomMember, CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'