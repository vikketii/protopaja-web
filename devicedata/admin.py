from django.contrib import admin

from .models import Device, Data, Email, Alarm

# Add models to admin interface
admin.site.register(Device)
admin.site.register(Data)
admin.site.register(Email)
admin.site.register(Alarm)
