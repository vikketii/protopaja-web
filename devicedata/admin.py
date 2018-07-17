from django.contrib import admin

from .models import Device, Data

# Add models to admin interface
admin.site.register(Device)

admin.site.register(Data) # for testing
