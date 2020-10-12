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
from .forms import ContractForm, ContractUpdateForm, ContractCreateForm
from .models import CusContract, CusService
from system.models import HrmsNewLog, TWagezone, ComRank, TShift
from customer.models import CusMain, Customer, CusBill
from decimal import Decimal
from django.utils import timezone
import datetime
from django.utils import formats
from django.db.models import Max
from hrms.settings import MEDIA_ROOT
from docxtpl import DocxTemplate
from django.views.static import serve
import mimetypes
import os
from django.conf import settings
from wsgiref.util import FileWrapper
from django.http import HttpResponse, Http404
from django.db import connection


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
            "log_date": datetime.datetime.now(),
            "log_description": None,
        }
        return True, record
    else: 
        return False, record


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def contract_create(request):

    template_name = 'contract/contract_create.html'
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    today_date = settings.TODAY_DATE
    response_data = dict()

    if request.method == "POST":
        print("POST: contract_create()")
        if form.is_valid():          
            contract_form = ContractCreateForm(request.POST, user=request.user)
            response_data['form_is_valid'] = True            
        else:            
            response_data['form_is_valid'] = False

        return JsonResponse(response_data)     
    else:
        print("GET: contract_create()")
        contract_create_form = ContractCreateForm()
        
    return render(request, 'contract/contract_create.html', 
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'contract_create_form': contract_create_form,
        })


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def get_cus_main(request):
    cus_id = request.POST.get('cus_id')    

    if cus_id is not None:
        try:                
            cusmain = CusMain.objects.filter(cus_id__exact=cus_id).get()
            cus_name_th = cusmain.cus_name_th
            cus_name_en = cusmain.cus_name_en

            response = JsonResponse(data={
                "success": True,
                "class": "bg_danger",
                "message": "",
                "is_existed": True,
                "cus_name_th": cus_name_th,
                "cus_name_en": cus_name_en,
            })
            response.status_code = 200
            return response
        except CusMain.DoesNotExist:
            response = JsonResponse(data={
                "success": True,
                "class": "bg_danger",
                "message": "",
                "is_existed": False,
                "cus_name_th": "",
                "cus_name_en": "",
            })
            response.status_code = 200
            return response            

    response = JsonResponse(data={
        "success": True,
        "class": "bg_danger",
        "message": "",
        "is_existed": True,
        "cus_name_th": "",
        "cus_name_en": "",
    })
    return response


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def get_customer(request):
    cus_id = request.POST.get('cus_id')
    cus_brn = request.POST.get('cus_brn')

    if cus_id is not None and cus_brn is not None:
        try:
            customer = Customer.objects.filter(cus_id=cus_id, cus_brn=cus_brn).get()
            cus_name_th = customer.cus_name_th
            cus_sht_th = customer.cus_sht_th
            cus_add1_th = customer.cus_add1_th
            cus_add2_th = customer.cus_add2_th
            cus_subdist_th = customer.cus_subdist_th

            cus_name_en = customer.cus_name_en
            cus_sht_en = customer.cus_sht_en
            cus_add1_en = customer.cus_add1_en
            cus_add2_en = customer.cus_add2_en
            cus_subdist_en = customer.cus_subdist_en

            cus_zip = customer.cus_zip
            cus_district_id = customer.cus_district_id
            cus_district_th = customer.cus_district.dist_th
            cus_district_en = customer.cus_district.dist_en
            cus_city_th = customer.cus_city.city_th
            cus_city_en = customer.cus_city.city_en
            cus_country_th = customer.cus_country.country_th
            cus_country_en = customer.cus_country.country_en
            
            cus_tel = customer.cus_tel
            cus_fax = customer.cus_fax
            cus_email = customer.cus_email
            
            site_contact_id_th = customer.site_contact_id
            site_contact_con_fname_th = customer.site_contact.con_fname_th
            site_contact_con_lname_th = customer.site_contact.con_lname_th
            site_contact_con_position_th = customer.site_contact.con_position_th

            site_contact_id_en = customer.site_contact_id
            site_contact_con_fname_en = customer.site_contact.con_fname_en
            site_contact_con_lname_en = customer.site_contact.con_lname_en
            site_contact_con_position_en = customer.site_contact.con_position_en
            
            site_contact_cus_zone_id = customer.cus_zone_id
            site_contact_cus_zone_th = customer.cus_zone.zone_th
            site_contact_cus_zone_en = customer.cus_zone.zone_en

            response = JsonResponse(data={
                # TH
                "success": True,
                "class": "bg_danger",
                "message": "",
                "is_existed": True,
                "cus_name_th": cus_name_th,
                "cus_sht_th": cus_sht_th,
                "cus_add_th": cus_add1_th + " " + cus_add2_th,
                "cus_subdist_th": cus_subdist_th,
                "cus_zip_th": cus_zip,
                "cus_district_id_th": cus_district_id,
                "cus_district_th": cus_district_th,
                "cus_city_th": cus_city_th,
                "cus_country_th": cus_country_th,
                "site_contact_id_th": site_contact_id_th,
                "site_contact_con_th": str(site_contact_id_th) + " | " + str(site_contact_con_fname_th) + " " + str(site_contact_con_lname_th),
                "site_contact_con_position_th": site_contact_con_position_th,
                
                # EN
                "cus_name_en": cus_name_en,
                "cus_sht_en": cus_sht_en,
                "cus_add_en": cus_add1_en + " " + cus_add2_en,
                "cus_subdist_en": cus_subdist_en,
                "cus_zip_en": cus_zip,
                "cus_district_id_en": cus_district_id,
                "cus_district_en": cus_district_en,
                "cus_city_en": cus_city_en,
                "cus_country_en": cus_country_en,                                                            
                "site_contact_id_en": site_contact_id_en,
                "site_contact_con_en": str(site_contact_id_en) + " | " + str(site_contact_con_fname_en) + " " + str(site_contact_con_lname_en),
                "site_contact_con_position_en": site_contact_con_position_en,                

                "cus_tel": cus_tel,
                "cus_fax": cus_fax,
                "cus_email": cus_email,
                "cus_zone_id": site_contact_cus_zone_id,
                "cus_zone_th": site_contact_cus_zone_th,
                "cus_zone_en": site_contact_cus_zone_en,
            })
            response.status_code = 200
            return response
        except Customer.DoesNotExist:            
            response = JsonResponse(data={
                "success": True,
                "class": "bg_danger",
                "message": "",
                "is_existed": False,
                "cus_name_th": "",
                "cus_sht_th": "",
                "cus_add1_th": "",
                "cus_add2_th": "",
                "cus_subdist_th": "",
                "cus_subdist_en": "",
                "cus_name_en": "",
                "cus_sht_en": "",
                "cus_add1_en": "",
                "cus_add2_en": "",
                "cus_subdist_en": "",
                "cus_zip": "",
                "cus_district": "",
                "site_contact": "",
            })
            response.status_code = 200
            return response            

    response = JsonResponse(data={
        "success": True,
        "class": "bg_danger",
        "message": "",
        "is_existed": False,
        "cus_name_th": "",
        "cus_name_en": "",
    })
    return response


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def get_cus_contract(request):
    cus_id = request.POST.get('cus_id')
    cus_brn = request.POST.get('cus_brn')
    cus_vol = request.POST.get('cus_vol')    
    cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
    
    # Double check if customer is existed
    try:                
        customer = Customer.objects.filter(cus_id=cus_id, cus_brn=cus_brn).get()
        if cnt_id is not None:
            try:                 
                cuscontract = CusContract.objects.filter(cnt_id=cnt_id).get()

                cnt_active = cuscontract.cnt_active
                if cnt_active:
                    cnt_active = 1
                else:
                    cnt_active = 0                

                cnt_doc_no = cuscontract.cnt_doc_no                
                
                if cuscontract.cnt_doc_date is not None:
                    cnt_doc_date = cuscontract.cnt_doc_date.strftime("%d/%m/%Y")
                else:
                    cnt_doc_date = datetime.datetime.now().strftime("%d/%m/%Y")
                
                if cuscontract.cnt_eff_frm is not None:
                    cnt_eff_frm = cuscontract.cnt_eff_frm.strftime("%d/%m/%Y")
                else:
                    cnt_eff_frm = datetime.datetime.now().strftime("%d/%m/%Y")

                if cuscontract.cnt_eff_to is not None:
                    cnt_eff_to = cuscontract.cnt_eff_to.strftime("%d/%m/%Y")
                else:
                    cnt_eff_to = datetime.datetime.now().strftime("%d/%m/%Y")

                if cuscontract.cnt_sign_frm is not None:
                    cnt_sign_frm = cuscontract.cnt_sign_frm.strftime("%d/%m/%Y")
                else:
                    cnt_sign_frm = datetime.datetime.now().strftime("%d/%m/%Y")

                if cuscontract.cnt_sign_to is not None:
                    cnt_sign_to = cuscontract.cnt_sign_to.strftime("%d/%m/%Y")
                else:
                    cnt_sign_to = datetime.datetime.now().strftime("%d/%m/%Y")

                cnt_wage_id = cuscontract.cnt_wage_id_id
                cnt_wage_text = str(cuscontract.cnt_wage_id_id) + "  |  " + str(cuscontract.cnt_wage_id.wage_en) + "    " + str(cuscontract.cnt_wage_id.wage_8hr)
                cnt_guard_amt = cuscontract.cnt_guard_amt
                cnt_sale_amt = cuscontract.cnt_sale_amt
                cnt_new = cuscontract.cnt_new
                cnt_print = cuscontract.cnt_print
                cnt_autoexpire = cuscontract.cnt_autoexpire

                # print("cnt_guard_amt = " + str(cnt_guard_amt))

                if cnt_autoexpire:
                    cnt_autoexpire = 1
                else:
                    cnt_autoexpire = 0

                # Check if cus_service is existed
                # start
                cus_service_list = []
                pickup_record = []
                try:                 
                    cus_service_list = CusService.objects.all().filter(cnt_id=cnt_id)
                    for item in cus_service_list:
                        record = {
                            "srv_id": item.srv_id,
                        }
                        pickup_record.append(record)
                except CusService.DoesNotExist:
                    cus_service_list = []        
                # end

                response = JsonResponse(data={
                    "success": True,
                    "class": "bg_danger",
                    "message": "",
                    "is_existed": True,
                    "cnt_id": cnt_id,
                    "cnt_active": cnt_active,
                    "cnt_doc_no": cnt_doc_no,
                    "cnt_doc_date": cnt_doc_date,
                    "cnt_eff_frm": cnt_eff_frm,
                    "cnt_eff_to": cnt_eff_to,
                    "cnt_sign_frm": cnt_sign_frm,
                    "cnt_sign_to": cnt_sign_to,
                    "cnt_wage_id": cnt_wage_id,
                    "cnt_wage_text": cnt_wage_text,
                    "cnt_guard_amt": cnt_guard_amt,
                    "cnt_sale_amt": cnt_sale_amt,
                    "cnt_new": cnt_new,
                    "cnt_print": cnt_print,
                    "cnt_autoexpire": cnt_autoexpire,
                    "cus_service_list": list(pickup_record)
                })

                response.status_code = 200
                return response
            except CusContract.DoesNotExist:
                response = JsonResponse(data={
                    "success": True,
                    "class": "bg_danger",
                    "message": "",
                    "is_existed": False,
                    "customer_not_existed": False,
                    "cnt_doc_no": "",
                })
                response.status_code = 200
                return response            
    except Customer.DoesNotExist:
        response = JsonResponse(data={
            "success": True,
            "class": "bg_danger",
            "message": "",
            "is_existed": False,
            "customer_not_existed": True,
            "cnt_doc_no": "",
        })
        response.status_code = 200
        return response  
        
    response = JsonResponse(data={
        "success": True,
        "class": "bg_danger",
        "message": "",
        "is_existed": False,
        "cnt_doc_no": "",
    })
    return response


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def ContractList(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE
    item_per_page = 15

    if request.method == "POST":    	
        data = dict()
        form = ContractForm(request.POST)
        cus_id = request.POST.get('cus_id')

        if form.is_valid():            
            try:
                int(cus_id)
                if cus_id is not None or cus_id != '':
                    rawsql = "select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn "
                    contract_list = CusContract.objects.raw(rawsql + " where cus.cus_id="+cus_id+ " and con.upd_flag!='D'" + " order by con.cnt_active desc")                    
                else:
                    contract_list = []
                    contract_list = CusContract.objects.raw("select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn where con.upd_flag!='D'")
            except ValueError:
                contract_list = []
                contract_list = CusContract.objects.raw("select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn where con.upd_flag!='D'")

        else:    		    		
            contract_list = []
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
        contract_list = CusContract.objects.raw("select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn where con.upd_flag!='D'")

        # cus_no = Decimal(request.POST['cus_id'] + request.POST.get('cus_brn').zfill(3))
        # contract_list = CusContract.objects.select_related('customer').all()

        paginator = Paginator(contract_list, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page', '1') or 1

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))

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
        # 'cus_brn': cus_brn,
        # 'cus_vol': cus_vol
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
def UpdateContract(request):

    print("****************************")
    print("FUNCTION: update_contract")
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
            cnt_active = request.POST.get('cnt_active')            
            cnt_doc_no = request.POST.get('cnt_doc_no')

            cnt_doc_date = request.POST.get('cnt_doc_date')
            if cnt_doc_date is not None and cnt_doc_date != "":
                cnt_doc_date = datetime.datetime.strptime(cnt_doc_date, "%d/%m/%Y")
            else:
                cnt_doc_date = None

            cnt_eff_frm = request.POST.get('cnt_eff_frm')
            if cnt_eff_frm is not None and cnt_eff_frm != "":
                cnt_eff_frm = datetime.datetime.strptime(cnt_eff_frm, "%d/%m/%Y")
            else:
                cnt_eff_frm = None

            cnt_eff_to = request.POST.get('cnt_eff_to')
            if cnt_eff_to is not None and cnt_eff_to != "":
                cnt_eff_to = datetime.datetime.strptime(cnt_eff_to, "%d/%m/%Y")
            else:
                cnt_eff_to = None

            cnt_sign_frm = request.POST.get('cnt_sign_frm')
            if cnt_sign_frm is not None and cnt_sign_frm != "":
                cnt_sign_frm = datetime.datetime.strptime(cnt_sign_frm, "%d/%m/%Y")
            else:
                cnt_sign_frm = None

            cnt_sign_to = request.POST.get('cnt_sign_to')
            if cnt_sign_to is not None and cnt_sign_to != "":
                cnt_sign_to = datetime.datetime.strptime(cnt_sign_to, "%d/%m/%Y")
            else:
                cnt_sign_to = None

            cnt_apr_by = request.POST.get('cnt_apr_by_id')            
            cnt_guard_amt = request.POST.get('cnt_guard_amt')
            cnt_sale_amt = request.POST.get('cnt_sale_amt')
            cnt_wage_id = request.POST.get('cnt_wage_id')
            # cnt_zone = request.POST.get('cnt_zone_id')
            cnt_autoexpire = request.POST.get('cnt_autoexpire')
            cnt_then = request.POST.get('cnt_then')
            cnt_print = request.POST.get('cnt_print')
            cnt_new = request.POST.get('cnt_new')
            # upd_date = timezone.now()
            upd_date = datetime.datetime.now()
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

                # Print Options radio
                if (cnt_then is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Print Options", cuscontract.cnt_then, cnt_then, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_then = cnt_then
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
                if (cnt_doc_date is not None and cnt_doc_date != ""):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Contract Date", cuscontract.cnt_doc_date, cnt_doc_date, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_doc_date = cnt_doc_date
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1
                else:
                    cuscontract.cnt_doc_date = None
                    
                # Effect Term From
                if (cnt_eff_frm is not None and cnt_eff_frm != ""):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Effect Term From", cuscontract.cnt_eff_frm, cnt_eff_frm, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_eff_frm = cnt_eff_frm
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1
                else:
                    cuscontract.cnt_eff_frm = None

                # Effect Term To
                print("aaaaaaa")
                if (cnt_eff_to is not None and cnt_eff_to != ""):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Effect Term To", cuscontract.cnt_eff_to, cnt_eff_to, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_eff_to = cnt_eff_to
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1
                else:
                    cuscontract.cnt_eff_to = None

                # Contract Term From
                if (cnt_sign_frm is not None and cnt_sign_frm != ""):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Contract Term From", cuscontract.cnt_sign_frm, cnt_sign_frm, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_sign_frm = cnt_sign_frm
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1
                else:
                    cuscontract.cnt_sign_frm = None

                # Contract Term To
                if (cnt_sign_to is not None and cnt_sign_to != ""):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Contract Term To", cuscontract.cnt_sign_to, cnt_sign_to, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_sign_to = cnt_sign_to
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1
                else:
                    cuscontract.cnt_sign_to = None

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
                    response_data['result'] = "Sorry, nothing to update."
                    response_data['class'] = "bg-warning"
               
            except CusContract.DoesNotExist:
                # Insert
                response_data['form_is_valid'] = True
                response_data['result'] = "Pending to save data"
                response_data['class'] = "bg-success"

                '''
                c = CusContract(
                    cnt_id = cnt_id,
                    cus_id = cus_id,
                    cus_brn = cus_brn,
                    cus_vol = cus_vol,
                )
                c.save()                
                '''
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
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def CreateContract(request):

    print("****************************")
    print("FUNCTION: create_contract")
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
            cus_id = request.POST.get('cus_id')
            cus_brn = request.POST.get('cus_brn')
            cus_vol = request.POST.get('cus_vol')
            cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
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
            if cnt_guard_amt == "":
                cnt_guard_amt = 0
            else:
                cnt_guard_amt = int(cnt_guard_amt)

            cnt_sale_amt = request.POST.get('cnt_sale_amt')
            if cnt_sale_amt == "":
                cnt_sale_amt = 0
            else:
                cnt_sale_amt = float(cnt_sale_amt)

            cnt_wage_id = request.POST.get('cnt_wage_id')
            # cnt_zone = request.POST.get('cnt_zone_id')
            cnt_autoexpire = request.POST.get('cnt_autoexpire')
            cnt_then = request.POST.get('cnt_then')
            cnt_print = request.POST.get('cnt_print')
            cnt_new = request.POST.get('cnt_new')
            # upd_date = timezone.now()
            upd_date = datetime.datetime.now()
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
                    response_data['result'] = "Sorry, nothing to update."
                    response_data['class'] = "bg-warning"
               
            except CusContract.DoesNotExist:
                # Insert
                c = CusContract(
                    cnt_id = cnt_id,
                    cus_id = cus_id,
                    cus_brn = cus_brn,
                    cus_vol = cus_vol,
                    cnt_active = cnt_active,
                    cnt_sign_frm = cnt_sign_frm,
                    cnt_sign_to = cnt_sign_to,
                    cnt_eff_to = cnt_eff_to,
                    cnt_doc_no = cnt_doc_no,
                    cnt_doc_date = cnt_doc_date,
                    cnt_apr_by_id = int(cnt_apr_by),
                    cnt_guard_amt = cnt_guard_amt,
                    cnt_sale_amt = cnt_sale_amt,
                    cnt_wage_id_id = 1,
                    cnt_zone = 0,
                    cnt_autoexpire = cnt_autoexpire,
                    cnt_then = 'T',
                    upd_date = datetime.datetime.now(),
                    upd_by = request.user.first_name,
                    upd_flag = 'A',

                )
                c.save()                
                response_data['form_is_valid'] = True
                response_data['result'] = "Saved success."
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
                    data = TWagezone.objects.all().filter(w2004=1)
                else:
                    print("debug3")
                    data = TWagezone.objects.all().filter(w2004=1)
            else:
                print("debug4")
                data = TWagezone.objects.all().filter(w2004=1)
        else:
            print("debug5")
            data = TWagezone.objects.all().filter(w2004=1)

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


@login_required(login_url='/accounts/login/')
def get_wagerate_list_modal(request):

    print("**********************************")    
    print("FUNCTION: get_wagerate_list_modal")
    print("**********************************")

    data = []
    item_per_page = 100
    page_no = request.GET["page_no"]
    current_wagerate_id = request.GET["current_wage_id"]
    search_option = request.GET["search_option"]
    search_text = request.GET["search_text"]

    print(current_wagerate_id)
    print(search_option)
    print(search_text)

    if search_option == '1':
        data = TWagezone.objects.all().filter(wage_id__exact=search_text).filter(w2004=1)

    if search_option == '2':
        data = TWagezone.objects.all().filter(wage_th__contains=search_text).filter(w2004=1)

    if search_option == '3':
        data = TWagezone.objects.all().filter(wage_en__contains=search_text).filter(w2004=1)

    if data is not None:
        print("not null")
        page = int(page_no)

        next_page = page + 1
        if page >= 1:
            previous_page = page - 1
        else:
            previous_page = 0


        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

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
                    "wage_8hr": d.wage_8hr,
                }
                pickup_records.append(record)

            response = JsonResponse(data={
                "success": True,
                "is_paginated": is_paginated,
                "page" : page,
                "next_page" : next_page,
                "previous_page" : previous_page,
                "current_page_number" : current_page_number,
                "current_page_paginator_num_pages" : current_page_paginator_num_pages,
                "results": list(pickup_records)         
                })
            response.status_code = 200
            return response
        else:
            # print("not found")      
            response = JsonResponse(data={
                "success": False,
                "results": [],
            })
            response.status_code = 403
            return response
    else:        
        print("not found 2")
        response = JsonResponse(data={
            "success": False,
            "error"
            "results": [],
        })
        response.status_code = 403
        return response

    return JsonResponse(data={"success": False, "results": ""})


