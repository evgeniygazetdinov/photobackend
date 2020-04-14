from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from .serializers import FileSerializer
import json
from .models import Photo
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated  # <-- Here
from userapp.models import PhotoUser
from rest_framework.decorators import api_view,permission_classes,action


      
class FileUploadView(ListAPIView):
    permission_classes = (IsAuthenticated,)  
    def post(self, request, *args, **kwargs):
        user = PhotoUser.objects.get(user__username = request.user)
        context = {"user": user}
        file_serializer = FileSerializer(data=request.data,context=context)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        photo = Photo.objects.all()
        serializer = FileSerializer(photo, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_picture_by_id(request,picture_id):
    cur_user = PhotoUser.objects.get(user__username=request.user)
    return Response(serializer.data,status.HTTP_200_OK)


