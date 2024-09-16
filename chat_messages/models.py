from django.db import models
from users.models import UserProfile


class Message(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Replied', 'Replied'),
        ('Spam', 'Spam'),
    )
    sender = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    content = models.TextField(max_length=1000)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    
    def __str__(self):
        return f'Subject: {self.subject}'

class Reply(models.Model):
    responder = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.TextField()
    replied_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'
    
    def __str__(self):
        return f'Reply To: {self.message.subject}'


class FeedBack(models.Model):
    fbk_sender = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    fbk_name = models.CharField(max_length=100)
    fbk_content = models.TextField(max_length=1000)
    fbk_sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.fbk_name.capitalize()}: {self.fbk_content}'