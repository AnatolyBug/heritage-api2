from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from relationships.models import Relationships
from relationships.serializers import RelationshipSerializer


class FollowRelationshipView(APIView):

    @staticmethod
    def post(request):
        serializer = RelationshipSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Some fields are missing',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )
        data = serializer.validated_data
        relationship = Relationships.objects.create(
            from_user_id=data['from_user'], to_user_id=data['to_user'], status=data['status'],
        )
        relationship.save()

        return Response(status=status.HTTP_201_CREATED)


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


