from .models import Place
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.six import text_type

class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place



class CreatePlaceSerializer(serializers.Serializer):
    #amount = serializers.IntegerField(required=True, min_value=0, null=True)
    #name = serializers.CharField(required=True, max_length=128)
    pass