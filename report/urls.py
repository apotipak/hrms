from django.urls import path
from . import views


urlpatterns = [
    path('', views.ReportList, name='report-list'),    
]
