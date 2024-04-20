from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.common.exceptions import BaseServiceException
from applications.common.permissions.helpers import IsAdministrator
from applications.members.api.serializers import RetrieveUserSerializer, CreateUserSerializer
from applications.members.models import User
from applications.members.services import create_user

USER_TAG = 'Пользователи'


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated, IsAdministrator]
    queryset = User.objects.all()
    serializer_class = RetrieveUserSerializer

    @extend_schema(
        responses={status.HTTP_200_OK: RetrieveUserSerializer},
        tags=[USER_TAG],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: RetrieveUserSerializer(many=True)},
        tags=[USER_TAG],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=CreateUserSerializer,
        responses={status.HTTP_201_CREATED: RetrieveUserSerializer},
        tags=[USER_TAG],
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = create_user(**serializer.validated_data)
        except BaseServiceException as e:
            return e.response()

        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_serializer(user).data,
        )
