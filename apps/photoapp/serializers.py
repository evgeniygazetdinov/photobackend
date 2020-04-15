from rest_framework import serializers
from .models import Photo
from userapp.models import PhotoUser
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import shutil
from datetime import datetime, timedelta




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
    views = serializers.SerializerMethodField(method_name='display_views')

    def display_views(self,obj):
        res = []
        
        
        views = obj.views.all()
        for view in views:
            obj_time = view.views+timedelta(hours=3)
            
            res.append(obj_time.strftime("%Y-%m-%d %H:%M"))
        return res


    def get_photo_url(self, car):
        request = self.context.get('request')
        photo_url = car.photo.url
        return request.build_absolute_uri(photo_url)


    def time_format(self,obj):
        obj_time = obj.created_date+timedelta(hours=3)
        return  obj_time.strftime("%Y-%m-%d %H:%M")


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



    def move_to_user(self,path_from_move,need_path,image):
        pass


    def create(self,validated_data):
        #TODO SAVE HERE
        image = validated_data.pop('image')
        current_user = self.context['user']
        request = self.context.get('request')
        #need_path = (os.getcwd()+'/media/'+str(current_user.user.username)+'/')
        #path_now = os.path.abspath(image.name)
        #path_from_move = os.path.dirname(path_now)+'/media/'+image.name
       # if not os.path.exists(need_path):
       #     os.mkdir(need_path)
     
        #shutil.move(path_from_move,need_path+image.name) 
        photo = Photo.objects.create(image=image)
        photo.user.add(current_user)
        #photo.image.upload_to = need_path+image.name
       
        #print(datetime.datetime.now())
        #dir(photo)
        return photo

    class Meta:
        model = Photo
        fields = ('id', 'image', 'user', 'created_date','views')
