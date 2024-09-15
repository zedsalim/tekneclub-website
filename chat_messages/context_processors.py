from .models import Message, Reply

def pending_messages(request):
    current_user = request.user
    if current_user.is_authenticated and hasattr(request.user, 'userprofile'):
        if current_user.userprofile.is_responder:
            pending_count = Message.objects.filter(status='Pending').count()
            return {'pending_count': pending_count}
    return {}


def unread_replied_messages(request):
    current_user = request.user
    if current_user.is_authenticated and hasattr(request.user, 'userprofile'):
        replied_msgs = Message.objects.filter(sender=current_user.userprofile, status='Replied')
        unread_replies = Reply.objects.filter(message__in=replied_msgs, is_read=False).count()
        context = {
            'unread_replies': unread_replies,
        }
        return context 
    return {}