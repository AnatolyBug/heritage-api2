from .models import Place
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
# from .constants import ACCOUNT_NOT_FOUND
from django.utils.six import text_type

class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = 'id', 'email', 'username', 'first_name', 'last_name', 'bio',


class CreatePlaceSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    bio = serializers.CharField()