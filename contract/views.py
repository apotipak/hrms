from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
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
from system.models import HrmsNewLog, TWagezone
from customer.models import CusMain, Customer
from decimal import Decimal
from django.utils import timezone
import datetime


def check_modified_field(table_name, primary_key, field_name, old_value, new_value, log_type, request):
    record = {}
    if old_value != new_value:
        record = {
            "log_table": table_name,
            "log_key": primary_key,
            "log_field": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "log_type": log_type,
            "log_by": request.user.first_name,
            "log_date": timezone.now(),
            "log_description": None,
        }
        return True, record
    else: 
        return False, record


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def ContractList(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE
    item_per_page = 25

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
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def ContractUpdate(request, pk):
    template_name = 'contract/contract_update.html'
    
    cus_contract = get_object_or_404(CusContract, pk=pk)
    # contract = CusContract.objects.raw("select con.cnt_id, con.cus_id, con.cus_brn from cus_contract con join customer cus on con.cus_id=cus.cus_id and con.cus_brn=cus.cus_brn and con.cnt_id='2771002001'") or None

    if cus_contract is not None:
        # print("wage_en = " + str(cus_contract.cnt_wage_id.wage_en))
        cusmain = CusMain.objects.filter(cus_id=cus_contract.cus_id).get()
        customer = Customer.objects.filter(cus_id=cus_contract.cus_id, cus_brn=cus_contract.cus_brn).get()
        cus_service = CusService.objects.filter(cnt_id=cus_contract.cnt_id).order_by('-srv_active')
    else:
        cusmain = []
        customer = []
        cus_contract = []
        cus_service = []
        
    if request.method == 'POST':
        print("debug method post")
        form = ContractUpdateForm(request.POST, instance=cus_contract)
    else:
        print("debug method get")
        form = ContractUpdateForm(instance=cus_contract)

    data = dict()
    form_is_valid = False
    update_message = ""

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
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
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


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def SaveContract(request):

    print("****************************")
    print("FUNCTION: save_contract")
    # print("****************************")

    template_name = 'contract/contract_update.html'
    response_data = {}
    modified_records = []

    if request.method == 'POST':
        print("SaveContract - Post method")
        
        # form = ContractUpdateForm(request.POST, instance=CusContract)
        form = ContractUpdateForm(request.POST)

        if form.is_valid():
            print("Form is valid")


            # Get values
            cnt_id = request.POST.get('cnt_id')
            # cus_brn
            # cus_vol
            cnt_active = request.POST.get('cnt_active')            
            cnt_doc_no = request.POST.get('cnt_doc_no')

            cnt_doc_date = request.POST.get('cnt_doc_date')
            if cnt_doc_date is not None:
                cnt_doc_date = datetime.datetime.strptime(cnt_doc_date, "%d/%m/%Y")

            cnt_eff_frm = request.POST.get('cnt_eff_frm')
            if cnt_eff_frm is not None:
                cnt_eff_frm = datetime.datetime.strptime(cnt_eff_frm, "%d/%m/%Y")

            cnt_eff_to = request.POST.get('cnt_eff_to')
            if cnt_eff_to is not None:
                cnt_eff_to = datetime.datetime.strptime(cnt_eff_to, "%d/%m/%Y")

            cnt_sign_frm = request.POST.get('cnt_sign_frm')
            if cnt_sign_frm is not None:
                cnt_sign_frm = datetime.datetime.strptime(cnt_sign_frm, "%d/%m/%Y")

            cnt_sign_to = request.POST.get('cnt_sign_to')
            if cnt_sign_to is not None:
                cnt_sign_to = datetime.datetime.strptime(cnt_sign_to, "%d/%m/%Y")

            cnt_apr_by = request.POST.get('cnt_apr_by_id')        
            cnt_guard_amt = request.POST.get('cnt_guard_amt')
            cnt_sale_amt = request.POST.get('cnt_sale_amt')
            cnt_wage_id = request.POST.get('cnt_wage_id')
            # cnt_zone = request.POST.get('cnt_zone_id')
            cnt_autoexpire = request.POST.get('cnt_autoexpire')
            cnt_then = request.POST.get('cnt_then')
            cnt_print = request.POST.get('cnt_print')
            cnt_new = request.POST.get('cnt_new')
            upd_date = timezone.now()
            upd_by = request.user.first_name
            upd_flag = 'E'

            print("")
            print("")
            print("----------- START ------------")
            print("cnt_active = " + str(cnt_active))
            print("cnt_doc_no = " + str(cnt_doc_no))
            print("cnt_doc_date = " + str(cnt_doc_date))
            print("cnt_eff_frm = " + str(cnt_eff_frm))
            print("cnt_eff_to = " + str(cnt_eff_to))
            print("cnt_sign_frm = " + str(cnt_sign_frm))
            print("cnt_sign_to = " + str(cnt_sign_to))
            print("cnt_apr_by = " + str(cnt_apr_by))
            print("cnt_guard_amt = " + str(cnt_guard_amt))
            print("cnt_sale_amt = " + str(cnt_sale_amt))
            print("cnt_wage_id = " + str(cnt_wage_id))
            print("cnt_autoexpire = " + str(cnt_autoexpire))
            print("cnt_then = " + str(cnt_then))
            print("cnt_print = " + str(cnt_print))
            print("cnt_new = " + str(cnt_new))
            print("upd_date  = " + str(upd_date))
            print("upd_by  = " + str(upd_by))
            print("upd_flag  = " + str(upd_flag))
            print("--------- END  ------------")
            print("")
            print("")

            # TODO
            try:
                modified_records = []
                field_is_modified_count = 0
                cuscontract = CusContract.objects.get(cnt_id=cnt_id)
                
                # New Report checkbox
                if (cnt_new is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "New Report Checkbox", cuscontract.cnt_new, cnt_new, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_new = cnt_new
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Customer checkbox
                if (cnt_print is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Customer Checkbox", cuscontract.cnt_print, cnt_print, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_print = cnt_print
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Auto expire
                if (cnt_autoexpire is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Auto Expired", int(cuscontract.cnt_autoexpire), int(cnt_autoexpire), "E", request)
                    if field_is_modified:
                        cuscontract.cnt_autoexpire = cnt_autoexpire
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Active
                if (cnt_active is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Active Status", int(cuscontract.cnt_active), int(cnt_active), "E", request)
                    if field_is_modified:
                        cuscontract.cnt_active = cnt_active
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Contract Ref.
                if (cnt_doc_no is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Contract Ref.", cuscontract.cnt_doc_no, cnt_doc_no, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_doc_no = cnt_doc_no
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Contract Date
                if (cnt_doc_date is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Contract Date", cuscontract.cnt_doc_date, cnt_doc_date, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_doc_date = cnt_doc_date
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1
                    
                # Effect Term From
                if (cnt_eff_frm is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Effect Term From", cuscontract.cnt_eff_frm, cnt_eff_frm, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_eff_frm = cnt_eff_frm
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Effect Term To
                if (cnt_eff_to is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Effect Term To", cuscontract.cnt_eff_to, cnt_eff_to, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_eff_to = cnt_eff_to
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Contract Term From
                if (cnt_sign_frm is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Contract Term From", cuscontract.cnt_sign_frm, cnt_sign_frm, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_sign_frm = cnt_sign_frm
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Contract Term To
                if (cnt_sign_to is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Contract Term To", cuscontract.cnt_sign_to, cnt_sign_to, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_sign_to = cnt_sign_to
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Wage Rate
                if (cnt_wage_id is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Wage Rate", int(cuscontract.cnt_wage_id_id), int(cnt_wage_id), "E", request)
                    if field_is_modified:
                        cuscontract.cnt_wage_id_id = int(cnt_wage_id)
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Guard Amount
                if (cnt_guard_amt is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Guard Amount", int(cuscontract.cnt_guard_amt), int(cnt_guard_amt), "E", request)
                    if field_is_modified:
                        cuscontract.cnt_guard_amt = int(cnt_guard_amt)
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Sale Amount
                if (cnt_sale_amt is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Sale Amount", float(cuscontract.cnt_sale_amt), float(cnt_sale_amt), "E", request)
                    if field_is_modified:
                        cuscontract.cnt_sale_amt = int(cnt_sale_amt)
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Authorized by
                if (cnt_apr_by is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Approved By", int(cuscontract.cnt_apr_by_id), int(cnt_apr_by), "E", request)
                    if field_is_modified:
                        cuscontract.cnt_apr_by_id = int(cnt_apr_by)
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1

                # Modified user
                if field_is_modified_count > 0:
                    cuscontract.upd_date = datetime.datetime.now()
                    cuscontract.upd_flag = 'E'
                    cuscontract.upd_by = request.user.first_name

                    cuscontract.save()

                    # History Log                    
                    for data in modified_records:
                        new_log = HrmsNewLog(
                            log_table = data['log_table'],
                            log_key = data['log_key'],
                            log_field = data['log_field'],
                            old_value = data['old_value'],
                            new_value = data['new_value'],
                            log_type = data['log_type'],
                            log_by = data['log_by'],
                            log_date = data['log_date'],
                            )
                        new_log.save()    
                        modified_records = []
                    # ./History Log                     

                    response_data['form_is_valid'] = True
                    response_data['result'] = "Saved success."
                    response_data['class'] = "bg-success"
                else:
                    response_data['form_is_valid'] = True
                    response_data['result'] = "Oops! Nothing to update."
                    response_data['class'] = "bg-warning"
               
            except CustomerOption.DoesNotExist:
                # Insert
                response_data['form_is_valid'] = True
                response_data['result'] = "Pending to save data"
                response_data['class'] = "bg-success"
        else:
            print("form is invalid")
            response_data['form_is_valid'] = False
            response_data['class'] = "bg-danger"
            response_data['message'] = "<b>Problem in cus_contract function</b>. Please inform IT department to support this case."

            if form.errors:
                for field in form:
                    for error in field.errors:
                        print(error)
                        response_data['message'] += error + "<br>"

                response_data['errors'] = form.errors
                response_data['class'] = "bg-danger"
            else:
                response_data['message'] = "<b>Problem in cus_contract function.</b>. Please inform IT department to support this case."
                response_data['class'] = "bg-danger"
            
    return JsonResponse(response_data)            


@login_required(login_url='/accounts/login/')
def get_wagerate_list(request):

    print("****************************")
    print("FUNCTION: get_wagerate_list")
    print("****************************")

    current_wagerate_id = request.POST.get('cnt_wage_id')
    print("current_wagerate_id : " + str(current_wagerate_id))

    item_per_page = 100

    if request.method == "POST":
        data = TDistrict.objects.filter('wage_id=current_wagerate_id')
        page = 1
        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))

    else:
        print("method get")
        if current_wagerate_id is not None:
            if current_wagerate_id != "":
                if current_wagerate_id.isnumeric():
                    print("debug1")
                    data = TWagezone.objects.all()
                else:
                    print("debug3")
                    data = TWagezone.objects.all()
            else:
                print("debug4")
                data = TWagezone.objects.all()
        else:
            print("debug5")
            data = TWagezone.objects.all()

        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page', 1) or 1
        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))   

    if current_page:
        current_page_number = current_page.number
        current_page_paginator_num_pages = current_page.paginator.num_pages

        pickup_dict = {}
        pickup_records=[]
        
        for d in current_page:            
            record = {
                "wage_id": d.wage_id,
                "wage_th": d.wage_th,
                "wage_en": d.wage_en,
                "wage_8hr": d.wage_8hr
            }
            pickup_records.append(record)

        response = JsonResponse(data={
            "success": True,
            "is_paginated": is_paginated,
            "page" : page,
            "next_page" : page + 1,
            "current_page_number" : current_page_number,
            "current_page_paginator_num_pages" : current_page_paginator_num_pages,
            "results": list(pickup_records)         
            })
        response.status_code = 200
        return response
    else:
        response = JsonResponse({"error": "there was an error"})
        response.status_code = 403
        return response

    return JsonResponse(data={"success": False, "results": ""})

