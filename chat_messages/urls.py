from django.urls import path
from .views import *

app_name = 'chat_messages'

urlpatterns = [
    path('messages/', listMessages_view, name='messages'),
    path('messages/<int:pk>/delete/', deleteMessage_view, name='delete-message'),
    path('messages/<int:pk>/spam/', markAsSpam_view, name='mark-spam'),
    path('messages/<int:pk>/reply/', replyToMessage_view, name='reply-message'),
] 