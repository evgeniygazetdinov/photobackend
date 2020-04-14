from rest_framework import serializers
from .models import Photo
from userapp.models import PhotoUser
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class FileSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField(method_name='time_format')
    id = serializers.IntegerField(required=False)
    user = serializers.SerializerMethodField(method_name='get_user')
   
    def time_format(self,obj):
        return  obj.created_date.strftime("%Y-%m-%d %H:%M")


    def get_user(self,obj):
        #iterate thoght photouser
        all = (obj.user.all())
        res = []
        for image in all:
            res.append(image.user.username)
        return res


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
        fields = ('id', 'image', 'user', 'created_date')
