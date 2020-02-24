from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='/accounts/login/')
def Index(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	return render(request, 'system/index.html', {'page_title': page_title, 'db_server': db_server})

@login_required(login_url='/accounts/login/')
def CompanyApprovePriority(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	return render(request, 'system/company_approve_priority.html', {'page_title': page_title, 'db_server': db_server})

@login_required(login_url='/accounts/login/')
def CompanyInformation(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	return render(request, 'system/company_information.html', {'page_title': page_title, 'db_server': db_server})
