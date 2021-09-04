from auths.serializers import UserSerializer
from rest_framework import serializers


class UserListSerializer(serializers.Serializer):
    data = UserSerializer(many=True)
    next_page = serializers.BooleanField()
    previous_page = serializers.BooleanField()
    total = serializers.IntegerField()