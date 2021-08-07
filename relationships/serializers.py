

from rest_framework import serializers


class RelationshipSerializer(serializers.Serializer):
    to_user = serializers.CharField()
    status = serializers.CharField()
