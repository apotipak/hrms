from django.urls import path
from . import views


urlpatterns = [
    path('', views.EmployeeList, name='employee-list'),
]
