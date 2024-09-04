from django.urls import path
from .views import SignupView, SearchUserView, FriendRequestView, FriendListView, MyTokenObtainPairView, \
    MyTokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('search/', SearchUserView.as_view(), name='search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friends/', FriendListView.as_view(), name='friends'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
