from django.db.models.base import ModelState
from django.shortcuts import render , redirect

from django.db import models
from django.contrib.auth.models import User
# from django.http import HttpResponse

# search in db
from django.db.models import Q

from .models import Room , Topic

#  flash messages
from django.contrib import messages

#  Import Form
from .forms import RoomForm , LoginForm

# Authenticate Users
from django.contrib.auth import authenticate , login , logout

# Create your views here.
def home(req):
    topic = Topic.objects.all()
    rooms = Room.objects.all()

    # print(req.user.is_authenticated)

    if req.GET.get('topic'):
        # print("topic avail")
        q = req.GET.get('topic')
        rooms = Room.objects.all() if not q else Room.objects.filter(topic__name=q)
        if not rooms : rooms = Room.objects.all()

    if req.GET.get("search"): 
        # print("query Avail")
        searchQuery = req.GET.get("search")
        rooms = Room.objects.filter(
            Q(topic__name__icontains=searchQuery) |
            Q(name__icontains=searchQuery) |
            Q(description__icontains=searchQuery)
        )
        if not rooms : rooms = Room.objects.all()
    room_count = rooms.count()
    context = {"rooms" : rooms , "topics" : topic , "room_count" : room_count}
    return render(req , 'base/home.html' , context)

def room(req , id):
    try:
        room = Room.objects.get(id=id)
    except Room.DoesNotExist:
        room = Room.objects.get(id=1)

    context = {"room" : room}
    # print(context["room"].description)
    return render(req , "base/room.html" , context)
 
def createRoom(req):
    form = RoomForm()
    if req.method == "POST":
        field = RoomForm(req.POST)
        if field.is_valid():
            field.save()
            return redirect("home")

    context = {'form' : form}
    return render (req , "base/room_form.html" , context)

def updateRoom(req , id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    if req.method == "POST":
        field = RoomForm(req.POST , instance=room)
        if field.is_valid():
            field.save()
            return redirect("home")

    context = {"form" : form}
    return render (req , "base/room_form.html" , context)

def deleteRoom(req , id):
    room = Room.objects.get(id=id)
    if req.method == "POST":
        room.delete()
        return redirect("home")
    context = {"id" : room.id , "name" : room.name}
    return render(req , "base/delete.html" ,context)

def LoginRegister(req):
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("pwd")
        try :
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(req, 'User Doesnot Exists')

        # if user exists authenticate the user
        user = authenticate(req , username=username , password=password)
        if user is not None:
            login(req , user)
            messages.success(req, 'Login Successfully')
            return redirect('home')
        else :
            messages.error(req, 'Username or Password Doesn\'t Exists')

    form = LoginForm()
    context = {"form" : form}
    return render(req , "base/login_register.html" , context)

def LogoutUser(req):
    try :
        logout(req)
    except :
        pass
    return redirect('home')