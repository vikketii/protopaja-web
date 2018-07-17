from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Data

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'devicedata/index.html'
    context_object_name = 'latest_data_list'

    def get_queryset(self):
        """ Return the last three datapoints."""
        return Data.objects.order_by('-collection_date')[:3]


"""
def index(request):
    latest_data_list = Data.objects.order_by('-collection_date')[:5]
    context = {
        'latest_data_list': latest_data_list,
    }
    return render(request, 'devicedata/index.html', context)
"""