from rest_framework import serializers

from applications.matches.models import RecommendationState, UserRecommendation
from applications.members.api.serializers import TagSerializer


class UserRelatedRecommendationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tags = TagSerializer(many=True, read_only=True)
    about = serializers.CharField()


class UserRecommendationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    object = UserRelatedRecommendationSerializer(read_only=True)
    state = serializers.ChoiceField(choices=RecommendationState.choices)
    is_bump = serializers.SerializerMethodField()

    def get_is_bump(self, instance: UserRecommendation):
        return getattr(instance, 'is_bump', False)




class UpdateUserRecommendationsSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=RecommendationState.choices)