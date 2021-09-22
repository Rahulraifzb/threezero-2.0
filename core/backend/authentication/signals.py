from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *

@receiver(post_save,sender=User)
def profile_create(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def profile_save(sender,instance,**kwargs):
    instance.profile.save()

@receiver(post_save,sender=Profile)
def social_create(sender,instance,created,**kwargs):
    if created:
        Social.objects.create(profile=instance)

@receiver(post_save,sender=Profile)
def social_save(sender,instance,**kwargs):
    instance.social.save()