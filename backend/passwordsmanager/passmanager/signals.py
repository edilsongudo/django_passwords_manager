from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MasterPassword


@receiver(post_save, sender=get_user_model())
def createMasterPassword(sender, instance, created, **kwargs):
    if created:
        MasterPassword.objects.create(author=instance)


@receiver(post_save, sender=get_user_model())
def saveMasterPassword(sender, instance, created, **kwargs):
    instance.masterpassword.save()
