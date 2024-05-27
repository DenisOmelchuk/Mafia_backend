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







