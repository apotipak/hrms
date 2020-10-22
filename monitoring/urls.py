from django.urls import path
from . import views


urlpatterns = [
    # path('', views.MonitoringList, name='monitoring-list'),
    path('', views.ScheduleMaintenance, name='schedule-maintenance'),
]
