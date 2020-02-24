from django.urls import path
from . import views


urlpatterns = [
    path('', views.ContractList, name='contract-list'),    
]
