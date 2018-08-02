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

data = 0
val = 5
ajax_ids = {}


def index(request):
    latest_data_list = Data.objects.order_by('-collection_date')[:3]
    context = {
        'latest_data_list': latest_data_list,
    }
    return render(request, 'devicedata/index.html', context)

def charts(request):
    context = {}
    return render(request, 'devicedata/charts.html', context)



def data_table(request):

    # This returns 5 most latest data objects to the table
    # old -> new
    num = 5
    obs = Data.objects.all()
    val = obs.count()
    latest_data_list = Data.objects.order_by('collection_date')[val-num:val]
        
    context = {
        'latest_data_list': latest_data_list,
    }
    return render(request, 'devicedata/data_table.html', context)



def update_data_table(request):

    #This get new object that aren't added to the table yet
    if request.is_ajax() and request.method == 'GET':
        
        global new_data
        global data 
        global ajax_ids

        ajax_id = request.GET.get('ajax_id',None)
        #print('Ajax id: {}'.format(ajax_id))

        try:
            ajax_data = ajax_ids[ajax_id]

        except KeyError:
            ajax_ids[ajax_id] = data

        finally:
            if ajax_ids[ajax_id] < data:
                obs = Data.objects.all()
                val = obs.count()

                latest_data_list = Data.objects.order_by('collection_date')[val-1:val]
                #latest_data_list = Data.objects.last()
                context = {
                    'latest_data_list': latest_data_list,
                 }
    
                ajax_ids[ajax_id] = data
                return render(request, 'devicedata/update_data_table.html', context)
            else:
                context = {
                    'latest_data_list': Data.objects.none(),
                 }
                return render(request,'devicedata/update_data_table.html', context)
            


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
            device_id = request.POST['device_id']
            temp = int(request.POST['temperature'])
            humd = int(request.POST['humidity'])
            time = request.POST['collection_date']

            try:
                # try to find the correct object
                device = Device.objects.get(id = device_id)

            except Device.DoesNotExist:
                # a new slave module, create a new device object
                device = Device.objects.create(info=('Sensor station '+str(device_id)), id = device_id)
                #return HttpResponse(device)
            
            finally:
                #device = Device.objects.get(id = device_id)
                # create a new data object for the correct device
                data_object = Data.objects.create(device = device, collection_date = time, temperature = temp, humidity = humd)
                global data
                data += 1
                return HttpResponse(data_object)

    # incorrect username/password
    return HttpResponse('Unauthorized request')


# API data, in product should require authentication made with Django REST or something similar
def get_data(request):
    # Get data as dictionary, newest first and limit is 100
    data_list = [ Data.as_dict() for Data in Data.objects.order_by('-collection_date')[:100]]

    # To get safe=True, we would have to write our own serializer
    return JsonResponse(({'data': data_list}), safe=False)





def all_devices (request):
    devices = Device.objects.all()
   
    data_objects = []
   
    for i in range(0,len(devices)):
        data = Data.objects.select_related().filter(device = devices[i])
        latest_data = data.latest('collection_date')
        data_objects.append(latest_data)

    context = {
    'device_list' : devices,
    'data_objects' : data_objects
    } 
     
    return render(request, 'devicedata/all_devices.html', context)



def modify_devices(request):
    if request.method == 'GET':
        device_id = request.GET.get('device_id')
        
        devices = Device.objects.select_related().filter(id = device_id)
        
        data = Data.objects.select_related().filter(device = devices[0])
        global val
        latest_data = data.order_by('-collection_date')[:val]
        
        #devices = Device.objects.all()
        context = {
        'device' : devices,
        'latest_data_list' : latest_data,
        'id' : device_id
        }
        return render(request, 'devicedata/modify_devices.html', context)

def new_device_content(request):
            

    if request.method == 'GET' and request.is_ajax():
        devices = Device.objects.all()
        data_objects = []
       
        for i in range(0,len(devices)):
            data = Data.objects.select_related().filter(device = devices[i])
            latest_data = data.latest('collection_date')
            data_objects.append(latest_data)

        context = {
        'device_list' : devices,
        'data_objects' : data_objects
        } 
        return render(request, 'devicedata/update_all_devices.html', context)


def update_info(request):
    if request.method == 'POST':
        info = request.POST.get('info')
        #print(info)
        device_id = request.POST.get('device_id',None)
        devices = Device.objects.all()
        device = devices.select_related().filter(id=device_id)
        
        if device:
            # update user_notes
            device[0].user_notes = info
            device[0].save(update_fields=['user_notes'])
          
        # go back to modify devices page
        data = Data.objects.select_related().filter(device = device[0])
        global val
        latest_data = data.order_by('-collection_date')[:val]
        
        #devices = Device.objects.all()
        context = {
        'device' : devices,
        'latest_data_list' : latest_data,
        'id' : device_id
        }
        return render(request, 'devicedata/modify_devices.html', context)
        