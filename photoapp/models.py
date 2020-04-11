from django.db import models

class File(models.Model):
    image = models.ImageField(blank=False, null=False)
    def __str__(self):
        return self.file.name