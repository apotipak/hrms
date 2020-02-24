from django.urls import path
from . import views


urlpatterns = [
    path('', views.CustomerList, name='customer-list'),
    path('performance-information/', views.PerformanceInformation, name='performance-information'),
    path('customer-report/', views.CustomerReport, name='customer-report'),
]
