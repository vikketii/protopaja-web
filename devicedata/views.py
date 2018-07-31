from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import generic

from .models import Data, Device

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

"""
class IndexView(generic.ListView):
    template_name = 'devicedata/index.html'
    context_object_name = 'latest_data_list'

    def get_queryset(self):
        # Return the last three datapoints.
        return Data.objects.order_by('-collection_date')[:3]
"""

def index(request):
    latest_data_list = Data.objects.order_by('-collection_date')[:3]
    context = {
        'latest_data_list': latest_data_list,
    }
    return render(request, 'devicedata/index.html', context)

def charts(request):
    context = {}
    return render(request, 'devicedata/charts.html', context)


# not requiring csrf
@csrf_exempt

# requires login and redirects to /accounts/login/ if not logged in
#@login_required
def send_json(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #authentication succesfull
            login(request, user)
            #response = 'POST request has arrived. Here is the data: {0}' .format(request.body)
            
            # These need to be integers as their matching fields
            # are defined as IntegerFields in models.py
            device_id = request.POST['device']
            temp = int(request.POST['temperature'])
            humd = int(request.POST['humidity'])
            time = request.POST['collection_date']

            try:
                # try to find the correct object
                device = Device.objects.get(id = device_id)

            except Device.DoesNotExist:
                # a new slave module, create a new device object
                device = Device.objects.create(info=('Sensor station '+str(device_id)), id = device_id)
                return HttpResponse(device)
            
            finally:
                #device = Device.objects.get(id = device_id)
                # create a new data object for the correct device
                data_object = Data.objects.create(device = device, collection_date = time, temperature = temp, humidity = humd)
                return HttpResponse(data_object)

    # incorrect username/password
    return HttpResponse('Unauthorized request')


# API data, in product should require authentication made with Django REST or something similar
def get_data(request):
    # Get data as dictionary, newest first and limit is 100
    data_list = [ Data.as_dict() for Data in Data.objects.order_by('-collection_date')[:100]]

    # To get safe=True, we would have to write our own serializer
    return JsonResponse(({'data': data_list}), safe=False)