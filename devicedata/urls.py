from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]



#urlpatterns = [
#    path('', views.IndexView.as_view(), name='index'),
#]