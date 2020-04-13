from django.db import models
from django.contrib.auth.models  import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin




class Photo(models.Model):
    photo_date = models.CharField(default='132', max_length=50)




# Create your models here.
class PhotoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.ForeignKey(Photo,on_delete=models.CASCADE,null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PhotoUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.photouser.save()