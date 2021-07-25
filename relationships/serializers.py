

from rest_framework import serializers


class RelationshipSerializer(serializers.Serializer):
    from_user = serializers.IntegerField()
    to_user = serializers.IntegerField()
    status = serializers.CharField()
