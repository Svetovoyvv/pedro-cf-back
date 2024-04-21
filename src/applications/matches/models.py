from django.db import models


class RecommendationState(models.IntegerChoices):
    PENDING = 0
    LIKE = 1
    DISLIKE = 2


class UserRecommendation(models.Model):
    subject = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
        related_name='recommendations',
    )
    object = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
        related_name='recommended_for',
    )
    state = models.IntegerField(
        choices=RecommendationState.choices,
        default=RecommendationState.PENDING,
        null=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


class MeetingState(models.IntegerChoices):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2


class Meeting(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    is_online = models.BooleanField()
    author = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
    )
    state = models.IntegerField(
        choices=MeetingState.choices,
        default=MeetingState.PENDING,
    )
    chat = models.OneToOneField(
        'chats.Chat',
        on_delete=models.CASCADE,
    )

class MeetingMemberState(models.IntegerChoices):
    PENDING = 0
    APPROVED = 1
    CANCELED = 2


class MeetingMember(models.Model):
    user = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
    )
    comment = models.TextField()
    state = models.IntegerField(
        choices=MeetingMemberState.choices,
        default=MeetingMemberState.PENDING,
    )



