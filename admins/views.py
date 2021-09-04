from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from admins.serializers import AdminUserListSerializer

class AdminUserViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAdminUser,)


    '''
    @swagger_auto_schema(responses={"200": AdminUserSerializer, "404": "Not Found"})
        def retrieve(self, request, pk):
            user = User.objects.filter(pk=pk, is_active=True).first()
            if user:
                serializer = UserSerializer(user)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data='Not Found', status=status.HTTP_404_NOT_FOUND)
    '''