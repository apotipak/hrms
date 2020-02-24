from django.urls import path
from . import views


urlpatterns = [
    path('', views.PayrollList, name='payroll-list'),    
]
