from django.db import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import FriendlyTags, TransportMethods, Guides
from .serializers import FriendlyTagSerializer, CreateFriendlyTagSerializer, \
    TransportMethodSerializer, CreateTransportMethodSerializer, GuideSerializer, CreateGuideSerializer


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


class TransportMethodViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        user_role = request.user.user_role

        if user_role == 'customer':
            response = 'You are not allowed to get transport methods.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            transport_methods = TransportMethods.objects.order_by('-created_at')
            serializer = TransportMethodSerializer(transport_methods, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreateTransportMethodSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        try:
            transport_method = TransportMethods.objects.create(transport_name=data['transport_method'])
        except IntegrityError:
            return Response({
                'message': 'Transport Name already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=TransportMethodSerializer(transport_method).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        user_role = request.user.user_role

        if user_role == 'superuser' or user_role == 'admin':
            transport_method = TransportMethods.objects.get(pk=pk)
            try:
                transport_method.transport_name = request.data['transport_method']
                transport_method.save()
            except IntegrityError:
                return Response({
                    'message': 'Transport Name already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response(data=TransportMethodSerializer(transport_method).data, status=status.HTTP_200_OK)
        else:
            response = 'You are not allowed to update this transport method.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def destroy(request, pk=None):
        user_role = request.user.user_role
        if user_role == 'superuser' or user_role == 'admin':
            transport_method = TransportMethods.objects.get(pk=pk)
            transport_method.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response = 'You are not allowed to delete this transport name.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class GuideViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        guides = Guides.objects.order_by('-created_at')
        serializer = GuideSerializer(guides, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        user_id = request.user.id
        serializer = CreateGuideSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        guide = Guides.objects.create(
            main_transport_method_id=data['main_transport_method'], user_id=user_id,
            friendly_tag_id=data['friendly_tag'], duration=data['duration'],
            transport_methods=data['transport_methods'])

        for place_id in data['place']:
            guide.place.add(place_id)

        return Response(data=GuideSerializer(guide).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        guide = Guides.objects.get(pk=pk)
        try:
            guide.place_id = request.data['place']
            guide.main_transport_method_id = request.data['main_transport_method']
            guide.friendly_tag_id = request.data['friendly_tag']
            guide.duration = request.data['duration']
            guide.save()
        except IntegrityError:
            return Response({
                'message': 'Transport Name already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=GuideSerializer(guide).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        guide = Guides.objects.get(pk=pk)
        guide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)