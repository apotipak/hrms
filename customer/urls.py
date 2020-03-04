from django.urls import path
from . import views


urlpatterns = [
    path('', views.CustomerListView.as_view(), name='customer-list'),
    path('performance-information/', views.PerformanceInformation, name='performance-information'),
    path('customer-report/', views.CustomerReport, name='customer-report'),
]
