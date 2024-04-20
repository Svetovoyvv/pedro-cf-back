from django.db import models
from django.db.models import Exists, OuterRef, F, Value as V, FilteredRelation, Q, Func
from django.db.models.functions import Concat

from applications.members.models import User


class ChatQuerySet(models.QuerySet):
    def visible_for(self, actor: User):
        return self.filter(
            Exists(
                ChatParticipant.objects.filter(
                    chat=OuterRef('pk'),
                    user=actor,
                )
            )
        )

    def annotate_name(self, actor: User):
        return self.annotate(
            name=ChatParticipant.objects.filter(
                chat=OuterRef('pk'),
            ).exclude(
                user=actor,
            ).annotate(
                _name=Concat(
                    F('user__first_name'),
                    V(' '),
                    F('user__last_name'),
                )
            ).values('_name')
        )


class Chat(models.Model):
    objects = ChatQuerySet.as_manager()

    created = models.DateTimeField(auto_now_add=True)
    last_message = models.ForeignKey(
        'Message',
        on_delete=models.PROTECT,
        related_name='last_message_chats',
        null=True,
    )

    def __str__(self):
        return f'Chat: {self.pk}'

    def get_participant(self, user: User):
        return self.participants.get(user=user)


class ChatParticipant(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='participants',
    )
    user = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Chat {self.pk} | {self.user}'


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    author = models.ForeignKey(
        ChatParticipant,
        on_delete=models.PROTECT,
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message: {self.pk} | {self.author} | {self.text}'