def update_customer_service(request):
    service_id = request.GET["service_id"]

    if service_id is not None:
        try:                
            data = CusService.objects.filter(srv_id__exact=service_id).get()

            srv_id = data.srv_id
            cnt_id = data.cnt_id_id
            srv_rank = data.srv_rank
            srv_shif_id = data.srv_shif_id
            srv_eff_frm = data.srv_eff_frm
            srv_eff_to = data.srv_eff_to
            srv_qty = data.srv_qty
            srv_mon = data.srv_mon
            srv_tue = data.srv_tue
            srv_wed = data.srv_wed
            srv_thu = data.srv_thu
            srv_fri = data.srv_fri
            srv_sat = data.srv_sat
            srv_sun = data.srv_sun
            srv_pub = data.srv_pub
            srv_active = data.srv_active
            srv_rate = data.srv_rate
            srv_cost = data.srv_cost
            srv_rem = data.srv_rem
            upd_date = data.upd_date
            upd_flag = data.upd_flag
            srv_cost_rate = data.srv_cost_rate
            srv_cost_change = data.srv_cost_change
            op1 = data.op1
            op2 = data.op2
            op3 = data.op3

            # Get com_rank
            comrank = ComRank.objects.all().exclude(upd_flag='D')
            pickup_comrank_record =[]            
            for d in comrank:
                record = {
                    "rank_id": d.rank_id,
                    "rank_th": d.rank_th,
                    "rank_en": d.rank_en,                    
                }
                pickup_comrank_record.append(record)

            # Get t_shift
            # TODO
            tshift = TShift.objects.all()
            pickup_tshift_record =[]            
            for d in tshift:
                record = {
                    "shf_id": d.shf_id,
                    "shf_desc": d.shf_desc,
                }
                pickup_tshift_record.append(record)

            response = JsonResponse(data={
                "success": True,
                "srv_id": data.srv_id,
                "cnt_id": data.cnt_id_id,
                "srv_rank": data.srv_rank,
                "srv_shif_id": data.srv_shif_id_id,
                "srv_eff_frm": data.srv_eff_frm.strftime('%d/%m/%Y'),
                "srv_eff_to": data.srv_eff_to.strftime('%d/%m/%Y'),
                "srv_qty": data.srv_qty,
                "srv_mon": data.srv_mon,
                "srv_tue": data.srv_tue,
                "srv_wed": data.srv_wed,
                "srv_thu": data.srv_thu,
                "srv_fri": data.srv_fri,
                "srv_sat": data.srv_sat,
                "srv_sun": data.srv_sun,
                "srv_pub": data.srv_pub,
                "srv_active": data.srv_active,
                "srv_rate": data.srv_rate,
                "srv_cost": data.srv_qty * data.srv_rate,
                "srv_total_cost": data.srv_qty * data.srv_rate,
                "srv_rem": data.srv_rem,
                "upd_date": data.upd_date,
                "upd_flag": data.upd_flag,
                "srv_cost_rate": data.srv_cost_rate,
                "srv_cost_change": data.srv_cost_change,
                "op1": data.op1,
                "op2": data.op2,
                "op3": data.op3,
                "com_rank_list": list(pickup_comrank_record),
                "t_shift_list": list(pickup_tshift_record),
            })
            response.status_code = 200
            return response

        except CusService.DoesNotExist:
            response = JsonResponse(data={
                "success": False,
                "message": "Service ID not found.",
                "results": [],
            })
            response.status_code = 403
            return response

    else:
        response = JsonResponse(data={
            "success": False,
            "message": "Service ID not found.",
            "results": [],
        })
        response.status_code = 403
        return response    


