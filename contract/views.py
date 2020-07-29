from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .forms import ContractForm
from .models import CusContract
from customer.models import Customer
from decimal import Decimal


@login_required(login_url='/accounts/login/')

@login_required(login_url='/accounts/login/')
def ContractList1(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE	

	return render(request, 'contract/contract_list.html', {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})

@login_required(login_url='/accounts/login/')
def ContractList(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE
    
    if request.method == "POST":    	
    	data = dict()
    	form = ContractForm(request.POST)

    	if form.is_valid():

    		cnt_id = Decimal(request.POST['cus_id'] + request.POST.get('cus_brn').zfill(3) + request.POST.get('cus_vol').zfill(3))
    		contract = CusContract.objects.filter(cnt_id__exact=cnt_id)
    		customer = Customer.objects.filter(cus_id__exact=request.POST.get('cus_id')).filter(cus_brn__exact=request.POST.get('cus_brn'))

    		if customer:
    			#print(customer.cus_name_th)
    			for item in customer:
    				cus_name_th = item.cus_name_th
    				cus_name_en = item.cus_name_en
    			
    			data['cus_name_th'] = cus_name_th
    			data['cus_name_en'] = cus_name_en
    		else:
    			data['cus_name_th'] = "Company"
    			data['cus_name_en'] = _("Company")

    		if contract:    			
    			data['error_message'] = _("Existing contract")
    			data['html_form'] = render_to_string('contract/partial_contract_information.html', {'contract':contract, 'customer':customer})
    		else:
    			data['html_form'] = _("Contract Number not found.")
    			data['cus_name_th'] = _("Company")
    			data['cus_name_en'] = _("Company")

    		#print("valid")
    		#for field, errors in form.errors.items():
    		#	print('Field: {} Error: {}'.format(field, ','.join(errors)))

    		return JsonResponse(data)
    	else:    		    		
    		form = ContractForm(request.POST)

    		print("invalid..")
    		for field, errors in form.errors.items():
    			print('Field: {} Error: {}'.format(field, ','.join(errors)))

    		data['errorlist'] = form.errors
    		data['html_form'] = render_to_string('contract/partial_contract_information.html', {'form':form, 'errorlist':form.errors})

    		return JsonResponse(data)
    else:
    	form = ContractForm()
    	print("Form action GET");
    	return render(request, 'contract/contract_form.html', {'form':form, 'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})

@login_required(login_url='/accounts/login/')
def SearchContractNumber(request):
	
	data = dict()
	data['cus_name_th'] = ""
	data['cus_name_en'] = ""
	username = None

	if request.user.is_authenticated:
		username = request.user.username

	data['error_message'] = _("Contract Number not found1.")

	print("json")

	return JsonResponse(data)
