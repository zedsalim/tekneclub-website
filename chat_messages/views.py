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


@login_required
def deleteMessage_view(request, pk):
  if request.method == 'POST':
    current_user = request.user
    if not current_user.userprofile.is_responder:
      messages.error(request, 'You do not have the necessary permissions.')
      return redirect('core:home')
    else:
      deleted_msg = Message.objects.filter(pk=pk).first()
      deleted_msg.delete()
      messages.success(request, 'Message deleted successfully')
      return redirect('chat_messages:messages')
  else:
    messages.error(request, 'Method Not Allowed!')
    return redirect('core:home')


@login_required
def markAsSpam_view(request, pk):
  if request.method == 'POST':
    current_user = request.user
    if not current_user.userprofile.is_responder:
      messages.error(request, 'You do not have the necessary permissions.')
      return redirect('core:home')
    else:
      spam_message = Message.objects.filter(pk=pk).first()
      spam_message.status = 'Spam'
      spam_message.save()
      messages.success(request, 'Message marked as spam')
      return redirect('chat_messages:messages')
  else:
    messages.error(request, 'Method Not Allowed!')
    return redirect('core:home')
