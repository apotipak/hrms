from django.urls import path
from . import views


urlpatterns = [
    path('', views.MonitoringList, name='monitoring-list'),    
]
