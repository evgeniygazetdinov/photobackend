from rest_framework import serializers
from django.contrib.auth.models import User # If used custom user model
from django.contrib.auth.password_validation import validate_password
from .models import PhotoUser
from photoapp.models import Photo,UploadList
from photoapp.serializers import FileSerializer,UploadListSerializer
from django.forms.models import model_to_dict
from datetime import datetime, timedelta


UserModel = PhotoUser



class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['user']['username'])
        user.set_password(validated_data['user']['password'])
        user.save()
        photo= PhotoUser(user=user)
        return photo
    

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


    def validate(self,data):
        is_already_exists = User.objects.filter(username=data['user']['username']).exists()
        if is_already_exists:
            raise serializers.ValidationError('already exists')
        return data

    def get_uploads_list(self,obj):
        #need username as string
        upload = UploadList.objects.all().filter(user__user__username=obj.user.username)
        #IF USER NOT UPLOADED WARNING
        #need check if upload list no on user return []
        serializer = UploadListSerializer(upload,many=True,context=self.context)
        return serializer.data
        
    def get_images(self,obj):
        photos = Photo.objects.all().filter(user__user__username=obj.user.username)
        serializer = FileSerializer(instance=photos, many=True,context=self.context)
        return serializer.data
    
    def user_last_visit(self,obj):
        visit = UserModel.objects.get(id = obj.user.id)
        return visit.last_visit

    def user_time_for_clear(self,obj):
        time = UserModel.objects.get(id = obj.user.id)

        return time.time_for_clear_messages

    id = serializers.CharField(source="user.id",required=False)
    password = serializers.CharField(source='user.password',write_only=True)
    username = serializers.CharField(source="user.username")
    is_admin = serializers.CharField(source="user.is_staff",required=False)
    time_for_clear_messages = serializers.SerializerMethodField(method_name='user_time_for_clear')
    last_visit = serializers.SerializerMethodField(method_name='user_last_visit')
    photos = serializers.SerializerMethodField(method_name='get_images') 
    upload_list = serializers.SerializerMethodField(method_name='get_uploads_list')

    class Meta:
        model = User
        fields = ('id','username','is_admin','last_visit','time_for_clear_messages','photos','upload_list','password')
  

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class ChangeTimeDeleteSerializer(serializers.Serializer):
    new_time = serializers.CharField(required=True)