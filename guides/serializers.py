from rest_framework import serializers
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

    class Meta:
        model = Guides
        fields = '__all__'


class CreateGuideSerializer(serializers.Serializer):
    place = serializers.IntegerField()
    main_transport_method = serializers.IntegerField()
    friendly_tag = serializers.IntegerField()
    duration = serializers.IntegerField()
