from django.db import models
from django.contrib.auth.models  import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin
from photoapp.models import Photo
from datetime import datetime




# Create your models here.
class PhotoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image =  models.ManyToManyField('photoapp.photo')
    time_for_clear_messages = models.IntegerField(default=60)
    last_visit = models.DateField(null=True, blank=True)
    upload_lists = models.ManyToManyField('photoapp.uploadlist')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PhotoUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.photouser.save()

