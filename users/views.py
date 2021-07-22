from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from auths.models import User
from auths.serializers import UserSerializer, CreateUserSerializer


class UserViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        user_id = request.user.id
        users = User.objects.exclude(id=user_id).order_by('-created_date')
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def retrieve(request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def update(request, pk=None):
        user = User.objects.get(pk=pk)
        try:
            user.username = request.data['username']
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.email = request.data['email']
            user.save()
        except IntegrityError:
            return Response({
                'message': 'Email already exists.',
                'errors': {'email': 'Email already exists.'}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
