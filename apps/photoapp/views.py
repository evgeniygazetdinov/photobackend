from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from .serializers import FileSerializer
import os
from .models import Photo,PhotoViews
from rest_framework.permissions import IsAuthenticated  # <-- Here
from userapp.models import PhotoUser
from rest_framework.decorators import api_view,permission_classes,action
from django.core.files.base import ContentFile
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
import datetime



class FileUploadView(ListAPIView):
    permission_classes = (IsAuthenticated,)  
    def post(self, request, *args, **kwargs):
        user = PhotoUser.objects.get(user__username = request.user)
        context = {'host' :(request.scheme +"://"+ request.get_host()),'user':request.user,'current_user_model':user}
        file_serializer = FileSerializer(data=request.data,context=context)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_picture_by_id(request,picture_id):
    cur_user = PhotoUser.objects.get(user__username=request.user)
    photo = Photo.objects.get(id = picture_id,user =cur_user)
    host = request.scheme +"://"+ request.get_host()
    now = datetime.datetime.now()
    photo_view = PhotoViews()
    photo_view.save()
    photo.views.add(photo_view)
    pic_propenty = {'host':host,'user':cur_user.user.username,'picture_url':photo.image.url}
    return render_to_response('photoapp/photo.html',pic_propenty)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_picture_from_unique_link(request,random_string,encript,key,owner):
    picture_id = (FileSerializer.decode_id(encript,key))
    owner_from_uri = (FileSerializer.decode_id(owner,key)).decode('utf-8')
    cur_user = PhotoUser.objects.get(user__username=owner_from_uri)
    photo = Photo.objects.get(id = int(picture_id),user =cur_user)
    host = request.scheme +"://"+ request.get_host()
    now = datetime.datetime.now()
    photo_view = PhotoViews()
    photo_view.save()
    photo.views.add(photo_view)
    pic_propenty = {'host':host,'user':cur_user.user.username,'picture_url':photo.image.url}
    return render_to_response('photoapp/photo.html',pic_propenty)



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def delete_picture_from_unique_link(request,random_string,encript,key):
    picture_id = FileSerializer.decode_id(encript,key)
    cur_user = PhotoUser.objects.get(user__username=request.user)
    photo = Photo.objects.get(id = picture_id,user =cur_user)
    photo.delete()
    os.remove(photo.image.path)
    pic_propenty = {'user':cur_user.user.username,'picture_url':photo.image.url +' was be removed','url':request.path}
    return Response(pic_propenty, status=status.HTTP_200_OK)