def add_new_service(request):    
    cus_id = request.GET["cus_id"]
    cus_brn = request.GET["cus_brn"]
    cus_vol = request.GET["cus_vol"]
    cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)

    # Check if cus_contract is existed
    try:
        data = CusContract.objects.filter(cnt_id=cnt_id).get()       
    except CusContract.DoesNotExist:
        response = JsonResponse(data={
            "success": True,
            "message": "Please save contract first.",
            "class": "bg-danger",
            "cnt_id": cnt_id,
        })

        response.status_code = 200
        return response

    # srv_eff_from = request.GET["srv_eff_frm_new"]
    print("srv_eff_frm = " + str(request.GET["srv_eff_frm_new"]))
    srv_eff_from = datetime.datetime.strptime(request.GET["srv_eff_frm_new"], "%d/%m/%Y").date()

    # srv_eff_to = request.GET["srv_eff_to_new"].strftime("%d/%m/%Y")
    srv_eff_to = datetime.datetime.strptime(request.GET["srv_eff_to_new"], "%d/%m/%Y").date()

    srv_rank = request.GET["srv_rank_new"]
    srv_shift_id = request.GET["srv_shift_id_new"]
    srv_qty = request.GET["srv_qty_new"]
    srv_mon = request.GET["srv_mon_new"]
    srv_tue = request.GET["srv_tue_new"]
    srv_wed = request.GET["srv_wed_new"]
    srv_thu = request.GET["srv_thu_new"]
    srv_fri = request.GET["srv_fri_new"]
    srv_sat = request.GET["srv_sat_new"]
    srv_sun = request.GET["srv_sun_new"]
    srv_pub = request.GET["srv_pub_new"]
    srv_active = request.GET["srv_active_new"]
    srv_rate = request.GET["srv_rate_new"]
    srv_cost = request.GET["srv_cost_new"]    
    srv_cost_rate = request.GET["srv_cost_rate_new"]
    srv_rem = request.GET["srv_rem_new"]


    # print("----------------------------")
    # print("cnt_id = " + str(cnt_id))
    # print("----------------------------")

    latest_service_number = CusService.objects.filter(cnt_id=cnt_id).aggregate(Max('srv_id'))
    latest_service_number = latest_service_number['srv_id__max']

    if latest_service_number is not None:
        new_service_number = latest_service_number + 1
    else:
        new_service_number = str(cnt_id) + "00001"


    s = CusService(
        srv_id = new_service_number,
        cnt_id_id = cnt_id,
        srv_rank = srv_rank,
        srv_shif_id_id = srv_shift_id,
        srv_eff_frm = srv_eff_from,
        srv_eff_to = srv_eff_to,
        srv_qty = srv_qty,
        srv_mon = srv_mon,
        srv_tue = srv_tue,
        srv_wed = srv_wed,
        srv_thu = srv_thu,
        srv_fri = srv_fri,
        srv_sat = srv_sat,
        srv_sun = srv_sun,
        srv_pub = srv_pub,
        srv_active = srv_active,
        srv_rate = float(srv_rate),
        srv_cost = int(srv_qty) * float(srv_rate),
        srv_rem = srv_rem,
        srv_cost_rate = float(srv_cost),
        upd_date = datetime.datetime.now(),
        upd_by = request.user.first_name,
        upd_flag = 'A',
        srv_cost_change = 0,
        op1 = 0,
        op2 = 0,
        op3 = 0,
    )
    s.save()

    # Recalculate cnt_guard_amt, cnt_sale_amt
    # start
    cus_service_list = CusService.objects.all().filter(cnt_id=cnt_id)
    active_cnt_guard_amt = 0
    active_cnt_sale_amt = 0
    for item in cus_service_list:
        if item.srv_active:                        
            active_cnt_guard_amt += item.srv_qty
            active_cnt_sale_amt += item.srv_rate * item.srv_qty
    c = CusContract.objects.get(cnt_id=cnt_id)
    c.cnt_guard_amt = active_cnt_guard_amt
    c.cnt_sale_amt = active_cnt_sale_amt
    c.save()
    # end

    response = JsonResponse(data={
        "success": True,
        "message": "Success.",
        "class": "bg-success",
        "cnt_id": cnt_id,
        "active_cnt_guard_amt": active_cnt_guard_amt,
        "active_cnt_sale_amt": active_cnt_sale_amt,        
    })

    response.status_code = 200
    return response


