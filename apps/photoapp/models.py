from django.db import models
from django.core.files.storage import Storage
import time
import os
from django.conf import settings
import uuid


class PhotoViews(models.Model):
    views = models.DateTimeField(auto_now_add=True)


class Photo(models.Model):
    user = models.ManyToManyField('userapp.photouser')
    image = models.ImageField()
    created_date = models.DateTimeField(auto_now_add=True)
    views = models.ManyToManyField(PhotoViews)


 

