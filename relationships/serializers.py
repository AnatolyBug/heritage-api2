from rest_framework import serializers
from .models import Relationships
from auths.models import User


class CustomerRelUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class RelationshipSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    def get_from_user(self, obj):
        return CustomerRelUserSerializer(obj.from_user).data

    def get_to_user(self, obj):
        return CustomerRelUserSerializer(obj.to_user).data

    class Meta:
        model = Relationships
        fields = 'from_user', 'to_user', 'status', 'id'


class CreateRelationshipSerializer(serializers.Serializer):
    to_user = serializers.IntegerField()
    status = serializers.CharField()
