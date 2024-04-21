from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from applications.chats.models import Chat
from applications.matches.models import RecommendationState, UserRecommendation, MeetingState, MeetingMemberState
from applications.members.api.serializers import TagSerializer, RetrieveUserSerializer


class UserRelatedRecommendationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tags = TagSerializer(many=True, read_only=True)
    about = serializers.CharField()


class UserRecommendationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    object = UserRelatedRecommendationSerializer(read_only=True)
    object_bump_info = serializers.SerializerMethodField()
    state = serializers.ChoiceField(choices=RecommendationState.choices)
    is_bump = serializers.SerializerMethodField()

    def get_is_bump(self, instance: UserRecommendation):
        return getattr(instance, 'is_bump', False)

    @extend_schema_field(RetrieveUserSerializer)
    def get_object_bump_info(self, instance: UserRecommendation):
        if getattr(instance, 'is_bump', False):
            return RetrieveUserSerializer(instance.object).data
        return None


class UpdateUserRecommendationsSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=RecommendationState.choices)


class MeetingSerializer(serializers.Serializer):
    ...


class CreateMeetingSerializer(serializers.Serializer):
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    is_online = serializers.BooleanField()
    chat = serializers.PrimaryKeyRelatedField(
        queryset=Chat.objects.all(),
    )


class UpdateMeetingMemberSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=MeetingMemberState)
    comment = serializers.CharField()
