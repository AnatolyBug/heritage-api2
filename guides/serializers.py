import os
from utils.aws import generate_aws_url
from rest_framework import serializers
from places.serializers import PlaceSerializer
from .models import FriendlyTags, TransportMethods, Guides


class FriendlyTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendlyTags
        fields = '__all__'


class CreateFriendlyTagSerializer(serializers.Serializer):
    tag_name = serializers.CharField()


class TransportMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransportMethods
        fields = '__all__'


class CreateTransportMethodSerializer(serializers.Serializer):
    transport_method = serializers.CharField()


class GuideSerializer(serializers.ModelSerializer):
    map_image_url = serializers.SerializerMethodField()
    friendly_tag = serializers.SerializerMethodField()
    place_images = serializers.SerializerMethodField()

    def get_map_image_url(self, obj):
        bucket_name = os.getenv('AWS_GUIDE_IMAGE_BUCKET_NAME')
        content_type = 'image/png'
        return generate_aws_url(key=obj.map_image_url, bucket=bucket_name, content_type=content_type)

    def get_friendly_tag(self, obj):
        return FriendlyTagSerializer(obj.friendly_tag).data

    def get_place_images(self, obj):
        return PlaceSerializer(obj.place, many=True).data

    class Meta:
        model = Guides
        fields = 'id', 'duration', 'map_image_url', 'friendly_tag', 'place_images', 'created_at'


class CreateGuideSerializer(serializers.Serializer):
    place = serializers.ListField()
    main_transport_method = serializers.IntegerField()
    friendly_tag = serializers.IntegerField()
    duration = serializers.IntegerField()
    transport_methods = serializers.ListField()
