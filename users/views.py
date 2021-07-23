from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from auths.models import User
from auths.serializers import UserSerializer, CreateUserSerializer


class UserViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        user_id = request.user.id
        user_role = request.user.user_role
        if user_role == 'superuser':
            users = User.objects.exclude(id=user_id).order_by('-created_date')
            serializer = UserSerializer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif user_role == 'admin':
            users = User.objects.filter(user_role='customer').order_by('-created_date')
            serializer = UserSerializer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            response = 'You are not allowed to get all customers.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def retrieve(request, pk=None):
        user_role = request.user.user_role
        if user_role == 'superuser' or user_role == 'admin':
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            response = 'You are not allowed to get this customer.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update(request, pk=None):
        user_role = request.user.user_role
        if user_role == 'superuser' or user_role == 'admin':

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
        else:
            response = 'You are not allowed to update this customer.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def destroy(request, pk=None):
        user_role = request.user.user_role
        if user_role == 'superuser' or user_role == 'admin':
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response = 'You are not allowed to delete this customer.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
