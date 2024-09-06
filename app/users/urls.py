from django.urls import path
from .views import SignupView, SearchUserView, FriendRequestView, FriendListView, MyTokenObtainPairView, \
    MyTokenRefreshView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_logout'),
    path('search/', SearchUserView.as_view(), name='search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friends-list/', FriendListView.as_view(), name='friends'),

]
