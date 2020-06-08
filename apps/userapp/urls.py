from django.urls import path
from .views import AllUserView, ChangePasswordView, CreateUserView, delete_user, check_user,exists_user, ChangeTimeDeleteView

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('check_current/', check_user),
    path('all/', AllUserView.as_view()),
    path('update/',ChangePasswordView.as_view()),
    path('update_delete_time/',ChangeTimeDeleteView.as_view()),
    path('delete_user/<int:user_id>',delete_user),
    path('exists/<str:username>/',exists_user),


]