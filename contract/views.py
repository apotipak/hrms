from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .forms import ContractForm
from .models import CusContract
from decimal import Decimal


@login_required(login_url='/accounts/login/')

@login_required(login_url='/accounts/login/')
def ContractList(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE	

	return render(request, 'contract/contract_list.html', {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})

@login_required(login_url='/accounts/login/')
def ContractCreate(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE
    
    if request.method == "POST":
    	form = ContractForm(request.POST)
    else:
    	form = ContractForm()

    return render(request, 'contract/contract_form.html', {'form':form, 'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})


@login_required(login_url='/accounts/login/')
def SearchContractNumber(request):
	
	data = dict()
	username = None
	if request.user.is_authenticated:
		username = request.user.username

	if request.method == "POST":
		
		form = ContractForm(request.POST, username)		
				
		if form.is_valid():
			cnt_id = Decimal(request.POST['cus_id'] + request.POST.get('cus_brn').zfill(3) + request.POST.get('cus_vol').zfill(3))		
			data['cnt_id'] = cnt_id


			contract = CusContract.objects.filter(cnt_id__exact=cnt_id)
			if contract:				
				data['error_message'] = "Found"

			else:
				data['error_message'] = "Not found"
		else:
			data['error_message'] = "Form error"

		return JsonResponse(data)

	else:
		form = ContractForm()