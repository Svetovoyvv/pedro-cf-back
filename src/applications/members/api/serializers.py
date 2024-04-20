from rest_framework import serializers

from applications.members.models import WorkPosition


class CreateTagSerializer(serializers.Serializer):
    name = serializers.CharField()


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class WorkPositionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class RetrieveUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    avatar = serializers.ImageField()
    birth_date = serializers.DateField()
    ages = serializers.IntegerField(read_only=True)
    time_preference = serializers.CharField()

    groups = GroupSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    position = WorkPositionSerializer(read_only=True)


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birth_date = serializers.DateField()
    position = serializers.PrimaryKeyRelatedField(
        queryset=WorkPosition.objects.all(),
    )


