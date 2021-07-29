from django.db import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import PlaceTypes, FriendlyTags, PriceCategories
from .serializers import PlaceTypeSerializer, CreatePlaceTypeSerializer, \
    FriendlyTagSerializer, CreateFriendlyTagSerializer, CreatePriceCategorySerializer, PriceCategorySerializer


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

