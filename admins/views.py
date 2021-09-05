from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from admins.serializers import AdminSingleUserListSerializer
from auths.models import User


class AdminUserViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAdminUser,)
    user_param = openapi.Parameter('user_id', openapi.IN_PATH, description="user id", type=openapi.TYPE_INTEGER)
    auth = openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <Token>", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[user_param, auth],
                         responses={"200": AdminSingleUserListSerializer, "404": "Not Found"},
                         security=[{'admin': 'admin'}])
    def retrieve(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            serializer = AdminSingleUserListSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data='Not Found', status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_description='Admin to Delete or Resurrect User')
    def destroy(self, request, pk=None):
        user = User.objects.filter(pk=pk).first()
        if not user:
            Response({'error': 'no such user'}, status=status.HTTP_400_BAD_REQUEST)
        _status = user.is_active
        user.is_active = not status
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
