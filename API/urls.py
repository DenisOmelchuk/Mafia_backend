from django.urls import path
from .views import registration, user_profile, user_update, list_friends, delete_friend, search_users, \
    send_friend_request, friend_request_accept, friend_request_refuse, create_game
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('registration/', registration, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', user_profile, name='profile'),
    path('profile/update/', user_update, name='user_update'),
    path('list_friends/', list_friends, name='list_friends'),
    path('delete_friend/', delete_friend, name='delete_friend'),
    path('search_users/', search_users, name='search_users'),
    path('send_friend_request/', send_friend_request, name='send_friend_request'),
    path('friend_request_accept/', friend_request_accept, name='friend_request_accept'),
    path('friend_request_refuse/', friend_request_refuse, name='friend_request_accept'),
    path('create_game/', create_game, name='create_game')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
