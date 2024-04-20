from django.contrib.messages.storage.cookie import MessageSerializer
from django.db.models import Exists, OuterRef
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.chats.api.serializers import RetrieveChatSerializer, RetrieveMessageSerializer, \
    CreateMessageSerializer, RetrieveMessageInChatSerializer
from applications.chats.models import Chat, ChatParticipant, Message
from applications.chats.services import create_message
from applications.common.exceptions import BaseServiceException

CHAT_TAG = 'Чаты'
MESSAGE_TAG = 'Сообщения чатов'

class ChatViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, )
    serializer_class = RetrieveChatSerializer

    queryset = Chat.objects.all()

    def get_queryset(self):
        self.queryset = self.queryset.visible_for(
            self.request.user
        ).annotate_name(
            self.request.user,
        ).select_related(
            'last_message',
        )
        return super().get_queryset()

    @extend_schema(
        responses={
            status.HTTP_200_OK: RetrieveChatSerializer,
        },
        tags=[CHAT_TAG],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_200_OK: RetrieveChatSerializer(many=True),
        },
        tags=[CHAT_TAG],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = RetrieveMessageInChatSerializer
    queryset = Message.objects.all().order_by('created')

    def initial(self, request, *args, **kwargs):
        chat_pk = kwargs.get('chat_pk')
        self.chat = get_object_or_404(
            Chat.objects.visible_for(self.request.user),
            pk=chat_pk,
        )

    def get_queryset(self):
        self.queryset = self.queryset.filter(
            chat=self.chat,
        )

    @extend_schema(
        responses={status.HTTP_200_OK: RetrieveMessageInChatSerializer},
        tags=[MESSAGE_TAG],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: RetrieveMessageInChatSerializer(many=True)},
        tags=[MESSAGE_TAG],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=CreateMessageSerializer,
        responses={status.HTTP_201_CREATED: RetrieveMessageInChatSerializer},
        tags=[MESSAGE_TAG],
    )
    def create(self, request, *args, **kwargs):
        serializer = CreateMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            msg = create_message(self.request.user, self.chat, **serializer.validated_data)
        except BaseServiceException as e:
            return e.response()
        return Response(
            status=status.HTTP_201_CREATED,
            data= self.get_serializer(msg).data,
        )
