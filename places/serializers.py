from rest_framework import serializers
from .models import PlaceTypes, PriceCategories, Places
from utils.aws import generate_aws_url


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


class PlaceSerializer(serializers.ModelSerializer):
    # audio_url = serializers.SerializerMethodField()
    #
    # def get_audio_url(self, obj):
    #     return generate_aws_url(obj.audio_url)

    class Meta:
        model = Places
        fields = ('name', 'description', 'address', 'longitude', 'latitude')


class CreatePlaceSerializer(serializers.Serializer):
    place_type = serializers.IntegerField()
    price_category = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    address = serializers.CharField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

