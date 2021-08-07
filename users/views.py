from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, status
from rest_framework.response import Response
from auths.models import User
from auths.serializers import UserSerializer, CustomerUserSerializer


class UserViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        user_id = request.user.id
        user_role = request.user.user_role

        if user_role == 'superuser':
            user_list = User.objects.exclude(id=user_id).order_by('-created_date')
        else:
            get_users = User.objects.exclude(id=user_id)
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

        return Response({'data': data,
                         'previous_page': previous_page,
                         'next_page': next_page,
                         'total': total
                         }, status=status.HTTP_200_OK)

    @staticmethod
    def retrieve(request, pk=None):
        user_role = request.user.user_role
        user = User.objects.filter(pk=pk).first()
        if user:
            if user_role == 'superuser' or user_role == 'admin':
                serializer = UserSerializer(user)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = CustomerUserSerializer(user)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data='Not Found', status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def update(request, pk=None):
        user_role = request.user.user_role

        if user_role == 'superuser' or user_role == 'admin':
            user = User.objects.get(pk=pk)
            try:
                user.username = request.data['username'].lower()
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
