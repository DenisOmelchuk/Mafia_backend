from rest_framework import serializers
from API.models import RoomMember, CustomUser
from django.contrib.auth import authenticate


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            avatar=validated_data['avatar']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar']


