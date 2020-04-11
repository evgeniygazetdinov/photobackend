from rest_framework import serializers
from .models import File
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


class FileSerializer(serializers.ModelSerializer):
    def validate(self, data):
        image = data['image']
        if str(image.name).lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            if image.image:
                if image.size != 0:
                    return data
        


    def create(self, validated_data):
        #TODO SAVE HERE
        image=validated_data.pop('image')
        print(self.context)
        photo=File.objects.create(image=image,owner=self.context['user'])
        
        return photo

    class Meta:
        model = File
        fields = ('image',)

from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password", )