from django.db.models.base import ModelState
from django.shortcuts import render , redirect

from django.db import models
from django.contrib.auth.models import User
# from django.http import HttpResponse

from django.http import HttpResponse

# search in db
from django.db.models import Q

from .models import Room , Topic , Message

#  flash messages
from django.contrib import messages

#  Import Form
from .forms import RoomForm , LoginForm , CreateUser

# Authenticate Users
from django.contrib.auth import authenticate , login , logout

# restrict  user to create room if they not logged in by Decorators
from django.contrib.auth.decorators import login_required

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

    if req.method == "POST":
        msg = req.POST.get("body")
        message = Message.objects.create(
            user = req.user,
            room = room,
            body = msg
        )
        message.save()
        return redirect('room' , id=room.id)
    # extract set of message related to this room
    room_msg = room.message_set.all().order_by('-created')
    context = {"room" : room , "room_msg" : room_msg} 
    # print(context["room"].description)
    return render(req , "base/room.html" , context)

 
@login_required(login_url='login') # if not logged in redirect to home paddge
def createRoom(req):
    form = RoomForm()
    if req.method == "POST":
        field = RoomForm(req.POST)
        if field.is_valid():
            field.save()
            return redirect("home")

    context = {'form' : form}
    return render (req , "base/room_form.html" , context)

@login_required(login_url='login') # if not logged in redirect to home paddge
def updateRoom(req , id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if req.user != room.host:
        return HttpResponse("User Restricted here")

    if req.method == "POST":
        field = RoomForm(req.POST , instance=room)
        if field.is_valid():
            field.save()
            return redirect("home")

    context = {"form" : form}
    return render (req , "base/room_form.html" , context)

@login_required(login_url='login') # if not logged in redirect to home paddge
def deleteRoom(req , id):
    room = Room.objects.get(id=id)

    if req.user != room.host:
        return HttpResponse("User Restricted here")

    if req.method == "POST":
        room.delete()
        return redirect("home")
    context = {"id" : room.id , "name" : room.name}
    return render(req , "base/delete.html" ,context)

def LoginPage(req):
    if req.user.is_authenticated :
        messages.info(req, 'User Already Logged In Please logged out to Logged In with Different Account')
        return redirect("home")
    if req.method == "POST":
        username = req.POST.get("username").lower()
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
    context = {
        "form" : form,
        "page" : "login"
    }
    return render(req , "base/login_register.html" , context)

def LogoutUser(req):
    if not req.user.is_authenticated :
        messages.info(req, 'User Already Loged Out')
        return redirect("home")
    try :
        logout(req)
    except :
        pass
    messages.success(req, 'Logout Successfully')
    return redirect('home')

def RegisterPage(req):
    if req.method == 'POST':
        form = CreateUser.form(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(req, 'Successfully user created')
            login(req , user)
            messages.success(req, 'User Logged In')
            return redirect('home')
        else:
            print(form.error_messages)
            messages.error(req, 'Error in Signup')

    context = {
        "form" : CreateUser.form(),
        "page" : "SignUp"
    }
    return render(req , "base/login_register.html", context)