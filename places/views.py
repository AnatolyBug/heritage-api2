import os
import time
import base64
from django.db import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import PlaceTypes, PriceCategories, Places
from utils.aws import upload_file_to_aws
from .serializers import PlaceTypeSerializer, CreatePlaceTypeSerializer, \
    CreatePriceCategorySerializer, PriceCategorySerializer, PlaceSerializer, CreatePlaceSerializer


class PlaceTypeViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        user_role = request.user.user_role

        if user_role == 'customer':
            response = 'You are not allowed to get place types.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            types = PlaceTypes.objects.order_by('-created_at')
            serializer = PlaceTypeSerializer(types, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreatePlaceTypeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        try:
            place_type = PlaceTypes.objects.create(place_type=data['place_type'])
        except IntegrityError:
            return Response({
                'message': 'Place Type already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=PlaceTypeSerializer(place_type).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        user_role = request.user.user_role

        if user_role == 'superuser' or user_role == 'admin':
            place_type = PlaceTypes.objects.get(pk=pk)
            try:
                place_type.place_type = request.data['place_type']
                place_type.save()
            except IntegrityError:
                return Response({
                    'message': 'Place Type already exists.',
                    'errors': {'type': 'Place Type already exists.'}
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response(data=PlaceTypeSerializer(place_type).data, status=status.HTTP_200_OK)
        else:
            response = 'You are not allowed to update this place type.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def destroy(request, pk=None):
        user_role = request.user.user_role
        if user_role == 'superuser' or user_role == 'admin':
            place_type = PlaceTypes.objects.get(pk=pk)
            place_type.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response = 'You are not allowed to delete this place type.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class PriceCategoriesViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        user_role = request.user.user_role

        if user_role == 'customer':
            response = 'You are not allowed to get price categories.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            price_categories = PriceCategories.objects.order_by('-created_at')
            serializer = PriceCategorySerializer(price_categories, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        serializer = CreatePriceCategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        try:
            price_category = PriceCategories.objects.create(category_name=data['category_name'])
        except IntegrityError:
            return Response({
                'message': 'Price Category already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=PriceCategorySerializer(price_category).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        user_role = request.user.user_role

        if user_role == 'superuser' or user_role == 'admin':
            price_category = PriceCategories.objects.get(pk=pk)
            try:
                price_category.category_name = request.data['category_name']
                price_category.save()
            except IntegrityError:
                return Response({
                    'message': 'Price Category already exists.',
                    'errors': {'type': 'Place Type already exists.'}
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response(data=PriceCategorySerializer(price_category).data, status=status.HTTP_200_OK)
        else:
            response = 'You are not allowed to update this price category.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def destroy(request, pk=None):
        user_role = request.user.user_role
        if user_role == 'superuser' or user_role == 'admin':
            price_category = PriceCategories.objects.get(pk=pk)
            price_category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response = 'You are not allowed to delete this price category.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class PlacesViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        places = Places.objects.order_by('-created_at')
        serializer = PlaceSerializer(places, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        user_id = request.user.id
        serializer = CreatePlaceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        audio_file = request.data['audio_file']
        audio_file_name = f"{user_id}_{time.time()}_audio.wav"

        if audio_file is not None:
            bucket_name = os.getenv('AWS_PLACE_AUDIO_BUCKET_NAME')
            upload = upload_file_to_aws(file_name=audio_file_name, bucket=bucket_name)

            if upload is True:
                os.remove(audio_file_name)

        image_file = request.data['image_file']
        img_file_name = ''

        if image_file is not None:
            file_format, img_str = image_file.split(';base64,')
            ext = file_format.split('/')[-1]
            img_file_name = f"{user_id}_{time.time()}_place_image.{ext}"

            with open(img_file_name, 'wb') as destination:
                destination.write(base64.b64decode(img_str))

            bucket_name = os.getenv('AWS_AVATAR_IMAGE_BUCKET_NAME')

            upload = upload_file_to_aws(file_name=img_file_name, bucket=bucket_name)
            if upload is True:
                os.remove(img_file_name)

        place = Places.objects.create(
            name=data['name'], description=data['description'], address=data['address'], longitude=data['longitude'],
            latitude=data['latitude'], place_type_id=data['place_type'], images=img_file_name,
            price_category_id=data['price_category'], created_by_user_id=user_id, audio_url=audio_file_name
        )

        return Response(data=PlaceSerializer(place).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update(request, pk=None):
        place = Places.objects.get(pk=pk)

        place.name = request.data['name']
        place.description = request.data['description']
        place.address = request.data['address']
        place.longitude = request.data['longitude']
        place.latitude = request.data['latitude']
        place.place_type_id = request.data['place_type']
        place.price_category_id = request.data['price_category']
        place.save()

        return Response(data=PlaceSerializer(place).data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy(request, pk=None):
        place = Places.objects.get(pk=pk)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
