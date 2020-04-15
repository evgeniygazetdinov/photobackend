from django.urls import path
from .views import FileUploadView,get_picture_by_id, unique_link
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('upload/', FileUploadView.as_view()),
    #path('get_picture/<int:picture_id>/',get_picture_by_id)
    path('get_picture/<str:random_string>/<str:key><str:encript>/',unique_link,name='unique')
]