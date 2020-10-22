from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [    
    path('', views.ScheduleMaintenance, name='schedule-maintenance'),
    url(r'^ajax/get_customer/$', views.ajax_get_customer, name='ajax_get_customer'),
]
