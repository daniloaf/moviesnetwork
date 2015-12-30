from rest_framework import serializers


class SearchActorSerializer(serializers.Serializer):
    actor_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
