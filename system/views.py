from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='/accounts/login/')
def Index(request):
	page_title = settings.PROJECT_NAME
	return render(request, 'system/index.html', {'page_title': page_title})

@login_required(login_url='/accounts/login/')
def Company(request):
	page_title = settings.PROJECT_NAME
	return render(request, 'system/company.html', {'page_title': page_title})

@login_required(login_url='/accounts/login/')
def CompanyInformation(request):
	page_title = settings.PROJECT_NAME
	return render(request, 'system/company_information.html', {'page_title': page_title})
