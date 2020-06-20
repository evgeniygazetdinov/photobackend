from django.urls import path
from .views import (FileUploadView,get_picture_by_id, get_picture_from_unique_link, 
                    delete_picture_from_unique_link,by_short_link, change_photoposition,
                    change_photo_description)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('<str:generated_string>',by_short_link,name='short_unique'),
    path('upload/', FileUploadView.as_view()),
    #path('get_picture/<int:picture_id>/',get_picture_by_id)
    path('change_photoposition/',change_photoposition),
    path('change_description/',change_photo_description),
    path('getPicture/<str:random_string>/<str:encript>/<str:key>/<str:owner>/',get_picture_from_unique_link,name='unique'),
    path('deletePicture/<str:random_string>/<str:encript>/<str:key>/',delete_picture_from_unique_link,name='delete_unique')
]
