import os
import time
import base64
from django.db import IntegrityError
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from relationships.models import Relationships
from utils.aws import upload_file_to_aws
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

        image_file = request.data['image_file']
        img_file_name = ''

        if image_file:
            file_format, img_str = image_file.split(';base64,')
            ext = file_format.split('/')[-1]
            img_file_name = f"{user_id}_{time.time()}_guide_image.{ext}"

            with open(img_file_name, 'wb') as destination:
                destination.write(base64.b64decode(img_str))

            bucket_name = os.getenv('AWS_GUIDE_IMAGE_BUCKET_NAME')

            upload = upload_file_to_aws(file_name=img_file_name, bucket=bucket_name)
            if upload is True:
                os.remove(img_file_name)

        guide = Guides.objects.create(user_id=user_id, main_transport_method_id=data['main_transport_method'],
                                      friendly_tag_id=data['friendly_tag'], duration=data['duration'],
                                      transport_methods=data['transport_methods'], map_image_url=img_file_name)

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


class FeedView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        user_id = request.user.id
        relationships = Relationships.objects.filter(to_user_id=user_id, status='approved')

        if relationships:
            followers = []
            for relationship in relationships:
                followers.append(relationship.from_user_id)

            guides = []
            for follower in followers:
                guide = Guides.objects.filter(user_id=follower)
                if guide:
                    results = []
                    for index in range(len(guide)):
                        friendly_tag = FriendlyTags.objects.get(id=guide[index].friendly_tag_id).tag_name
                        main_transport = TransportMethods.objects.get(
                            id=guide[index].main_transport_method_id).transport_name
                        results.append({'guide_id': guide[index].id,
                                        'duration': guide[index].duration,
                                        'transport_methods': guide[index].transport_methods,
                                        'friendly_tag': friendly_tag, 'main_transport_method': main_transport,
                                        'created_at': guide[index].created_at
                                        })
                    guides.append({'user_id': follower, 'results': results})
                else:
                    guides.append({'user_id': follower, 'results': 'No Guides'})

            return Response(data=guides, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No Guides'}, status=status.HTTP_404_NOT_FOUND)

