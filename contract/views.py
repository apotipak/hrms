from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .forms import ContractForm
from .models import CusContract


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

    data = dict()

    if request.method == 'POST':		
    	form = ContractForm(request.POST)
    	contract_number = request.POST['cus_id'] + request.POST.get('cus_brn') + request.POST.get('cus_vol')
    	data['contract_number'] = contract_number
    	data['message'] = "Success"
    else:
    	form = ContractForm()

    #return render(request, 'contract/contract_form.html', {'form': form})
    return render(request, 'contract/contract_form.html', {'form':form, 'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})
    #return JsonResponse(data)


@login_required(login_url='/accounts/login/')
def SearchContractNumber(request):  
    if request.method == "POST":
        
        #form = ContractForm(request.POST, user=request.user)
        form = ContractForm()

        if form.is_valid():
        	return HttpResponseRedirect('/?submitted=True')
        else:
        	return HttpResponseRedirect('/?submitted=False')

    else:
        form = ContractForm()