from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.common.exceptions import BaseServiceException
from applications.common.mixins import CustomUpdateModelMixin
from applications.matches.api.serializers import UserRecommendationSerializer, UpdateUserRecommendationsSerializer
from applications.matches.models import UserRecommendation
from applications.matches.services import update_recommendation

MATCH_TAG = 'Рекомендации пользователей'

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