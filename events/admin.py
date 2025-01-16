from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(EventGroup)
admin.site.register(Media)
admin.site.register(ContactInfo)
