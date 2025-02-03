from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class ContactInfo(models.Model):
    # add full name and address
    name = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField(null=True)

    def __str__(self):
        return self.phone

class EventGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class UserProfile(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)

    def __str__(self):
        return self.username

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    group = models.ForeignKey(EventGroup, on_delete=models.SET_NULL, null=True, blank=True)
    contacts = models.ManyToManyField(ContactInfo)
    tagged_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tagged_events')
    file = models.FileField(upload_to='media/', blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
