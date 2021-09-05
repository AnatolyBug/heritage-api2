from auths.serializers import BaseUserSerializer
from auths.models import User
from rest_framework import serializers


class SingleUserListSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'avatar_url')


class UserListSerializer(serializers.Serializer):
    data = SingleUserListSerializer(many=True)
    next_page = serializers.BooleanField()
    previous_page = serializers.BooleanField()
    total = serializers.IntegerField()

