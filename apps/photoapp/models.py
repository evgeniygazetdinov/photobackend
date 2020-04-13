from django.db import models
from django.core.files.storage import Storage
import time
import os
from django.conf import settings

class Photo(models.Model):
    image = models.ImageField()
    user = models.ManyToManyField('userapp.photouser')

    def __str__(self):
        return self.photo.name