from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from users.models import UserProfile


@login_required
def listMessages_view(request):
  current_user = request.user
  if not current_user.userprofile.is_responder:
    messages.error(request, 'You do not have permission to see the messages')
    return redirect('core:home')
  else:
    pending_messages = Message.objects.filter(status='Pending').all()
    replied_messages = Message.objects.filter(status='Replied').all()
    spam_messages = Message.objects.filter(status='Spam').all()

    context = {
      'pending_messages': pending_messages,
      'replied_messages': replied_messages,
      'spam_messages': spam_messages
    }
    return render(request, 'chat_messages/all_messages.html', context)
