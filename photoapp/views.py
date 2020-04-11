from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from .serializers import FileSerializer
import json
from .models import File
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model # If used custom user model
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated  # <-- Here



      
class FileUploadView(ListAPIView):
    permission_classes = (IsAuthenticated,)  
    def get_serializer_context(self,request):
      #pass request from to serializer here!
      return {'user':request.user}

    def post(self, request, *args, **kwargs):
      print('THIS IS USER')
      context = {"user":request.user}
      file_serializer = FileSerializer(data=request.data,context=context)
      if file_serializer.is_valid():
        file_serializer.save()
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        photo = File.objects.all()
        serializer = FileSerializer(photo, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



  


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
      permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer
    