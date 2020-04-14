from rest_framework import serializers
from .models import Photo
from userapp.models import PhotoUser
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import shutil



class CountViewsPhotoSerializer(serializers.ModelSerializer):
    views = serializers.SerializerMethodField(method_name='get_list_views')
    links = serializers.SerializerMethodField(method_name='get_unique_link_for_image') 
    def get_list_views(self, obj):
        pass
    
    def get_unique_link_for_image(self, obj):
        pass


class FileSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField(method_name='time_format')
    id = serializers.IntegerField(required=False)
    user = serializers.SerializerMethodField(method_name='get_user')
   

    
    def get_photo_url(self, car):
        request = self.context.get('request')
        photo_url = car.photo.url
        return request.build_absolute_uri(photo_url)


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
        


    def create(self,validated_data):
        #TODO SAVE HERE
        image = validated_data.pop('image')
        current_user = self.context['user']
        request = self.context.get('request')
        photo = Photo.objects.create(image=image)
        photo.user.add(current_user)
        need_path = (os.getcwd()+'/media/'+str(current_user.user.username)+'/')
        path_now = os.path.abspath(image.name)
        path_from_move = os.path.dirname(path_now)+'/media/'+image.name
        if not os.path.exists(need_path):
            os.mkdir(need_path)
            os.rename(path_from_move,need_path+image.name)
        os.rename(path_from_move,need_path+image.name)
        return photo

    class Meta:
        model = Photo
        fields = ('id', 'image', 'user', 'created_date')
