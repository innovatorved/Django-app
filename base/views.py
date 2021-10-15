from django.shortcuts import render

# from django.http import HttpResponse


# Create your views here.
def home(req):return render(req , 'base/home.html')

rooms = [
    {"id" : 1 , "name" : "Music" },
    {"id" : 2 , "name" : "Tableau" },
    {"id" : 3 , "name" : "Python" }
]

def room(req):
    return render(req , "base/room.html" , {"rooms" : rooms})