def save_new_service(request):
    cnt_id = request.GET["cnt_id"]

    # srv_eff_from = request.GET["srv_eff_frm_new"]
    print("srv_eff_frm = " + str(request.GET["srv_eff_frm_new"]))
    srv_eff_from = datetime.datetime.strptime(request.GET["srv_eff_frm_new"], "%d/%m/%Y").date()

    # srv_eff_to = request.GET["srv_eff_to_new"].strftime("%d/%m/%Y")
    srv_eff_to = datetime.datetime.strptime(request.GET["srv_eff_to_new"], "%d/%m/%Y").date()

    srv_rank = request.GET["srv_rank_new"]
    srv_shift_id = request.GET["srv_shift_id_new"]
    srv_qty = request.GET["srv_qty_new"]
    srv_mon = request.GET["srv_mon_new"]
    srv_tue = request.GET["srv_tue_new"]
    srv_wed = request.GET["srv_wed_new"]
    srv_thu = request.GET["srv_thu_new"]
    srv_fri = request.GET["srv_fri_new"]
    srv_sat = request.GET["srv_sat_new"]
    srv_sun = request.GET["srv_sun_new"]
    srv_pub = request.GET["srv_pub_new"]
    srv_active = request.GET["srv_active_new"]
    srv_rate = request.GET["srv_rate_new"]
    srv_cost = request.GET["srv_cost_new"]    
    srv_cost_rate = request.GET["srv_cost_rate_new"]
    srv_rem = request.GET["srv_rem_new"]

    # print("----------------------------")
    # print("cnt_id = " + str(cnt_id))
    # print("----------------------------")
    
    latest_service_number = CusService.objects.filter(cnt_id=cnt_id).aggregate(Max('srv_id'))
    latest_service_number = latest_service_number['srv_id__max']

    if latest_service_number is not None:
        new_service_number = latest_service_number + 1
    else:
        new_service_number = str(cnt_id) + "00001"


    s = CusService(
        srv_id = new_service_number,
        cnt_id_id = cnt_id,
        srv_rank = srv_rank,
        srv_shif_id_id = srv_shift_id,
        srv_eff_frm = srv_eff_from,
        srv_eff_to = srv_eff_to,
        srv_qty = srv_qty,
        srv_mon = srv_mon,
        srv_tue = srv_tue,
        srv_wed = srv_wed,
        srv_thu = srv_thu,
        srv_fri = srv_fri,
        srv_sat = srv_sat,
        srv_sun = srv_sun,
        srv_pub = srv_pub,
        srv_active = srv_active,
        srv_rate = float(srv_rate),
        srv_cost = int(srv_qty) * float(srv_rate),
        srv_rem = srv_rem,
        srv_cost_rate = float(srv_cost),
        upd_date = datetime.datetime.now(),
        upd_by = request.user.first_name,
        upd_flag = 'A',
        srv_cost_change = 0,
        op1 = 0,
        op2 = 0,
        op3 = 0,
    )
    s.save()

    # Recalculate cnt_guard_amt, cnt_sale_amt
    # start
    cus_service_list = CusService.objects.all().filter(cnt_id=cnt_id)
    active_cnt_guard_amt = 0
    active_cnt_sale_amt = 0
    for item in cus_service_list:
        if item.srv_active:                        
            active_cnt_guard_amt += item.srv_qty
            active_cnt_sale_amt += item.srv_rate * item.srv_qty
    c = CusContract.objects.get(cnt_id=cnt_id)
    c.cnt_guard_amt = active_cnt_guard_amt
    c.cnt_sale_amt = active_cnt_sale_amt
    c.save()
    # end

    response = JsonResponse(data={
        "success": True,
        "message": "Success.",
        "class": "bg-success",
        "cnt_id": cnt_id,
        "active_cnt_guard_amt": active_cnt_guard_amt,
        "active_cnt_sale_amt": active_cnt_sale_amt,        
    })

    response.status_code = 200
    return response


