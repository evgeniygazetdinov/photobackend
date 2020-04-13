from rest_framework import serializers
from django.contrib.auth.models import User # If used custom user model
from django.contrib.auth.password_validation import validate_password
from .models import PhotoUser



UserModel = PhotoUser



class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="photouser.user.id",required=False)
    password = serializers.CharField(source='photouser.user.password',write_only=True)
    username = serializers.CharField(source="photouser.user.username")
    is_admin = serializers.CharField(source="photouser.user.is_staff",required=False)
    date = serializers.CharField(source="photouser.date",required=False)
    def create(self, validated_data):
        print(validated_data)
        print(validated_data['photouser']['user']['username'])
        user = User.objects.create(
            username=validated_data['photouser']['user']['username']
        )
        user.set_password(validated_data['photouser']['user']['password'])
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