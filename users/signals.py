import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(pre_save, sender=UserProfile)
def delete_old_profile_pic(sender, instance, **kwargs):
    if not instance.pk:
        # If this is a new instance, there is no old image to delete
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # If the old instance doesn't exist, do nothing
        return

    if old_instance.profile_pic and old_instance.profile_pic != 'default.jpg':
        if old_instance.profile_pic != instance.profile_pic:
            if os.path.isfile(old_instance.profile_pic.path):
                os.remove(old_instance.profile_pic.path)
