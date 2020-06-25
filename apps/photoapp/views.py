from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from .serializers import FileSerializer, UploadListSerializer
import os
from .models import Photo, PhotoViews, PhotoPosition, UploadList
from rest_framework.permissions import IsAuthenticated  # <-- Here
from userapp.models import PhotoUser
from rest_framework.decorators import api_view,permission_classes,action
from django.core.files.base import ContentFile
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
import datetime
from django.utils.six.moves.urllib.parse import urlsplit
import ast



class FileUploadView(ListAPIView):
    permission_classes = (IsAuthenticated,)  
    def post(self, request, *args, **kwargs):
        user = PhotoUser.objects.get(user__username = request.user)
        context = {'host' :(urlsplit(request.build_absolute_uri(None)).scheme +"://"+ request.get_host()),'user':request.user,'current_user_model':user}
        file_serializer = FileSerializer(data=request.data,context=context)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_userlist(request,id):
    lists = UploadList.objects.filter(user__user__username=request.user.username,id=id)
    return Response('1', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def add_photos_to_upload_list(request):
    #
    #get photoname from request
    #get photo objects
    #set to all 
    #upload list
    #return {uploads:photos with with }
    user = PhotoUser.objects.filter(user__username = request.user)
    context = {'host' :('https' +"://"+ request.get_host()),'user':user}
    queryset = UploadList.objects.create()
    queryset.user.set(user)
    photos = (request.data['photos']).split(',')
    for photo in photos:
        cur_photo = Photo.objects.get(image=photo)
        queryset.image.add(cur_photo)
        queryset.save()
    serializer = UploadListSerializer(instance=queryset, data=request.data, context=context)
    if serializer.is_valid():
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def find_id(request):
    photo_name = request.data['image']
    all_images = Photo.objects.all()
    for image in all_images.values():
        if photo_name == image['image']:
            return image
        else :
            continue
    return None        
       

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def change_photoposition(request):
    photo_instance = find_id(request)
    if photo_instance:
        position = PhotoPosition.objects.get(id=photo_instance['id'])
        longitude = request.data['longitude']
        latitude = request.data['latitude']
        position.latitude = latitude
        position.longitude = longitude
        position.save()
        return Response({'id':photo_instance['id'],'file':request.data['image'],'longitude':position.longitude ,'latitude':position.latitude}, status=status.HTTP_200_OK)
    else:
        
        return Response({'error':'file {} not exists'.format(request.data['image'])}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def change_photo_description(request):
    photo_instance = find_id(request)
    photo_instance = Photo.objects.get(image = (photo_instance['image']))
    if photo_instance:
        desc = request.data['description']
        photo_instance.description = desc

        photo_instance.save()
        return Response({'description':desc,'file':request.data['image']}, status=status.HTTP_200_OK)
    else:
    
        return Response({'error':'file {} not exists'.format(request.data['image'])}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def by_short_link(request,generated_string):
    picture_id = FileSerializer.key_and_id_from_short_link(generated_string)
    photo = Photo.objects.get(id = int(picture_id))
    desc = photo.description
    photo_view = PhotoViews()
    photo_view.save()
    photo.views.add(photo_view)
    pos = PhotoPosition.objects.get_or_create(id=picture_id)
    if photo.description is "null":
        desc = False
    if pos[0].longitude ==0.0 or pos[0].latitude == 0.0:
        pos_on_map = False
    else:
        pos_on_map = 'https://www.google.com/maps/place/{},{}'.format(pos[0].latitude,pos[0].longitude)
    pic_propenty = { 'picture_url':photo.image.url,'geopostion':pos_on_map,'desc':desc}
    return render_to_response('photoapp/photo.html',pic_propenty)



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
    pos = PhotoPosition.objects.get_or_create(id=picture_id)
    # if pos[0].longitude or pos[0].latitude == 0.0:
    #     pos_on_map = 'отсутствует'
    pos_on_map = 'https://www.google.com/maps/@{},{}'.format(pos[0].longitude,pos[0].latitude)
    pic_propenty = {'host':host,'user':cur_user.user.username,'picture_url':photo.image.url,'geopostion':pos_on_map}
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
    desc = photo.description
    photo_view = PhotoViews()
    photo_view.save()
    photo.views.add(photo_view)
    pos = PhotoPosition.objects.get_or_create(id=picture_id)
    if photo.description is "null":
        desc = False

    if pos[0].longitude ==0.0 or pos[0].latitude == 0.0:
        pos_on_map = False
    else:
        pos_on_map = 'https://www.google.com/maps/place/{},{}'.format(pos[0].latitude,pos[0].longitude)
    pic_propenty = {'host':host,'user':cur_user.user.username,'picture_url':photo.image.url,'geopostion':pos_on_map,'desc':desc}
    return render_to_response('photoapp/photo.html',pic_propenty)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def delete_picture_from_unique_link(request,random_string,encript,key):
    picture_id = FileSerializer.decode_id(encript,key)
    cur_user = PhotoUser.objects.get(user__username=request.user)
    photo = Photo.objects.get(id = picture_id,user =cur_user)
    photo.delete()
    os.remove(photo.image.path)
    pic_propenty = {'user':cur_user.user.username,'picture_url':photo.image.url +' was be removed','url':request.path}
    return Response(pic_propenty, status=status.HTTP_200_OK)


