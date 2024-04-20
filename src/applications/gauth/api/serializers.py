import contextlib
from typing import cast

from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from applications.members.api.serializers import RetrieveUserSerializer
from applications.members.models import User, WorkPosition, TimePreference, Tag


class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=False, read_only=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(read_only=True)

    def get_auth_user_using_orm(self, username, email, password):
        with contextlib.suppress(cast(type[Exception], User.DoesNotExist)):
            return User.objects.get(email=email)


class TokenSerializer(serializers.Serializer):
    user = RetrieveUserSerializer(read_only=True)
    access = serializers.CharField()
    refresh = serializers.CharField()


class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birth_date = serializers.DateField()
    avatar = serializers.ImageField()
    position = serializers.PrimaryKeyRelatedField(
        queryset=WorkPosition.objects.all(),
    )
    time_preference = serializers.PrimaryKeyRelatedField(
        queryset=TimePreference.objects.all(),
    )
    about = serializers.CharField()
    tags = serializers.ListSerializer(
        child=serializers.IntegerField(),
    )

