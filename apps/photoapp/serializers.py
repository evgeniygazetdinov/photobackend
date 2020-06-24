from rest_framework import serializers
from .models import Photo,PhotoPosition
from userapp.models import PhotoUser

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import shutil
from datetime import datetime, timedelta
from django.urls import reverse
from django.utils.crypto import get_random_string
import base64
import uuid


class UploadListSerializer(serializers.ModelSerializer):
    def indify_user(self,obj):

        return obj.id


    def get_photos_from_upload_list(self,obj):
        return 1
    

    user = serializers.SerializerMethodField(method_name='indify_user')
    date_upload =  serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, source='uploadlist.pub_date')
    photos  = serializers.SerializerMethodField(method_name='get_photos_from_upload_list')

    class Meta:
        model = Photo
        fields = ('id','user', 'date_upload',  'photos')


class FileSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField(method_name='time_format')
    id = serializers.IntegerField(required=False)
    user = serializers.SerializerMethodField(method_name='get_user')
    views = serializers.SerializerMethodField(method_name='display_views')
    unique_link = serializers.SerializerMethodField(method_name='generate_link')
    unique_short_link = serializers.SerializerMethodField(method_name='generate_short_link')
    delete_by_unique_link = serializers.SerializerMethodField(method_name='generate_delete_link')
    position = serializers.SerializerMethodField(method_name='get_photo_position')
    descript = serializers.SerializerMethodField(method_name='get_descript')


    def encode_piece(self,ori_str, key):
        enc = []
        b = bytearray(ori_str)
        k = bytearray(key)
        for i, c in enumerate(b):
            key_c = k[i % len(key)]
            enc_c = (c + key_c) % 256
            enc.append(enc_c)
        return (base64.urlsafe_b64encode(bytes(bytearray(enc))))




    @staticmethod
    #call this stuff in view/for back id
    def decode_id(enc_str, key):
        dec = []
        byte_key = bytes(key, 'utf-8')
        enc_str = bytearray(base64.urlsafe_b64decode(enc_str))
        k = bytearray(byte_key)
        for i, c in enumerate(enc_str):
            key_c = k[i % len(byte_key)]
            dec_c = (c - key_c) % 256
            dec.append(dec_c)
        return (bytes(bytearray(dec)))#for barbara
    
    
    @staticmethod
    def key_and_id_from_short_link(generated_string):
        from_string = generated_string.split('&')
        key = from_string[1]
        decripted = (FileSerializer.decode_id(from_string[0],key))
        from_decripted = (decripted.decode('utf-8')).split('#')
        picture_id = FileSerializer.decode_id(from_decripted[1],key)
        return int(picture_id)



    def generate_short_link(self,obj):
        key = (uuid.uuid4().hex.upper()[0:1]).encode('utf-8')
        enc = self.encode_piece(str(obj.id).encode('utf-8'),key)
        unique_random =key.decode('utf-8')+'#'+enc.decode('utf-8')
        encode_unique_random =self.encode_piece(unique_random.encode('utf-8'),key)
        link = reverse('short_unique', kwargs={'generated_string':str(encode_unique_random.decode('utf-8')+'&'+key.decode('utf-8'))})
        return self.context['host']+link


    def generate_link(self,obj):
        randomstring = get_random_string(length=1)
        key = (uuid.uuid4().hex.upper()[0:1]).encode('utf-8')
        owner = self.encode_piece(str(self.context['user']).encode('utf-8'),key)
        enc = self.encode_piece(str(obj.id).encode('utf-8'),key)
        link = reverse('unique', kwargs={'random_string':randomstring,
            'encript':enc.decode('utf-8'),'key':key.decode('utf-8'),
            'owner':owner.decode('utf-8')})
        return self.context['host']+link


    #YES THIS REPEAT BUT i have not found flags. for methodfield for split one func
    def generate_delete_link(self,obj):
        randomstring = get_random_string()
        key = uuid.uuid4().hex.upper()[0:6]
        enc = self.encode_piece(str(obj.id).encode('utf-8'),key.encode('utf-8'))
        link = reverse('delete_unique', kwargs={'random_string':randomstring,'encript':enc.decode('utf-8'),'key':key})
        return self.context['host']+link


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

    def get_photo_position(self,obj):
        pos = PhotoPosition.objects.get_or_create(id=obj.id)
        photo_position = {'id':pos[0].id,'longitude':pos[0].longitude,'latitude':pos[0].latitude}

        return photo_position

    def get_descript(self,obj):
        return obj.description


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
        image = validated_data.pop('image')
        current_user = self.context['current_user_model']
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
        fields = ('id', 'image', 'user','descript', 'created_date','views','unique_link', 'unique_short_link', 'delete_by_unique_link','position')