from rest_framework import serializers
from .models import Photo
from userapp.models import PhotoUser
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class FileSerializer(serializers.ModelSerializer):
    def get_user(self,obj):
        #iterate thoght photouser
        all = (obj.user.all())
        res = []
        for image in all:
            res.append(image.user.username)
        return res

    user = serializers.SerializerMethodField(method_name='get_user')
    def validate(self, data):
        image = data['image']
        if str(image.name).lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            if image.image:
                if image.size != 0:
                    return data
        


    def create(self, validated_data):
        #TODO SAVE HERE
        image = validated_data.pop('image')
        current_user = self.context['user']
        photo = Photo.objects.create(image=image)
        photo.user.add(current_user)
        return photo

    class Meta:
        model = Photo
        fields = ('image','user')
