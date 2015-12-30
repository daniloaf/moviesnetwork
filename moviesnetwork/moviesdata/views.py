from rest_framework import views
from rest_framework import serializers
from rest_framework.response import Response

from services import search_actor
from serializers import SearchActorSerializer


class SearchActorView(views.APIView):

    def get(self, request):
        """
        Searches actors in IMDB by name
        """
        if not 'name' in request.query_params:
            raise serializers.ValidationError({'name': 'This field is required'})

        actors = search_actor(request.query_params['name'])
        serializer = SearchActorSerializer(actors, many=True)
        return Response(serializer.data)
