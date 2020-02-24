from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='/accounts/login/')
def CustomerList(request):	
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	return render(request, 'customer/customer_list.html', {'page_title': page_title, 'db_server': db_server})

@login_required(login_url='/accounts/login/')
def PerformanceInformation(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	return render(request, 'customer/performance_information.html', {'page_title': page_title, 'db_server': db_server})

@login_required(login_url='/accounts/login/')
def CustomerReport(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	return render(request, 'customer/customer_report.html', {'page_title': page_title, 'db_server': db_server})
