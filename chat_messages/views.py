from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Message
from .forms import ReplyMessageForm
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


@login_required
def replyToMessage_view(request, pk):
  current_user = request.user
  if not current_user.userprofile.is_responder:
    messages.error(request, 'You do not have the necessary permissions.')
    return redirect('core:home')
  else:
    msg_to_reply = Message.objects.filter(pk=pk).first()
    if request.method == 'POST':
      reply_form = ReplyMessageForm(request.POST)
      if reply_form.is_valid():
        reply_msg = reply_form.save(commit=False)
        reply_msg.responder = current_user.userprofile
        reply_msg.message = msg_to_reply
        reply_msg.save()
        msg_to_reply.status = 'Replied'
        msg_to_reply.save()
        messages.success(request, 'Message replied successfully')
        return redirect('chat_messages:messages')
      else:
        messages.error(request, 'Something went wrong!')
    else:
      reply_form = ReplyMessageForm()
    
    context = {
      'reply_form': reply_form,
      'msg_to_reply': msg_to_reply
    }
    return render(request, 'chat_messages/reply.html', context)
