from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response
from relationships.models import Relationships
from relationships.serializers import RelationshipSerializer, CreateRelationshipSerializer
from auths.models import User
from rest_framework import permissions


class RelationshipViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def list(request):
        user_id = request.user.id
        user_role = request.user.user_role

        if user_role == 'superuser' or user_role == 'admin':
            relationships = Relationships.objects.order_by('-updated_at')
            data = RelationshipSerializer(relationships, many=True).data
            return Response({'data': data}, status=status.HTTP_200_OK)

        else:
            user_name = User.objects.get(id=user_id).username
            relationships_from_user = Relationships.objects.filter(from_user_id=user_id,
                                                                   to_user__is_active=True).order_by('-updated_at')
            relationships_to_user = Relationships.objects.filter(to_user_id=user_id,
                                                                 from_user__is_active=True).order_by('-updated_at')
            rel_from = RelationshipSerializer(relationships_from_user, many=True).data
            rel_to = RelationshipSerializer(relationships_to_user, many=True).data
            return Response({
                'user_name': user_name,
                'relationships_from_user': rel_from,
                'relationships_to_user': rel_to
            }, status=status.HTTP_200_OK)

    @staticmethod
    def retrieve(request, pk):
        user_id = request.user.id
        user_role = request.user.user_role

        if user_role == 'superuser' or user_role == 'admin':
            check_to_user = User.objects.filter(id=pk).first()
            if not check_to_user:
                return Response({'error': 'No such user exists'}, status=status.HTTP_404_NOT_FOUND)

            if user_id == pk:
                return Response({'status': 'SELF'}, status=status.HTTP_400_BAD_REQUEST)

            user_name = User.objects.get(id=pk).username
            relationships_to = Relationships.objects.filter(from_user_id=pk).order_by('-updated_at')
            relationships_from = Relationships.objects.filter(to_user_id=pk).order_by('-updated_at')

            return Response({
                'user_name': user_name,
                'relationships_to': RelationshipSerializer(relationships_to, many=True).data,
                'relationships_from': RelationshipSerializer(relationships_from, many=True).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not allowed to get relationship data.'},
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def create(request):
        serializer = CreateRelationshipSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Bad request',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
            )
        data = serializer.validated_data

        from_user_id = request.user.id
        to_user_id = data['to_user']
        check_to_user = User.objects.filter(id=to_user_id).first()

        if not check_to_user:
            return Response({'error': 'No such user exists'}, status=status.HTTP_404_NOT_FOUND)
        if from_user_id == to_user_id:
            return Response({'status': 'SELF'}, status=status.HTTP_204_NO_CONTENT)

        current_rel = Relationships.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).first()
        rel_requested = data['status']

        if not current_rel and rel_requested in ['FOLLOW', 'BLOCK']:
            relationship = Relationships.objects.create(
                from_user_id=from_user_id, to_user_id=to_user_id, status=rel_requested,
            )
            relationship.save()
            return Response({'status': rel_requested}, status=status.HTTP_201_CREATED)

        elif not current_rel:
            return Response({'error': 'The requests are incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        elif (current_rel.status == 'FOLLOW' and rel_requested == 'UNFOLLOW') or \
                (current_rel.status == 'BLOCK' and rel_requested == 'UNBLOCK') or \
                (current_rel.status in ['UNFOLLOW', 'UNBLOCK'] and rel_requested in ['FOLLOW', 'BLOCK']):

            current_rel.status = rel_requested
            current_rel.save()
            return Response({'status': rel_requested}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'The requests are incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_object(pk):
        try:
            return Relationships.objects.get(pk=pk)
        except Relationships.DoesNotExist:
            raise Http404

    @staticmethod
    def destroy(request, pk):
        user_role = request.user.user_role
        if user_role == 'superuser' or user_role == 'admin':
            relationship = RelationshipViewSet.get_object(pk)
            relationship.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
