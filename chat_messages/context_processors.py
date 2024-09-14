from .models import Message

def pending_messages(request):
    if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        pending_count = Message.objects.filter(status='Pending').count()
        return {'pending_count': pending_count}
    return {}
