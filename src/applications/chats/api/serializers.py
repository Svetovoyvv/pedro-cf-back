from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from applications.chats.models import Chat
from applications.members.api.serializers import RetrieveUserSerializer


class RetrieveMessageInChatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    author = RetrieveUserSerializer(read_only=True, source='author.user')


class RetrieveChatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    last_message = RetrieveMessageInChatSerializer(read_only=True)

    participants = serializers.SerializerMethodField()

    @extend_schema_field(RetrieveUserSerializer(many=True))
    def get_participants(self, instance: Chat):
        return RetrieveUserSerializer(instance.participants.all(), many=True)


class RetrieveMessageSerializer(RetrieveMessageInChatSerializer):
    chat = RetrieveChatSerializer(read_only=True)


class CreateMessageSerializer(serializers.Serializer):
    text = serializers.CharField()
