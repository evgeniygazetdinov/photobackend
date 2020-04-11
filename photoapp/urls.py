from django.urls import path
from .views import FileUploadView, CreateUserView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('upload/', FileUploadView.as_view()),
    path('create_user/', CreateUserView.as_view()),
]