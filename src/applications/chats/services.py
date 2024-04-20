from django.db import transaction

from applications.chats.models import Chat, Message, ChatParticipant
from applications.common.exceptions import BaseServiceException
from applications.members.models import User


def create_chat(participants: list[User]) -> Chat:
    if len(participants) != 2:
        raise BaseServiceException(
            'Невозможно создать чат в котором количество участников отличается от 2'
        )
    with transaction.atomic():
        chat = Chat.objects.create()
        for participant in participants:
            ChatParticipant.objects.create(
                chat=chat,
                user=participant,
            )
    return chat


def create_message(actor: User,
                   chat: Chat,
                   text: str) -> Message:
    with transaction.atomic():
        msg = Message.objects.create(
            author=chat.get_participant(actor),
            chat=chat,
            text=text,
        )
        chat.last_message = msg
        chat.save()
    return msg


