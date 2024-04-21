from datetime import timedelta, datetime
import random

from django.db import transaction, IntegrityError
from django.db.models import Exists, OuterRef
from django.utils import timezone

from applications.chats.models import Chat
from applications.chats.services import create_chat
from applications.common.exceptions import BaseServiceException
from applications.matches.models import UserRecommendation, RecommendationState, Meeting, MeetingMember
from applications.members.models import User


def get_recommendations_delta():
    return timezone.now() - timedelta(weeks=2)

def random_spread_recommendations():
    UserRecommendation.objects.all().update(
        is_deleted=True,
    )
    recommendations = []
    with transaction.atomic():
        users = User.objects.all()
        min_delta = get_recommendations_delta()
        for user in users:
            recommends = User.objects.exclude(
                id=user.id,
            ).exclude(
                Exists(
                    UserRecommendation.objects.filter(
                        subject=user,
                        object=OuterRef('pk'),
                        state=RecommendationState.DISLIKE,
                        created__gte=min_delta,
                    )
                )
            )
            rec_users = list(recommends.values_list('id', flat=True))
            rec_users = list(set(random.choices(rec_users, k=5)))
            for rec_user in rec_users:
                recommendations.append(
                    UserRecommendation(
                        subject_id=user.id,
                        object_id=rec_user,
                    )
                )
        UserRecommendation.objects.bulk_create(recommendations)


def update_recommendation(actor: User,
                          recommendation: UserRecommendation,
                          state: RecommendationState):
    if recommendation.state != RecommendationState.PENDING:
        raise BaseServiceException(
            'Невозможно изменить выбор действия по рекомендации',
        )

    if state == RecommendationState.LIKE:
        reply_recommendation = UserRecommendation.objects.filter(
            subject=recommendation.object,
            object=recommendation.subject,
            is_deleted=False,
        ).first()

        if reply_recommendation is None:
            reply_recommendation = UserRecommendation.objects.create(
                subject=recommendation.object,
                object=recommendation.subject,
            )
        if reply_recommendation.state == RecommendationState.LIKE:
            create_chat([recommendation.subject, recommendation.object])
            recommendation.is_bump = True

    recommendation.state = state
    recommendation.save()
    return recommendation


def create_meeting(actor: User,
                   chat: Chat,
                   start_datetime: datetime,
                   end_datetime: datetime) -> Meeting:
    try:
        with transaction.atomic():
            meeting = Meeting.objects.create(
                author=actor,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                chat=chat,
            )
            for participant in chat.participants.all():
                MeetingMember.objects.create(
                    participant=meeting,
                    user=participant.user,
                )
        return meeting.refresh_from_db()
    except IntegrityError as e:
        raise BaseServiceException(
            'Ошибка при создании встречи'
        ) from e