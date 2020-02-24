from django.urls import path
from . import views


urlpatterns = [
    path('', views.DeductList, name='deduct-list'),    
]
