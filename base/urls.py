from django.urls import path
from . import views


urlpatterns =[
    path('' , views.home , name="home"),
    path('room/<str:id>/' , views.room , name="room" ),
    path('create-room/' , views.createRoom , name="create-room"),
    path('update-room/<str:id>' , views.updateRoom , name="update-room"),
    path('delete-room/<str:id>' , views.deleteRoom  , name="delete-room"),
    path('login/' , views.LoginPage , name="login"),
    path('logout/' , views.LogoutUser , name="logout"),
    path('signup/' , views.RegisterPage , name="signup")
]
