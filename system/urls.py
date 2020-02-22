from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index, name='index'),
    path('company-approve-priority', views.CompanyApprovePriority, name='company-approve-priority'),
    path('company-company-information', views.CompanyInformation, name='company-company-information'),
]
