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
from time import sleep
from docx2pdf import convert
from os import path
import mimetypes
import os
from django.conf import settings
from wsgiref.util import FileWrapper
from django.http import HttpResponse, Http404
from django.http import FileResponse
from django.db import connection
import django.db as db
import docx
import win32com.client
from num2words import num2words


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
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        })


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def get_cus_main(request):
    cus_id = request.POST.get('cus_id')    
    print("cus_id:", cus_id)

    if cus_id==0:
        response = JsonResponse(data={
            "success": True,
            "is_existed": False,
            "class": "bg-danger",
            "message": "Not found",  
            "cus_name_th": "",
            "cus_name_en": "",
        })
        return response

    if cus_id is not None:
        try:                
            cusmain = CusMain.objects.filter(cus_id__exact=cus_id).get()

            if cusmain is not None:
                is_existed = True
                alert_class = "bg-success"
                cus_name_th = cusmain.cus_name_th
                cus_name_en = cusmain.cus_name_en
            else:
                is_existed = False
                alert_class = "bg-danger"
                cus_name_th = ""
                cus_name_en = ""

        except CusMain.DoesNotExist:
            is_existed = False
            alert_class = "bg-danger"
            cus_name_th = ""
            cus_name_en = ""

    print("is_existed:", is_existed)

    response = JsonResponse(data={
        "success": True,
        "is_existed": is_existed,
        "class": alert_class,
        "message": "",        
        "cus_name_th": cus_name_th,
        "cus_name_en": cus_name_en,
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

            if customer.cus_district_id is not None:
                cus_district_id = customer.cus_district_id

                cus_district_th = customer.cus_district.dist_th
                cus_district_en = customer.cus_district.dist_en
            else:
                cus_district_id = 0
                cus_district_th = ""
                cus_district_en = ""

            if customer.cus_city_id is not None:
                cus_city_th = customer.cus_city.city_th
                cus_city_en = customer.cus_city.city_en
            else:
                cus_city_id = 0
                cus_city_th = ""
                cus_city_en = ""

            if customer.cus_country_id is not None:
                cus_country_th = customer.cus_country.country_th
                cus_country_en = customer.cus_country.country_en
            else:
                cus_country_id = 0
                cus_country_th = ""
                cus_country_en = ""
            
            cus_tel = customer.cus_tel
            cus_fax = customer.cus_fax
            cus_email = customer.cus_email
            
            if customer.site_contact_id is not None:
                site_contact_id_th = customer.site_contact_id
                site_contact_con_fname_th = customer.site_contact.con_fname_th
                site_contact_con_lname_th = customer.site_contact.con_lname_th
                site_contact_con_position_th = customer.site_contact.con_position_th

                site_contact_id_en = customer.site_contact_id
                site_contact_con_fname_en = customer.site_contact.con_fname_en
                site_contact_con_lname_en = customer.site_contact.con_lname_en
                site_contact_con_position_en = customer.site_contact.con_position_en
            else:
                site_contact_id_th = 0
                site_contact_con_fname_th = ""
                site_contact_con_lname_th = ""
                site_contact_con_position_th = ""

                site_contact_id_en = 0
                site_contact_con_fname_en = ""
                site_contact_con_lname_en = ""
                site_contact_con_position_en = ""


            if customer.cus_zone_id is not None:            
                site_contact_cus_zone_id = customer.cus_zone_id
                site_contact_cus_zone_th = customer.cus_zone.zone_th
                site_contact_cus_zone_en = customer.cus_zone.zone_en
            else:
                site_contact_cus_zone_id = 0
                site_contact_cus_zone_th = ""
                site_contact_cus_zone_en = ""


            # Get default wage rate
            default_customer_city_id = None
            default_wage_id = None
            default_wage_en = ""
            default_wage_th = ""
            default_wage_8hr = 0 
            message = ""                      
            sql = "select cu.cus_city,ct.wage_id,wz.wage_en,wz.wage_th,wz.wage_8hr from customer cu ";
            sql += "join t_citywage ct on cu.cus_city=ct.city_id ";
            sql += "join t_wagezone wz on ct.wage_id=wz.wage_id ";
            sql += "where cu.cus_id=" + str(cus_id) + " and cu.cus_brn=" + str(cus_brn) + ";"

            if customer.cus_city_id is not None:
                try:
                    with connection.cursor() as cursor:     
                        cursor.execute(sql)
                        wage_rate_obj = cursor.fetchone()

                    if wage_rate_obj is not None:
                        default_customer_city_id = wage_rate_obj[0]
                        default_wage_id = wage_rate_obj[1]
                        default_wage_en = wage_rate_obj[2]
                        default_wage_th = wage_rate_obj[3]
                        default_wage_8hr = wage_rate_obj[4]                        
                    message = "OK"
                    is_error = False
                except db.OperationalError as e:
                    is_error = True
                    message = "Please send this error to IT team or try again | " + str(e)                    
                except db.Error as e:
                    is_error = True
                    message = "Please send this error to IT team or try again | " + str(e)
                finally:
                    cursor.close()
            else:                
                is_error = True
                message = "Default wage_id is no found."

            # Get default Effective To
            default_sign_to = None
            default_effective_to = None
            message = ""                                  
            sql = "select cnt_sign_to, cnt_eff_to from cus_contract where cus_id=" + str(cus_id) + " and cus_brn=" + str(cus_brn) + " and cus_vol=1;"
            try:
                with connection.cursor() as cursor:     
                    cursor.execute(sql)
                    cus_contract_obj = cursor.fetchone()

                if cus_contract_obj is not None:
                    if cus_contract_obj[0] is not None:
                        default_sign_to = cus_contract_obj[0].strftime("%d/%m/%Y")

                    if cus_contract_obj[1]:
                        default_effective_to = cus_contract_obj[1].strftime("%d/%m/%Y")
                
                message = "OK"
                is_error = False
            except db.OperationalError as e:
                is_error = True
                message = "Please send this error to IT team or try again | " + str(e)                    
            except db.Error as e:
                is_error = True
                message = "Please send this error to IT team or try again | " + str(e)
            finally:
                cursor.close()
            
            print("default_effective_to:", default_effective_to)                        
            print("default_sign_to:", default_sign_to)
                
            response = JsonResponse(data={
                # TH
                "success": True,
                "class": "bg-danger",
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
                
                "default_wage_id": default_wage_id,
                "default_wage_en": default_wage_en,
                "default_wage_th": default_wage_th,
                "default_wage_8hr": default_wage_8hr,

                "default_sign_to": default_sign_to,
                "default_effective_to": default_effective_to,
            })

            response.status_code = 200
            return response
        except Customer.DoesNotExist:            
            response = JsonResponse(data={
                "success": True,
                "class": "bg-danger",
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
        "class": "bg-danger",
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

                cnt_then = cuscontract.cnt_then                
                cnt_doc_no = cuscontract.cnt_doc_no                
                
                if cuscontract.cnt_doc_date is not None:
                    cnt_doc_date = cuscontract.cnt_doc_date.strftime("%d/%m/%Y")
                else:
                    cnt_doc_date = datetime.datetime.now().strftime("%d/%m/%Y")
                
                if cuscontract.cnt_eff_frm is not None:                    
                    cnt_eff_frm = cuscontract.cnt_eff_frm.strftime("%d/%m/%Y")
                else:
                    # cnt_eff_frm = datetime.datetime.now().strftime("%d/%m/%Y")
                    # cnt_eff_frm = "31/12/2999"
                    cnt_eff_frm = None

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
                cnt_wage_en = cuscontract.cnt_wage_id.wage_en
                cnt_wage_8hr = cuscontract.cnt_wage_id.wage_8hr
                cnt_guard_amt = cuscontract.cnt_guard_amt
                cnt_sale_amt = cuscontract.cnt_sale_amt
                cnt_new = cuscontract.cnt_new
                cnt_print = cuscontract.cnt_print
                cnt_autoexpire = cuscontract.cnt_autoexpire
                cnt_upd_flag = cuscontract.upd_flag

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
                    cus_service_list = CusService.objects.all().exclude(upd_flag='D').filter(cnt_id=cnt_id)
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
                    "class": "bg-danger",
                    "message": "",
                    "is_existed": True,
                    "cnt_id": cnt_id,
                    "cnt_then": cnt_then,
                    "cnt_active": cnt_active,
                    "cnt_doc_no": cnt_doc_no,
                    "cnt_doc_date": cnt_doc_date,
                    "cnt_eff_frm": cnt_eff_frm,
                    "cnt_eff_to": cnt_eff_to,
                    "cnt_sign_frm": cnt_sign_frm,
                    "cnt_sign_to": cnt_sign_to,
                    "cnt_wage_id": cnt_wage_id,
                    "cnt_wage_en": cnt_wage_en,
                    "cnt_wage_text": cnt_wage_text,
                    "cnt_wage_8hr": cnt_wage_8hr,
                    "cnt_guard_amt": cnt_guard_amt,
                    "cnt_sale_amt": cnt_sale_amt,
                    "cnt_new": cnt_new,
                    "cnt_print": cnt_print,
                    "cnt_autoexpire": cnt_autoexpire,
                    "cus_service_list": list(pickup_record),
                    "cnt_upd_flag": cnt_upd_flag
                })

                response.status_code = 200
                return response
            except CusContract.DoesNotExist:
                response = JsonResponse(data={
                    "success": True,
                    "class": "bg-danger",
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
            "class": "bg-danger",
            "message": "",
            "is_existed": False,
            "customer_not_existed": True,
            "cnt_doc_no": "",
        })
        response.status_code = 200
        return response  
        
    response = JsonResponse(data={
        "success": True,
        "class": "bg-danger",
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
    item_per_page = 30

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
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],        
        # 'cus_brn': cus_brn,
        # 'cus_vol': cus_vol
    }

    return render(request, 'contract/contract_list.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def ContractUpdate(request, pk):
    template_name = 'contract/contract_update.html'
    
    cus_contract = get_object_or_404(CusContract, pk=pk)

    if cus_contract is not None:
        cusmain = CusMain.objects.filter(cus_id=cus_contract.cus_id).get()
        customer = Customer.objects.filter(cus_id=cus_contract.cus_id, cus_brn=cus_contract.cus_brn).get()
        cus_service = CusService.objects.filter(cnt_id=cus_contract.cnt_id).exclude(upd_flag='D').order_by('-srv_active','srv_shif_id')

        cus_service_list = []
        sql = "Select a.srv_id,a.srv_shif_id,b.shf_desc,b.shf_type,a.srv_rank, c.rank_en,a.srv_eff_frm,a.srv_eff_to,a.srv_qty,"
        sql += "a.srv_mon,a.srv_tue,a.srv_wed,a.srv_thu,a.srv_fri,a.srv_sat,a.srv_sun,a.srv_pub,a.srv_rate,a.srv_cost,a.srv_cost_rate,"
        sql += "a.srv_rem,a.srv_active, a.upd_date,a.upd_by,a.upd_flag From cus_service as a left join t_shift as b on a.srv_shif_id=b.shf_id "
        sql += "left join com_rank as c on a.srv_rank=c.rank_id Where  a.upd_flag<>'D' and a.cnt_id = " + str(cus_contract.cnt_id) + " "        
        sql += "order by a.srv_active desc,b.shf_type,a.srv_rank desc;"
        print("SQL:", sql)
        try:
            with connection.cursor() as cursor:     
                cursor.execute(sql)
                cus_service_obj = cursor.fetchall()
        except db.OperationalError as e:
            is_found = False
            message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
        except db.Error as e:
            is_found = False
            message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
        finally:
            cursor.close()

        for item in cus_service_obj:
            record = {
                "srv_id": item[0],
                "srv_eff_frm": item[6],
                "srv_eff_to": item[7],
                "shf_desc": item[2],
                "srv_qty": item[8],
                "srv_rank": item[4],
                "srv_rate": item[17],
                "srv_cost": item[18],
                "srv_mon": item[9],
                "srv_tue": item[10],
                "srv_wed": item[11],
                "srv_thu": item[12],
                "srv_fri": item[13],
                "srv_sat": item[14],
                "srv_sun": item[15],
                "srv_pub": item[16],
                "srv_rem": item[20],
                "srv_active": item[21],
                "upd_date": item[22].strftime("%d/%m/%Y %H:%M:%S"),
                "upd_by": item[23],
            }
            cus_service_list.append(record)

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
        'cus_service_list': cus_service_list,
        'request': request,
        'form_is_valid': form_is_valid,
        'update_message': update_message,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],        
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
            

            cnt_doc_date_status = request.POST.get('cnt_doc_date_status')
            if cnt_doc_date_status=="0":
                cnt_doc_date = "2999-12-31"
            else:
                cnt_doc_date = request.POST.get('cnt_doc_date')
                if cnt_doc_date is not None and cnt_doc_date != "":
                    cnt_doc_date = datetime.datetime.strptime(cnt_doc_date, "%d/%m/%Y")
                else:
                    cnt_doc_date = None
                

            cnt_eff_frm_status = request.POST.get('cnt_eff_frm_status')
            if cnt_eff_frm_status=="0":
                cnt_eff_frm = "2999-12-31"
            else:
                cnt_eff_frm = request.POST.get('cnt_eff_frm')
                if cnt_eff_frm is not None and cnt_eff_frm != "":
                    cnt_eff_frm = datetime.datetime.strptime(cnt_eff_frm, "%d/%m/%Y")
                else:
                    cnt_eff_frm = None


            cnt_eff_to_status = request.POST.get('cnt_eff_to_status')
            if cnt_eff_to_status=="0":
                cnt_eff_to = "2999-12-31"
            else:
                cnt_eff_to = request.POST.get('cnt_eff_to')
                if cnt_eff_to is not None and cnt_eff_to != "":
                    cnt_eff_to = datetime.datetime.strptime(cnt_eff_to, "%d/%m/%Y")
                else:
                    cnt_eff_to = None


            cnt_sign_from_status = request.POST.get('cnt_sign_frm_status')
            if cnt_sign_from_status=="0":
                cnt_sign_frm = "2999-12-31"
            else:
                cnt_sign_frm = request.POST.get('cnt_sign_frm')
                if cnt_sign_frm is not None and cnt_sign_frm != "":
                    cnt_sign_frm = datetime.datetime.strptime(cnt_sign_frm, "%d/%m/%Y")
                else:
                    cnt_sign_frm = None

            cnt_sign_to_status = request.POST.get('cnt_sign_to_status')
            if cnt_sign_to_status=="0":
                cnt_sign_to = "2999-12-31"
            else:
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
                    response_data['result'] = "บันทึกรายการสำเร็จ"
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
    print("FUNCTION: create_contract()")
    # print("****************************")

    template_name = 'contract/contract_update.html'
    response_data = {}
    modified_records = []

    if request.method == 'POST':
        print("SaveContract - Post method")
        
        # form = ContractUpdateForm(request.POST, instance=CusContract)
        form = ContractUpdateForm(request.POST)

        if form.is_valid():
            # print("Form is valid")

            # Get values
            cus_id = request.POST.get('cus_id')
            cus_brn = request.POST.get('cus_brn')
            cus_vol = request.POST.get('cus_vol')
            cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
            cnt_active = request.POST.get('cnt_active')            
            cnt_doc_no = request.POST.get('cnt_doc_no')

            
            '''
            cnt_doc_date = request.POST.get('cnt_doc_date')
            cnt_doc_date_status = request.POST.get('cnt_doc_date_status')
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

            '''

            cnt_doc_date_status = request.POST.get('cnt_doc_date_status')
            if cnt_doc_date_status=="0":
                cnt_doc_date = "2999-12-31"
            else:
                cnt_doc_date = request.POST.get('cnt_doc_date')
                if cnt_doc_date is not None and cnt_doc_date != "":
                    cnt_doc_date = datetime.datetime.strptime(cnt_doc_date, "%d/%m/%Y")
                else:
                    cnt_doc_date = None
                

            cnt_eff_frm_status = request.POST.get('cnt_eff_frm_status')
            if cnt_eff_frm_status=="0":
                cnt_eff_frm = "2999-12-31"
            else:
                cnt_eff_frm = request.POST.get('cnt_eff_frm')
                if cnt_eff_frm is not None and cnt_eff_frm != "":
                    cnt_eff_frm = datetime.datetime.strptime(cnt_eff_frm, "%d/%m/%Y")
                else:
                    cnt_eff_frm = None


            cnt_eff_to_status = request.POST.get('cnt_eff_to_status')
            if cnt_eff_to_status=="0":
                cnt_eff_to = "2999-12-31"
            else:
                cnt_eff_to = request.POST.get('cnt_eff_to')
                if cnt_eff_to is not None and cnt_eff_to != "":
                    cnt_eff_to = datetime.datetime.strptime(cnt_eff_to, "%d/%m/%Y")
                else:
                    cnt_eff_to = None


            cnt_sign_from_status = request.POST.get('cnt_sign_frm_status')
            if cnt_sign_from_status=="0":
                cnt_sign_frm = "2999-12-31"
            else:
                cnt_sign_frm = request.POST.get('cnt_sign_frm')
                if cnt_sign_frm is not None and cnt_sign_frm != "":
                    cnt_sign_frm = datetime.datetime.strptime(cnt_sign_frm, "%d/%m/%Y")
                else:
                    cnt_sign_frm = None

            cnt_sign_to_status = request.POST.get('cnt_sign_to_status')
            if cnt_sign_to_status=="0":
                cnt_sign_to = "2999-12-31"
            else:
                cnt_sign_to = request.POST.get('cnt_sign_to')
                if cnt_sign_to is not None and cnt_sign_to != "":
                    cnt_sign_to = datetime.datetime.strptime(cnt_sign_to, "%d/%m/%Y")
                else:
                    cnt_sign_to = None


            cnt_apr_by = request.POST.get('cnt_apr_by_id')


            cnt_guard_amt = request.POST.get('cnt_guard_amt')
            if cnt_guard_amt == "":
                cnt_guard_amt = 0
            else:
                cnt_guard_amt = int(cnt_guard_amt)

            cnt_sale_amt = request.POST.get('cnt_sale_amt').replace(",", "")
            
            if cnt_sale_amt == "":
                cnt_sale_amt = 0
            else:
                cnt_sale_amt = float(cnt_sale_amt)


            cnt_wage_id = request.POST.get('cnt_wage_id')
            # ironman
            is_cnt_wage_id_found = False
            current_wage_id_list = TWagezone.objects.all().filter(w2004=1)            
            if current_wage_id_list is not None:                
                for item in current_wage_id_list:
                    print(item.wage_id)
                    if int(cnt_wage_id) == item.wage_id:
                        is_cnt_wage_id_found = True                        

            if not is_cnt_wage_id_found:
                response_data['form_is_valid'] = False
                response_data['class'] = "bg-danger"
                response_data['message'] = "<b>รหัสค่าแรง&nbsp;&nbsp;" + cnt_wage_id + "</b><br/> เลิกใช้งานแล้ว กรุณาเลือกรหัสค่าแรงใหม่"
                return JsonResponse(response_data)

            cnt_zone_id = request.POST.get('cnt_zone_id')
            cnt_autoexpire = request.POST.get('cnt_autoexpire')
            cnt_then = request.POST.get('cnt_then')
            cnt_print = request.POST.get('cnt_print')
            cnt_new = request.POST.get('cnt_new')
            upd_date = datetime.datetime.now()
            upd_by = request.user.first_name
            upd_flag = 'E'

            '''
            print("")
            print("")
            print("----------- START ------------")
            print("cnt_active = " + str(cnt_active))
            print("cnt_doc_no = " + str(cnt_doc_no))
            print("cnt_doc_date = " + str(cnt_doc_date))
            print("cnt_doc_date_status = " + str(cnt_doc_date_status))
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
            print("cnt_zone_id =", cnt_zone_id)
            print("--------- END  ------------")
            print("")
            print("")
            '''

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

                # Cnt Zone ID
                if (cnt_zone_id is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Cnt Zone ID", int(cuscontract.cnt_zone), int(cnt_zone_id), "E", request)
                    if field_is_modified:
                        cuscontract.cnt_zone = int(cnt_zone_id)
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

                # CNT_TH_EN
                if (cnt_then is not None):
                    field_is_modified, record = check_modified_field("CUS_CONTRACT", cnt_id, "Print TH/EN", cuscontract.cnt_then, cnt_then, "E", request)
                    if field_is_modified:
                        cuscontract.cnt_then = cnt_then
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
                            log_description = cnt_id,
                            )
                        new_log.save()    
                        modified_records = []
                    # ./History Log                     

                    response_data['form_is_valid'] = True
                    response_data['result'] = "บันทึกรายการสำเร็จ"
                    response_data['class'] = "bg-success"
                else:
                    response_data['form_is_valid'] = True
                    response_data['result'] = "ยังไม่มีการแก้ไขข้อมูล"
                    response_data['class'] = "bg-warning"
               
            except CusContract.DoesNotExist:
                # Insert
                c = CusContract(
                    cnt_id = cnt_id,
                    cus_id = cus_id,
                    cus_brn = cus_brn,
                    cus_vol = cus_vol,
                    cnt_active = cnt_active,

                    cnt_eff_frm = cnt_eff_frm,
                    cnt_eff_to = cnt_eff_to,
                    
                    cnt_sign_frm = cnt_sign_frm,
                    cnt_sign_to = cnt_sign_to,
                    
                    cnt_doc_no = cnt_doc_no,
                    cnt_doc_date = cnt_doc_date,
                    cnt_apr_by_id = int(cnt_apr_by),
                    cnt_guard_amt = cnt_guard_amt,
                    cnt_sale_amt = cnt_sale_amt,
                    cnt_zone = cnt_zone_id,
                    cnt_wage_id_id = cnt_wage_id,                    
                    cnt_autoexpire = cnt_autoexpire,
                    cnt_then = 'T',
                    upd_date = datetime.datetime.now(),
                    upd_by = request.user.first_name,
                    upd_flag = 'A',

                )
                c.save()                
                response_data['form_is_valid'] = True
                response_data['result'] = "สร้างสัญญาใหม่สำเร็จ"
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


'''
@login_required(login_url='/accounts/login/')
def get_customer_list(request):

    print("****************************")
    print("FUNCTION: get_customer_list")
    print("****************************")

    item_per_page = 500
    return JsonResponse(data={"success": False, "results": ""})
'''


@login_required(login_url='/accounts/login/')
def get_contract_list(request):

    print("****************************")
    print("FUNCTION: get_contract_list")
    print("****************************")

    item_per_page = 500

    if request.method == "POST":
        # data = TDistrict.objects.filter('wage_id=current_wagerate_id')        
        sql = "SELECT cnt_id,cus_name_th,cus_name_en,b.cus_brn as cus_brn,b.cus_add1_th as cus_add1_th FROM cus_contract  as a left join customer  as b on a.cus_id=b.cus_id  and a.cus_brn=b.cus_brn WHERE not(cnt_id is null)  Order by cnt_id;"
        data = CusContract.objects.raw(sql)

        page = 1
        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))
    else:
        print("method get")

        sql = "SELECT cnt_id,cus_name_th,cus_name_en,b.cus_brn as cus_brn,b.cus_add1_th as cus_add1_th FROM cus_contract  as a left join customer  as b on a.cus_id=b.cus_id  and a.cus_brn=b.cus_brn WHERE not(cnt_id is null)  Order by cnt_id;"
        data = CusContract.objects.raw(sql)

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
                "cnt_id": d.cnt_id,
                "cus_name_th": d.cus_name_th,
                "cus_name_en": d.cus_name_en,
                "cus_brn": d.cus_brn,
                "cus_add1_th": d.cus_add1_th[0:40],
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
def get_contract_list_modal(request):

    print("**********************************")    
    print("FUNCTION: get_contract_list_modal")
    print("**********************************")

    data = []
    item_per_page = 500
    page_no = request.GET["page_no"]
    search_option = request.GET["search_option"]
    search_text = request.GET["search_text"]

    # Replace symbol character
    search_text = search_text.replace("\"", "'")

    print("page_no:", page_no)
    print("search_option:", search_option)
    print("search_text:", search_text)


    # amnaj
    if search_option == '1':    # Search by cnt_id
        # sql = "select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn where cnt_id=" + search_text        
        search_text = search_text + "%"
        data = CusContract.objects.raw('select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn where cnt_id like %s', tuple([search_text]))

    if search_option == '2':    # Search by cus_name_th
        search_text = "%" + search_text + "%"
        data = CusContract.objects.raw('select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn where cus_name_th like %s', tuple([search_text]))

    if search_option == '3':    # Search by cus_name_en
        search_text = "%" + search_text + "%"
        data = CusContract.objects.raw('select * from customer cus join cus_contract con on cus.cus_id=con.cus_id and cus.cus_brn=con.cus_brn where cus_name_en like %s', tuple([search_text]))

    if data is not None:
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
                cus_name_th = d.cus_name_th.replace("\"", "")
                cus_name_th = d.cus_name_th.replace("\'", "")
                cus_name_en = d.cus_name_en.replace("\"", "")
                cus_name_en = d.cus_name_en.replace("\'", "")
                cus_brn = d.cus_brn
                cus_add1_th = d.cus_add1_th.replace("\'", "")

                record = {
                    "cnt_id": d.cnt_id,
                    "cus_name_th": cus_name_th,
                    "cus_name_en": cus_name_en,
                    "cus_brn": cus_brn,
                    "cus_add1_th": cus_add1_th[0:40],
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
            data = CusService.objects.filter(srv_id__exact=service_id).exclude(upd_flag='D').get()

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
            
            if data.srv_cost_rate is None:
                srv_cost_rate = 0
            else:
                srv_cost_rate = data.srv_cost_rate        

            srv_cost_change = data.srv_cost_change
            op1 = data.op1
            op2 = data.op2
            op3 = data.op3
            spay1 = data.spay1
            spay2 = data.spay2
            spay3 = data.spay3
            spay4 = data.spay4

            # Get com_rank
            # comrank = ComRank.objects.all().exclude(upd_flag='D')
            comrank = ComRank.objects.all().filter(rank_type='CNT')
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
                "srv_rank": data.srv_rank_id,
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
                "srv_cost_rate": srv_cost_rate,
                "srv_cost_change": data.srv_cost_change,
                "op1": data.op1,
                "op2": data.op2,
                "op3": data.op3,
                "spay1": data.spay1,
                "spay2": data.spay2,
                "spay3": data.spay3,
                "spay4": data.spay4,
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

    srv_eff_from = datetime.datetime.strptime(request.GET["srv_eff_frm_new"], "%d/%m/%Y").date()

    srv_eff_to_new_status = request.GET["srv_eff_to_new_status"]    
    if srv_eff_to_new_status=="1":
        srv_eff_to = datetime.datetime.strptime(request.GET["srv_eff_to_new"], "%d/%m/%Y").date()
    else:
        srv_eff_to = "2999-12-31"

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

    srv_Spay1 = 0 if float(request.GET["srv_Spay1"]) <= 0 else float(request.GET["srv_Spay1"])
    srv_Spay2 = 0 if float(request.GET["srv_Spay2"]) <= 0 else float(request.GET["srv_Spay2"])
    srv_Spay3 = 0 if float(request.GET["srv_Spay3"]) <= 0 else float(request.GET["srv_Spay3"])
    srv_Spay4 = 0 if float(request.GET["srv_Spay4"]) <= 0 else float(request.GET["srv_Spay4"])

    # Change op1 status
    if (srv_Spay1<=0 and srv_Spay2<=0 and srv_Spay3<=0 and srv_Spay4<=0):
        op1_value = 0
    else:
        op1_value = 1

    # print("%s %s %s %s", srv_Spay1, srv_Spay2, srv_Spay3, srv_Spay4)
    # print("----------------------------")
    # print("cnt_id = " + str(cnt_id))
    # print("----------------------------")




    # Generate new sch_no NEW
    latest_service_number = 0
    is_error = True
    sql = "select max(right(srv_id,4)) from cus_service where cnt_id=" + str(cnt_id) + ";"
    message = ""
    try:
        with connection.cursor() as cursor:     
            cursor.execute(sql)
            cus_service_obj = cursor.fetchone()

        if cus_service_obj is not None:
            
            if cus_service_obj[0] is None:
                latest_service_number = 0
            else:
                latest_service_number = cus_service_obj[0]

            is_error = False
            message = "SUCCESS"
            print("latest_service_number = ", latest_service_number)
        else:
            latest_service_number = 0

    except db.OperationalError as e:
        is_error = True
        message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
    except db.Error as e:
        is_error = True
        message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
    finally:
        cursor.close()

    print("DEBUG: message = ", message)
    print("DEBUG: latest_service_number = ", latest_service_number)

    if not is_error:
        latest_service_number = int(latest_service_number) + 1
        new_service_number = str(cnt_id) + str(latest_service_number).zfill(5)        
    # else:
    #    new_service_number = str(cnt_id) + "00001"

    
    
    print("DEBUG: new_service_number = ", new_service_number)

    # Generate new sch_no
    '''
    latest_service_number = CusService.objects.filter(cnt_id=cnt_id).aggregate(Max('srv_id'))
    latest_service_number = latest_service_number['srv_id__max']
    if latest_service_number is not None:
        new_service_number = latest_service_number + 1
    else:
        new_service_number = str(cnt_id) + "00001"
    '''

    # print("DEBUG : latest_service_number = ", latest_service_number)
    # print("DEBUG : cnt_id = ", cnt_id)

    s = CusService(
        srv_id = new_service_number,
        cnt_id_id = cnt_id,
        srv_rank_id = srv_rank,
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
        op1 = op1_value,
        op2 = 0,
        op3 = 0,
        spay1 = srv_Spay1,
        spay2 = srv_Spay2,
        spay3 = srv_Spay3,
        spay4 = srv_Spay4,
        spay5 = 0,
        spay6 = 0,
        spay7 = 0,
        spay8 = 0,
        spay9 = 0,
    )
    s.save()

    # Recalculate cnt_guard_amt, cnt_sale_amt
    # start
    cus_service_list = CusService.objects.all().exclude(upd_flag='D').filter(cnt_id=cnt_id)
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
        "message": "บันทึกรายการสำเร็จ",
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
    # srv_eff_to = datetime.datetime.strptime(request.GET["srv_eff_to_new"], "%d/%m/%Y").date()

    srv_eff_to_status = request.GET["srv_eff_to_new_status"]
    print("srv_eff_to_status:", srv_eff_to_status)
    if srv_eff_to_status=="0":
        srv_eff_to = "2999-12-31"
    else:
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
        srv_rank_id = srv_rank,
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
    cus_service_list = CusService.objects.all().exclude(upd_flag='D').filter(cnt_id=cnt_id)
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
        "message": "บันทึกรายการสำเร็จ",
        "class": "bg-success",
        "cnt_id": cnt_id,
        "active_cnt_guard_amt": active_cnt_guard_amt,
        "active_cnt_sale_amt": active_cnt_sale_amt,        
    })

    response.status_code = 200
    return response



