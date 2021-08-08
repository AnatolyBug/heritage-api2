from rest_framework import serializers
from .models import Relationships
from auths.serializers import CustomerUserSerializer


class RelationshipSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    def get_from_user(self, obj):
        return CustomerUserSerializer(obj.from_user).data

    def get_to_user(self, obj):
        return CustomerUserSerializer(obj.to_user).data

    class Meta:
        model = Relationships
        fields = 'from_user', 'to_user', 'status'


class CreateRelationshipSerializer(serializers.Serializer):
    to_user = serializers.IntegerField()
    status = serializers.CharField()
