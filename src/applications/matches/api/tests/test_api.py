from rest_framework import status
from rest_framework.test import APITestCase

from applications.chats.models import Chat
from applications.chats.services import create_chat, create_message
from applications.matches.models import RecommendationState
from applications.matches.services import random_spread_recommendations
from applications.members.models import User


class AppBaseTestClass:
    fixtures = [
        'groups.json',
        'users.json',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin = None
        self.test_user_1 = None

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.test_user_1 = User.objects.get(username='test_user_1')

        super().setUp()


class MatchTestCase(AppBaseTestClass, APITestCase):
    def test_create_bump(self):
        random_spread_recommendations()

        self.client.force_authenticate(user=self.admin)

        response = self.client.get('/api/recommendations/match/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rec_pk = response.data['results'][0]['id']
        response = self.client.patch(
            f'/api/recommendations/match/{rec_pk}/',
            {'state': RecommendationState.LIKE},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_bump'], False)

        self.client.force_authenticate(user=self.test_user_1)
        response = self.client.get('/api/recommendations/match/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rec_pk = response.data['results'][0]['id']
        response = self.client.patch(
            f'/api/recommendations/match/{rec_pk}/',
            {'state': RecommendationState.LIKE},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_bump'], True)

        self.assertEqual(
            set(Chat.objects.first().participants.values_list('user__id', flat=True)),
            {self.admin.id, self.test_user_1.id},
        )
