from rest_framework import status
from rest_framework.test import APITestCase

from applications.chats.models import Chat
from applications.chats.services import create_chat, create_message
from applications.members.models import User


class ChatAppBaseTestClass:
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


class ChatTestCase(ChatAppBaseTestClass, APITestCase):
    def test_list_chats(self):
        chat = create_chat([self.test_user_1, self.admin])
        msg = create_message(self.admin, chat, text='hello world')

        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/chats/chat/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        apichat = response.data['results'][0]
        self.assertEqual(
            apichat['name'], self.test_user_1.get_full_name()
        )
        self.assertEqual(
            apichat['last_message']['text'], msg.text
        )

