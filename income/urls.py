from django.urls import path
from . import views


urlpatterns = [
    path('', views.IncomeDeductList, name='income-deduct-list'),    
]
