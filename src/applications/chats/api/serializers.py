from rest_framework import serializers

from applications.members.api.serializers import RetrieveUserSerializer


class RetrieveMessageInChatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    author = RetrieveUserSerializer(read_only=True, source='author.user')



class RetrieveChatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    last_message = RetrieveMessageInChatSerializer(read_only=True)


class RetrieveMessageSerializer(RetrieveMessageInChatSerializer):
    chat = RetrieveChatSerializer(read_only=True)


class CreateMessageSerializer(serializers.Serializer):
    text = serializers.CharField()
