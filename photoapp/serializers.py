from rest_framework import serializers
from .models import File
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings



class FileSerializer(serializers.ModelSerializer):
    def validate(self, data):
        #TODO VALIDATE NAME
        if ((data['image']).endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
            print(validate)
            return data    
        print('not valid')


    def create(self, validated_data):
        #TODO SAVE HERE
        """
        path = default_storage.save('tmp/somename.mp3', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        """
        blogs=Blogs.objects.latest('created_at')
        image=validated_data.pop('image')
        print('here')
        for img in image:
            photo=File.objects.create(image=image)
        return photo

    class Meta:
        model = File
        fields = "__all__"