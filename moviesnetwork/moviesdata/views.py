from rest_framework import views, serializers, response

from services import search_actor, get_actor_info
from serializers import SearchActorSerializer, ActorSerializer


class SearchActorView(views.APIView):

    def get(self, request):
        """
        Searches actors in IMDB by name.
        """
        if not 'name' in request.query_params:
            raise serializers.ValidationError({'name': 'This field is required'})

        actors = search_actor(request.query_params['name'])
        serializer = SearchActorSerializer(actors, many=True)
        return response.Response(serializer.data)


class ActorView(views.APIView):

    def get(self, request, actor_id):
        """
        Gets an actor full information.
        """
        actor = get_actor_info(actor_id)
        if actor:
            serializer = ActorSerializer(actor)
            return response.Response(serializer.data)
        else:
            return response.Response({'detail': 'Actor not found'}, status=404)
