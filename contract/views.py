from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _
from .forms import ContractForm, ContractUpdateForm
from .models import CusContract, CusService
from customer.models import Customer
from decimal import Decimal


@login_required(login_url='/accounts/login/')
def ContractList(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE
    item_per_page = 5

    if request.method == "POST":    	
        data = dict()
        form = ContractForm(request.POST)
        cus_id = request.POST.get('cus_id')
        cus_brn = request.POST.get('cus_brn')
        cus_vol = request.POST.get('cus_vol')
        cnt_id = Decimal(request.POST['cus_id'] + request.POST.get('cus_brn').zfill(3) + request.POST.get('cus_vol').zfill(3))
        print("cnt_id_123 = " + str(cnt_id))

        if form.is_valid():
            rawsql = "select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn "
            contract_list = CusContract.objects.raw(rawsql + " where cus.cus_id="+cus_id+" order by con.cnt_active desc")
        else:    		    		
            form = ContractForm(request.POST)
            print("invalid..")
            for field, errors in form.errors.items():
            	print('Field: {} Error: {}'.format(field, ','.join(errors)))

            data['errorlist'] = form.errors
            data['html_form'] = render_to_string('contract/partial_contract_information.html', {'form':form, 'errorlist':form.errors})

            # return JsonResponse(data)
        page = 1
        paginator = Paginator(contract_list, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))            
    else:
        form = ContractForm()
        cus_id = request.GET.get('cus_id', '')
        cus_brn = request.GET.get('cus_brn', '')
        cus_vol = request.GET.get('cus_vol', '')

        # contract_list = CusContract.objects.all().order_by('-cnt_active','cus_id','cus_brn','cus_vol')
        contract_list = []
        contract_list = CusContract.objects.raw("select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn")

        # cus_no = Decimal(request.POST['cus_id'] + request.POST.get('cus_brn').zfill(3))
        # contract_list = CusContract.objects.select_related('customer').all()

        paginator = Paginator(contract_list, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page', '1') or 1

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))

    print("cus_id = " + str(cus_id))
    print("cus_brn = " + str(cus_brn))
    print("cus_vol = " + str(cus_vol))

    context = {
        'page_title': page_title, 
        'db_server': db_server, 'today_date': today_date,
        'project_name': project_name, 
        'project_version': project_version,         
        'contract_list': contract_list,
        'current_page': current_page,
        'is_paginated': is_paginated,
        'form': form,
        'cus_id': cus_id,
        'cus_brn': cus_brn,
        'cus_vol': cus_vol
    }

    return render(request, 'contract/contract_list.html', context)


@login_required(login_url='/accounts/login/')
def ContractUpdate(request, pk):
    template_name = 'contract/contract_update.html'
    
    cus_contract = get_object_or_404(CusContract, pk=pk)

    #contract = CusContract.objects.raw("select con.cnt_id, con.cus_id, con.cus_brn from cus_contract con join customer cus on con.cus_id=cus.cus_id and con.cus_brn=cus.cus_brn and con.cnt_id='2771002001'") or None
    if cus_contract:
        print(cus_contract.cnt_wage_id.wage_en)
        customer = Customer.objects.filter(cus_id=cus_contract.cus_id, cus_brn=cus_contract.cus_brn).get()
        cus_service = CusService.objects.filter(cnt_id=cus_contract.cnt_id).order_by('-srv_active')
    else:
        customer = []
        cus_contract = []
        cus_service = []
        

    '''
    if cus_contract:
        cnt_id = cus_contract.cnt_id
        cus_id = cus_contract.cus_id
        cus_brn = cus_contract.cus_brn
    else:
        cnt_id = None
        cus_id = None
        cus_brn = None

    print("cnt_id = " + str(cnt_id))
    print("cus_id = " + str(cus_id))
    print("cus_brn = " + str(cus_brn))
    '''

    if request.method == 'POST':
        form = ContractUpdateForm(request.POST, instance=cus_contract)
    else:
        form = ContractUpdateForm(instance=cus_contract)

    data = dict()
    form_is_valid = False
    update_message = ""

    '''
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            
            if request.user.is_superuser:
                obj.upd_by = 'Superuser'
            else:
                obj.upd_by = request.user.first_name

            if obj.upd_flag == 'A':
                obj.upd_flag = 'E'

            obj.upd_date = timezone.now()

            obj.save()
            form_is_valid = True            
            update_message = "ทำรายการสำเร็จ"
        else:
            form_is_valid = False
            update_message = "ไม่สามารถทำรายการได้..!"
    '''

    context = {
        'page_title': settings.PROJECT_NAME,
        'today_date': settings.TODAY_DATE,
        'project_version': settings.PROJECT_VERSION,
        'db_server': settings.DATABASES['default']['HOST'],
        'project_name': settings.PROJECT_NAME,
        'form': form, 
        'contract': cus_contract,        
        'customer': customer,
        'cus_service': cus_service,
        'request': request,
        'form_is_valid': form_is_valid,
        'update_message': update_message,
    }
    return render(request, template_name, context)


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
