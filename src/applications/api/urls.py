from django.urls import path, include

urlpatterns = [
    path('auth/', include('applications.gauth.api.urls')),
    path('chats/', include('applications.chats.api.urls')),
    path('members/', include('applications.members.api.urls')),
]
