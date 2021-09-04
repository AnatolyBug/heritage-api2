from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from auths.models import User
from auths.serializers import UserSerializer
from users.serializers import UserListSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    page_param = openapi.Parameter('page', openapi.IN_QUERY, description="page number", type=openapi.TYPE_INTEGER)
    user_param = openapi.Parameter('user_id', openapi.IN_PATH, description="user id", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[page_param],
                         operation_description='List all users',
                         responses={"200": UserListSerializer})
    def list(self, request):
        """Currently used for search"""
        user_id = request.user.id
        user_role = request.user.user_role

        get_users = User.objects.exclude(id=user_id, is_active=False, is_staff=False)
        user_list = get_users.filter(user_role='customer').order_by('-created_date')

        page = request.query_params.get('page', 1)
        paginator = Paginator(user_list, 20)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        previous_page = users.has_previous()
        next_page = users.has_next()
        total = paginator.num_pages
        data = UserSerializer(users, many=True).data

        # Put response into a serializer
        return Response({'data': data, 'previous_page': previous_page, 'next_page': next_page,
                         'total': total}, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={"200": UserSerializer, "404": "Not Found"})
    def retrieve(self, request, pk):
        user = User.objects.filter(pk=pk, is_active=True).first()
        if user:
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data='Not Found', status=status.HTTP_404_NOT_FOUND)
