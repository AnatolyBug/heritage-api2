from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from relationships.models import Relationships
from relationships.serializers import RelationshipSerializer
from auths.models import User
from rest_framework import permissions


class FollowRelationshipView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request):
        serializer = RelationshipSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Bad request',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )
        data = serializer.validated_data

        from_user = request.user
        to_user = User.objects.filter(username=data['to_user'].lower()).first()
        rel_requested = data['status']

        if not to_user:
            return Response({'error': 'No such username exists'}, status=status.HTTP_404_NOT_FOUND)

        current_rel = Relationships.objects.filter(from_user=from_user,
                                                   to_user=to_user).first()

        if not current_rel and rel_requested in ['FOLLOW_REQUESTED', 'BLOCK']:
            relationship = Relationships.objects.create(
                from_user=from_user, to_user_id=to_user, status=rel_requested,
            )
            relationship.save()
            return Response({'status': rel_requested}, status=status.HTTP_201_CREATED)

        elif (current_rel.status == 'FOLLOW_REQUESTED' and rel_requested == 'UNFOLLOW') or \
             (current_rel.status == 'BLOCKED' and rel_requested == 'UNBLOCK') or \
             (current_rel.status in ['UNFOLLOW', 'UNBLOCK'] and rel_requested in ['FOLLOW', 'BLOCK']):

            current_rel.status = rel_requested
            current_rel.save()
            return Response({'status': rel_requested}, status=status.HTTP_200_OK)

    @staticmethod
    def get(request, username):
        from_user = request.user
        to_user = User.objects.filter(username=username.lower()).first()
        if not to_user:
            return Response({'error': 'No such username exists'}, status=status.HTTP_404_NOT_FOUND)

        current_rel = Relationships.objects.filter(from_user=from_user,
                                                   to_user=to_user).first()

        if current_rel:
            return Response({'status': current_rel.status}, status=status.HTTP_200_OK)
        else:
            return Response({'status': None}, status=status.HTTP_200_OK)

'''
class UpdateRelationshipView(APIView):

    @staticmethod
    def put(request):
        from_user = request.data['from_user']
        to_user = request.data['to_user']
        relationship = Relationships.objects.get(from_user_id=from_user, to_user_id=to_user)

        if relationship:
            relationship.status = request.data['status']
            relationship.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
'''


