from .models import Place
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.six import text_type

class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place



class CreatePlaceSerializer(serializers.Serializer):

    class Meta:
        model = Place
        fields = 'name', 'type', 'description', 'address', 'images', 'price_category', 'friendly_tags',