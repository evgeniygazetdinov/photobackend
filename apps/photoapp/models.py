from django.db import models
from django.core.files.storage import Storage
import time
import os
from django.conf import settings


class Photo(models.Model):
    image = models.ImageField()
    user = models.ManyToManyField('userapp.photouser')
    created_date = models.DateTimeField(auto_now_add=True)

# class PhotoViews(models.Model):
#     image = models.ManyToManyField('userapp.photouser')
#     data_views = 
