from django.db import models
from django.core.files.storage import Storage
import time
import os
from django.conf import settings
import uuid
from django.utils import timezone
import pytz

class UploadList(models.Model):
    user = models.ManyToManyField('userapp.photouser')
    pub_date = models.DateTimeField(default=timezone.now)
    images = models.ManyToManyField('photoapp.photo')

class PhotoViews(models.Model):
    views = models.DateTimeField(auto_now_add=True)


class PhotoPosition(models.Model):
    photo_with_position = models.ManyToManyField('photoapp.photo')
    latitude = models.DecimalField(max_digits=5, decimal_places=2,default=0.0)
    longitude = models.DecimalField(max_digits=5, decimal_places=2,default=0.0)


class Photo(models.Model):
    user = models.ManyToManyField('userapp.photouser')
    image = models.ImageField()
    created_date = models.DateTimeField(auto_now_add=True)
    views = models.ManyToManyField(PhotoViews)
    position = models.ManyToManyField('photoapp.photoposition')
    description = models.TextField(null=True, blank=True)
    upload_list = models.ManyToManyField('photoapp.uploadlist')
    