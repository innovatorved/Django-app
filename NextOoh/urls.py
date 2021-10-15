from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import path , include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('base.urls'))
]
