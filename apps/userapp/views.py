from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model # If used custom user model
from .serializers import UserSerializer,ChangePasswordSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # 
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated   
from rest_framework.decorators import api_view,permission_classes,action



class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
      permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class AllUserView(ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
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
    cur_user = get_user_model()

    if not (cur_user.objects.filter(id=user_id).exists()):
        response = {
                'status': 'USER NOT EXIST',
                'code': status.HTTP_400_BAD_REQUEST,
            }
        return Response(response,status.HTTP_400_BAD_REQUEST)
    cur_user.objects.get(id=user_id).delete()

    response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'user with id: {} deleted'.format(user_id),
            }
    return Response(response,status.HTTP_200_OK)