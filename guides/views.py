from django.db import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import FriendlyTags
from .serializers import FriendlyTagSerializer, CreateFriendlyTagSerializer


class FriendlyTagViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        user_role = request.user.user_role

        if user_role == 'customer':
            response = 'You are not allowed to get friendly tags.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            types = FriendlyTags.objects.order_by('-created_at')
            serializer = FriendlyTagSerializer(types, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreateFriendlyTagSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        try:
            friendly_tag = FriendlyTags.objects.create(tag_name=data['tag_name'])
        except IntegrityError:
            return Response({
                'message': 'Friendly Tag already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=FriendlyTagSerializer(friendly_tag).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        user_role = request.user.user_role

        if user_role == 'superuser' or user_role == 'admin':
            friendly_tag = FriendlyTags.objects.get(pk=pk)
            try:
                friendly_tag.tag_name = request.data['tag_name']
                friendly_tag.save()
            except IntegrityError:
                return Response({
                    'message': 'Friendly Tag already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response(data=FriendlyTagSerializer(friendly_tag).data, status=status.HTTP_200_OK)
        else:
            response = 'You are not allowed to update this friendly tag.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def destroy(request, pk=None):
        user_role = request.user.user_role
        if user_role == 'superuser' or user_role == 'admin':
            friendly_tag = FriendlyTags.objects.get(pk=pk)
            friendly_tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response = 'You are not allowed to delete this friendly tag.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
