from django.urls import path
from . import views


urlpatterns = [
    # path('', views.CustomerListView.as_view(), name='customer-list'),
    path('', views.CustomerList, name='customer-list'),
    path('customer/create', views.CustomerCreate, name='customer-create'),
    path('customer/<int:pk>/update', views.CustomerUpdate, name='customer-update'),
   	path('customer/<int:pk>/delete', views.CustomerDelete, name='customer-delete'),
]

urlpatterns += [
   	path('performance-information/', views.PerformanceInformation, name='performance-information'),
	path('customer-report/', views.CustomerReport, name='customer-report'),
]
