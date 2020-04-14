for shell

./manage.py shell_plus


for run 

./manage.py runserver


urls:



users
**************************


create/ |POST

you must be non-authorized 

send field username,password in body



check_current/ GET

you must be authorized



update/|PUT

send new_password,old_password in body;

you must be authorized



all/ |GET

you must be authorized as admin



delete_user/<pk> |PUT

you must be authorized as admin




photos
**************************

upload/ |POST

you must authorized send pic in body
