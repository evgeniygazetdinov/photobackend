from rest_framework import serializers
from django.contrib.auth.models import User # If used custom user model
from django.contrib.auth.password_validation import validate_password
from .models import PhotoUser
from photoapp.models import Photo
from photoapp.serializers import FileSerializer
from django.forms.models import model_to_dict

UserModel = PhotoUser



class UserSerializer(serializers.ModelSerializer):
    def get_images(self,obj):
        res = []
        photos = Photo.objects.all().filter(user__user__username=obj.user.username)
        serializer = FileSerializer(instance=photos, many=True)
        return serializer.data


    id = serializers.CharField(source="user.id",required=False)
    password = serializers.CharField(source='user.password',write_only=True)
    username = serializers.CharField(source="user.username")
    is_admin = serializers.CharField(source="user.is_staff",required=False)
    photos = serializers.SerializerMethodField(method_name='get_images')
    def create(self, validated_data):
        user = PhotoUser.objects.create(
            user__username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
    
        fields = ('id','username','is_admin','photos','password')
  

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value