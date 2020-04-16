BACKEND FOR PHOTOHOSTING WITH CUSTOM LOGIC

**************************

>>>>>>> 
for shell

./manage.py shell_plus

**************************

>>>>>>> 
for run 

./manage.py runserver

**************************
**************************

urls:

**************************
users
**************************



**************************
create/ |POST

you must be non-authorized 

send field username,password in body



**************************
check_current/ GET

you must be authorized



**************************
update/|PUT

send new_password,old_password in body;

you must be authorized


**************************
all/ |GET

you must be authorized as admin



**************************
delete_user/<pk> |PUT

you must be authorized as admin


**************************


**************************
photo/
**************************

upload/ |POST

you must authorized send pic in body

**************************
get_picture_by_id/<id> |GET

you must be authorized

-with count your views

**************************

get_picture/<str:random_string>/<str:encript>/<str:key>/<str:owner>/ |GET


user must be authorized,posible not owner

**************************

delete_picture/<str:random_string>/<str:encript>/<str:key>/ |POST

user must be authorized as owner
