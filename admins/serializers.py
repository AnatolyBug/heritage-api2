from auths.serializers import BaseUserSerializer
from auths.models import User
from rest_framework import serializers


class AdminSingleUserListSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AdminUserListSerializer(serializers.Serializer):
    data = AdminSingleUserListSerializer(many=True)
    next_page = serializers.BooleanField()
    previous_page = serializers.BooleanField()
    total = serializers.IntegerField()
