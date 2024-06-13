from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
import jwt


@database_sync_to_async
def get_user(user_id):
    """
    Retrieve user by ID asynchronously.
    If the user does not exist, return an anonymous user.
    """
    try:
        return get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        """
        Middleware to authenticate users based on JWT token in the query string.
        """
        close_old_connections()

        query_string = scope['query_string'].decode()  # Decode query string
        query_params = parse_qs(query_string)  # Parse query string into parameters
        token = query_params.get('token')  # Get token from query parameters

        if token:
            try:
                validated_token = UntypedToken(token[0])  # Validate JWT token
                user_id = validated_token['user_id']  # Extract user ID from token
                scope['user'] = await get_user(user_id)  # Retrieve user from database
            except (InvalidToken, TokenError, jwt.ExpiredSignatureError, jwt.DecodeError):
                scope['user'] = AnonymousUser()  # Set to anonymous user if token is invalid
        else:
            scope['user'] = AnonymousUser()  # Set to anonymous user if no token

        return await super().__call__(scope, receive, send)  # Proceed with the request