# Save existed service
def save_customer_service_item(request):

    print("debug...")

    srv_id = request.GET["srv_id"]
    srv_eff_from = request.GET["srv_eff_frm"]
        
    srv_eff_to_status = request.GET["srv_eff_to_status"]
    print("srv_eff_to_status:", srv_eff_to_status)

    if srv_eff_to_status=="1":
        srv_eff_to = request.GET["srv_eff_to"]        
    else:
        srv_eff_to = "31/12/2999"

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

    print("SRV_COST_RATE = ", srv_cost_rate)

    # DEMO
    # START
    '''
    spay1 = float(request.GET["spay1"])
    spay2 = float(request.GET["spay2"])
    spay3 = float(request.GET["spay3"])
    spay4 = float(request.GET["spay4"])
    '''
    # STOP


    # ACTUAL
    # START
    
    spay1 = 0
    spay2 = 0
    spay3 = 0
    spay4 = 0
    
    # STOP

    #TODO - all print below will be comment
    '''
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
    '''

    if srv_id is not None:
        try:                
            field_is_modified_count = 0
            modified_records = []
            data = CusService.objects.filter(srv_id__exact=srv_id).exclude(upd_flag='D').get()
            cnt_id = data.cnt_id_id

            # SRV_RANK
            if (srv_rank is not None):
                # print("RANK")
                # print("%s,%s", data.srv_rank_id, srv_rank)
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "Rank", str(data.srv_rank_id), srv_rank, "E", request)
                if field_is_modified:
                    data.srv_rank_id = srv_rank
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
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_ACTIVE", float(data.srv_active), float(srv_active), "E", request)
                if field_is_modified:
                    data.srv_active = srv_active
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_RATE
            if (srv_rate is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_RATE", float(data.srv_rate), float(srv_rate), "E", request)
                if field_is_modified:
                    data.srv_rate = srv_rate
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_COST
            if (srv_cost is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_COST", float(data.srv_cost), float(srv_cost), "E", request)
                if field_is_modified:
                    data.srv_cost = int(srv_qty) * float(srv_rate)
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1


            # SRV_COST_RATE
            if (srv_cost_rate is not None):
                if data.srv_cost_rate is None:
                    field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_COST_RATE", 0, float(srv_cost_rate), "E", request)
                    if field_is_modified:
                        data.srv_cost_rate = srv_cost_rate
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1
                else:                
                    field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SRV_COST_RATE", float(data.srv_cost_rate), float(srv_cost_rate), "E", request)
                    if field_is_modified:
                        data.srv_cost_rate = srv_cost_rate
                        modified_records.append(record)
                        field_is_modified_count = field_is_modified_count + 1


            # SRV_REM
            if (srv_rem is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "Remark", data.srv_rem, srv_rem, "E", request)
                if field_is_modified:
                    data.srv_rem = srv_rem
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1


            # SRV_SPECIAL_POSITION
            if (spay1 is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SPECIAL_POSITION", data.spay1, spay1, "E", request)
                if field_is_modified:
                    data.spay1 = spay1
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1                    

            # SRV_SPECIAL_INCENTIVE
            if (spay2 is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SPECIAL_INCENTIVE", data.spay2, spay2, "E", request)
                if field_is_modified:
                    data.spay2 = spay2
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_SPECIAL_CCTV
            if (spay3 is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SPECIAL_CCTV", data.spay3, spay3, "E", request)
                if field_is_modified:
                    data.spay3 = spay3
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # SRV_SPECIAL_TRAFFIC
            if (spay4 is not None):
                field_is_modified, record = check_modified_field("CUS_SERVICE", srv_id, "SPECIAL_TRAFFIC", data.spay4, spay4, "E", request)
                if field_is_modified:
                    data.spay4 = spay4
                    modified_records.append(record)
                    field_is_modified_count = field_is_modified_count + 1

            # Change op1 status
            if (spay1<=0 and spay2<=0 and spay3<=0 and spay4<=0):
                data.op1 = 0
            else:
                data.op1 = 1

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
                        log_description = cnt_id,
                        )
                    new_log.save()                
                # ./History Log                     

                # TODO
                # Recalculate cnt_guard_amt, cnt_sale_amt
                # start
                cus_service_list = CusService.objects.all().exclude(upd_flag='D').filter(cnt_id=cnt_id)
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
                    "message": "บันทึกรายการสำเร็จ",
                    "class": "bg-success",
                    "cnt_id": cnt_id,
                    "active_cnt_guard_amt": active_cnt_guard_amt,
                    "active_cnt_sale_amt": active_cnt_sale_amt,
                })            
                response.status_code = 200

            else:
                response = JsonResponse(data={
                    "success": True,
                    "cnt_id": cnt_id,
                    "message": "Sorry, nothing to update.",
                    "class": "bg-warning",
                })            
                response.status_code = 200

            return response            
        except CusService.DoesNotExist:
            response = JsonResponse(data={
                "success": False,
                "cnt_id": cnt_id,
                "message": "Service ID not found.",
                "results": [],
            })
            response.status_code = 403
            return response
    else:
        response = JsonResponse(data={
            "success": False,
            "cnt_id": cnt_id,
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
    # select * from com_rank where rank_type='CNT'    
    if request.method == "POST":
        # data = ComRank.objects.all().exclude(upd_flag='D').filter(rank_type='CNT')
        data = ComRank.objects.all().filter(rank_type='CNT')
    else:
        # data = ComRank.objects.all().exclude(upd_flag='D').filter(rank_type='CNT')
        data = ComRank.objects.all().filter(rank_type='CNT')

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

    '''
    data = CusService.objects.all().exclude(upd_flag='D').filter(cnt_id=cnt_id).order_by('-srv_active')    
    cus_service_list=[]
    for d in data:
        record = {
            "srv_id": d.srv_id,
            "cnt_id": d.cnt_id_id,
            "srv_rank": d.srv_rank_id,
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
    '''
    cus_service_list = []
    sql = "Select a.srv_id,a.srv_shif_id,b.shf_desc,b.shf_type,a.srv_rank, c.rank_en,a.srv_eff_frm,a.srv_eff_to,a.srv_qty,"
    sql += "a.srv_mon,a.srv_tue,a.srv_wed,a.srv_thu,a.srv_fri,a.srv_sat,a.srv_sun,a.srv_pub,a.srv_rate,a.srv_cost,a.srv_cost_rate,"
    sql += "a.srv_rem,a.srv_active, a.upd_date,a.upd_by,a.upd_flag,a.op1 From cus_service as a left join t_shift as b on a.srv_shif_id=b.shf_id "
    sql += "left join com_rank as c on a.srv_rank=c.rank_id Where  a.upd_flag<>'D' and a.cnt_id = " + str(cnt_id) + " "        
    sql += "order by a.srv_active desc,b.shf_type,a.srv_rank desc;"
    print("SQL11:", sql)

    try:
        with connection.cursor() as cursor:     
            cursor.execute(sql)
            cus_service_obj = cursor.fetchall()
    except db.OperationalError as e:
        is_found = False
        message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
    except db.Error as e:
        is_found = False
        message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
    finally:
        cursor.close()

    for item in cus_service_obj:
        record = {
            "srv_id": item[0],                    
            "srv_eff_frm": item[6].strftime("%d/%m/%Y"),
            "srv_eff_to": item[7].strftime("%d/%m/%Y"),
            "shf_desc": item[2],
            "srv_qty": item[8],
            "srv_rank": item[4],
            "srv_rate": item[17],
            "srv_cost": item[18],
            "srv_cost_rate": item[19],
            "srv_mon": item[9],
            "srv_tue": item[10],
            "srv_wed": item[11],
            "srv_thu": item[12],
            "srv_fri": item[13],
            "srv_sat": item[14],
            "srv_sun": item[15],
            "srv_pub": item[16],
            "srv_rem": item[20],
            "srv_active": item[21],
            "upd_date": item[22].strftime("%d/%m/%Y %H:%M:%S"),
            "upd_by": item[23],
            "op1": item[25],
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

    data = CusService.objects.exclude(upd_flag='D').filter(srv_id=srv_id).get() 
    cnt_id = data.cnt_id_id
    data.delete()

    # Recalculate cnt_guard_amt, cnt_sale_amt
    # start
    cus_service_list = CusService.objects.all().exclude(upd_flag='D').filter(cnt_id=cnt_id)
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

    # cus_service_data = CusService.objects.all().filter(cnt_id=cnt_id).delete()

    try:
        cus_service_data = CusService.objects.all().filter(cnt_id=cnt_id)
        for item in cus_service_data:
            item.upd_flag = 'D'
            item.save()
    except CusService.DoesNotExist:
        print("Contact administrator!")

    response = JsonResponse(data={
        "success": True,
        "message": "Contract ID " + str(cnt_id) + " has been deleted.",
        "class": "bg-danger",
        "cnt_id": cnt_id,
    })

    response.status_code = 200
    return response


def convert_date_english_to_thai_format(date_en_format):
    
    old_date = datetime.datetime.strptime(date_en_format, '%d %m %Y')
    day = old_date.strftime('%d')
    month = old_date.strftime('%m')
    year = old_date.strftime('%Y')
    
    print("-----------")
    print("month = " + month)
    print("-----------")

    if month == "01":
        month = "มกราคม"
    elif month == "02":
        month = "กุมภาพันธ์"
    elif month == "03":
        month = "มีนาคม"
    elif month == "04":
        month = "เมษายน"
    elif month == "05":
        month = "พฤษภาคม"
    elif month == "06":
        month = "มิถุนายน"
    elif month == "07":
        month = "กรกฎาคม"
    elif month == "08":
        month = "สิงหาคม"
    elif month == "09":
        month = "กันยายน"
    elif month == "10":
        month = "ตุลาคม"        
    elif month == "11":
        month = "พฤศจิกายน"
    elif month == "12":
        month = "ธันวาคม"
    else:
        month = "xx"

    year = int(year) + 543
    return day + " " + month + " " + str(year)


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def generate_contract_old(request, *args, **kwargs):    
    base_url = MEDIA_ROOT + '/contract/template/'

    # Identify which template to be used
    cnt_id = kwargs['cnt_id']
    language_option = kwargs['language_option']
    is_new_report = kwargs['is_new_report']
    is_amendment = kwargs['is_amendment']
    is_customer_address = kwargs['is_customer_address']

    print("-----------------------")
    print("language_option = " + str(language_option)) 
    print("is_new_report = " + str(is_new_report))
    print("is_amendment = " + str(is_amendment))
    # print("is_customer_address = " + str(is_customer_address))
    print("-----------------------")

    template_name = None
    if language_option=='T':
        if is_new_report=='1':
            if is_amendment=='1':
                print("Guarding Services Addendum - TH")                
                template_name = base_url + 'ReNC102A_TH.docx'
            else:
                print("Guarding Services - TH")                
                template_name = base_url + 'ReNC102_TH.docx'
        else:
            if is_amendment=='1':
                print("Service Agreement Amendment - TH")                
                template_name = base_url + 'ReC102A_TH.docx'
            else:
                print("Service Agreement - TH")
                template_name = base_url + 'ReC102_TH.docx' 

        # file_name = request.user.username + "_" + cnt_id + "_TH.docx"
        file_name = cnt_id + "_TH"
    else:
        if is_new_report=='1':
            if is_amendment=='1':
                print("Guarding Services Addendum - EN")
                template_name = base_url + 'ReNC102A_EN.docx'
            else:
                print("Guarding Services - EN")
                template_name = base_url + 'ReNC102_EN.docx'
        else:
            if is_amendment=='1':
                print("Service Agreement Amendment - EN")
                template_name = base_url + 'ReC102A_EN.docx'
            else:
                print("Service Agreement - EN")
                template_name = base_url + 'ReC102_EN.docx'                        

        # file_name = request.user.username + "_" + cnt_id + "_EN.docx"
        file_name = cnt_id + "_EN"


    today_date_en_format = datetime.datetime.now().strftime("%d %B %Y")
    today_date_th_format = convert_date_english_to_thai_format(datetime.datetime.now().strftime("%d %m %Y"))

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
                # get data from view V_CONTRACT
                cursor = connection.cursor()
                try:        
                    cursor.execute("select cus_name_th, cus_name_en, shf_type, shf_time_frm, shf_time_to, srv_qty, rank_th, srv_rem, srv_rate, shf_desc, rank_en from V_CONTRACT where cnt_id=" + cnt_id + " and srv_active=1 and shf_type='D' order by shf_type,srv_rank desc")
                    cus_service_list_day = cursor.fetchall()
                    count_shift_day = len(cus_service_list_day)
                    for row in cus_service_list_day:                        
                        srv_rate_day = srv_rate_day + (int(row[5]) * int(row[8])) # row[8] = srv_rate



                    cursor.execute("select cus_name_th, cus_name_en, shf_type, shf_time_frm, shf_time_to, srv_qty, rank_th, srv_rem, srv_rate, shf_desc, rank_en from V_CONTRACT where cnt_id=" + cnt_id + " and srv_active=1 and shf_type='N' order by shf_type,srv_rank desc")
                    cus_service_list_night = cursor.fetchall()
                    count_shift_night = len(cus_service_list_night)
                    for row in cus_service_list_night:
                        srv_rate_night = srv_rate_night + (int(row[5]) * int(row[8])) # row[8] = srv_rate

                finally:
                    cursor.close()
                

                for (cus_name_th, cus_name_en, shf_type, shf_time_frm,shf_time_to,srv_qty,rank_th,srv_rem,srv_rate,shf_desc,rank_en) in cus_service_list_day:
                    
                    shf_time_frm = str(shf_time_frm).zfill(4)
                    shf_time_frm = shf_time_frm[:2] + ':' + shf_time_frm[2:]
                    shf_time_to = str(shf_time_to).zfill(4)
                    shf_time_to = shf_time_to[:2] + ':' + shf_time_to[2:]

                    srv_rate_qty = '{:20,.2f}'.format(float(srv_rate * srv_qty)).strip()
                    srv_rate = '{:20,.2f}'.format(float(srv_rate)).strip()

                    record = {
                        "cus_name_th": cus_name_th,
                        "cus_name_en": cus_name_en,
                        "shf_type": shf_type,
                        "shf_time_frm": shf_time_frm,
                        "shf_time_to": shf_time_to,
                        "srv_qty": srv_qty,
                        "srv_rank_th": rank_th.strip(),
                        "srv_rank_en": rank_en.strip(),
                        "srv_rem": srv_rem,
                        "srv_rate": srv_rate,
                        "srv_rate_qty": srv_rate_qty,
                        "shf_desc": shf_desc,
                    }
                    pickup_record_day.append(record)                

                for (cus_name_th, cus_name_en, shf_type, shf_time_frm,shf_time_to,srv_qty,rank_th,srv_rem,srv_rate,shf_desc,rank_en) in cus_service_list_night: 
                    shf_time_frm = str(shf_time_frm).zfill(4)
                    shf_time_frm = shf_time_frm[:2] + ':' + shf_time_frm[2:]
                    shf_time_to = str(shf_time_to).zfill(4)
                    shf_time_to = shf_time_to[:2] + ':' + shf_time_to[2:]
                    srv_rate_qty = '{:20,.2f}'.format(float(srv_rate * srv_qty)).strip()
                    srv_rate = '{:20,.2f}'.format(float(srv_rate)).strip()
                    record = {
                        "cus_name_th": cus_name_th,
                        "cus_name_en": cus_name_en,
                        "shf_type": shf_type,
                        "shf_time_frm": str(shf_time_frm).zfill(4),
                        "shf_time_to": shf_time_to,
                        "srv_qty": srv_qty,
                        "srv_rank_th": rank_th.strip(),
                        "srv_rank_en": rank_en.strip(),
                        "srv_rem": srv_rem,
                        "srv_rate": srv_rate,
                        "srv_rate_qty": srv_rate_qty,
                        "shf_desc": shf_desc,
                    }
                    pickup_record_night.append(record)                

            except CusService.DoesNotExist:
                cus_service_list_day = []
                cus_service_list_night = []


            # TH EN Date format
            effective_from_en_format = cus_contract.cnt_eff_frm.strftime("%d %B %Y")
            effective_from_th_format = convert_date_english_to_thai_format(cus_contract.cnt_eff_frm.strftime("%d %m %Y"))            

            effective_to_en_format = cus_contract.cnt_eff_to.strftime("%d %B %Y")
            effective_to_th_format = convert_date_english_to_thai_format(cus_contract.cnt_eff_to.strftime("%d %m %Y"))

            sign_from_en_format = cus_contract.cnt_sign_frm.strftime("%d %B %Y")
            sign_from_th_format = convert_date_english_to_thai_format(cus_contract.cnt_sign_frm.strftime("%d %m %Y"))

            sign_to_en_format = cus_contract.cnt_sign_to.strftime("%d %B %Y")
            sign_to_th_format = convert_date_english_to_thai_format(cus_contract.cnt_sign_to.strftime("%d %m %Y"))

            srv_rate_total = '{:20,.2f}'.format(float(srv_rate_day + srv_rate_night))
            #srv_rate_total_th_word = "("+num2words(srv_rate_day + srv_rate_night, lang='th')+"บาทถ้วน)"
            srv_rate_total_th_word = num2words(srv_rate_day + srv_rate_night, lang='th')+"บาทถ้วน"
            srv_rate_total_en_word = num2words(srv_rate_day + srv_rate_night, lang='en').upper()
            # print("Debug : " + str(srv_rate_total_en_word))

            if customer.cus_brn==0:
                customer_id = customer.cus_id
            else:
                customer_id = str(customer.cus_id) + "-" + str(customer.cus_brn)

            context = {
                'customer': customer,
                'file_name': file_name,
                'docx_file_name': file_name+".docx",
                'pdf_file_name': file_name+".pdf",
                'template_name': template_name,
                'language_option': language_option,
                'is_new_report': is_new_report,
                'is_amendment': is_amendment,
                'cnt_id': cnt_id,               
                'cnt_doc_no': cus_contract.cnt_doc_no,
                'today_date_en_format': today_date_en_format,
                'today_date_th_format': today_date_th_format,
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

                'customer_id': customer_id,

                'customer_name_th': customer.cus_name_th,
                'customer_name_en': customer.cus_name_en,
                'customer_address_th': customer.cus_add1_th,
                'customer_address_en': customer.cus_add1_en,                
                'customer_site_th': customer.cus_add1_th,
                'customer_site_add2_th': customer.cus_add2_th,
                'customer_site_en': customer.cus_add1_en,
                'customer_site_add2_en': customer.cus_add2_en,
                'customer_site_cus_subdist_th': customer.cus_subdist_th,
                'customer_site_cus_subdist_en': customer.cus_subdist_en,
                'customer_site_cus_district_th': customer.cus_district.dist_th,
                'customer_site_cus_district_en': customer.cus_district.dist_en,
                'customer_site_cus_city_th': customer.cus_city.city_th,
                'customer_site_cus_city_en': customer.cus_city.city_en,
                'customer_site_cus_zip': customer.cus_zip,

                # 'effective_from': cus_contract.cnt_eff_frm.strftime("%d %B %Y"),
                'effective_from_en_format': effective_from_en_format,
                'effective_from_th_format': effective_from_th_format,

                # 'effective_to': cus_contract.cnt_eff_to.strftime("%d %B %Y"),
                'effective_to_en_format': effective_to_en_format,
                'effective_to_th_format': effective_to_th_format,

                # 'sign_from': cus_contract.cnt_sign_frm.strftime("%d %B %Y"),
                'sign_from_en_format': sign_from_en_format,
                'sign_from_th_format': sign_from_th_format,

                # 'sign_to': cus_contract.cnt_sign_to.strftime("%d %B %Y"),
                'sign_to_en_format': sign_to_en_format,
                'sign_to_th_format': sign_to_th_format,

                'shift_list_day': list(pickup_record_day),
                'shift_list_night': list(pickup_record_night),
                'count_shift_day': count_shift_day,
                'count_shift_night': count_shift_night,
                'total_count_shift': count_shift_day + count_shift_night,
                'srv_rate_total': srv_rate_total,
                'srv_rate_total_th_word': srv_rate_total_th_word,
                'srv_rate_total_en_word': srv_rate_total_en_word,
            }
        except CusContract.DoesNotExist:
            context = {
                'customer': "",
                'file_name': "",
                'docx_file_name': "",
                'pdf_file_name': "",
                'cnt_id': "",
                'cnt_doc_no': "",
                'today_date_en_format': today_date_en_format,
                'today_date_th_format': today_date_th_format,
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
                'docx_file_name': "",
                'pdf_file_name': "",
                'cnt_id': "",
                'cnt_doc_no': "",
                'today_date_en_format': today_date_en_format,
                'today_date_th_format': today_date_th_format,                
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
    
    tpl = DocxTemplate(template_name)
    tpl.render(context)
    tpl.save(MEDIA_ROOT + '/contract/download/' + file_name + ".docx")


    # docx2pdf
    docx_file = path.abspath("media\\contract\\download\\" + file_name + ".docx")
    pdf_file = path.abspath("media\\contract\\download\\" + file_name + ".pdf")    
    convert(docx_file, pdf_file)

    #from time import sleep
    #sleep(3)
    return FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')


    #Word
    '''
    from os import path
    from win32com.client import Dispatch
    word1 = Dispatch("Word.Application")    
    in_file = path.abspath('C:\\Test\\test.docx')
    out_file = path.abspath('C:\\Test\\1.pdf')
    doc1 = word1.Documents.Open(in_file)
    doc1.SaveAs(out_file, FileFormat=17)
    doc1.Close()
    word1.Quit()
    '''

    '''
    import pythoncom
    import win32com.client as win32
    from os import path
    pythoncom.CoInitialize()
    #word = win32.Dispatch("Word.Application")    
    word = win32.gencache.EnsureDispatch("Word.Application")
    in_file = path.abspath('C:\\Test\\test.docx')
    out_file = path.abspath('C:\\Test\\1.pdf')
    doc = word.Documents.Open(in_file)
    #doc.SaveAs(out_file, FileFormat=17)        
    #word.SaveAs("C:\\Test\\MyFile.html", FileFormat=8)
    #doc.Close()
    word.Quit()
    '''

    
    '''
    from win32com.client import Dispatch
    myWord = Dispatch('Word.Application')
    myWord.Visible = 1
    in_file = path.abspath('C:\\Test\\test.docx')
    new_file = path.abspath('C:\\Test\\1.pdf')
    #myWord.Documents.Open(in_file, False, False, True)
    myWord = myWord.Documents.Open(FileName=wordfile, ReadOnly=True)
    myWord.ActiveDocument.SaveAs(new_file)
    myWord.Quit()
    '''



    '''
    import comtypes.client
    word = comtypes.client.CreateObject('Word.Application')
    from pathlib import Path
    in_file = Path(os.path.abspath("media\\contract\\download\\" + file_name + ".docx"))    
    with open(in_file,'rb') as doc:
        response = HttpResponse(doc.read(), content_type='application/ms-word')
        response['Content-Disposition'] = 'attachment;filename=name.docx'
        return response
    '''



    '''
    from pathlib import Path
    in_file = Path(os.path.abspath("media\\contract\\download\\" + file_name + ".docx"))    
    with open(in_file,'rb') as doc:
        response = HttpResponse(doc.read(), content_type='application/ms-word')
        response['Content-Disposition'] = 'inline; filename=name.pdf'
        return response
    '''

    '''
    #import win32com.client as win32
    #word = win32.gencache.EnsureDispatch('Word.Application')
    import comtypes.client
    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False
    in_file = 'C:/hrms/media/contract/download/test.docx'
    doc = word.Documents.Open(in_file)
    doc.SaveAs('C:/hrms/media/contract/download/test1.docx')
    '''

    '''
    from pathlib import Path
    from time import sleep
    import comtypes.client
    #import win32com.client as win32
    wdFormatPDF = 17
    in_file = Path(os.path.abspath("media\\contract\\download\\" + file_name + ".docx"))
    out_file = Path(os.path.abspath("media\\contract\\download\\" + file_name + ".pdf"))    
    #word = win32.gencache.EnsureDispatch('Word.Application')
    word = comtypes.client.CreateObject('Word.Application')
    #word.Visible = False
    #sleep(3)
    #doc = word.Documents.Open(in_file)
    #doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    #doc.Close()
    #doc.Quit()
    '''

    '''
    file_name = 'test'
    wdFormatPDF = 17
    in_file = Path(os.path.abspath("media\\contract\\download\\" + file_name + ".docx"))
    in_file = 'C:/hrms/media/contract/download/test.docx'
    out_file = 'C:/hrms/media/contract/download/test.pdf'
    word = win32.gencache.EnsureDispatch('Word.Application')
    word.Visible = 0
    doc = word.Documents.Open(in_file, ReadOnly = 1)
    doc.SaveAs(out_file, FileFormat = 17)
    '''



    '''
    import win32com.client
    import win32com.client as win32
    from pathlib import Path
    #path_file_name = "C:\hrms\media\contract\download\test.docx"
    path_file_name= Path(os.path.abspath("media\\contract\\download\\" + "test.docx")),
    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(path_file_name )
    '''    


    '''
    doc.Activate()
    word.ActiveDocument.TrackRevisions = False  # Maybe not need this (not really but why not)
    word.ActiveDocument.Revisions.AcceptAll()
    if word.ActiveDocument.Comments.Count >= 1:
        word.ActiveDocument.DeleteAllComments()
    word.ActiveDocument.Save()
    doc.Close(False)
    word.Application.Quit()
    '''
    
    # docx2pdf
    '''
    from docx2pdf import convert
    docx_file_name = MEDIA_ROOT + "/contract/download/" + file_name + ".docx"
    pdf_file_name = MEDIA_ROOT + "/contract/download/" + file_name + ".pdf"    
    print("pdf_file_name = " + str(pdf_file_name))
    convert(docx_file_name)
    '''

    # comtypes
    '''
    wdFormatPDF = 17
    in_file = MEDIA_ROOT + "/contract/download/" + file_name + ".docx"
    # in_file = "C:/hrms/media/contract/download/" + file_name + ".docx"
    print("in_file = " + str(in_file))
    out_file = MEDIA_ROOT + "/contract/download/" + file_name + ".pdf"
    # out_file = "C:/hrms/media/contract/download/" + file_name + ".pdf"
    print("out_file = " + str(out_file))
    # word = comtypes.client.CreateObject('Word.Application')
    word = win32com.client.DispatchEx("Word.Application")
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()
    '''

    '''
    import comtypes.client
    from win32com import client
    wdFormatPDF = 17
    in_file = os.path.abspath("media\\contract\\download\\" + file_name + ".docx")
    out_file = os.path.abspath("media\\contract\\download\\" + file_name + ".pdf")
    print("in_file = " + in_file)
    print("out_file = " + out_file)
    #word = comtypes.client.CreateObject('Word.Application')    
    #word = client.Dispatch("Word.Application")
    #word = client.DispatchEx("Word.Application")
    #doc = word.Documents.Open(in_file)
    #doc.SaveAs(out_file, FileFormat=17)
    #doc.Close()
    word.Quit()
    '''
    
    # pywin32
    '''
    from win32com import client
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    wdFormatPDF = 17
    in_file = os.path.abspath("media\\contract\\download\\" + file_name + ".docx")
    out_file = os.path.abspath("media\\contract\\download\\" + file_name + ".pdf")
    word = comtypes.client.CreateObject('Word.Application')
    '''

    # comtypes
    # from pathlib import Path
    #import comtypes.client
    #import win32com.client
    #from win32com import client
    #import win32com.client as win32
    #from win32com.client import Dispatch

    '''
    import win32com.client as win32
    file_name = 'test'
    wdFormatPDF = 17
    in_file = Path(os.path.abspath("media\\contract\\download\\" + file_name + ".docx"))
    in_file = 'C:/hrms/media/contract/download/test.docx'
    out_file = 'C:/hrms/media/contract/download/test.pdf'
    word = win32.gencache.EnsureDispatch('Word.Application')
    word.Visible = 0
    doc = word.Documents.Open(in_file, ReadOnly = 1)
    doc.SaveAs(out_file, FileFormat = 17)
    '''

    '''
    #if in_file.is_file():
    #    word = win32.gencache.EnsureDispatch('Word.Application')
    #    word.Visible = 0
    #    doc = word.Documents.Open(in_file)
    #else:
    #    print("test")
    '''
   

    '''    
    word.Visible = False
    wdFormatPDF = 17
    in_file = os.path.abspath("media\\contract\\download\\" + file_name + ".docx")    
    out_file = os.path.abspath("media\\contract\\download\\" + file_name + ".pdf")
    doc = word.Documents.Open(in_file)
    #doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    #doc.Close()
    #word.Quit()
    '''

    return render(request, 'contract/generate_contract.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def download_contract(request, *args, **kwargs):    
    base_url = MEDIA_ROOT + '/contract/template/'

    # Identify which template to be used
    cnt_id = kwargs['cnt_id']
    language_option = kwargs['language_option']
    is_new_report = kwargs['is_new_report']
    is_amendment = kwargs['is_amendment']
    is_customer_address = kwargs['is_customer_address']

    '''
    print("-----------------------")
    print("language_option = " + str(language_option)) 
    print("is_new_report = " + str(is_new_report))
    print("is_amendment = " + str(is_amendment))
    # print("is_customer_address = " + str(is_customer_address))
    print("-----------------------")
    '''

    if len(cnt_id)>=13:
        cnt_id = cnt_id[3:13]

    template_name = None
    if language_option=='T':
        if is_new_report=='1':
            if is_amendment=='1':
                print("Guarding Services Addendum - TH")                
                template_name = base_url + 'ReNC102A_TH.docx'
            else:
                print("Guarding Services - TH")                
                template_name = base_url + 'ReNC102_TH.docx'
        else:
            if is_amendment=='1':
                print("Service Agreement Amendment - TH")                
                template_name = base_url + 'ReC102A_TH.docx'
            else:
                print("Service Agreement - TH")
                template_name = base_url + 'ReC102_TH.docx' 

        # file_name = request.user.username + "_" + cnt_id + "_TH.docx"
        file_name = cnt_id + "_TH"
    else:
        if is_new_report=='1':
            if is_amendment=='1':
                print("Guarding Services Addendum - EN")
                template_name = base_url + 'ReNC102A_EN.docx'
            else:
                print("Guarding Services - EN")
                template_name = base_url + 'ReNC102_EN.docx'
        else:
            if is_amendment=='1':
                print("Service Agreement Amendment - EN")
                template_name = base_url + 'ReC102A_EN.docx'
            else:
                print("Service Agreement - EN")
                template_name = base_url + 'ReC102_EN.docx'                        

        # file_name = request.user.username + "_" + cnt_id + "_EN.docx"
        file_name = cnt_id + "_EN"


    today_date_en_format = datetime.datetime.now().strftime("%d %B %Y")
    today_date_th_format = convert_date_english_to_thai_format(datetime.datetime.now().strftime("%d %m %Y"))

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
                # get data from view V_CONTRACT
                cursor = connection.cursor()
                try:        
                    cursor.execute("select cus_name_th, cus_name_en, shf_type, shf_time_frm, shf_time_to, srv_qty, rank_th, srv_rem, srv_rate, shf_desc, rank_en from V_CONTRACT where cnt_id=" + cnt_id + " and srv_active=1 and shf_type='D' order by cnt_id, shf_type, rank_grd")
                    cus_service_list_day = cursor.fetchall()
                    count_shift_day = len(cus_service_list_day)
                    for row in cus_service_list_day:                        
                        srv_rate_day = srv_rate_day + (float(row[5]) * float(row[8])) # row[8] = srv_rate



                    cursor.execute("select cus_name_th, cus_name_en, shf_type, shf_time_frm, shf_time_to, srv_qty, rank_th, srv_rem, srv_rate, shf_desc, rank_en from V_CONTRACT where cnt_id=" + cnt_id + " and srv_active=1 and shf_type='N' order by cnt_id, shf_type, rank_grd")
                    cus_service_list_night = cursor.fetchall()
                    count_shift_night = len(cus_service_list_night)
                    for row in cus_service_list_night:
                        srv_rate_night = srv_rate_night + (float(row[5]) * float(row[8])) # row[8] = srv_rate

                finally:
                    cursor.close()
                

                for (cus_name_th, cus_name_en, shf_type, shf_time_frm,shf_time_to,srv_qty,rank_th,srv_rem,srv_rate,shf_desc,rank_en) in cus_service_list_day:
                    
                    shf_time_frm = str(shf_time_frm).zfill(4)
                    shf_time_frm = shf_time_frm[:2] + ':' + shf_time_frm[2:]
                    shf_time_to = str(shf_time_to).zfill(4)
                    shf_time_to = shf_time_to[:2] + ':' + shf_time_to[2:]

                    srv_rate_qty = '{:20,.2f}'.format(float(srv_rate * srv_qty)).strip()
                    srv_rate = '{:20,.2f}'.format(float(srv_rate)).strip()

                    record = {
                        "cus_name_th": cus_name_th,
                        "cus_name_en": cus_name_en,
                        "shf_type": shf_type,
                        "shf_time_frm": shf_time_frm,
                        "shf_time_to": shf_time_to,
                        "srv_qty": srv_qty,
                        "srv_rank_th": rank_th.strip(),
                        "srv_rank_en": rank_en.strip(),
                        "srv_rem": srv_rem,
                        "srv_rate": srv_rate,
                        "srv_rate_qty": srv_rate_qty,
                        "shf_desc": shf_desc,
                    }
                    pickup_record_day.append(record)                

                for (cus_name_th, cus_name_en, shf_type, shf_time_frm,shf_time_to,srv_qty,rank_th,srv_rem,srv_rate,shf_desc,rank_en) in cus_service_list_night: 
                    shf_time_frm = str(shf_time_frm).zfill(4)
                    shf_time_frm = shf_time_frm[:2] + ':' + shf_time_frm[2:]
                    shf_time_to = str(shf_time_to).zfill(4)
                    shf_time_to = shf_time_to[:2] + ':' + shf_time_to[2:]
                    srv_rate_qty = '{:20,.2f}'.format(float(srv_rate * srv_qty)).strip()
                    srv_rate = '{:20,.2f}'.format(float(srv_rate)).strip()
                    record = {
                        "cus_name_th": cus_name_th,
                        "cus_name_en": cus_name_en,
                        "shf_type": shf_type,
                        "shf_time_frm": str(shf_time_frm).zfill(4),
                        "shf_time_to": shf_time_to,
                        "srv_qty": srv_qty,
                        "srv_rank_th": rank_th.strip(),
                        "srv_rank_en": rank_en.strip(),
                        "srv_rem": srv_rem,
                        "srv_rate": srv_rate,
                        "srv_rate_qty": srv_rate_qty,
                        "shf_desc": shf_desc,
                    }
                    pickup_record_night.append(record)                

            except CusService.DoesNotExist:
                cus_service_list_day = []
                cus_service_list_night = []


            # TH EN Date format
            effective_from_en_format = cus_contract.cnt_eff_frm.strftime("%d %B %Y")
            effective_from_th_format = convert_date_english_to_thai_format(cus_contract.cnt_eff_frm.strftime("%d %m %Y"))            

            effective_to_en_format = cus_contract.cnt_eff_to.strftime("%d %B %Y")
            effective_to_th_format = convert_date_english_to_thai_format(cus_contract.cnt_eff_to.strftime("%d %m %Y"))

            sign_from_en_format = cus_contract.cnt_sign_frm.strftime("%d %B %Y")
            sign_from_th_format = convert_date_english_to_thai_format(cus_contract.cnt_sign_frm.strftime("%d %m %Y"))

            sign_to_en_format = cus_contract.cnt_sign_to.strftime("%d %B %Y")
            sign_to_th_format = convert_date_english_to_thai_format(cus_contract.cnt_sign_to.strftime("%d %m %Y"))

            srv_rate_total = '{:20,.2f}'.format(float(srv_rate_day + srv_rate_night))
            #srv_rate_total_th_word = "("+num2words(srv_rate_day + srv_rate_night, lang='th')+"บาทถ้วน)"
            srv_rate_total_th_word = num2words(srv_rate_day + srv_rate_night, lang='th')+"บาทถ้วน"
            #srv_rate_total_en_word = num2words(srv_rate_day + srv_rate_night, lang='en')
            srv_rate_total_en_word = num2words(srv_rate_day + srv_rate_night, lang='en').upper()
            
            if customer.cus_brn==0:
                customer_id = customer.cus_id
            else:
                customer_id = str(customer.cus_id) + "-" + str(customer.cus_brn)

            print("file_name:", file_name)

            context = {
                'customer': customer,
                'file_name': file_name,
                'docx_file_name': file_name+".docx",
                'pdf_file_name': file_name+".pdf",
                'template_name': template_name,
                'language_option': language_option,
                'is_new_report': is_new_report,
                'is_amendment': is_amendment,
                'cnt_id': cnt_id,               
                'cnt_doc_no': cus_contract.cnt_doc_no,
                'today_date_en_format': today_date_en_format,
                'today_date_th_format': today_date_th_format,
                'cusbill_name_th': cusbill.cus_name_th,
                'cusbill_name_en': cusbill.cus_name_en,
                'cusbill_address_th': cusbill.cus_add1_th,
                'cusbill_address2_th': cusbill.cus_add2_th,
                'cusbill_address_en': cusbill.cus_add1_en,
                'cusbill_address2_en': cusbill.cus_add2_en,               
                'cusbill_site_th': cusbill.cus_add1_th,
                'cusbill_site_en': cusbill.cus_add1_en,
                'cusbill_site_cus_subdist_th': cusbill.cus_subdist_th,
                'cusbill_site_cus_subdist_en': cusbill.cus_subdist_en,

                'cusbill_site_cus_district_th': cusbill.cus_district.dist_th,
                'cusbill_site_cus_district_en': cusbill.cus_district.dist_en,

                'cusbill_site_cus_city_th': cusbill.cus_city.city_th,
                'cusbill_site_cus_city_en': cusbill.cus_city.city_en,

                'cusbill_site_cus_zip': cusbill.cus_zip,

                'customer_id': customer_id,
                'customer_name_th': customer.cus_name_th,
                'customer_name_en': customer.cus_name_en,
                'customer_address_th': customer.cus_add1_th,
                'customer_site_add2_th': customer.cus_add2_th,
                'customer_address_en': customer.cus_add1_en,                
                'customer_site_add2_en': customer.cus_add2_en,
                'customer_site_th': customer.cus_add1_th,
                'customer_site_en': customer.cus_add1_en,
                'customer_site_cus_subdist_th': customer.cus_subdist_th,
                'customer_site_cus_subdist_en': customer.cus_subdist_en,
                'customer_site_cus_district_th': customer.cus_district.dist_th,
                'customer_site_cus_district_en': customer.cus_district.dist_en,
                'customer_site_cus_city_th': customer.cus_city.city_th,
                'customer_site_cus_city_en': customer.cus_city.city_en,
                'customer_site_cus_zip': customer.cus_zip,

                # 'effective_from': cus_contract.cnt_eff_frm.strftime("%d %B %Y"),
                'effective_from_en_format': effective_from_en_format,
                'effective_from_th_format': effective_from_th_format,

                # 'effective_to': cus_contract.cnt_eff_to.strftime("%d %B %Y"),
                'effective_to_en_format': effective_to_en_format,
                'effective_to_th_format': effective_to_th_format,

                # 'sign_from': cus_contract.cnt_sign_frm.strftime("%d %B %Y"),
                'sign_from_en_format': sign_from_en_format,
                'sign_from_th_format': sign_from_th_format,

                # 'sign_to': cus_contract.cnt_sign_to.strftime("%d %B %Y"),
                'sign_to_en_format': sign_to_en_format,
                'sign_to_th_format': sign_to_th_format,

                'shift_list_day': list(pickup_record_day),
                'shift_list_night': list(pickup_record_night),
                'count_shift_day': count_shift_day,
                'count_shift_night': count_shift_night,
                'total_count_shift': count_shift_day + count_shift_night,
                'srv_rate_total': srv_rate_total,
                'srv_rate_total_th_word': srv_rate_total_th_word,
                'srv_rate_total_en_word': srv_rate_total_en_word,                
            }
        except CusContract.DoesNotExist:
            context = {
                'customer': "",
                'file_name': "",
                'docx_file_name': "",
                'pdf_file_name': "",
                'cnt_id': "",
                'cnt_doc_no': "",
                'today_date_en_format': today_date_en_format,
                'today_date_th_format': today_date_th_format,
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
                'docx_file_name': "",
                'pdf_file_name': "",
                'cnt_id': "",
                'cnt_doc_no': "",
                'today_date_en_format': today_date_en_format,
                'today_date_th_format': today_date_th_format,                
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
    
    tpl = DocxTemplate(template_name)
    tpl.render(context)
    tpl.save(MEDIA_ROOT + '/contract/download/' + file_name + ".docx")

    in_file = os.path.abspath("media\\contract\\download\\" + file_name + ".docx")
    with open(in_file,'rb') as doc:
        response = HttpResponse(doc.read(), content_type='application/ms-word')
        response['Content-Disposition'] = 'attachment;filename=' + file_name + '.docx'
        return response
    

@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def print_contract(request, *args, **kwargs):
    print("print_contract()")

    file_name = kwargs['file_name']
    # file_name = "test.pdf"
    file_path = "media/contract/download/" + file_name

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

    raise Http404






@login_required(login_url='/accounts/login/')
def ajax_undelete_contract(request):
    cnt_id = request.POST.get('cnt_id')

    print("cnt_id = " + str(cnt_id))


    try:
        cus_contract = CusContract.objects.get(cnt_id=cnt_id)
        cus_contract.upd_flag = 'R'
        cus_contract.save()

        new_log = HrmsNewLog(
            log_table = "cus_contract",
            log_key = cnt_id,
            log_field = "upd_flag",
            old_value = "D",
            new_value = "R",
            log_type = "R",
            log_by = request.user.first_name,
            log_date = datetime.datetime.now(),
            )
        new_log.save()   

    except CusContract.DoesNotExist:
        print("not saved")
        cus_service = None

    response = JsonResponse({
        "success": "Form is valid", 
        })

    response.status_code = 200
    return response   




@login_required(login_url='/accounts/login/')
@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def generate_contract(request, *args, **kwargs):    
    base_url = MEDIA_ROOT + '/contract/template/'

    # Identify which template to be used
    cnt_id = kwargs['cnt_id']
    language_option = kwargs['language_option']
    is_new_report = kwargs['is_new_report']
    is_amendment = kwargs['is_amendment']
    is_customer_address = kwargs['is_customer_address']

    '''
    print("-----------------------")
    print("language_option = " + str(language_option)) 
    print("is_new_report = " + str(is_new_report))
    print("is_amendment = " + str(is_amendment))
    print("-----------------------")
    '''

    template_name = None
    if language_option=='T':
        if is_new_report=='1':
            if is_amendment=='1':
                print("Guarding Services Addendum - TH")                
                template_name = base_url + 'ReNC102A_TH.docx'
            else:
                print("Guarding Services - TH")                
                template_name = base_url + 'ReNC102_TH.docx'
        else:
            if is_amendment=='1':
                print("Service Agreement Amendment - TH")                
                template_name = base_url + 'ReC102A_TH.docx'
            else:
                print("Service Agreement - TH")
                template_name = base_url + 'ReC102_TH.docx' 

        # file_name = request.user.username + "_" + cnt_id + "_TH.docx"
        file_name = cnt_id + "_TH"
    else:
        if is_new_report=='1':
            if is_amendment=='1':
                print("Guarding Services Addendum - EN")
                template_name = base_url + 'ReNC102A_EN.docx'
            else:
                print("Guarding Services - EN")
                template_name = base_url + 'ReNC102_EN.docx'
        else:
            if is_amendment=='1':
                print("Service Agreement Amendment - EN")
                template_name = base_url + 'ReC102A_EN.docx'
            else:
                print("Service Agreement - EN")
                template_name = base_url + 'ReC102_EN.docx'                        

        file_name = cnt_id + "_EN"


    today_date_en_format = datetime.datetime.now().strftime("%d %B %Y")
    today_date_th_format = convert_date_english_to_thai_format(datetime.datetime.now().strftime("%d %m %Y"))

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
                # get data from view V_CONTRACT
                cursor = connection.cursor()
                try:        
                    cursor.execute("select cus_name_th, cus_name_en, shf_type, shf_time_frm, shf_time_to, srv_qty, rank_th, srv_rem, srv_rate, shf_desc, rank_en from V_CONTRACT where cnt_id=" + cnt_id + " and srv_active=1 and shf_type='D' order by cnt_id, shf_type, rank_grd")
                    cus_service_list_day = cursor.fetchall()
                    count_shift_day = len(cus_service_list_day)
                    for row in cus_service_list_day:                        
                        srv_rate_day = srv_rate_day + (float(row[5]) * float(row[8])) # row[8] = srv_rate

                    cursor.execute("select cus_name_th, cus_name_en, shf_type, shf_time_frm, shf_time_to, srv_qty, rank_th, srv_rem, srv_rate, shf_desc, rank_en from V_CONTRACT where cnt_id=" + cnt_id + " and srv_active=1 and shf_type='N' order by cnt_id, shf_type, rank_grd")
                    cus_service_list_night = cursor.fetchall()
                    count_shift_night = len(cus_service_list_night)
                    for row in cus_service_list_night:
                        srv_rate_night = srv_rate_night + (float(row[5]) * float(row[8])) # row[8] = srv_rate

                finally:
                    cursor.close()
                

                for (cus_name_th, cus_name_en, shf_type, shf_time_frm,shf_time_to,srv_qty,rank_th,srv_rem,srv_rate,shf_desc,rank_en) in cus_service_list_day:
                    
                    shf_time_frm = str(shf_time_frm).zfill(4)
                    shf_time_frm = shf_time_frm[:2] + ':' + shf_time_frm[2:]
                    shf_time_to = str(shf_time_to).zfill(4)
                    shf_time_to = shf_time_to[:2] + ':' + shf_time_to[2:]

                    srv_rate_qty = '{:20,.2f}'.format(float(srv_rate * srv_qty)).strip()
                    srv_rate = '{:20,.2f}'.format(float(srv_rate)).strip()

                    record = {
                        "cus_name_th": cus_name_th,
                        "cus_name_en": cus_name_en,
                        "shf_type": shf_type,
                        "shf_time_frm": shf_time_frm,
                        "shf_time_to": shf_time_to,
                        "srv_qty": srv_qty,
                        "srv_rank_th": rank_th.strip(),
                        "srv_rank_en": rank_en.strip(),
                        "srv_rem": srv_rem,
                        "srv_rate": srv_rate,
                        "srv_rate_qty": srv_rate_qty,
                        "shf_desc": shf_desc,
                    }
                    pickup_record_day.append(record)                

                for (cus_name_th, cus_name_en, shf_type, shf_time_frm,shf_time_to,srv_qty,rank_th,srv_rem,srv_rate,shf_desc,rank_en) in cus_service_list_night: 
                    shf_time_frm = str(shf_time_frm).zfill(4)
                    shf_time_frm = shf_time_frm[:2] + ':' + shf_time_frm[2:]
                    shf_time_to = str(shf_time_to).zfill(4)
                    shf_time_to = shf_time_to[:2] + ':' + shf_time_to[2:]
                    srv_rate_qty = '{:20,.2f}'.format(float(srv_rate * srv_qty)).strip()
                    srv_rate = '{:20,.2f}'.format(float(srv_rate)).strip()
                    record = {
                        "cus_name_th": cus_name_th,
                        "cus_name_en": cus_name_en,
                        "shf_type": shf_type,
                        "shf_time_frm": str(shf_time_frm).zfill(4),
                        "shf_time_to": shf_time_to,
                        "srv_qty": srv_qty,
                        "srv_rank_th": rank_th.strip(),
                        "srv_rank_en": rank_en.strip(),
                        "srv_rem": srv_rem,
                        "srv_rate": srv_rate,
                        "srv_rate_qty": srv_rate_qty,
                        "shf_desc": shf_desc,
                    }
                    pickup_record_night.append(record)                

            except CusService.DoesNotExist:
                cus_service_list_day = []
                cus_service_list_night = []


            # TH EN Date format
            effective_from_en_format = cus_contract.cnt_eff_frm.strftime("%d %B %Y")
            effective_from_th_format = convert_date_english_to_thai_format(cus_contract.cnt_eff_frm.strftime("%d %m %Y"))            

            effective_to_en_format = cus_contract.cnt_eff_to.strftime("%d %B %Y")
            effective_to_th_format = convert_date_english_to_thai_format(cus_contract.cnt_eff_to.strftime("%d %m %Y"))

            sign_from_en_format = cus_contract.cnt_sign_frm.strftime("%d %B %Y")
            sign_from_th_format = convert_date_english_to_thai_format(cus_contract.cnt_sign_frm.strftime("%d %m %Y"))

            sign_to_en_format = cus_contract.cnt_sign_to.strftime("%d %B %Y")
            sign_to_th_format = convert_date_english_to_thai_format(cus_contract.cnt_sign_to.strftime("%d %m %Y"))
            
            srv_rate_total = '{:20,.2f}'.format(float(srv_rate_day + srv_rate_night))
            
            #srv_rate_total_th_word = "("+num2words(srv_rate_day + srv_rate_night, lang='th')+"บาทถ้วน)"
            srv_rate_total_th_word = num2words(srv_rate_day + srv_rate_night, lang='th')+"บาทถ้วน"
            srv_rate_total_en_word = num2words(srv_rate_day + srv_rate_night, lang='en').upper()
            # print("Debug : " + str(srv_rate_total_en_word))

            if customer.cus_brn==0:
                customer_id = customer.cus_id
            else:
                customer_id = str(customer.cus_id) + "-" + str(customer.cus_brn)

            context = {
                'customer': customer,
                'file_name': file_name,
                'docx_file_name': file_name+".docx",
                'pdf_file_name': file_name+".pdf",
                'template_name': template_name,
                'language_option': language_option,
                'is_new_report': is_new_report,
                'is_amendment': is_amendment,
                'cnt_id': cnt_id,               
                'cnt_doc_no': cus_contract.cnt_doc_no,
                'today_date_en_format': today_date_en_format,
                'today_date_th_format': today_date_th_format,
                'cusbill_name_th': cusbill.cus_name_th,
                'cusbill_name_en': cusbill.cus_name_en,
                'cusbill_address_th': cusbill.cus_add1_th,
                'cusbill_address2_th': cusbill.cus_add2_th,
                'cusbill_address_en': cusbill.cus_add1_en,
                'cusbill_address2_en': cusbill.cus_add2_en,
                'cusbill_site_th': cusbill.cus_add1_th,
                'cusbill_site_en': cusbill.cus_add1_en,
                'cusbill_site_cus_subdist_th': cusbill.cus_subdist_th,
                'cusbill_site_cus_subdist_en': cusbill.cus_subdist_en,

                'cusbill_site_cus_district_th': cusbill.cus_district.dist_th,
                'cusbill_site_cus_district_en': cusbill.cus_district.dist_en,

                'cusbill_site_cus_city_th': cusbill.cus_city.city_th,
                'cusbill_site_cus_city_en': cusbill.cus_city.city_en,

                'cusbill_site_cus_zip': cusbill.cus_zip,

                'customer_id': customer_id,

                'customer_name_th': customer.cus_name_th,
                'customer_name_en': customer.cus_name_en,
                'customer_address_th': customer.cus_add1_th,
                'customer_address_en': customer.cus_add1_en,                
                'customer_site_th': customer.cus_add1_th,
                'customer_site_add2_th': customer.cus_add2_th,
                'customer_site_en': customer.cus_add1_en,
                'customer_site_add2_en': customer.cus_add2_en,
                'customer_site_cus_subdist_th': customer.cus_subdist_th,
                'customer_site_cus_subdist_en': customer.cus_subdist_en,
                'customer_site_cus_district_th': customer.cus_district.dist_th,
                'customer_site_cus_district_en': customer.cus_district.dist_en,
                'customer_site_cus_city_th': customer.cus_city.city_th,
                'customer_site_cus_city_en': customer.cus_city.city_en,
                'customer_site_cus_zip': customer.cus_zip,

                # 'effective_from': cus_contract.cnt_eff_frm.strftime("%d %B %Y"),
                'effective_from_en_format': effective_from_en_format,
                'effective_from_th_format': effective_from_th_format,

                # 'effective_to': cus_contract.cnt_eff_to.strftime("%d %B %Y"),
                'effective_to_en_format': effective_to_en_format,
                'effective_to_th_format': effective_to_th_format,

                # 'sign_from': cus_contract.cnt_sign_frm.strftime("%d %B %Y"),
                'sign_from_en_format': sign_from_en_format,
                'sign_from_th_format': sign_from_th_format,

                # 'sign_to': cus_contract.cnt_sign_to.strftime("%d %B %Y"),
                'sign_to_en_format': sign_to_en_format,
                'sign_to_th_format': sign_to_th_format,

                'shift_list_day': list(pickup_record_day),
                'shift_list_night': list(pickup_record_night),
                'count_shift_day': count_shift_day,
                'count_shift_night': count_shift_night,
                'total_count_shift': count_shift_day + count_shift_night,
                'srv_rate_total': srv_rate_total,
                'srv_rate_total_th_word': srv_rate_total_th_word,
                'srv_rate_total_en_word': srv_rate_total_en_word,
            }
        except CusContract.DoesNotExist:
            context = {
                'customer': "",
                'file_name': "",
                'docx_file_name': "",
                'pdf_file_name': "",
                'cnt_id': "",
                'cnt_doc_no': "",
                'today_date_en_format': today_date_en_format,
                'today_date_th_format': today_date_th_format,
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
                'docx_file_name': "",
                'pdf_file_name': "",
                'cnt_id': "",
                'cnt_doc_no': "",
                'today_date_en_format': today_date_en_format,
                'today_date_th_format': today_date_th_format,                
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
    
    tpl = DocxTemplate(template_name)
    tpl.render(context)
    tpl.save(MEDIA_ROOT + '/contract/download/' + file_name + ".docx")

    # docx2pdf
    docx_file = path.abspath("media\\contract\\download\\" + file_name + ".docx")
    pdf_file = path.abspath("media\\contract\\download\\" + file_name + ".pdf")    
    convert(docx_file, pdf_file)

    return FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')



@permission_required('contract.view_cuscontract', login_url='/accounts/login/')
def ajax_sp_adjust_new_price(request):
    print("******************************************")
    print("FUNCTION: ajax_sp_adjust_new_price()")
    print("******************************************")
            
    cnt_id = request.POST.get('cnt_id').strip("0")    
    adjust_price = request.POST.get('adjust_price')
    adjust_price_option = request.POST.get('adjust_price_option')
    update_by = request.user.first_name                
    effective_from = datetime.datetime.strptime(request.POST.get('effective_from'), '%d/%m/%Y').date()
    output = request.POST.get('output')
    error_message = ""
    active_cnt_guard_amt = 0
    active_cnt_sale_amt = 0

    if adjust_price_option=="1":
        adjust_price = -abs(float(adjust_price))

    print(cnt_id, adjust_price, update_by, effective_from, output)
    # exec UPDATE_HRMS_PRICE '1486000001', 10, 'Test', '2021-05-03', 1;

    try:
        cursor = connection.cursor()
        cursor.execute("exec dbo.UPDATE_HRMS_PRICE %s, %s, %s, %s, %s", [cnt_id, adjust_price, update_by, effective_from, output])
        is_error = False
        error_message = "ปรับรายการเป็นราคาใหม่สำเร็จ"


        cus_service_list = CusService.objects.all().exclude(upd_flag='D').filter(cnt_id=cnt_id)
        active_cnt_guard_amt = 0
        active_cnt_sale_amt = 0
        for item in cus_service_list:
            if item.srv_active:                        
                active_cnt_guard_amt += item.srv_qty
                active_cnt_sale_amt += item.srv_rate * item.srv_qty
    except db.OperationalError as e:
        is_error = False
        error_message = "exec UPDATE_HRMS_PRICE is error - " + str(e)
        return is_error, error_message
    except db.Error as e:
        is_error = True
        error_message = "exec UPDATE_HRMS_PRICE is error - " + str(e)
        return is_error, error_message

    print("AA : ", active_cnt_sale_amt)
    response = JsonResponse(data={"success": True, "is_error": False, "class": "bg-success", "error_message": error_message, "active_cnt_guard_amt": active_cnt_guard_amt, "active_cnt_sale_amt": active_cnt_sale_amt})
    response.status_code = 200  
    return response


