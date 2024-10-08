from django.urls import path
from .views import *

app_name = 'chat_messages'

urlpatterns = [
    path('messages/', listMessages_view, name='messages'),
    path('my_messages/', listMessagesForRegularUsers_view, name='users-messages'),
    path('messages/<int:pk>/delete/', deleteMessage_view, name='delete-message'),
    path('messages/<int:pk>/spam/', markAsSpam_view, name='mark-spam'),
    path('messages/<int:pk>/reply/', replyToMessage_view, name='reply-message'),
    path('messages/<int:pk>/display/', displayMessage_view, name='display-message'),
    path('my_messages/<int:pk>/read/', markAsRead_view, name='mark-read'),
] 