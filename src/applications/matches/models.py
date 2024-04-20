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

