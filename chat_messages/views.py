from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Message, Reply
from .forms import ReplyMessageForm


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
def listMessagesForRegularUsers_view(request):
  current_user = request.user.userprofile
  pending_messages = Message.objects.filter(sender=current_user, status='Pending').all()
  replied_messages = Message.objects.filter(sender=current_user, status='Replied').all()
  spam_messages = Message.objects.filter(sender=current_user, status='Spam').all()

  context = {
    'pending_messages': pending_messages,
    'replied_messages': replied_messages,
    'spam_messages': spam_messages
  }
  return render(request, 'chat_messages/users_messages.html', context)


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

      spam_message = get_object_or_404(Message, pk=pk)
      spam_message.status = 'Spam'
      spam_message.save()
      messages.success(request, 'Message marked as spam')
      return redirect('chat_messages:messages')

  else:
    messages.error(request, 'Invalid request method.')
    return redirect('core:home')


@login_required
def markAsRead_view(request, pk):
  if request.method == 'POST':
      message = get_object_or_404(Message, pk=pk, status='Replied')
      unread_reply = Reply.objects.filter(message=message, is_read=False).first()
      unread_reply.is_read = True
      unread_reply.save()
      messages.success(request, 'Reply marked as read')
      return redirect('chat_messages:users-messages')

  else:
    messages.error(request, 'Invalid request method.')
    return redirect('core:home')


@login_required
def replyToMessage_view(request, pk):
    current_user = request.user
    if not current_user.userprofile.is_responder:
        messages.error(request, 'You do not have the necessary permissions.')
        return redirect('core:home')

    msg_to_reply = get_object_or_404(Message, pk=pk)
    if msg_to_reply.status == 'Pending': 
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

    else:
       messages.info(request, 'This message has already been replied to.')
       return redirect('chat_messages:display-message', msg_to_reply.pk)

@login_required
def displayMessage_view(request, pk):
    msg_to_display = get_object_or_404(Message, pk=pk)
    current_user = request.user
    if current_user.userprofile.is_responder or current_user.userprofile == msg_to_display.sender:
        reply_msg = Reply.objects.filter(message=msg_to_display).first()
        
        context = {
            'reply_msg': reply_msg,
            'msg_to_display': msg_to_display
        }
        return render(request, 'chat_messages/message_detail.html', context)
    else:
        messages.error(request, 'You do not have the necessary permissions.')
        return redirect('core:home')
