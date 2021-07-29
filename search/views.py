from django.db.models import Q
from rest_framework.views import APIView, status
from auths.serializers import UserSerializer
from auths.models import User
from rest_framework.response import Response


class UserSearchView(APIView):

    @staticmethod
    def get(request):
        user_id = request.user.id
        search_query = request.query_params['user']
        check_user = User.objects.exclude(id=user_id).filter(
            Q(username=search_query.lower()) |
            Q(first_name=search_query) |
            Q(last_name=search_query)
        ).exists()

        if check_user:
            users = User.objects.exclude(id=user_id).get(
                Q(username=search_query.lower()) |
                Q(first_name=search_query) |
                Q(last_name=search_query)
            )
            serializer = UserSerializer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data='No Results', status=status.HTTP_404_NOT_FOUND)
