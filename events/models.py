from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class ContactInfo(models.Model):
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.phone

class EventGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class UserProfile(AbstractUser):
    fullname = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.username

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    group = models.ForeignKey(EventGroup, on_delete=models.SET_NULL, null=True, blank=True)
    contacts = models.ManyToManyField(ContactInfo)
    tagged_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tagged_events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Media(models.Model):
    file = models.FileField(upload_to='media/')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='media')
    def __str__(self):
        return f'{str(self.file)}'
