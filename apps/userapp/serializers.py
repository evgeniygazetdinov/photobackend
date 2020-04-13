from rest_framework import serializers
from django.contrib.auth.models import User # If used custom user model
from django.contrib.auth.password_validation import validate_password
from .models import PhotoUser,Photo



UserModel = PhotoUser



class UserSerializer(serializers.ModelSerializer):
    def get_images(self,obj):
        #iterate thoght photouser
        all = (obj.date.all())
        res = []
        for image in all:
            res.append(image.photo_date)
        return res





    id = serializers.CharField(source="user.id",required=False)
    password = serializers.CharField(source='user.password',write_only=True)
    username = serializers.CharField(source="user.username")
    is_admin = serializers.CharField(source="user.is_staff",required=False)
    date = serializers.SerializerMethodField(method_name='get_images')
    #date = serializers.CharField(source="photouser.date",required=False, allow_null=True)
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
    
        fields = ('id','username','is_admin','date','password')
  

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value