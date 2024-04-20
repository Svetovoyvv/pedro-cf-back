from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from applications.chats.api import views

router = SimpleRouter()

router.register(r'chat', views.ChatViewSet)
chat_router = NestedSimpleRouter(router, r'chat', lookup='chat')
chat_router.register(r'message', views.MessageViewSet, basename='chat-message')

urlpatterns = router.urls + chat_router.urls
