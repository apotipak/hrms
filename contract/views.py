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

    data = dict()
    contract = None
    cnt_id = 0
    cnt_id_is_existed = False
    
    form = ContractForm(request.POST)

    if request.method == 'POST':

    	if form.is_valid():    		
    		cnt_id = Decimal(request.POST['cus_id'] + request.POST.get('cus_brn').zfill(3) + request.POST.get('cus_vol').zfill(3))
    		contract = CusContract.objects.filter(cnt_id__exact=cnt_id)
    		
    		if contract:
    			cnt_id_is_existed = True
    			data['cnt_id'] = cnt_id
    			return JsonResponse(data)
    		
    	else:
    		form = ContractForm()		
    else:
    	form = ContractForm()

    return render(request, 'contract/contract_form.html', {'cnt_id':cnt_id, 'contract':contract, 'form':form, 'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})
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