from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    # path('', views.CustomerListView.as_view(), name='customer-list'),
    # path('', views.CustomerList, name='customer-list'),
    
    # path('', views.CustomerList, name='customer-list'),
    url(r'^$', views.CustomerList, name='customer-list'),
    #url(r'^/$', views.CustomerList, name='customer-list'),

    path('customer/create', views.CustomerCreate, name='customer-create'),
    
    # path('customer/<int:pk>/update', views.CustomerUpdate, name='customer-update'),
    path('customer/<int:pk>/update', views.CusMainUpdate, name='cus-main-update'),

   	path('customer/<int:pk>/delete', views.CustomerDelete, name='customer-delete'),
]

urlpatterns += [
  path('performance-information/', views.PerformanceInformation, name='performance-information'),
	path('customer-report/', views.CustomerReport, name='customer-report'),
]

urlpatterns += [    
  url(r'^ajax/get_district_list/$', views.get_district_list, name='get_district_list'),
]

