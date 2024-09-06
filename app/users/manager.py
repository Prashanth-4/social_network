from django.core.paginator import Paginator
from django.db.models import Q
from .models import FriendRequest, CustomUser


class SocialNetworkManager:

    @staticmethod
    def get_search_users(request):
        page = request.data.get('page') or 1
        email = request.data.get('email')
        username = request.data.get('username')
        query = ~Q(id=request.user.id)
        if email:
            query &= Q(email__exact=email)
        elif username:
            query &= Q(username__icontains=username)
        users = list(CustomUser.objects.filter(query).values('username', 'email'))
        paginator = Paginator(users, 10)
        paginator = paginator.get_page(int(page))
        users = paginator.object_list
        return users

    @staticmethod
    def create_friend_request(request):
        to_user = CustomUser.objects.get(id=request.data.get('to_user'))
        if not to_user or to_user == request.user:
            raise Exception('Please send request to valid user')
        if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status__in=['pending', 'accepted']):
            request = FriendRequest(
                from_user=request.user,
                to_user=to_user,
                status='pending',
            )
            request.save()
            return {'message': 'Friend request sent successfully'}
        return {'message': 'Friend request already sent'}

    @staticmethod
    def accept_or_reject_request(friend_req_id, type):
        if type not in ['accepted', 'rejected']:
            raise Exception('Please send a valid request type')
        queryset = FriendRequest.objects.get(id=friend_req_id)
        queryset.status=type
        queryset.save()
        return {'message': 'Friend request {0}'.format(type)}

    @staticmethod
    def get_friend_requests(request):
        page = request.data.get('page') or 1
        received_requests = list(FriendRequest.objects.filter(to_user=request.user, status='pending').
                                 values('id', 'from_user'))
        paginator = Paginator(received_requests, 10)
        paginator = paginator.get_page(int(page))
        received_requests = paginator.object_list
        user_ids = [user.get('from_user') for user in received_requests]
        users = list(CustomUser.objects.filter(id__in=user_ids).values('id', 'username'))
        friend_request_users = []
        for request in received_requests:
            for user in users:
                if request.get('from_user') == user.get('id'):
                    friend_request_users.append({'friend_request_id': request.get('id'), 'username': user.get('username')})
                    break
        return friend_request_users

    @staticmethod
    def get_friends_list(request):
        page = request.data.get('page') or 1
        friend_ids = list(FriendRequest.objects.filter(status='accepted', from_user=request.user).
                          values_list('to_user', flat=True))
        paginator = Paginator(friend_ids, 10)
        paginator = paginator.get_page(int(page))
        friend_ids = paginator.object_list
        friends = list(CustomUser.objects.filter(id__in=friend_ids).values_list('username', flat=True))
        return friends
