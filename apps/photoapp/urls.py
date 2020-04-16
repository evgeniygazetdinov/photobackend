from django.urls import path
from .views import FileUploadView,get_picture_by_id
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('upload/', FileUploadView.as_view()),
    path('get_picture_by_id/<int:picture_id>/',get_picture_by_id)
]