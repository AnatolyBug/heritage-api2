from rest_framework import serializers
from .models import Relationships


class RelationshipSerializer(serializers.ModelSerializer):
    to_user = serializers.CharField()
    #status = serializers.CharField()

    class Meta:
        model = Relationships
        fields = ('to_user', 'status')
