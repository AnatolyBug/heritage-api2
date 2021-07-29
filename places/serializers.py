from .models import PlaceTypes, PriceCategories
from rest_framework import serializers


class PlaceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaceTypes
        fields = '__all__'


class CreatePlaceTypeSerializer(serializers.Serializer):
    place_type = serializers.CharField()


class PriceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceCategories
        fields = '__all__'


class CreatePriceCategorySerializer(serializers.Serializer):
    category_name = serializers.CharField()
