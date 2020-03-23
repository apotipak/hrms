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
    	data = dict()
    	form = ContractForm(request.POST)

    	if form.is_valid():
    		print("valid")
    		    		
    		cnt_id = Decimal(request.POST['cus_id'] + request.POST.get('cus_brn').zfill(3) + request.POST.get('cus_vol').zfill(3))
    		contract = CusContract.objects.filter(cnt_id__exact=cnt_id)
    		customer = Customer.objects.filter(cus_id__exact=request.POST.get('cus_id')).filter(cus_brn__exact=request.POST.get('cus_brn'))
    		
    		#data['errorlist'] = None

    		if contract:
    			data['error_message'] = "Existing contract"
    			data['html_form'] = render_to_string('contract/partial_contract_information.html', {'contract':contract, 'customer':customer})
    		else:
    			data['html_form'] = _("Not found")

    		#for field, errors in form.errors.items():
    		#	print('Field: {} Error: {}'.format(field, ','.join(errors)))

    		return JsonResponse(data)
    	else:    		
    		print("invalid..")
    		form = ContractForm(request.POST)

    		#for field, errors in form.errors.items():
    		#	print('Field: {} Error: {}'.format(field, ','.join(errors)))

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
	username = None
	if request.user.is_authenticated:
		username = request.user.username

	data['error_message'] = "Not found"
	print("json")

	return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def SearchContractNumber1(request):
	
	data = dict()
	username = None
	if request.user.is_authenticated:
		username = request.user.username

	if request.method == "POST":
		
		form = ContractForm(request.POST, username)		
				
		if form.is_valid():
			data['form_is_valid'] = True
			
			cnt_id = Decimal(request.POST['cus_id'] + request.POST.get('cus_brn').zfill(3) + request.POST.get('cus_vol').zfill(3))
			contract = CusContract.objects.filter(cnt_id__exact=cnt_id)
			customer = Customer.objects.filter(cus_id__exact=request.POST.get('cus_id')).filter(cus_brn__exact=request.POST.get('cus_brn'))

			if contract:

				data['error_message'] = "Existing contract"
				data['html_form'] = render_to_string('contract/partial_contract_information.html', {'contract':contract, 'customer':customer})
			else:
				data['error_message'] = "Not found"
		else:
			data['error_message'] = "Form error"

		return JsonResponse(data)

	else:
		form = ContractForm()