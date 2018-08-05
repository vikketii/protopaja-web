from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('charts/', views.charts, name='charts'),
    path('send-json/', views.send_json, name='send-json'),
    path('api/data/', views.get_data, name='api-data'),
    path('device/<int:id>', views.device, name='history'),
    path('data_table/', views.data_table, name='data_table'),
    path('update_data_table/', views.update_data_table, name='update_data_table'),
    path('devices/all_devices/', views.all_devices, name='all_devices'),
    path('devices/modify_devices/', views.modify_devices, name='modify_devices'),
    path('new_device_content/', views.new_device_content, name='new_device_content'),
    path('update_info/', views.update_info, name='update_info'),
    path('send_string/', views.send_string, name='send_string'),
    path('update_select/', views.update_select, name='update_select'),
    path('devices_refresh/', views.devices_refresh, name='devices_refresh')
]
