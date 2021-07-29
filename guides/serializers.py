from rest_framework import serializers
from .models import FriendlyTags


class FriendlyTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendlyTags
        fields = '__all__'


class CreateFriendlyTagSerializer(serializers.Serializer):
    tag_name = serializers.CharField()
