from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # api
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),

    path('api/v1/', include('core.client.urls')),
    path('api/v1/', include('core.team.urls')), 
    path('api/v1/', include('core.invoice.urls')), 
]

'''
https://djoser.readthedocs.io/en/latest/getting_started.html
https://djoser.readthedocs.io/_/downloads/en/2.1.0/pdf/

available endpoints:
/users/
/token/login/ (Token Based Authentication)
/token/logout/ (Token Based Authentication)

http://127.0.0.1:8000/api/v1/users/
http://127.0.0.1:8000/api/v1/token/login/  >>> auth_token
http://127.0.0.1:8000/api/v1/token/logout/

test
curl -X POST http://127.0.0.1:8000/api/v1/token/login/ --data 'username=test@test.eu&password=test1234'
{"auth_token":"b6be377fe13914a5e385ee94ab0280e740e9c496"}
curl -X POST http://127.0.0.1:8000/api/v1/token/logout/ -H 'Authorization: Token b6be377fe13914a5e385ee94ab0280e740e9c496'

db.authtoken_token
create new record for each user at login
delete the token record for each user at logout

'''
