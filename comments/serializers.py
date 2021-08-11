from rest_framework import serializers
from .models import Comments


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'


class CreateCommentSerializer(serializers.Serializer):
    comment_guide = serializers.IntegerField()
    comment = serializers.CharField()
    like = serializers.BooleanField()
