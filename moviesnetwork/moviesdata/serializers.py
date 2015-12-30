from rest_framework import serializers


class SearchActorSerializer(serializers.Serializer):
    actor_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)


class MovieSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)
    cover = serializers.CharField()
    rating = serializers.IntegerField()


class ActorSerializer(serializers.Serializer):
    actor_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    headshot = serializers.CharField(required=False)
    movies = MovieSerializer(required=True, many=True)
