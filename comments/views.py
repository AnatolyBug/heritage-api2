from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import status
from guides.models import Guides
from .models import Comments
from .serializers import CommentSerializer, CreateCommentSerializer


class CommentsViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        user_id = request.user.id
        user_role = request.user.user_role

        if user_role == 'superuser' or user_role == 'admin':
            comments = Comments.objects.order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            comments = Comments.objects.filter(comment_user_id=user_id).order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        user_id = request.user.id
        serializer = CreateCommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'message': 'Some fields are missing',
                'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        check_guide = Guides.objects.filter(id=data['comment_guide']).exists()

        if check_guide:
            try:
                comment = Comments.objects.create(comment_user_id=user_id, comment_guide_id=data['comment_guide'],
                                                  comment=data['comment'], like=data['like'])
            except IntegrityError:
                return Response({'message': 'Comments already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data=CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        else:
            response = "Guide doesn't exist."
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update(request, pk=None):
        user_id = request.user.id
        user_role = request.user.user_role

        check_comment = Comments.objects.filter(id=pk).exists()
        if check_comment:
            sel_comment = Comments.objects.get(id=pk)
            if user_role == 'superuser' or user_role == 'admin' or user_id == sel_comment.comment_user_id:
                sel_comment.comment = request.data['comment']
                sel_comment.like = request.data['like']
                sel_comment.save()
                return Response(data=CommentSerializer(sel_comment).data, status=status.HTTP_200_OK)
            else:
                return Response({'error', "You can't update other comments."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = 'There is no such comments.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def destroy(request, pk=None):
        user_id = request.user.id
        user_role = request.user.user_role
        check_comment = Comments.objects.filter(id=pk).exists()
        if check_comment:
            comment = Comments.objects.get(id=pk)
            if user_role == 'superuser' or user_role == 'admin' or comment.comment_user_id == user_id:
                comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error', "You can't delete other comments."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = 'There is no such comments.'
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

