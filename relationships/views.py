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

        if not to_user:
            return Response({'error': 'No such username exist'}, status=status.HTTP_404_NOT_FOUND)
        if from_user == to_user:
            return Response({'status': 'SELF'}, status=status.HTTP_204_NO_CONTENT)

        current_rel = Relationships.objects.filter(from_user=from_user, to_user=to_user).first()
        rel_requested = data['status']

        if not current_rel and rel_requested in ['FOLLOW', 'BLOCK']:
            relationship = Relationships.objects.create(
                from_user=from_user, to_user=to_user, status=rel_requested,
            )
            relationship.save()
            return Response({'status': rel_requested}, status=status.HTTP_201_CREATED)

        elif (current_rel.status == 'FOLLOW' and rel_requested == 'UNFOLLOW') or \
             (current_rel.status == 'BLOCK' and rel_requested == 'UNBLOCK') or \
             (current_rel.status in ['UNFOLLOW', 'UNBLOCK'] and rel_requested in ['FOLLOW', 'BLOCK']):

            current_rel.status = rel_requested
            current_rel.save()
            return Response({'status': rel_requested}, status=status.HTTP_200_OK)

    @staticmethod
    def get(request):
        from_user = request.user
        to_username=request.query_params['username']
        to_user = User.objects.filter(username=to_username.lower()).first()
        if not to_user:
            return Response({'error': 'No such username exist'}, status=status.HTTP_404_NOT_FOUND)

        if from_user == to_user:
            return Response({'status': 'SELF'}, status=status.HTTP_204_NO_CONTENT)

        current_rel = Relationships.objects.filter(from_user=from_user,
                                                   to_user=to_user).first()

        if current_rel:
            return Response({'status': current_rel.status}, status=status.HTTP_200_OK)
        else:
            return Response({'status': None}, status=status.HTTP_204_NO_CONTENT)
