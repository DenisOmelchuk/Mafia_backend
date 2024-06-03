import os
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from API.serializers import RegisterUserSerializer, UserProfileSerializer
from .models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def registration(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = serializer.validated_data['username']
        user = CustomUser.objects.get(username=username)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    old_avatar = None
    if 'avatar' in request.FILES:
        if user.avatar:
            if os.path.isfile(user.avatar.path):
                old_avatar = user.avatar.path
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        if 'avatar' in request.FILES:
            os.remove(old_avatar)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    if not isinstance(request.user, CustomUser):
        return Response({"error": "Only authenticated users can access this endpoint."}, status=403)

    user = request.user
    friends = user.friends.all()
    serializer = UserProfileSerializer(friends, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_friend(request):
    user = request.user
    try:
        friend_to_delete = CustomUser.objects.get(username=request.data['username'])
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if friend_to_delete in user.friends.all():
        user.friends.remove(friend_to_delete)
        return Response({"message": "Friend removed successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User is not in your friends list"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_users(request):
    part_of_username = request.data.get('username', None)
    if part_of_username:
        current_user = request.user
        users = CustomUser.objects.filter(
            username__icontains=part_of_username
        ).exclude(
            id=current_user.id
        ).exclude(
            friends=current_user
        ).exclude(
            friends_request_sent=current_user
        ).exclude(
            friends_request_received=current_user
        )[:5]

        if users.exists():
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'No users were found'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    user = request.user
    try:
        requested_user = CustomUser.objects.get(username=request.data['username'])
        if requested_user != user:
            requested_user.friends_request_received.add(user)
            user.friends_request_sent.add(requested_user)
            return Response({"success": "Friend request sent"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You cannot send a friend request to yourself"}, status=status
                            .HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
