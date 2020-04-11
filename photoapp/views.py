from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from .serializers import FileSerializer
import json



class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)
      print(request.data)
      image = request.FILES["image"]
      if file_serializer.is_valid():
          print(request.FILES['image'])
          print(request.data['data'])
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)