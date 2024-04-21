from django.db.models import Exists, OuterRef
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from applications.common.exceptions import BaseServiceException
from applications.common.mixins import CustomUpdateModelMixin
from applications.matches.api.serializers import UserRecommendationSerializer, UpdateUserRecommendationsSerializer, \
    MeetingSerializer, CreateMeetingSerializer, UpdateMeetingMemberSerializer
from applications.matches.models import UserRecommendation, RecommendationState, Meeting, MeetingMember
from applications.matches.services import update_recommendation, create_meeting, update_meeting_state

MATCH_TAG = 'Рекомендации пользователей'
MEETING_TAG = 'Встречи'

class MatchViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   CustomUpdateModelMixin,
                   viewsets.GenericViewSet):

    queryset = UserRecommendation.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserRecommendationSerializer

    def get_queryset(self):
        self.queryset = self.queryset.filter(
            subject=self.request.user,
            is_deleted=False,
            state=RecommendationState.PENDING,
        )
        return super().get_queryset()

    @extend_schema(
        responses={status.HTTP_200_OK: UserRecommendationSerializer},
        tags=[MATCH_TAG],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: UserRecommendationSerializer(many=True)},
        tags=[MATCH_TAG],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=UpdateUserRecommendationsSerializer,
        responses={status.HTTP_200_OK: UserRecommendationSerializer},
        tags=[MATCH_TAG],
    )
    def partial_update(self, request, *args, **kwargs):
        serializer = UpdateUserRecommendationsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            recommendation = update_recommendation(
                request.user,
                self.get_object(),
                **serializer.validated_data
            )
        except BaseServiceException as e:
            return e.response()

        return Response(
            status=status.HTTP_200_OK,
            data=self.get_serializer(recommendation).data,
        )


class MeetingViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = self.queryset.filter(
            Exists(
                MeetingMember.objects.filter(
                    meeting=OuterRef('id'),
                    user=self.request.user,
                )
            )
        )

    @extend_schema(
        responses={status.HTTP_200_OK: MeetingSerializer(many=True)},
        tags=[MEETING_TAG]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: MeetingSerializer},
        tags=[MEETING_TAG],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=CreateMeetingSerializer,
        responses={status.HTTP_201_CREATED: MeetingSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateMeetingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            meeting = create_meeting(request.user, **serializer.validated_data)
        except BaseServiceException as e:
            return e.response()

        return Response(
            data=self.get_serializer(meeting).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=UpdateMeetingMemberSerializer,
        responses={status.HTTP_200_OK: MeetingSerializer},
        tags=[MEETING_TAG],
    )
    @action(methods=['PATCH'], url_path='member', detail=True, )
    def update_member(self, request: Request, *args, **kwargs):
        serializer = UpdateMeetingMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            meeting = update_meeting_state(
                self.get_object(),
                request.user,
                **serializer.validated_data,
            )
        except BaseServiceException as e:
            return e.response()
        return Response(
            status=status.HTTP_200_OK,
            data=self.get_serializer(meeting).data,
        )


