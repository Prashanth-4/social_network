from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .manager import SocialNetworkManager
from .models import CustomUser, FriendRequest
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer


class SignupView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            username = request.data.get('username')
            CustomUser.objects.create_user(email, password, username=username)
            return Response('message: User Created Successfully', status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SearchUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            users = SocialNetworkManager.get_search_users(request)
            return Response({'data': users}, 200)
        except Exception as e:
            return Response(str(e), 500)


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            id = request.data.get('friend_request_id', '')
            if not id:
                cache_key = f"friend_request_{request.user.id}"
                request_count = cache.get(cache_key, 0)
                if request_count >= 3:
                    return Response({
                        "error": "Rate limit exceeded. You can only send 3 friend requests per minute."
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)
                response = SocialNetworkManager.create_friend_request(request)
                cache.set(cache_key, request_count + 1, timeout=60)
            else:
                response = SocialNetworkManager.accept_or_reject_request(id, request.data.get('request_type'))
            return Response(response,200)
        except Exception as e:
            return Response(str(e), 500)

    def get(self, request):
        try:
            users = SocialNetworkManager.get_friend_requests(request)
            return Response({'data': users}, 200)
        except Exception as e:
            return Response(str(e), 500)


class FriendListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            friends = SocialNetworkManager.get_friends_list(request)
            return Response({'data': friends}, 200)
        except Exception as e:
            return Response(str(e), 500)