def save_customer_service_item(request):
    srv_id = request.GET["srv_id"]
    srv_eff_from = request.GET["srv_eff_frm"]
    srv_eff_to = request.GET["srv_eff_to"]
    srv_rank = request.GET["srv_rank"]
    srv_shift_id = request.GET["srv_shift_id"]     
    srv_qty = request.GET["srv_qty"]
    srv_mon = request.GET["srv_mon"]
    srv_tue = request.GET["srv_tue"]
    srv_wed = request.GET["srv_wed"]
    srv_thu = request.GET["srv_thu"]
    srv_fri = request.GET["srv_fri"]
    srv_sat = request.GET["srv_sat"]
    srv_sun = request.GET["srv_sun"]
    srv_pub = request.GET["srv_pub"]
    srv_active = request.GET["srv_active"]
    srv_rate = request.GET["srv_rate"]
    srv_cost = request.GET["srv_cost"]
    srv_cost_rate = request.GET["srv_cost_rate"]
    srv_rem = request.GET["srv_rem"]

    #TODO - all print below will be comment
    print("START")
    print("srv_id = " + str(srv_id))
    print("srv_eff_frm = " + str(srv_eff_from))
    print("srv_eff_to = " + str(srv_eff_to))
    print("srv_rank = " + str(srv_rank))
    print("srv_shift_id = " + str(srv_shift_id))
    print("srv_qty = " + str(srv_qty))
    print("srv_mon = " + str(srv_mon))
    print("srv_tue = " + str(srv_tue))
    print("srv_wed = " + str(srv_wed))
    print("srv_thu = " + str(srv_thu))
    print("srv_fri = " + str(srv_fri))
    print("srv_sat = " + str(srv_sat))
    print("srv_sun = " + str(srv_sun))
    print("srv_pub = " + str(srv_pub))
    print("srv_active = " + str(srv_active))
    print("srv_rate = " + str(srv_rate))
    print("srv_cost = " + str(srv_cost))
    print("srv_cost_rate = " + str(srv_cost_rate))
    print("srv_rem = " + str(srv_rem))
    print("END")

    if srv_id is not None:
        try:                
            field_is_modified_count = 0
            modified_records = []
            data = CusService.objects.filter(srv_id__exact=srv_id).get()
            cnt_id = data.cnt_id_id

            # SRV_RANK
            if (srv_rank is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "Rank", str(data.srv_rank), srv_rank, "E", request)
                if field_is_modified:
                    data.srv_rank = srv_rank
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_SHIFT_ID
            if (srv_shift_id is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "Shift", int(data.srv_shif_id_id), int(srv_shift_id), "E", request)
                if field_is_modified:
                    data.srv_shif_id_id = srv_shift_id
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1
 
            # SRV_EFF_FROM
            if (srv_eff_from is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "Eff From", data.srv_eff_frm, datetime.datetime.strptime(srv_eff_from, "%d/%m/%Y"), "E", request)
                if field_is_modified:
                    data.srv_eff_frm = datetime.datetime.strptime(srv_eff_from, "%d/%m/%Y")
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_EFF_TO
            if (srv_eff_to is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "Eff From", data.srv_eff_to, datetime.datetime.strptime(srv_eff_to, "%d/%m/%Y"), "E", request)
                if field_is_modified:
                    data.srv_eff_to = datetime.datetime.strptime(srv_eff_to, "%d/%m/%Y")
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_QTY
            if (srv_qty is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "QTY", int(data.srv_qty), int(srv_qty), "E", request)
                if field_is_modified:
                    data.srv_qty = srv_qty
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_MON
            if (srv_mon is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_MON", int(data.srv_mon), int(srv_mon), "E", request)
                if field_is_modified:
                    data.srv_mon = srv_mon
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_TUE
            if (srv_tue is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_TUE", int(data.srv_tue), int(srv_tue), "E", request)
                if field_is_modified:
                    data.srv_tue = srv_tue
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_WED
            if (srv_wed is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_WED", int(data.srv_wed), int(srv_wed), "E", request)
                if field_is_modified:
                    data.srv_wed = srv_wed
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_THU
            if (srv_thu is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_THU", int(data.srv_thu), int(srv_thu), "E", request)
                if field_is_modified:
                    data.srv_thu = srv_thu
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_FRI
            if (srv_fri is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_FRI", int(data.srv_fri), int(srv_fri), "E", request)
                if field_is_modified:
                    data.srv_fri = srv_fri
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_SAT
            if (srv_sat is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_SAT", int(data.srv_sat), int(srv_sat), "E", request)
                if field_is_modified:
                    data.srv_sat = srv_sat
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_SUN
            if (srv_sun is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_SUN", int(data.srv_sun), int(srv_sun), "E", request)
                if field_is_modified:
                    data.srv_sun = srv_sun
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_PUB
            if (srv_pub is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_PUB", int(data.srv_pub), int(srv_pub), "E", request)
                if field_is_modified:
                    data.srv_pub = srv_pub
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_ACTIVE
            if (srv_active is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_ACTIVE", int(data.srv_active), int(srv_active), "E", request)
                if field_is_modified:
                    data.srv_active = srv_active
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_RATE
            if (srv_rate is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_RATE", int(data.srv_rate), int(srv_rate), "E", request)
                if field_is_modified:
                    data.srv_rate = srv_rate
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_COST
            if (srv_cost is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_COST", int(data.srv_cost), int(srv_cost), "E", request)
                if field_is_modified:
                    data.srv_cost = int(srv_qty) * float(srv_rate)
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_REM
            if (srv_rem is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "Remark", data.srv_rem, srv_rem, "E", request)
                if field_is_modified:
                    data.srv_rem = srv_rem
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1


            # Modified user
            if field_is_modified_count > 0:
                data.upd_date = datetime.datetime.now()
                data.upd_by = request.user.first_name
                data.upd_flag = 'E'
                data.save()

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
                # ./History Log                     

                # TODO
                # Recalculate cnt_guard_amt, cnt_sale_amt
                # start
                cus_service_list = CusService.objects.all().filter(cnt_id=cnt_id)
                active_cnt_guard_amt = 0
                active_cnt_sale_amt = 0
                for item in cus_service_list:
                    if item.srv_active:                        
                        active_cnt_guard_amt += item.srv_qty
                        active_cnt_sale_amt += item.srv_rate * item.srv_qty
                c = CusContract.objects.get(cnt_id=cnt_id)
                c.cnt_guard_amt = active_cnt_guard_amt
                c.cnt_sale_amt = active_cnt_sale_amt
                c.save()
                # end
                
                # Return result
                response = JsonResponse(data={
                    "success": True,
                    "message": "Saved success.",
                    "class": "bg-success",
                    "cnt_id": cnt_id,
                    "active_cnt_guard_amt": active_cnt_guard_amt,
                    "active_cnt_sale_amt": active_cnt_sale_amt,
                })            
                response.status_code = 200

            else:
                response = JsonResponse(data={
                    "success": True,
                    "message": "Sorry, nothing to update.",
                    "class": "bg-warning",
                })            
                response.status_code = 200

            return response            
        except CusService.DoesNotExist:
            response = JsonResponse(data={
                "success": False,
                "message": "Service ID not found.",
                "results": [],
            })
            response.status_code = 403
            return response
    else:
        response = JsonResponse(data={
            "success": False,
            "message": "Service ID not found.",
            "results": [],
        })
        response.status_code = 403
        return response          


@login_required(login_url='/accounts/login/')
def get_rank_shift_list(request):

    print("****************************")
    print("FUNCTION: get_rank_list")
    print("****************************")

    # COM_RANK
    if request.method == "POST":
        data = ComRank.objects.all().exclude(upd_flag='D')
    else:
        data = ComRank.objects.all().exclude(upd_flag='D')

    # no_of_active_customer = Customer.objects.filter(cus_active=1).exclude(upd_flag='D').count()

    com_rank_list=[]
    for d in data:
        record = {
            "rank_id": d.rank_id,
            "rank_th": d.rank_th,
            "rank_en": d.rank_en,
        }
        com_rank_list.append(record)


    # T_SHIFT
    if request.method == "POST":
        data = TShift.objects.all()
    else:
        data = TShift.objects.all()

    t_shift_list=[]
    for d in data:
        record = {
            "shf_id": d.shf_id,
            "shf_desc": d.shf_desc,
        }
        t_shift_list.append(record)

    response = JsonResponse(data={
        "success": True,
        "com_rank_list": list(com_rank_list),
        "t_shift_list": list(t_shift_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
def reload_service_list(request):

    print("*******************************")
    print("FUNCTION: reload_service_list")
    print("*******************************")

    cnt_id = request.GET["cnt_id"]

    data = CusService.objects.all().filter(cnt_id=cnt_id).order_by('-srv_active')
    
    cus_service_list=[]
    for d in data:
        record = {
            "srv_id": d.srv_id,
            "cnt_id": d.cnt_id_id,
            "srv_rank": d.srv_rank,
            "srv_shif_id": d.srv_shif_id_id,
            "srv_shift_text": d.srv_shif_id.shf_desc,
            "srv_eff_frm": d.srv_eff_frm.strftime("%d/%m/%Y"),
            "srv_eff_to": d.srv_eff_to.strftime("%d/%m/%Y"),
            "srv_qty": d.srv_qty,
            "srv_rate": d.srv_rate,
            "srv_cost": d.srv_cost,
            "srv_cost_rate": d.srv_cost_rate,
            "srv_mon": d.srv_mon,
            "srv_tue": d.srv_tue,
            "srv_wed": d.srv_wed,
            "srv_thu": d.srv_thu,
            "srv_fri": d.srv_fri,
            "srv_sat": d.srv_sat,
            "srv_sun": d.srv_sun,
            "srv_pub": d.srv_pub,
            "srv_rem": d.srv_rem,
            "srv_active": d.srv_active,
        }
        cus_service_list.append(record)

    response = JsonResponse(data={
        "success": True,
        "cus_service_list": list(cus_service_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
def delete_customer_service(request):

    print("*******************************")
    print("FUNCTION: delete_customer_service")
    print("*******************************")

    srv_id = request.GET["srv_id"]

    data = CusService.objects.filter(srv_id=srv_id).get() 
    cnt_id = data.cnt_id_id
    data.delete()

    # Recalculate cnt_guard_amt, cnt_sale_amt
    # start
    cus_service_list = CusService.objects.all().filter(cnt_id=cnt_id)
    active_cnt_guard_amt = 0
    active_cnt_sale_amt = 0
    for item in cus_service_list:
        if item.srv_active:                        
            active_cnt_guard_amt += item.srv_qty
            active_cnt_sale_amt += item.srv_rate * item.srv_qty
    c = CusContract.objects.get(cnt_id=cnt_id)
    c.cnt_guard_amt = active_cnt_guard_amt
    c.cnt_sale_amt = active_cnt_sale_amt
    c.save()
    # end

    response = JsonResponse(data={
        "success": True,
        "message": "Service ID " + srv_id + " has been deleted.",
        "class": "bg-danger",
        "cnt_id": cnt_id,
        "active_cnt_guard_amt": active_cnt_guard_amt,
        "active_cnt_sale_amt": active_cnt_sale_amt,        
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
def reload_contract_list(request):

    print("*******************************")
    print("FUNCTION: reload_contract_list")
    print("*******************************")

    cnt_id = request.GET["cnt_id"]
    cus_id = request.GET["cus_id"]
    print("cus_id = " + str(cus_id))

    if cus_id != "":
        data = CusContract.objects.all().filter(cus_id=cus_id).exclude(upd_flag='D').order_by('-cnt_active')
    else:
        # data = CusContract.objects.all().exclude(upd_flag='D').order_by('-cnt_active')
        data = []
    
    # for item in data:
    #    print(item.cnt_id)

    cus_contract_list=[]
    for d in data:
        record = {
            "cnt_id": d.cnt_id,
            "cus_name_th": "aa",
            "cus_name_en": "bb",
        }
        cus_contract_list.append(record)

    response = JsonResponse(data={
        "success": True,
        "cus_contract_list": list(cus_contract_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
def delete_customer_contract(request):

    print("************************************")
    print("FUNCTION: delete_customer_contract")
    print("************************************")

    cnt_id = request.GET["cnt_id"]

    data = CusContract.objects.filter(cnt_id=cnt_id).get() 
    data.upd_flag = 'D'
    data.upd_date = datetime.datetime.now()
    data.upd_by = request.user.first_name    
    cnt_id = data.cnt_id 
    data.save()

    response = JsonResponse(data={
        "success": True,
        "message": "Contract ID " + str(cnt_id) + " has been deleted.",
        "class": "bg-danger",
        "cnt_id": cnt_id,
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def generate_contract(request, *args, **kwargs):
    cnt_id = kwargs['cnt_id']
    language_option = kwargs['language_option']
    print(language_option)
    base_url = MEDIA_ROOT + '/contract/template/'

    if language_option == 'T':
        file_name = request.user.username + "_" + cnt_id + "_TH.docx"
        template_language = base_url + 'ReNC102_TH.docx'
    else:
        file_name = request.user.username + "_" + cnt_id + "_EN.docx"
        template_language = base_url + 'ReNC102_EN.docx'

    if cnt_id is not None:
        try:                
            # Get Contract information
            cus_contract = CusContract.objects.filter(cnt_id__exact=cnt_id).get()
            cus_contract_cus_id = cus_contract.cus_id
            cus_contract_cus_brn = cus_contract.cus_brn

            # Get Customer information
            customer = Customer.objects.filter(cus_id=cus_contract_cus_id).filter(cus_brn=cus_contract_cus_brn).get()
            cusbill = CusBill.objects.filter(cus_id=cus_contract_cus_id).filter(cus_brn=cus_contract_cus_brn).get()

            # Get Cutomer Service information
            pickup_record_day = []
            pickup_record_night = []
            count_shift_day = 0
            count_shift_night = 0
            srv_rate_day = 0
            srv_rate_night = 0
            srv_rate_total = 0

            try:                 
                # cus_service_list = CusService.objects.all().filter(cnt_id=cnt_id).order_by('-srv_rank', '-srv_shif_id')
                
                # Test
                cursor = connection.cursor()
                try:        
                    cursor.execute("select cus_name_th, cus_name_en, shf_type, shf_time_frm, shf_time_to, srv_qty, rank_th, srv_rem, srv_rate from V_CONTRACT where cnt_id=" + cnt_id + " and srv_active=1 and shf_type='D' order by shf_type,srv_rank desc")
                    cus_service_list_day = cursor.fetchall()
                    count_shift_day = len(cus_service_list_day)
                    for row in cus_service_list_day:
                        srv_rate_day = srv_rate_day + (int(row[5]) * int(row[8])) # row[8] = srv_rate


                    cursor.execute("select cus_name_th, cus_name_en, shf_type, shf_time_frm,shf_time_to,srv_qty,rank_th,srv_rem,srv_rate from V_CONTRACT where cnt_id=" + cnt_id + " and srv_active=1 and shf_type='N' order by shf_type,srv_rank desc")
                    cus_service_list_night = cursor.fetchall()
                    count_shift_night = len(cus_service_list_night)
                    for row in cus_service_list_night:
                        srv_rate_night = srv_rate_night + (int(row[5]) * int(row[8])) # row[8] = srv_rate

                finally:
                    cursor.close()
                
                for (cus_name_th, cus_name_en, shf_type, shf_time_frm,shf_time_to,srv_qty,rank_th,srv_rem,srv_rate) in cus_service_list_day:                    
                    record = {
                        "cus_name_th": cus_name_th,
                        "cus_name_en": cus_name_en,
                        "shf_type": shf_type,
                        "shf_time_frm": shf_time_frm,
                        "shf_time_to": shf_time_to,
                        "srv_qty": srv_qty,
                        "srv_rank_th": rank_th,
                        "srv_rem": srv_rem,
                        "srv_rate": srv_qty * srv_rate,
                    }
                    pickup_record_day.append(record)                

                for (cus_name_th, cus_name_en, shf_type, shf_time_frm,shf_time_to,srv_qty,rank_th,srv_rem,srv_rate) in cus_service_list_night: 
                    record = {
                        "cus_name_th": cus_name_th,
                        "cus_name_en": cus_name_en,
                        "shf_type": shf_type,
                        "shf_time_frm": shf_time_frm,
                        "shf_time_to": shf_time_to,
                        "srv_qty": srv_qty,
                        "srv_rank_th": rank_th,
                        "srv_rem": srv_rem,
                        "srv_rate": srv_qty * srv_rate,                    
                    }
                    pickup_record_night.append(record)                

            except CusService.DoesNotExist:
                cus_service_list_day = []
                cus_service_list_night = []



    # cus_district = models.ForeignKey(TDistrict, related_name='cus_site_t_district_fk', db_column='cus_district', to_field='dist_id', on_delete=models.SET_NULL, null=True)    
    # cus_city = models.ForeignKey(TCity, related_name='cus_site_cus_city_fk', db_column='cus_city', to_field='city_id', on_delete=models.SET_NULL, null=True)
    # cus_country = models.ForeignKey(TCountry, related_name='cus_site_t_country_fk', db_column='cus_country', to_field='country_id', on_delete=models.SET_NULL, null=True)
    # cus_zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)

            context = {
                'customer': customer,
                'file_name': file_name,
                'language_option': language_option,
                'cnt_id': cnt_id,               
                'cnt_doc_no': cus_contract.cnt_doc_no,
                'today_date': datetime.datetime.now().strftime("%d %B %Y"),

                'cusbill_name_th': cusbill.cus_name_th,
                'cusbill_name_en': cusbill.cus_name_en,
                'cusbill_address_th': cusbill.cus_add1_th,
                'cusbill_address_en': cusbill.cus_add1_en,                
                'cusbill_site_th': cusbill.cus_add1_th,
                'cusbill_site_en': cusbill.cus_add1_en,
                'cusbill_site_cus_subdist_th': cusbill.cus_subdist_th,
                'cusbill_site_cus_subdist_en': cusbill.cus_subdist_en,
                'cusbill_site_cus_district_th': cusbill.cus_district.dist_th,
                'cusbill_site_cus_district_en': cusbill.cus_district.dist_en,
                'cusbill_site_cus_city_th': cusbill.cus_city.city_th,
                'cusbill_site_cus_city_en': cusbill.cus_city.city_en,
                'cusbill_site_cus_zip': cusbill.cus_zip,

                'customer_name_th': customer.cus_name_th,
                'customer_name_en': customer.cus_name_en,
                'customer_address_th': customer.cus_add1_th,
                'customer_address_en': customer.cus_add1_en,                
                'customer_site_th': customer.cus_add1_th,
                'customer_site_en': customer.cus_add1_en,
                'customer_site_cus_subdist_th': customer.cus_subdist_th,
                'customer_site_cus_subdist_en': customer.cus_subdist_en,
                'customer_site_cus_district_th': customer.cus_district.dist_th,
                'customer_site_cus_district_en': customer.cus_district.dist_en,
                'customer_site_cus_city_th': customer.cus_city.city_th,
                'customer_site_cus_city_en': customer.cus_city.city_en,
                'customer_site_cus_zip': customer.cus_zip,


                'effective_from': cus_contract.cnt_eff_frm.now().strftime("%d %B %Y"),
                'effective_to': cus_contract.cnt_eff_frm.now().strftime("%d %B %Y"),
                'shift_list_day': list(pickup_record_day),
                'shift_list_night': list(pickup_record_night),
                'count_shift_day': count_shift_day,
                'count_shift_night': count_shift_night,
                'total_count_shift': count_shift_day + count_shift_night,
                'srv_rate_total': srv_rate_day + srv_rate_night,
            }
        except CusContract.DoesNotExist:
            context = {
                'customer': "",
                'file_name': "",
                'cnt_id': "",
                'cnt_doc_no': "",
                'today_date': datetime.datetime.now().strftime("%d/%B/%Y"),
                'customer_name': "",
                'customer_address': "",
                'customer_site': "",
                'effect_from': "",
                'effect_to': "",
                'items' : [
                    {'desc' : 'test1', 'qty' : 2, 'price' : '0.00' },
                    {'desc' : 'test2', 'qty' : 2, 'price' : '0.00' },
                ],
                'is_changed' : True,
            }            
    else:
        context = {
                'customer': "",
                'file_name': "",
                'cnt_id': "",
                'cnt_doc_no': "",
                'today_date': datetime.datetime.now().strftime("%d/%B/%Y"),
                'customer_name': "",
                'customer_address': "",
                'customer_site': "",
                'effect_from': "",
                'effect_to': "",
                'items' : [
                    {'desc' : 'test1', 'qty' : 2, 'price' : '0.00' },
                    {'desc' : 'test2', 'qty' : 2, 'price' : '0.00' },
                ],
                'is_changed' : True,
        }
    
    tpl = DocxTemplate(template_language)
    tpl.render(context)
    tpl.save(MEDIA_ROOT + '/contract/download/' + file_name)

    return render(request, 'contract/generate_contract.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def download_contract(request, *args, **kwargs):    
    file_name = kwargs['file_name']
    file_path = "media/contract/download/" + file_name
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-word")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404