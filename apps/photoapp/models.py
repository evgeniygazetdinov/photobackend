from django.db import models
from django.core.files.storage import Storage
import time
import os
from django.contrib.auth.models import User

class File(models.Model):
    image = models.ImageField(blank=False, null=False)
    owner = models.ForeignKey('auth.User', related_name='image',on_delete="CASCADE",null=False)
    def __str__(self):
        return self.file.name