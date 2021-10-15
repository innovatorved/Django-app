from django.db.models.base import ModelState
from django.shortcuts import render , redirect
from django.db import models
# from django.http import HttpResponse

from .models import Room

#  Import Form
from .forms import RoomForm


# Create your views here.
def home(req):
    rooms = Room.objects.all()
    context = {"rooms" : rooms}
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
