from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from django.contrib.auth.models import User # If used custom user model
from .serializers import UserSerializer, ChangePasswordSerializer, ChangeTimeDeleteSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny  # 
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,action
from .models import PhotoUser


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def check_user(request):
    cur_user = PhotoUser.objects.get(user__username=request.user)
    context = {'host' :(request.scheme +"://"+ request.get_host()),'user':request.user}
    serializer = UserSerializer(cur_user,context=context)
    return Response(serializer.data,status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def exists_user(request,username):
    user_exists = PhotoUser.objects.filter(user__username=username).exists()
    response = {}
    if user_exists:
        return Response({'username':'exists'},status.HTTP_200_OK)
    return Response({'username':'not exists'}, status=status.HTTP_400_BAD_REQUEST)



class CreateUserView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    model = PhotoUser
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          

class AllUserView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    queryset = PhotoUser.objects.all()



class ChangeTimeDeleteView(UpdateAPIView):
    serializer_class = ChangeTimeDeleteSerializer
    model = PhotoUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            # set_password also hashes the password that the user will get
            #self.object(serializer.data.get("new_time"))
            self.object.photouser.time_for_clear_messages = serializer.data.get("new_time")
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'current_time': self.object.photouser.time_for_clear_messages,
                'message': 'time updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = PhotoUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['delete'])
@permission_classes((IsAdminUser, ))
def delete_user(request, user_id):
    cur_user = PhotoUser
    if not (cur_user.objects.filter(id=user_id).exists()):
        response = {
                'status': 'USER NOT EXIST',
                'code': status.HTTP_400_BAD_REQUEST,
            }
        return Response(response,status.HTTP_400_BAD_REQUEST)
    User.objects.get(id=user_id).delete()
    response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'user with id: {} deleted'.format(user_id),
            }
    return Response(response,status.HTTP_200_OK)
  
  
  