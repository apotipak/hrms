from django.urls import path
from . import views


urlpatterns = [
    path('', views.CustomerList, name='customer-list'),    
]
