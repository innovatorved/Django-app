from django.db import models

# Import User Model
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User , on_delete=models.SET_NULL ,null=True)
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL ,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500 , null=True , blank=True)
    # participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']
    
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    room = models.ForeignKey(Room , on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.body[0:50]