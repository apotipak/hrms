from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import generic
from .models import Customer, CusMain, CusBill, CustomerOption
from system.models import HrmsNewLog
from .forms import CustomerCreateForm, CusMainForm, CusSiteForm, CusBillForm, CusAllTabsForm
from .forms import CustomerCodeCreateForm
from .forms import CustomerSearchForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from system.models import TDistrict, TCity, CusContact
from django.core import serializers
from decimal import Decimal
import json
import sys, locale

@login_required(login_url='/accounts/login/')
@permission_required('customer.view_customer', login_url='/accounts/login/')
def CustomerCreate(request):
    template_name = 'customer/customer_create.html'
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    today_date = settings.TODAY_DATE
    response_data = dict()

    if request.method == "POST":
        print("POST: CustomerCreate()")
        if form.is_valid():          
            cus_site_form = CusSiteCreateForm(request.POST, user=request.user)
            response_data['form_is_valid'] = True            
        else:            
            response_data['form_is_valid'] = False

        return JsonResponse(response_data)     
    else:
        print("GET: CustomerCreate()")
        customer_code_create_form = CustomerCodeCreateForm()
        

    return render(request, 'customer/customer_create.html', 
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'customer_code_create_form': customer_code_create_form,
        })



@login_required(login_url='/accounts/login/')
def ajax_check_exist_cus_main(request):

    print("************************************************")
    print("FUNCTION: ajax_check_exist_cus_main")
    print("************************************************")

    response_data = {}

    if request.method == "POST":
        cus_id = request.POST.get('cus_id')
        cus_brn = request.POST.get('cus_brn')        

        form = CustomerCodeCreateForm(request.POST)        
        pickup_records=[]
        group_id =  []
        business_type_list = []
        group_1_list = []
        group_2_list = []
        customer_option = []

        if form.is_valid():
            try:                
                cus_main = CusMain.objects.get(pk=cus_id)
                
                if cus_main:

                    if not cus_main.cus_district:
                        cus_main_cus_district_th = None
                        cus_main_cus_district_en = None
                    else:
                        cus_main_cus_district_th = cus_main.cus_district.dist_th
                        cus_main_cus_district_en = cus_main.cus_district.dist_en

                    if not cus_main.cus_city:
                        cus_main_cus_city_th = None
                        cus_main_cus_city_en = None
                    else:
                        cus_main_cus_city_th = cus_main.cus_city.city_th
                        cus_main_cus_city_en = cus_main.cus_city.city_en

                    if not cus_main.cus_country:
                        cus_main_cus_country_th = None
                        cus_main_cus_country_en = None
                    else:
                        cus_main_cus_country_th = cus_main.cus_country.country_th
                        cus_main_cus_country_en = cus_main.cus_country.country_en

                    if not cus_main.cus_contact_id:
                        cus_main_cus_contact_title_th = ""
                        cus_main_cus_contact_fname_th = ""
                        cus_main_cus_contact_lname_th = ""
                        cus_main_cus_contact_position_th = "" 
                    else:
                        cus_main_cus_contact_title_th = cus_main.cus_contact.con_title.title_th
                        cus_main_cus_contact_fname_th = cus_main.cus_contact.con_fname_th
                        cus_main_cus_contact_lname_th = cus_main.cus_contact.con_lname_th,
                        cus_main_cus_contact_position_th = cus_main.cus_contact.con_position_th

                    record = {
                        "cus_id": cus_main.cus_id,
                        "cus_active": cus_main.cus_active,
                        "cus_name_th": cus_main.cus_name_th,
                        "cus_add1_th": cus_main.cus_add1_th,
                        "cus_add2_th": cus_main.cus_add2_th,
                        "cus_subdist_th": cus_main.cus_subdist_th,
                        "cus_district_id": cus_main.cus_district_id,                    
                        "cus_district_th": cus_main_cus_district_th,
                        "cus_city_th": cus_main_cus_city_th,
                        "cus_country_th": cus_main_cus_country_th,
                        
                        "cus_name_en": cus_main.cus_name_en,
                        "cus_add1_en": cus_main.cus_add1_en,
                        "cus_add2_en": cus_main.cus_add2_en,
                        "cus_subdist_en": cus_main.cus_subdist_en,
                        "cus_district_en": cus_main_cus_district_en,
                        "cus_city_en": cus_main_cus_city_en,
                        "cus_country_en": cus_main_cus_country_en,

                        "cus_zip": cus_main.cus_zip,                    
                        "cus_tel": cus_main.cus_tel,
                        "cus_fax": cus_main.cus_fax,
                        "cus_email": cus_main.cus_email,
                        "cus_zone": cus_main.cus_zone_id,
                        "cus_contact_id": cus_main.cus_contact_id,
                        "cus_contact_title_th": cus_main_cus_contact_title_th,
                        "cus_contact_fname_th": cus_main_cus_contact_fname_th,
                        "cus_contact_lname_th": cus_main_cus_contact_lname_th,
                        "cus_contact_position_th": cus_main_cus_contact_position_th,
                    }
                    pickup_records.append(record)
                
                    cus_main_form = CusMainForm(instance=cus_main)
            except CusMain.DoesNotExist:
                cus_main = None
                record = {
                    "cus_id": None,
                    "cus_name_th": None,
                    "cus_name_en": None,
                    "cus_name_th": None,
                    "cus_add1_th": None,
                    "cus_add2_th": None,
                    "cus_subdist_th": None,
                    "cus_district_id": None,                    
                    "cus_district_th": None,
                    "cus_city_th": None,
                    "cus_country_th": None,
                    "cus_name_en": None,
                    "cus_add1_en": None,
                    "cus_add2_en": None,
                    "cus_subdist_en": None,
                    "cus_district_en": None,
                    "cus_city_en": None,
                    "cus_country_en": None,
                    "cus_zip": None,
                    "cus_tel": None,
                    "cus_fax": None,
                    "cus_email": None,
                    "cus_zone": None,
                    "cus_contact_id": None,
                    "cus_contact_title_th": None,
                    "cus_contact_fname_th": None,
                    "cus_contact_lname_th": None,
                    "cus_contact_position_th": None,
                }
                pickup_records.append(record)      
            
            response = JsonResponse({"success": "Form is valid", 
                "results": list(pickup_records), 
                #"business_type_list": list(business_type_list)
                })

            response.status_code = 200
            return response            
        else:
            print("form is invalid")
            print(form.errors)
            response = JsonResponse({ "error": "Customer ID is not correct.", "results": list(pickup_records) })
            response.status_code = 403
            return response


@login_required(login_url='/accounts/login/')
def ajax_check_exist_cus_site(request):

    print("************************************************")
    print("FUNCTION: ajax_check_exist_cus_site")
    print("************************************************")

    response_data = {}
    pickup_records=[]
    group_id = []
    business_type_list = []
    group_1_list = []
    group_2_list = []
    customer_option = []

    if request.method == "POST":
        form = CustomerCodeCreateForm(request.POST)
        cus_id = request.POST.get('cus_id')
        cus_brn = request.POST.get('cus_brn').zfill(3)

        '''
        print("**************************")
        print("cus_id = " + str(cus_id))
        print("cus_brn = " + str(cus_brn))
        print("**************************")
        '''

        if form.is_valid():
            # print("form is valid")

            # Get customer site information
            cus_no = str(cus_id) + str(cus_brn)            
            # print("cus_no = " + str(cus_no))
            try:
                customer_site = Customer.objects.get(pk=cus_no)
            except Customer.DoesNotExist:
                customer_site = None

            if customer_site:
                # print("todo: update customer site")

                # 1.Bind customer_option information on Main Office tab
                try:
                    customer_option = CustomerOption.objects.get(cus_no=cus_no)
                    customer_option_btype = customer_option.btype
                    customer_option_op1 = customer_option.op1
                    customer_option_op2 = customer_option.op2
                    customer_option_op3 = customer_option.op3
                    customer_option_op4 = customer_option.op4
                except CustomerOption.DoesNotExist:
                    customer_option_btype = ""
                    customer_option_op1 = ""
                    customer_option_op2 = ""
                    customer_option_op3 = ""
                    customer_option_op4 = ""

                # 2.Bind customer site on Site tab
                # cus_site_cus_district_id = customer_site.cus_district_id

                if not customer_site.cus_district:
                    cus_site_cus_district_th = None
                    cus_site_cus_district_en = None
                else:
                    cus_site_cus_district_th = customer_site.cus_district.dist_th
                    cus_site_cus_district_en = customer_site.cus_district.dist_en

                if not customer_site.cus_city:
                    cus_site_cus_city_th = None
                    cus_site_cus_city_en = None
                else:
                    cus_site_cus_city_th = customer_site.cus_city.city_th
                    cus_site_cus_city_en = customer_site.cus_city.city_en

                if not customer_site.cus_country:
                    cus_site_cus_country_th = None
                    cus_site_cus_country_en = None
                else:
                    cus_site_cus_country_th = customer_site.cus_country.country_th
                    cus_site_cus_country_en = customer_site.cus_country.country_en

                if not customer_site.site_contact_id:
                    cus_site_site_contact_title_th = ""
                    cus_site_site_contact_fname_th = ""
                    cus_site_site_contact_lname_th = ""
                    cus_site_site_contact_position_th = "" 
                else:
                    cus_site_site_contact_title_th = customer_site.site_contact.con_title.title_th
                    cus_site_site_contact_fname_th = customer_site.site_contact.con_fname_th
                    cus_site_site_contact_lname_th = customer_site.site_contact.con_lname_th,
                    cus_site_site_contact_position_th = customer_site.site_contact.con_position_th

                record = {
                    "cus_no": customer_site.cus_no,
                    "cus_active": customer_site.cus_active,
                    "cus_name_th": customer_site.cus_name_th,
                    "cus_add1_th": customer_site.cus_add1_th,
                    "cus_add2_th": customer_site.cus_add2_th,
                    "cus_subdist_th": customer_site.cus_subdist_th,
                    "cus_district_id": customer_site.cus_district_id,                    
                    "cus_district_th": cus_site_cus_district_th,
                    "cus_city_th": cus_site_cus_city_th,
                    "cus_country_th": cus_site_cus_country_th,

                    "cus_name_en": customer_site.cus_name_en,
                    "cus_add1_en": customer_site.cus_add1_en,
                    "cus_add2_en": customer_site.cus_add2_en,
                    "cus_subdist_en": customer_site.cus_subdist_en,
                    "cus_subdist_en": customer_site.cus_subdist_en,
                    "cus_district_en": cus_site_cus_district_en,
                    "cus_city_en": cus_site_cus_city_en,
                    "cus_country_en": cus_site_cus_country_en,

                    "cus_zip": customer_site.cus_zip,
                    "cus_tel": customer_site.cus_tel,
                    "cus_fax": customer_site.cus_fax,
                    "cus_email": customer_site.cus_email,
                    "cus_zone": customer_site.cus_zone_id,

                    "cus_site_site_contact_id": customer_site.site_contact_id,
                    "cus_site_site_contact_title_th": cus_site_site_contact_title_th,
                    "cus_site_site_contact_fname_th": cus_site_site_contact_fname_th,
                    "cus_site_site_contact_lname_th": cus_site_site_contact_lname_th,
                    "cus_site_site_contact_position_th": cus_site_site_contact_position_th,

                    "customer_option_btype": customer_option_btype,
                    "customer_option_op1": customer_option_op1,
                    "customer_option_op2": customer_option_op2,
                    "customer_option_op3": customer_option_op3,
                    "customer_option_op4": customer_option_op4,
                }

                pickup_records.append(record)

            else:
                print("todo: add new customer site")
                # 1.Bind customer site on Site tab                
                record = {
                    "cus_no": "",
                    "cus_active": "",
                    "cus_name_th": "",
                    "cus_add1_th": "",
                    "cus_add2_th": "",
                    "cus_subdist_th": "",
                    "cus_district_id": "",                    
                    "cus_district_th": "",
                    "cus_city_th": "",
                    "cus_country_th": "",

                    "cus_name_en": "",
                    "cus_add1_en": "",
                    "cus_add2_en": "",
                    "cus_subdist_en": "",
                    "cus_district_en": "",
                    "cus_city_en": "",
                    "cus_country_en": "",
                    
                    "cus_zip": "",
                    "cus_tel": "",
                    "cus_fax": "",
                    "cus_email": "",
                    "cus_zone": "",

                    "cus_site_contact_id": "",
                    "cus_site_site_contact_title_th": "",
                    "cus_site_site_contact_fname_th": "",
                    "cus_site_site_contact_lname_th": "",
                    "cus_site_site_contact_position_th": "",
                    
                    "customer_option_btype": "",
                    "customer_option_op1": "",
                    "customer_option_op2": "",
                    "customer_option_op3": "",
                    "customer_option_op4": "",
                }
                pickup_records.append(record)


            response = JsonResponse({"success": "Form is valid", 
                "results": list(pickup_records), 
                "business_type_list": list(business_type_list)
                })

            response.status_code = 200
            return response            
        else:
            # print("form is invalid")       
            response = JsonResponse({ "error": "Data is not correct.", "results": list(pickup_records) })
            response.status_code = 403
            return response   
    else:
        print("TODO: Handle get request")


    response = JsonResponse({ "error": "Contact admistrator.", "results": list(pickup_records) })
    response.status_code = 403
    return response


@login_required(login_url='/accounts/login/')
def ajax_check_exist_cus_bill(request):

    print("************************************************")
    print("FUNCTION: ajax_check_exist_cus_bill")
    print("************************************************")

    response_data = {}
    pickup_records=[]
    business_type_list = []
    group_1_list = []
    group_2_list = []
    customer_option = []

    if request.method == "POST":
        form = CustomerCodeCreateForm(request.POST)
        cus_id = request.POST.get('cus_id')
        cus_brn = request.POST.get('cus_brn').zfill(3)

        if form.is_valid():
            # Get customer site information
            cus_no = str(cus_id) + str(cus_brn)            
            print("cus_no = " + str(cus_no))

            try:
                customer_bill = CusBill.objects.get(pk=cus_no)
                print(customer_bill.cus_district)
            except CusBill.DoesNotExist:
                customer_bill = None

            if customer_bill:
                if not customer_bill.cus_district:
                    cus_bill_cus_district_th = None
                    cus_bill_cus_district_en = None
                else:
                    cus_bill_cus_district_th = customer_bill.cus_district.dist_th
                    cus_bill_cus_district_en = customer_bill.cus_district.dist_en

                print("debug 2 : " + str(cus_bill_cus_district_th))

                if not customer_bill.cus_city:
                    cus_bill_cus_city_th = None
                    cus_bill_cus_city_en = None
                else:
                    cus_bill_cus_city_th = customer_bill.cus_city.city_th
                    cus_bill_cus_city_en = customer_bill.cus_city.city_en

                print("debug 3 : " + str(cus_bill_cus_city_en))

                if not customer_bill.cus_country:
                    cus_bill_cus_country_th = None
                    cus_bill_cus_country_en = None
                else:
                    cus_bill_cus_country_th = customer_bill.cus_country.country_th
                    cus_bill_cus_country_en = customer_bill.cus_country.country_en

                if not customer_bill.cus_contact_id:
                    cus_bill_cus_contact_title_th = ""
                    cus_bill_cus_contact_fname_th = ""
                    cus_bill_cus_contact_lname_th = ""
                    cus_bill_cus_contact_position_th = "" 
                else:
                    cus_bill_cus_contact_title_th = customer_bill.cus_contact.con_title.title_th
                    cus_bill_cus_contact_fname_th = customer_bill.cus_contact.con_fname_th
                    cus_bill_cus_contact_lname_th = customer_bill.cus_contact.con_lname_th,
                    cus_bill_cus_contact_position_th = customer_bill.cus_contact.con_position_th

                record = {
                    "cus_no": customer_bill.cus_no,
                    "cus_active": customer_bill.cus_active,
                    "cus_name_th": customer_bill.cus_name_th,
                    "cus_add1_th": customer_bill.cus_add1_th,
                    "cus_add2_th": customer_bill.cus_add2_th,
                    "cus_subdist_th": customer_bill.cus_subdist_th,
                    "cus_district_id": customer_bill.cus_district_id,                    
                    "cus_district_th": cus_bill_cus_district_th,
                    "cus_city_th": cus_bill_cus_city_th,
                    "cus_country_th": cus_bill_cus_country_th,
                    "cus_name_en": customer_bill.cus_name_en,
                    "cus_add1_en": customer_bill.cus_add1_en,
                    "cus_add2_en": customer_bill.cus_add2_en,
                    "cus_subdist_en": customer_bill.cus_subdist_en,
                    "cus_subdist_en": customer_bill.cus_subdist_en,
                    "cus_district_en": cus_bill_cus_district_en,
                    "cus_city_en": cus_bill_cus_city_en,
                    "cus_country_en": cus_bill_cus_country_en,

                    "cus_zip": customer_bill.cus_zip,
                    "cus_tel": customer_bill.cus_tel,
                    "cus_fax": customer_bill.cus_fax,
                    "cus_email": customer_bill.cus_email,
                    "cus_zone": customer_bill.cus_zone_id,

                    "cus_bill_cus_contact_id": customer_bill.cus_contact_id,
                    "cus_bill_cus_contact_title_th": cus_bill_cus_contact_title_th,
                    "cus_bill_cus_contact_fname_th": cus_bill_cus_contact_fname_th,
                    "cus_bill_cus_contact_lname_th": cus_bill_cus_contact_lname_th,
                    "cus_bill_cis_contact_position_th": cus_bill_cus_contact_position_th,
                }

                pickup_records.append(record)

            else:
                print("todo: add new customer bill")
                record = {
                    "cus_no": "",
                    "cus_active": "",
                    "cus_name_th": "",
                    "cus_add1_th": "",
                    "cus_add2_th": "",
                    "cus_subdist_th": "",
                    "cus_district_id": "",
                    "cus_district_th": "",
                    "cus_city_th": "",
                    "cus_country_th": "",
                    "cus_name_en": "",
                    "cus_add1_en": "",
                    "cus_add2_en": "",
                    "cus_subdist_en": "",
                    "cus_subdist_en": "",
                    "cus_district_en": "",
                    "cus_city_en": "",
                    "cus_country_en": "",
                    "cus_zip": "",
                    "cus_tel": "",
                    "cus_fax": "",
                    "cus_email": "",
                    "cus_zone": "",
                    "cus_bill_cus_contact_id": "",
                    "cus_bill_cus_contact_title_th": "",
                    "cus_bill_cus_contact_fname_th": "",
                    "cus_bill_cus_contact_lname_th": "",
                    "cus_bill_cis_contact_position_th": "",
                }
                pickup_records.append(record)

            response = JsonResponse({"success": "Form is valid", 
                "results": list(pickup_records), 
                })

            response.status_code = 200
            return response            
        else:
            # print("form is invalid")       
            response = JsonResponse({ "error": "Data is not correct.", "results": list(pickup_records) })
            response.status_code = 403
            return response   
    else:
        print("TODO: Handle get request")


    response = JsonResponse({ "error": "Contact admistrator.", "results": list(pickup_records) })
    response.status_code = 403
    return response


@permission_required('customer.view_customer', login_url='/accounts/login/')
def CustomerDashboard(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE    

    # Get number of active customer    
    no_of_active_customer = Customer.objects.filter(cus_active=1).exclude(upd_flag='D').count()
    # Get number of pending customer
    no_of_pending_customer = Customer.objects.filter(cus_active=0).exclude(upd_flag='D').count()
    # Get number of delete customer   
    no_of_delete_customer = Customer.objects.filter(upd_flag='D').count()
    total_customer = no_of_active_customer+no_of_pending_customer+no_of_delete_customer

    # History Logs
    history_log = HrmsNewLog.objects.all().order_by('-log_date')[:25]
    if not history_log:
        history_log = None

    context = {
        'page_title': page_title, 
        'db_server': db_server, 'today_date': today_date,
        'project_name': project_name, 
        'project_version': project_version,
        'no_of_active_customer': no_of_active_customer,
        'no_of_pending_customer': no_of_pending_customer,
        'no_of_delete_customer': no_of_delete_customer,
        'total_customer': total_customer,
        'history_log': history_log,
    }
    return render(request, 'customer/customer_dashboard.html', context)


@permission_required('customer.view_customer', login_url='/accounts/login/')
def CustomerList(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = settings.TODAY_DATE    
    item_per_page = 50

    if request.method == "POST":
        form = CustomerSearchForm(request.POST, user=request.user)
        cus_name = request.POST.get('cus_name')
        cus_id = request.POST.get('cus_id')
        cus_brn = request.POST.get('cus_brn')        

        '''
        print("post")
        print("POST: cus_name = " +  str(cus_name))
        print("POST: cus_id = " +  str(cus_id))
        print("POST: cus_brn = " +  str(cus_brn))
        '''

        # cus_name
        if cus_name!='' and cus_id!='' and cus_brn!='':
            print("post case 1")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).filter(cus_id=cus_id).filter(cus_brn=cus_brn).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_name!='' and cus_id=='' and cus_brn=='':
            print("post case 2")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).exclude(upd_flag='D').order_by('cus_id', 'cus_brn', '-cus_active')

        if cus_name!='' and cus_id=='' and cus_brn!='':
            print("post case 3")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).filter(cus_brn=cus_brn).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_name=='' and cus_id!='' and cus_brn!='':
            print("post case 4")
            customer_list = Customer.objects.exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_name=='' and cus_id=='' and cus_brn=='':
            print("post case 5")
            customer_list = Customer.objects.exclude(upd_flag='D').order_by('cus_id', 'cus_brn', '-cus_active')            

        # cus_id
        if cus_id!='' and cus_name=='' and cus_brn=='':
            print("post case 6")
            customer_list = Customer.objects.filter(cus_id=cus_id).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_id!='' and cus_name!='' and cus_brn=='':
            print("post case 7")
            customer_list = Customer.objects.filter(cus_id=cus_id).filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_id!='' and cus_name=='' and cus_brn!='':
            print("post case 8")
            customer_list = Customer.objects.filter(cus_id=cus_id).filter(cus_brn=cus_brn).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        # cus_brn
        if cus_brn!='' and cus_name=='' and cus_id=='':
            print("post case 9")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_brn!='' and cus_name!='' and cus_id=='':
            print("post case 10")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_brn!='' and cus_name=='' and cus_id!='':
            print("post case 11")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).filter(cus_id=cus_id).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        page = 1
        paginator = Paginator(customer_list, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)            
        except InvalidPage as e:
            raise Http404(str(e))        
    else:
        form = CustomerSearchForm(user=request.user)                    
        cus_name = request.GET.get('cusname', '')
        cus_id = request.GET.get('cusid', '')
        cus_brn = request.GET.get('cusbrn', '')

        # TODO
        # cus_id = "1001"
        '''
        print("get")
        print("GET: cus_name = " +  str(cus_name))
        print("GET: cus_id = " +  str(cus_id))
        print("GET: cus_brn = " +  str(cus_brn))
        '''
        
        # cus_name
        if cus_name!='' and cus_id!='' and cus_brn!='':
            print("get case 1")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).filter(cus_id=cus_id).filter(cus_brn=cus_brn).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_name!='' and cus_id=='' and cus_brn=='':
            print("get case 2")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_name!='' and cus_id=='' and cus_brn!='':
            print("get case 3")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).filter(cus_brn=cus_brn).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_name=='' and cus_id!='' and cus_brn!='':
            print("get case 4")
            customer_list = Customer.objects.exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_name=='' and cus_id=='' and cus_brn=='':
            print("get case 5")
            customer_list = Customer.objects.exclude(upd_flag='D').order_by('cus_id','cus_brn')

        # cus_id
        if cus_id!='' and cus_name=='' and cus_brn=='':
            print("post case 6")
            customer_list = Customer.objects.filter(cus_id=cus_id).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_id!='' and cus_name!='' and cus_brn=='':
            print("get case 7")
            customer_list = Customer.objects.filter(cus_id=cus_id).filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_id!='' and cus_name=='' and cus_brn!='':
            print("get case 8")
            customer_list = Customer.objects.filter(cus_id=cus_id).filter(cus_brn=cus_brn).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        # cus_brn
        if cus_brn!='' and cus_name=='' and cus_id=='':
            print("post case 9")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_brn!='' and cus_name!='' and cus_id=='':
            print("get case 10")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        if cus_brn!='' and cus_name=='' and cus_id!='':
            print("get case 11")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).filter(cus_id=cus_id).exclude(upd_flag='D').order_by('-cus_active','cus_id','cus_brn')

        paginator = Paginator(customer_list, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page', '1') or 1

        try:
            current_page = paginator.get_page(page)
            '''
            print("current_page = " + str(current_page))
            print("current_page.number = " + str(current_page.number))        
            print("current_page.paginator.num_pages = " + str(current_page.paginator.num_pages))
            
            print("current_page.has_next = " + str(current_page.has_next))
            print("current_page.has_previous = " + str(current_page.has_previous))            
            '''
        except InvalidPage as e:
            raise Http404(str(e))

        # customer_list = []
    
    context = {
        'page_title': page_title, 
        'db_server': db_server, 'today_date': today_date,
        'project_name': project_name, 
        'project_version': project_version,         
        'current_page': current_page,
        'is_paginated': is_paginated,
        'customer_list': customer_list,
        'form': form,
        'cus_name': cus_name,
        'cus_id': cus_id,
        'cus_brn': cus_brn,
    }

    return render(request, 'customer/customer_list.html', context)


# Load all 3 forms (cus_main, cus_site, cus_bill)
@permission_required('customer.view_customer', login_url='/accounts/login/')
def CustomerUpdate(request, pk):
    print("pk = " + str(pk))

    template_name = 'customer/customer_update.html'
    cus_no = pk
    cus_id = None
    cus_brn = None
    customer = get_object_or_404(Customer, pk=pk)
    cus_main = None
    cus_site = None
    cus_bill = None

    if customer is not None:
        try:
            cus_main = CusMain.objects.get(pk=customer.cus_id)
            # print("cus_id = " + str(customer.cus_id))
            # print("cus_brn = " + str(customer.cus_brn).zfill(3))
            cus_id = cus_main.cus_id            
        except CusMain.DoesNotExist:
            cus_main = None
            cus_main_cus_id = None
        try:
            cus_site = Customer.objects.get(pk=pk)
            cus_site_cus_no = cus_site.cus_no
            cus_site_cus_id = cus_site.cus_id
            cus_site_cus_brn = cus_site.cus_brn
        except Customer.DoesNotExist:
            cus_site = None
            cus_site_cus_no = None
            cus_site_cus_id = None
            cus_site_cus_brn = None
        try:
            # cus_bill = CusBill.objects.get(pk=pk).order_by('cus_no').distinct('cus_no')
            cus_bill = CusBill.objects.get(pk=pk)
            cus_bill_cus_no = cus_bill.cus_no
            cus_bill_cus_id = cus_bill.cus_id
            cus_bill_cus_brn = cus_bill.cus_brn
        except CusBill.DoesNotExist:
            cus_bill = None
            cus_bill_cus_no = None
            cus_bill_cus_id = None
            cus_bill_cus_brn = None

    if request.method == 'POST':        
        cus_main_form = CusMainForm(request.POST, instance=cus_main, cus_no=pk)
        cus_site_form = CusSiteForm(request.POST, instance=cus_site, cus_no=pk)
        cus_bill_form = CusBillForm(request.POST, instance=cus_bill, cus_no=pk)
    else:
        cus_main_form = CusMainForm(instance=cus_main, cus_no=pk)    
        cus_site_form = CusSiteForm(instance=cus_site)
        cus_bill_form = CusBillForm(instance=cus_bill)

    # Business Type
    group_id = CusMain.objects.values_list('cus_taxid', flat=True).exclude(cus_taxid=None).order_by('cus_taxid').distinct()
    business_type_list = CustomerOption.objects.values_list('btype', flat=True).exclude(btype=None).order_by('btype').distinct()
    group_1_list = CustomerOption.objects.values_list('op2', flat=True).exclude(op2=None).order_by('op2').distinct()
    group_2_list = CustomerOption.objects.values_list('op3', flat=True).exclude(op2=None).order_by('op3').distinct()

    customer_option = []
    try:
        customer_option = CustomerOption.objects.get(cus_no=pk)
        business_type = customer_option.btype
    except CustomerOption.DoesNotExist:
        business_type = None
        customer_option = None
        print("No customer_option")

    context = {
        'page_title': settings.PROJECT_NAME,
        'today_date': settings.TODAY_DATE,
        'project_version': settings.PROJECT_VERSION,
        'db_server': settings.DATABASES['default']['HOST'],
        'project_name': settings.PROJECT_NAME,
        'cus_no': cus_no,
        'cus_main_form': cus_main_form,
        'cus_main': cus_main,
        'cus_site_form': cus_site_form,
        'cus_site': cus_site,
        'cus_bill_form': cus_bill_form,
        'cus_bill': cus_bill,
        'customer': customer,        
        'request': request,
        'customer_option': customer_option,
        'group_id': group_id,
        'business_type_list': business_type_list,
        'group_1_list': group_1_list,
        'group_2_list': group_2_list,
    }

    # print("test")
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def get_district_list_modal(request):

    print("**********************************")    
    print("FUNCTION: get_district_list_modal")
    print("**********************************")

    data = []
    item_per_page = 100
    page_no = request.GET["page_no"]
    current_district_id = request.GET["current_district_id"]
    search_district_option = request.GET["search_district_option"]
    search_district_text = request.GET["search_district_text"]
    
    # print("current_district_id = " + str(current_district_id))

    if search_district_option == '1':
        data = TDistrict.objects.select_related('city_id').filter(dist_id__exact=search_district_text)

    if search_district_option == '2':
        data = TDistrict.objects.select_related('city_id').filter(dist_th__contains=search_district_text)
        if not data:
            data = TDistrict.objects.select_related('city_id').filter(dist_en__contains=search_district_text)        

    if search_district_option == '3':
        data = TDistrict.objects.select_related('city_id').filter(city_id__city_th__contains=search_district_text)
        if not data:
            data = TDistrict.objects.select_related('city_id').filter(city_id__city_en__contains=search_district_text)        

    if data:
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
                # print("debug 1")
                record = {
                    "dist_id": d.dist_id,
                    "city_id": d.city_id_id,
                    "dist_th": d.dist_th,
                    "dist_en": d.dist_en,
                    "city_th": d.city_id.city_th,
                    "city_en": d.city_id.city_en,
                    "country_name_th": d.city_id.country_id.country_th,
                    "country_name_en": d.city_id.country_id.country_en,
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
        # print("not found 2")
        response = JsonResponse(data={
            "success": False,
            "error"
            "results": [],
        })
        response.status_code = 403
        return response

    return JsonResponse(data={"success": False, "results": ""})


@login_required(login_url='/accounts/login/')
def get_district_list(request):

    print("****************************")
    print("FUNCTION: get_district_list")
    print("****************************")

    current_district_id = request.GET.get('current_district_id')
    cus_active = request.POST.get('cus_main_cus_active')

    print("current_district_id : " + str(current_district_id))

    item_per_page = 100

    if request.method == "POST":
        print("method post")        
        data = TDistrict.objects.select_related('city_id')

        page = 1
        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))

    else:
        print("method get")
        if current_district_id is not None:
            if current_district_id != "":
                if current_district_id.isnumeric():
                    print("debug1")
                    district_object = TDistrict.objects.filter(dist_id__exact=current_district_id).get()
                    data = TDistrict.objects.select_related('city_id').filter(city_id__city_th__contains=district_object.city_id.city_th)
                    if not data:
                        print("debug2")
                        data = TDistrict.objects.select_related('city_id').filter(city_id__city_en__contains=district_object.city_id.city_en)
                else:
                    print("debug3")
                    data = TDistrict.objects.all()
            else:
                print("debug4")
                data = TDistrict.objects.all()
        else:
            print("debug5")
            data = TDistrict.objects.all()

        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page', 1) or 1
        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))   

    #if data:
    if current_page:
        '''
        print("current_page = " + str(current_page))
        print("current_page.number = " + str(current_page.number))        
        print("current_page.paginator.num_pages = " + str(current_page.paginator.num_pages))
        
        print("current_page.has_next = " + str(current_page.has_next))
        print("current_page.has_previous = " + str(current_page.has_previous))
        '''

        current_page_number = current_page.number
        current_page_paginator_num_pages = current_page.paginator.num_pages

        pickup_dict = {}
        pickup_records=[]
        
        for d in current_page:
            country_name_th = d.city_id.country_id.country_th
            country_name_en = d.city_id.country_id.country_en
            
            record = {
                "dist_id": d.dist_id,
                "city_id": d.city_id_id,
                "dist_th": d.dist_th,
                "dist_en": d.dist_en,
                "city_th": d.city_id.city_th,
                "city_en": d.city_id.city_en,
                "country_name_th": country_name_th,
                "country_name_en": country_name_th, 
            }
            pickup_records.append(record)

        # serialized_qs = serializers.serialize('json', current_page)
        # print(serialized_qs);
        # pages = current_page.paginator.num_pages
        # current_page = 1

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


def save_customer_form(request, form, template_name):
    # print("todo : save_customer_form")
    data = dict()
    if request.method == 'POST':
        #form = CustomerCreateForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            fields = request.POST.dict()

            if request.user.is_superuser:
                obj.upd_by = 'Superuser'
            else:
                obj.upd_by = request.user.first_name

            if obj.upd_flag == 'A':
                obj.upd_flag = 'E'

            # Check duplicate Customer No
            cus_no = fields.get('cus_id') + fields.get('cus_brn').zfill(3)            
            obj.cus_no = cus_no

            # Get current date time
            obj.upd_date = timezone.now()
            obj.cus_active = 1
            
            obj.save()

            data['form_is_valid'] = True
            
            # TODO:
            #customer_list = Customer.objects.all()
            customer_list = Customer.objects.filter(cus_code__exact=[2094]).order_by('-upd_date', 'cus_id', '-cus_active')

            data['html_customer_list'] = render_to_string('customer/partial_customer_list.html', {
                'customer_list': customer_list
            })
            data['message'] = "ทำรายการสำเร็จ"
        else:
            data['form_is_valid'] = False
            #data['message'] = "ไม่สามารถทำรายการได้!! กรุณาตรวจสอบข้อมูล"
            
            for field in form.errors:
                if field == 'cus_no':
                    print(field)
                    data['message'] = "รหัสสาขานี้มีอยู่แล้ว"                
                else:
                    data['message'] = "กรุณาป้อนข้อมูลให้ครบถ้วน"
            
            #print(form.errors)

    '''
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
    '''

    context = {'form': form, 'cus_name': "Demo"}
    return render(request, template_name, context)    

"""
def CustomerCreate(request):
    if request.method == 'POST':
        form = CustomerCreateForm(request.POST)
    else:
        form = CustomerCreateForm()

    return save_customer_form(request, form, 'customer/partial_customer_create.html')
"""


@login_required(login_url='/accounts/login/')
@permission_required('customer.view_customer', login_url='/accounts/login/')
def CustomerDelete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    data = dict()

    if request.method == 'POST':        
        cus_no = request.POST.get('cus_no')        
        
        # customer.delete()
        if customer:
            customer.upd_flag = 'D'
            customer.upd_by = request.user.first_name
            customer.upd_date = timezone.now()
            customer.save()

            # History Log                    
            new_log = HrmsNewLog(
                log_table = 'CUSTOMER',
                log_key = cus_no,
                log_field = None,
                old_value = None,
                new_value = None,
                log_type = 'D',
                log_by = request.user.username,
                log_date = timezone.now(),
                log_description = None
                )
            new_log.save()    
            # ./History Log

        data['form_is_valid'] = True
        customer_list = Customer.objects.all()
        data['html_customer_list'] = render_to_string('customer/partial_customer_list.html', {
            'customer_list': customer_list
        })
        data['message'] = ""
        data['cus_no'] = cus_no
        context = {'customer': customer_list}
    else:
        print("aaaaaaGET")
        data['message'] = ""
        context = {'customer': customer, "results": 'Error!', "success": False}
        data['html_form'] = render_to_string('customer/partial_customer_delete.html', context, request=request)
        
    return JsonResponse(data)


@login_required(login_url='/accounts/login/')
def PerformanceInformation(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION	
	today_date = settings.TODAY_DATE

	return render(request, 'customer/performance_information.html', {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})


@login_required(login_url='/accounts/login/')
def CustomerReport(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION	
	today_date = settings.TODAY_DATE
	return render(request, 'customer/customer_report.html', {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})



@login_required(login_url='/accounts/login/')
def get_district_list_backup(request):        
    # data = TDistrict.objects.all() or None    
    item_per_page = 5

    if request.method == "POST":
        # print("method post")
        data = TDistrict.objects.raw("select d.dist_id,d.dist_th,d.dist_en,c.city_id,c.city_th,c.city_en from t_district d join t_city c on d.city_id = c.city_id order by c.city_th") or None

        page = 1
        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))
    else:
        # print("method get")
        data = TDistrict.objects.raw("select d.dist_id,d.dist_th,d.dist_en,c.city_id,c.city_th,c.city_en from t_district d join t_city c on d.city_id = c.city_id order by c.city_th") or None
        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page', '1') or 1
 
        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))   



    #if data:
    if current_page:
        pickup_dict = {}
        pickup_records=[]
        
        for d in current_page:
            # print("debug 1")
            record = {
                "dist_id": d.dist_id, 
                "city_id": d.city_id,
                "dist_th": d.dist_th,
                "dist_en": d.dist_en,
                "city_th": d.city_th
            }
            pickup_records.append(record)

        serialized_qs = serializers.serialize('json', current_page)
        # print(serialized_qs);
        # print("has_previous : " + str(current_page.has_previous))
        
        pages = current_page.paginator.num_pages,
        current_page = 5,
        next_page = 6
        previous_page = 4

        response = JsonResponse(data={
            "success": True,
            "is_paginated": is_paginated, 
            "pages": pages,
            "current_page": current_page,
            "previous_page": previous_page,
            "next_page": next_page,
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
def update_cus_main(request):

    print("****************************")
    print("FUNCTION: update_cus_main")    
    # print("****************************")

    template_name = 'customer/customer_update.html'    
    response_data = {}
    modified_records=[]

    if request.method == 'POST':
        form = CusMainForm(request.POST)

        if form.is_valid():
            cus_active = request.POST.get('cus_main_cus_active')
            cus_id = request.POST.get('cus_id')
            cus_brn = request.POST.get('cus_brn').zfill(3)
            cus_no = str(cus_id) + str(cus_brn)                        
            cus_name_th = request.POST.get('cus_main_cus_name_th')            
            cus_add1_th = request.POST.get('cus_main_cus_add1_th')
            cus_add2_th = request.POST.get('cus_main_cus_add2_th')
            cus_subdist_th = request.POST.get('cus_main_cus_subdist_th')                        
            cus_name_en = request.POST.get('cus_main_cus_name_en')                          
            cus_add1_en = request.POST.get('cus_main_cus_add1_en')
            cus_add2_en = request.POST.get('cus_main_cus_add2_en')
            cus_subdist_en = request.POST.get('cus_main_cus_subdist_en')
            cus_zip = request.POST.get('cus_main_cus_zip')
            if not cus_zip.isnumeric():
                cus_zip = 0
                
            cus_tel = request.POST.get('cus_main_cus_tel')
            cus_fax = request.POST.get('cus_main_cus_fax')
            cus_email = request.POST.get('cus_main_cus_email')
            cus_zone = request.POST.get('cus_main_cus_zone')                

            business_type = request.POST.get('cus_main_business_type')
            cus_main_customer_option_op1 = request.POST.get('cus_main_customer_option_op1')
            cus_main_customer_option_op2 = request.POST.get('cus_main_customer_option_op2')
            cus_main_customer_option_op3 = request.POST.get('cus_main_customer_option_op3')
            cus_main_customer_option_op4 = request.POST.get('cus_main_customer_option_op4')

            cus_main_cus_contact_id = request.POST.get('cus_main_cus_contact_id')
            if cus_main_cus_contact_id:
                cus_main_cus_contact_id = cus_main_cus_contact_id
            else:
                cus_main_cus_contact_id = None

            cus_main = get_object_or_404(CusMain, pk=cus_id)
        
            select_district_id = request.POST.get('select_district_id')
            if select_district_id != "":
                try:
                    select_district_id = select_district_id
                    district_obj = TDistrict.objects.get(dist_id=select_district_id)
                    if district_obj:
                        cus_main.cus_district_id = select_district_id
                        cus_main.cus_city_id = district_obj.city_id
                        cus_main.cus_country_id = district_obj.city_id.country_id
                    else:
                        cus_main.cus_district_id = None
                        cus_main.cus_city_id = None
                        cus_main_cus_country_id = None
                except TDistrict.DoesNotExist:
                        cus_main.cus_district_id = None
                        cus_main.cus_city_id = None
                        cus_main_cus_country_id = None
            else:
                print("not ok")
                cus_main.cus_district_id = None
                cus_main.cus_city_id = None
                cus_main_cus_country_id = None

            cus_main.cus_active = cus_active
            cus_main.cus_name_th = cus_name_th
            cus_main.cus_add1_th = cus_add1_th
            cus_main.cus_add2_th = cus_add2_th
            cus_main.cus_subdist_th = cus_subdist_th
            
            cus_main.cus_name_en = cus_name_en
            cus_main.cus_add1_en = cus_add1_en
            cus_main.cus_add2_en = cus_add2_en
            cus_main.cus_subdist_en = cus_subdist_en

            cus_main.cus_zip = cus_zip
            cus_main.cus_tel = cus_tel
            cus_main.cus_fax = cus_fax
            cus_main.cus_email = cus_email
            cus_main.cus_zone_id = cus_zone


            # cus_main.cus_contact_id = None
            cus_main.cus_contact_id = cus_main_cus_contact_id

            if cus_main.upd_flag == 'A':
                cus_main.upd_flag = 'E'
            cus_main.upd_by = request.user.first_name
            cus_main.upd_date = timezone.now()
            
            cus_main.save()

            # Business Type
            try:
                # Update
                customer_option = CustomerOption.objects.get(cus_no=cus_no)
                if customer_option:
                    customer_option.btype = business_type.replace('&amp;', '&')
                    customer_option.op1 = cus_main_customer_option_op1.rstrip() # Status
                    customer_option.op2 = cus_main_customer_option_op2.replace('&amp;', '&') # Group 1
                    customer_option.op3 = cus_main_customer_option_op3.replace('&amp;', '&') # Group 2
                    customer_option.op4 = cus_main_customer_option_op4.rstrip() # A/R Code
                    customer_option.save()
            except CustomerOption.DoesNotExist:
                print("customer_option error!")
                # Insert
                '''
                c = CustomerOption(
                    cus_no = cus_no, 
                    btype = business_type.replace('&amp;', '&'), 
                    op1 = cus_main_customer_option_op1,   # Status
                    op2 = cus_main_customer_option_op2.replace('&amp;', '&'), # Group 1
                    op3 = cus_main_customer_option_op3.replace('&amp;', '&'), # Group 2
                    op4 = cus_main_customer_option_op4)   # A/R Code

                c.save()
                '''

            # Return success message
            response_data['result'] = "Update complete."
            response_data['message'] = "ทำรายการสำเร็จ"
            response_data['form_is_valid'] = True

            print("OK")
            print("****************************")

        else:
            print("form is invalid")

            response_data['form_is_valid'] = False
            response_data['message'] = ""
            if form.errors:
                for field in form:
                    for error in field.errors:
                        response_data['message'] += field.name + " | " + error + "<br>"

                response_data['errors'] = form.errors
            else:
                response_data['message'] = "ไม่สามารถทำรายการได้..!"
        
            print("Error!")
            print("****************************")

        return JsonResponse(response_data)
    else:
        print("debug - found cus_main_form problem")

    context = {
        'page_title': settings.PROJECT_NAME,
        'today_date': settings.TODAY_DATE,
        'project_version': settings.PROJECT_VERSION,
        'db_server': settings.DATABASES['default']['HOST'],
        'project_name': settings.PROJECT_NAME,
        'business_type': 'abc',
    }

    return render(request, template_name, context)    


@login_required(login_url='/accounts/login/')
def update_cus_site(request):
    
    print("*************************")
    print("FUNCTION: update_cus_site")
    # print("*************************")

    template_name = 'customer/customer_update.html'    
    response_data = {}

    if request.method == 'POST':
        form = CusSiteForm(request.POST)
        if form.is_valid():

            cus_no = request.POST.get('cus_no')
            # print("aaa")
            # print("cus_no = " + str(cus_no))

            cus_id = request.POST.get('cus_id')
            cus_brn = request.POST.get('cus_brn')

            cus_active = request.POST.get('cus_site_cus_active')
            cus_name_th = request.POST.get('cus_site_cus_name_th')
            cus_add1_th = request.POST.get('cus_site_cus_add1_th')
            cus_add2_th = request.POST.get('cus_site_cus_add2_th')
            cus_subdist_th = request.POST.get('cus_site_cus_subdist_th')

            cus_name_en = request.POST.get('cus_site_cus_name_en')
            cus_add1_en = request.POST.get('cus_site_cus_add1_en')
            cus_add2_en = request.POST.get('cus_site_cus_add2_en')
            cus_subdist_en = request.POST.get('cus_site_cus_subdist_en')

            cus_zip = request.POST.get('cus_site_cus_zip')
            if not cus_zip:
                cus_zip = None

            cus_tel = request.POST.get('cus_site_cus_tel')
            cus_fax = request.POST.get('cus_site_cus_fax')
            cus_email = request.POST.get('cus_site_cus_email')
            cus_zone = request.POST.get('cus_site_cus_zone')

            cus_site_cus_contact_con_sex = request.POST.get('cus_site_cus_contact_con_sex')
            #print("sex = " + str(cus_site_cus_contact_con_sex))

            cus_site_site_contact_id = request.POST.get('cus_site_site_contact_id')
            print("debug: " + str(cus_site_site_contact_id))

            customer = get_object_or_404(Customer, pk=cus_no)
            
            cus_site_cus_district_id = request.POST.get('select_district_id')
            #if cus_site_cus_district_id:
            if cus_site_cus_district_id != "":
                try:
                    district_obj = TDistrict.objects.get(dist_id=cus_site_cus_district_id)
                    if district_obj:                        
                        customer.cus_district_id = cus_site_cus_district_id
                        customer.cus_city_id = district_obj.city_id
                        customer.cus_country_id = district_obj.city_id.country_id

                except TDistrict.DoesNotExist:
                        customer.cus_district_id = None
                        customer.cus_city_id = None
                        customer.cus_country_id = None

            customer.cus_active = cus_active
            customer.cus_name_th = cus_name_th
            customer.cus_add1_th = cus_add1_th
            customer.cus_add2_th = cus_add2_th
            customer.cus_subdist_th = cus_subdist_th
            customer.cus_name_en = cus_name_en
            customer.cus_add1_en = cus_add1_en
            customer.cus_add2_en = cus_add2_en
            customer.cus_subdist_en = cus_subdist_en
            
            customer.cus_zip = cus_zip
            customer.cus_tel = cus_tel
            customer.cus_fax = cus_fax
            customer.cus_email = cus_email
            customer.cus_zone_id = cus_zone

            if cus_site_site_contact_id:
                customer.site_contact_id = cus_site_site_contact_id

            if customer.upd_flag == 'A':
                customer.upd_flag = 'E'

            if customer.upd_flag == 'D':
                customer.upd_flag = 'E'

            customer.upd_by = request.user.first_name
            customer.upd_date = timezone.now()
            
            customer.save()

            response_data['result'] = "Update complete."
            response_data['message'] = "ทำรายการสำเร็จ"
            response_data['form_is_valid'] = True
            print("OK")
            print("****************************")            
        else:
            response_data['form_is_valid'] = False
            response_data['message'] = ""
            if form.errors:
                for field in form:
                    for error in field.errors:
                        response_data['message'] += error + "<br>"

                response_data['errors'] = form.errors
            else:
                response_data['message'] = "ไม่สามารถทำรายการได้..!"
            print("ERROR")
            print("****************************")                

    else:
        response_data['result'] = "There is an error!"
        response_data['message'] = "ไม่สามารถทำรายการได้..!"
        response_data['form_is_valid'] = False        

    return JsonResponse(response_data)


@login_required(login_url='/accounts/login/')
def update_cus_bill(request):

    print("****************************")
    print("FUNCTION: update_cus_bill")
    # print("****************************")

    template_name = 'customer/customer_update.html'    
    response_data = {}

    if request.method == 'POST':
        form = CusBillForm(request.POST)

        if form.is_valid():
            cus_active = request.POST.get('cus_bill_cus_active')

            cus_no = request.POST.get('cus_no')
            cus_id = request.POST.get('cus_id')
            cus_brn = request.POST.get('cus_brn')
            
            cus_name_th = request.POST.get('cus_bill_cus_name_th')            
            cus_add1_th = request.POST.get('cus_bill_cus_add1_th')
            cus_add2_th = request.POST.get('cus_bill_cus_add2_th')
            cus_subdist_th = request.POST.get('cus_bill_cus_subdist_th')            
            
            cus_name_en = request.POST.get('cus_bill_cus_name_en')                          
            cus_add1_en = request.POST.get('cus_bill_cus_add1_en')
            cus_add2_en = request.POST.get('cus_bill_cus_add2_en')
            cus_subdist_en = request.POST.get('cus_bill_cus_subdist_en')

            cus_zip = request.POST.get('cus_bill_cus_zip')
            if not cus_zip:
                cus_zip = None

            cus_tel = request.POST.get('cus_bill_cus_tel')
            cus_fax = request.POST.get('cus_bill_cus_fax')
            cus_email = request.POST.get('cus_bill_cus_email')
            cus_zone = request.POST.get('cus_bill_cus_zone')
                    
            cus_bill_cus_contact_id = request.POST.get('cus_bill_cus_contact_id', None)


            try:
                cus_bill = CusBill.objects.get(pk=cus_no)
            except CusBill.DoesNotExist:
                cus_bill = None

            if cus_bill:
                # print("UPDATE")

                cus_bill.cus_active = cus_active
                cus_bill.cus_name_th = cus_name_th
                cus_bill.cus_add1_th = cus_add1_th
                cus_bill.cus_add2_th = cus_add2_th
                cus_bill.cus_subdist_th = cus_subdist_th                
                cus_bill.cus_name_en = cus_name_en
                cus_bill.cus_add1_en = cus_add1_en
                cus_bill.cus_add2_en = cus_add2_en
                cus_bill.cus_subdist_en = cus_subdist_en

                #cus_bill.cus_zip = cus_zip
                cus_bill.cus_tel = cus_tel
                cus_bill.cus_fax = cus_fax
                cus_bill.cus_email = cus_email
                cus_bill.cus_zone_id = cus_zone

                # select_district_id = request.POST.get('select_district_id', None)
                select_district_id = request.POST.get('select_district_id')            
                if select_district_id:
                    try:
                        district_obj = TDistrict.objects.get(dist_id=select_district_id)
                        if district_obj:                        
                            cus_bill.cus_district_id = select_district_id
                            cus_bill.cus_city_id = district_obj.city_id
                            cus_bill.cus_country_id = district_obj.city_id.country_id

                    except TDistrict.DoesNotExist:
                            cus_bill.cus_district_id = None
                            cus_bill.cus_city_id = None
                            cus_bill.cus_country_id = None

                # Address Info
                if not select_district_id or select_district_id == '':
                    select_district_id = None
                    cus_city = None
                    cus_country = None

                # Contact Person Info
                if not cus_bill_cus_contact_id or cus_bill_cus_contact_id == '':
                    cus_bill_cus_contact_id = None
                else:
                    cus_bill.cus_contact_id = cus_bill_cus_contact_id
                    cus_bill.site_contact_id = cus_bill_cus_contact_id

                if not cus_zip or cus_zip =='':
                    cus_zip = None

                if not cus_bill.upd_flag:
                    cus_bill.upd_flag = 'A'

                if cus_bill.upd_flag == 'A':
                    cus_bill.upd_flag = 'E'

                cus_bill.upd_by = request.user.first_name
                cus_bill.upd_date = timezone.now()

                cus_bill.cus_zip = cus_zip

                cus_bill.save()                
            else:
                # print("INSERT")

                if not cus_zone or cus_zone == '':
                    cus_zone = None

                if not cus_bill_cus_contact_id or cus_bill_cus_contact_id == '':
                    cus_zone_id = None

                if not select_district_id or select_district_id == '':
                    select_district_id = None
                    city_id = None
                    country_id = None
                else:                    
                    district_obj = TDistrict.objects.get(dist_id=select_district_id)
                    if district_obj:
                        city_id = district_obj.city_id_id                        
                        select_district_id = select_district_id
                        
                        city_id = district_obj.city_id_id               
                        # print("city id = " + str(city_id))

                        city_obj = TCity.objects.get(city_id=city_id)
                        country_id = city_obj.country_id_id
                        # print("country id = " + str(country_id))

                if not cus_zip or cus_zip == '':
                    cus_zip = None

                if not cus_bill_cus_contact_id or cus_bill_cus_contact_id == '':
                    cus_contact_id = None
                    site_contact_id = None                

                new_cus_bill = CusBill(
                    cus_no = cus_no,
                    cus_id = cus_id,
                    cus_brn = cus_brn,

                    cus_active = cus_active,
                    cus_name_th = cus_name_th,
                    cus_add1_th = cus_add1_th,
                    cus_add2_th = cus_add2_th,
                    cus_subdist_th = cus_subdist_th,                
                    cus_name_en = cus_name_en,
                    cus_add1_en = cus_add1_en,
                    cus_add2_en = cus_add2_en,
                    cus_district_id = select_district_id,
                    cus_city_id = city_id,
                    cus_country_id = country_id,                    
                    cus_zip = cus_zip,
                    cus_zone_id = cus_zone,
                    cus_contact_id = cus_bill_cus_contact_id,
                    site_contact_id = cus_bill_cus_contact_id,

                    upd_flag = 'A',
                    upd_by = request.user.first_name,
                    upd_date = timezone.now()
                )
                new_cus_bill.save()                

            # Return success message
            response_data['result'] = "Update complete."
            response_data['message'] = "ทำรายการสำเร็จ"
            response_data['form_is_valid'] = True

            print("OK")
            print("****************************")
        else:
            response_data['form_is_valid'] = False
            response_data['message'] = ""
            if form.errors:
                for field in form:
                    for error in field.errors:
                        response_data['message'] += field.name + " | " + error + "<br>"

                response_data['errors'] = form.errors
            else:
                response_data['message'] = "ไม่สามารถทำรายการได้..!"

            print("ERROR!")
            print("****************************")
        return JsonResponse(response_data)
    else:
        print("debug - found cus_main_form problem")

    context = {
        'page_title': settings.PROJECT_NAME,
        'today_date': settings.TODAY_DATE,
        'project_version': settings.PROJECT_VERSION,
        'db_server': settings.DATABASES['default']['HOST'],
        'project_name': settings.PROJECT_NAME,
        'business_type': 'abc',
    }
    
    return render(request, template_name, context)    


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
def update_all_cus_tabs(request):

    print("****************************")
    print("FUNCTION: update_all_cus_tabs")
    # print("****************************")

    template_name = 'customer/customer_update.html'        
    response_data = {}
    modified_records = []

    if request.method == 'POST':
        print("POST: update_all_cus_tabs()")

        form = CusAllTabsForm(request.POST)

        if form.is_valid():            
            cus_id = request.POST.get('cus_id')
            cus_brn = request.POST.get('cus_brn').zfill(3)
            cus_no = str(cus_id) + str(cus_brn)

            # ******************************************
            # **************  CUS_MAIN  ****************
            # ******************************************            
            cus_main_cus_active = request.POST.get('cus_main_cus_active')
            cus_customer_cus_active = request.POST.get('customer_cus_active')
            cus_bill_cus_active = request.POST.get('cus_bill_cus_active')            
            
            cus_main_cus_name_th = request.POST.get('cus_main_cus_name_th')            
            cus_main_cus_add1_th = request.POST.get('cus_main_cus_add1_th')
            cus_main_cus_add2_th = request.POST.get('cus_main_cus_add2_th')
            cus_main_cus_subdist_th = request.POST.get('cus_main_cus_subdist_th')                        
            cus_main_cus_name_en = request.POST.get('cus_main_cus_name_en')                          
            cus_main_cus_add1_en = request.POST.get('cus_main_cus_add1_en')
            cus_main_cus_add2_en = request.POST.get('cus_main_cus_add2_en')            
            cus_main_cus_subdist_en = request.POST.get('cus_main_cus_subdist_en')
            cus_main_cus_zip = request.POST.get('cus_main_cus_zip')
            if not cus_main_cus_zip:
                cus_main_cus_zip = None
            cus_main_cus_tel = request.POST.get('cus_main_cus_tel')
            cus_main_cus_fax = request.POST.get('cus_main_cus_fax')
            cus_main_cus_email = request.POST.get('cus_main_cus_email')

            cus_main_cus_zone = request.POST.get('cus_main_cus_zone')                
            cus_main_cus_district_id_new = request.POST.get('cus_main_cus_district_id')
            # print("cus_main_cus_district_id_new = " + str(cus_main_cus_district_id_new))

            # Fulfill district, city, country
            cus_main_cus_district_id = None
            cus_main_city_id = None
            cus_main_country_id = None    
            cus_main_cus_district_id = request.POST.get('cus_main_cus_district_id')
            if (cus_main_cus_district_id is not None):
                if (cus_main_cus_district_id.isnumeric()):
                    try:
                        district_obj = TDistrict.objects.get(dist_id=cus_main_cus_district_id)

                        if district_obj is not None:
                            cus_main_city_id = district_obj.city_id_id
                            city_obj = TCity.objects.get(city_id=cus_main_city_id)
                            cus_main_country_id = city_obj.country_id_id
                    except TDistrict.DoesNotExist:
                        cus_main_cus_district_id = None
                        cus_main_city_id = None
                        cus_main_country_id = None
            else:
                cus_main_cus_district_id = None
                cus_main_city_id = None
                cus_main_country_id = None            

            '''
            print("------------------------------")
            print("cus_main_cus_district_id = " + str(cus_main_cus_district_id))
            print("cus_main_city_id = " + str(cus_main_city_id))
            print("cus_main_country_id = " + str(cus_main_country_id))
            print("------------------------------")
            '''

            cus_main_business_type = request.POST.get('cus_main_business_type')            
            cus_main_customer_option_op1 = request.POST.get('cus_main_customer_option_op1')
            cus_main_customer_option_op2 = request.POST.get('cus_main_customer_option_op2')
            cus_main_customer_option_op3 = request.POST.get('cus_main_customer_option_op3')
            cus_main_customer_option_op4 = request.POST.get('cus_main_customer_option_op4')
            cus_main_customer_option_opn1 = request.POST.get('cus_main_customer_option_opn1')
            # print("cus_main_customer_option_opn1 = " + str(cus_main_customer_option_opn1))

            cus_main_cus_taxid = request.POST.get('cus_main_cus_taxid')
            # print("aeiouxyz : " +  str(cus_main_cus_taxid))


            cus_main_cus_contact_id = request.POST.get('cus_main_cus_contact_id')
            if cus_main_cus_contact_id:
                cus_main_cus_contact_id = cus_main_cus_contact_id
            else:
                cus_main_cus_contact_id = None

            try:
                modified_records = []
                cus_main = CusMain.objects.get(pk=cus_id)

                if (cus_main is not None):

                    # CUS_ACTIVE
                    field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Active Status", int(cus_main.cus_active), int(cus_main_cus_active), "E", request)
                    if field_is_modified:
                        cus_main.cus_active = cus_main_cus_active
                        modified_records.append(record)
                        cus_main.cus_main = 1

                        if int(cus_main_cus_active) == 1:
                            cus_main.cus_main = 1
                        else:
                            cus_main.cus_main = 0

                    # CUS_NAME_TH                    
                    if (cus_main_cus_name_th is not None):
                        if (cus_main_cus_name_th != ""):
                            field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Name TH", cus_main.cus_name_th, cus_main_cus_name_th, "E", request)
                            if field_is_modified:
                                cus_main.cus_name_th = cus_main_cus_name_th
                                modified_records.append(record)                                

                    # CUS_ADD1_TH
                    if (cus_main_cus_add1_th is not None):
                        if (cus_main_cus_add1_th != ""):
                            field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Address TH", cus_main.cus_add1_th, cus_main_cus_add1_th, "E", request)
                            if field_is_modified:
                                cus_main.cus_add1_th = cus_main_cus_add1_th
                                modified_records.append(record)  

                    # CUS_ADD2_TH
                    if (cus_main_cus_add2_th is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Address2 TH", cus_main.cus_add2_th, cus_main_cus_add2_th, "E", request)
                        if field_is_modified:
                            cus_main.cus_add2_th = cus_main_cus_add2_th
                            modified_records.append(record)                           

                    # CUS_SUBDIST_TH
                    if (cus_main_cus_subdist_th is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Subdist TH", cus_main.cus_subdist_th, cus_main_cus_subdist_th, "E", request)
                        if field_is_modified:
                            cus_main.cus_subdist_th = cus_main_cus_subdist_th
                            modified_records.append(record)

                    # CUS_DISTRICT_ID
                    # print("cus_main.cus_district_id 1: " + str(cus_main.cus_district_id))
                    # print("cus_main_cus_district_id 2: " + str(cus_main_cus_district_id))
                    if (cus_main_cus_district_id is not None):
                        if (cus_main_cus_district_id.isnumeric()):
                            if cus_main.cus_district_id is not None:
                                field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "District ID", int(cus_main.cus_district_id), int(cus_main_cus_district_id), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "District ID", cus_main.cus_district_id, int(cus_main_cus_district_id), "E", request)
                            if field_is_modified:
                                cus_main.cus_district_id = cus_main_cus_district_id
                                cus_main.cus_city_id = cus_main_city_id
                                cus_main.cus_country_id = cus_main_country_id
                                modified_records.append(record)

                    # CUS_NAME_EN
                    if (cus_main_cus_name_en is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Name EN", cus_main.cus_name_en, cus_main_cus_name_en, "E", request)
                        if field_is_modified:
                            cus_main.cus_name_en = cus_main_cus_name_en
                            modified_records.append(record)

                    # CUS_ADD1_EN
                    if (cus_main_cus_add1_en is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Address EN", cus_main.cus_add1_en, cus_main_cus_add1_en, "E", request)
                        if field_is_modified:
                            cus_main.cus_add1_en = cus_main_cus_add1_en
                            modified_records.append(record)                                

                    # CUS_ADD2_EN
                    if (cus_main_cus_add2_en is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Address2 EN", cus_main.cus_add2_en, cus_main_cus_add2_en, "E", request)
                        if field_is_modified:
                            cus_main.cus_add2_en = cus_main_cus_add2_en
                            modified_records.append(record)                                

                    # CUS_SUBDIST_EN
                    if (cus_main_cus_subdist_en is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Subdist EN", cus_main.cus_subdist_en, cus_main_cus_subdist_en, "E", request)
                        if field_is_modified:
                            cus_main.cus_subdist_en = cus_main_cus_subdist_en
                            modified_records.append(record)

                    # CUS_ZIP
                    if (cus_main_cus_zip is not None):
                        if cus_main_cus_zip.isnumeric():
                            if cus_main.cus_zip is not None:
                                field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Zip", int(cus_main.cus_zip), int(cus_main_cus_zip), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Zip", cus_main.cus_zip, int(cus_main_cus_zip), "E", request)

                            if field_is_modified:
                                cus_main.cus_zip = cus_main_cus_zip
                                modified_records.append(record)

                    # CUS_TEL
                    if (cus_main_cus_tel is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Telephone", cus_main.cus_tel, cus_main_cus_tel, "E", request)
                        if field_is_modified:
                            cus_main.cus_tel = cus_main_cus_tel
                            modified_records.append(record)

                    # CUS_FAX
                    if (cus_main_cus_fax is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Fax", cus_main.cus_fax, cus_main_cus_fax, "E", request)
                        if field_is_modified:
                            cus_main.cus_fax = cus_main_cus_fax
                            modified_records.append(record)

                    # CUS_EMAIL
                    if (cus_main_cus_email is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Email", cus_main.cus_email, cus_main_cus_email, "E", request)
                        if field_is_modified:
                            cus_main.cus_email = cus_main_cus_email
                            modified_records.append(record)

                    # Group ID - cus_taxid
                    cus_main_cus_taxid = request.POST.get('cus_main_cus_taxid')            
                    if (cus_main_cus_taxid is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Group ID", cus_main.cus_taxid, cus_main_cus_taxid, "E", request)
                        if field_is_modified:
                            cus_main.cus_taxid = cus_main_cus_taxid
                            modified_records.append(record)

                    # CUS_ZONE
                    if cus_main_cus_zone is not None:
                        if cus_main_cus_zone.isnumeric():
                            if cus_main.cus_zone_id is not None: 
                                field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Zone ID", int(cus_main.cus_zone_id), int(cus_main_cus_zone), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Zone ID", cus_main.cus_zone_id, int(cus_main_cus_zone), "E", request)
                            if field_is_modified:
                                cus_main.cus_zone_id = cus_main_cus_zone
                                modified_records.append(record)

                    # CUS_CONTACT
                    if cus_main_cus_contact_id is not None:
                        if cus_main_cus_contact_id.isnumeric():                  
                            if cus_main.cus_contact_id is not None:
                                field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Contact ID", int(cus_main.cus_contact_id), int(cus_main_cus_contact_id), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Contact ID", cus_main.cus_contact_id, int(cus_main_cus_contact_id), "E", request)
                            if field_is_modified:
                                cus_main.cus_contact_id = cus_main_cus_contact_id
                                modified_records.append(record)


                    if cus_main.upd_flag == 'A':
                        cus_main.upd_flag = 'E'
                    cus_main.upd_by = request.user.first_name
                    cus_main.upd_date = timezone.now()

                    cus_main.save()


                    # CUS_MAIN Business Type
                    try:
                        customer_option = CustomerOption.objects.get(cus_no=cus_no)

                        if customer_option is not None:
                            # customer_option.btype = cus_main_business_type.replace('&amp;', '&')
                            field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Business Type", customer_option.btype, cus_main_business_type.replace('&amp;', '&'), "E", request)
                            if field_is_modified:
                                customer_option.btype = cus_main_business_type.replace('&amp;', '&')
                                modified_records.append(record)

                            # Business Status
                            # customer_option.op1 = cus_main_customer_option_op1.rstrip() # Status
                            if (cus_main_customer_option_op1 is not None):
                                field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Status", customer_option.op1, cus_main_customer_option_op1, "E", request)
                                if field_is_modified:
                                    customer_option.op1 = cus_main_customer_option_op1
                                    modified_records.append(record)

                            # Business Group 1
                            # customer_option.op2 = cus_main_customer_option_op2.replace('&amp;', '&') # Group 1
                            field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Group 1", customer_option.op2, cus_main_customer_option_op2.replace('&amp;', '&'), "E", request)
                            if field_is_modified:
                                customer_option.op2 = cus_main_customer_option_op2.replace('&amp;', '&') # Group 1
                                modified_records.append(record)

                            # Business Group 2
                            # customer_option.op3 = cus_main_customer_option_op3.replace('&amp;', '&') # Group 2
                            field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Group 2", customer_option.op3, cus_main_customer_option_op3.replace('&amp;', '&'), "E", request)
                            if field_is_modified:
                                customer_option.op3 = cus_main_customer_option_op3.replace('&amp;', '&') # Group 2
                                modified_records.append(record)

                            # Business A/R Code
                            # customer_option.op4 = cus_main_customer_option_op4.rstrip() # A/R Code
                            field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "A/R Code", customer_option.op4, cus_main_customer_option_op4.replace('&amp;', '&'), "E", request)
                            if field_is_modified:
                                customer_option.op4 = cus_main_customer_option_op4.replace('&amp;', '&') # A/R Code
                                modified_records.append(record)

                            # Business GP Margin
                            if cus_main_customer_option_opn1 is not None:
                                if customer_option.opn1 is not None:
                                    field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "GP Margin", float(customer_option.opn1), float(cus_main_customer_option_opn1), "E", request)
                                else:
                                    field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "GP Margin", customer_option.opn1, float(cus_main_customer_option_opn1), "E", request)                                    
                                    
                                if field_is_modified:
                                    customer_option.opn1 = cus_main_customer_option_opn1 # GP Margin
                                    modified_records.append(record)
                            else:
                                customer_option.opn1 = 0

                            customer_option.save()
                            
                    except CustomerOption.DoesNotExist:
                        # Insert
                        if not cus_main_customer_option_opn1.isnumeric():
                            cus_main_customer_option_opn1 = 0                        

                        c = CustomerOption(
                            cus_no = cus_no, 
                            btype = cus_main_business_type.replace('&amp;', '&'), 
                            op1 = cus_main_customer_option_op1,   # Status
                            op2 = cus_main_customer_option_op2.replace('&amp;', '&'), # Group 1
                            op3 = cus_main_customer_option_op3.replace('&amp;', '&'), # Group 2
                            op4 = cus_main_customer_option_op4, # A/R Code
                            opn1 = float(cus_main_customer_option_opn1))
                        c.save()

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


            except CusMain.DoesNotExist:
                cus_main_cus_taxid = request.POST.get('cus_main_cus_taxid')            
                print("cus_main_cus_taxid " + str(cus_main_cus_taxid))

                new_customer_main = CusMain(
                    cus_active = cus_main_cus_active,
                    cus_main = cus_main,
                    cus_id = cus_id,
                    cus_name_th = cus_main_cus_name_th,
                    cus_add1_th = cus_main_cus_add1_th,
                    cus_add2_th = cus_main_cus_add2_th,
                    cus_subdist_th = cus_main_cus_subdist_th,
                    cus_district_id = cus_main_cus_district_id,
                    cus_city_id = cus_main_city_id,
                    cus_country_id = cus_main_country_id,
                    cus_name_en = cus_main_cus_name_en,
                    cus_add1_en = cus_main_cus_add1_en,
                    cus_add2_en = cus_main_cus_add2_en,
                    cus_subdist_en = cus_main_cus_subdist_en,                    
                    cus_zip = cus_main_cus_zip,
                    cus_tel = cus_main_cus_tel,
                    cus_fax = cus_main_cus_fax,
                    cus_email = cus_main_cus_email,
                    cus_taxid = cus_main_cus_taxid,
                    cus_zone_id = cus_main_cus_zone,
                    site_contact_id = cus_main_cus_contact_id,
                    upd_date = timezone.now(),
                    upd_flag = 'A',
                    upd_by = request.user.first_name
                    )
                new_customer_main.save()                     

                # CUS_MAIN Business Type
                try:
                    customer_option = CustomerOption.objects.get(cus_no=cus_no)
                    customer_option.btype = cus_main_business_type.replace('&amp;', '&')
                    customer_option.op1 = cus_main_customer_option_op1.rstrip() # Status
                    customer_option.op2 = cus_main_customer_option_op2.replace('&amp;', '&') # Group 1
                    customer_option.op3 = cus_main_customer_option_op3.replace('&amp;', '&') # Group 2
                    customer_option.op4 = cus_main_customer_option_op4.rstrip() # A/R Code
                    customer_option.save()
                    print("save cus_main_customer_option")
                except CustomerOption.DoesNotExist:
                    # Insert
                    c = CustomerOption(
                        cus_no = cus_no, 
                        btype = cus_main_business_type.replace('&amp;', '&'), 
                        op1 = cus_main_customer_option_op1,   # Status
                        op2 = cus_main_customer_option_op2.replace('&amp;', '&'), # Group 1
                        op3 = cus_main_customer_option_op3.replace('&amp;', '&'), # Group 2
                        op4 = cus_main_customer_option_op4, # A/R Code
                        opn1 = cus_main_customer_option_opn1)   # GP Margin
                    c.save()


            # ******************************************
            # **************  CUS_SITE  ****************
            # ******************************************
            cus_site_cus_active = request.POST.get('cus_site_cus_active')
            print("********************************")
            print("cus_site_cus_active = " + str(cus_site_cus_active))
            print("********************************")
            
            cus_site_cus_name_th = request.POST.get('cus_site_cus_name_th')
            cus_site_cus_add1_th = request.POST.get('cus_site_cus_add1_th')
            cus_site_cus_add2_th = request.POST.get('cus_site_cus_add2_th')
            cus_site_cus_subdist_th = request.POST.get('cus_site_cus_subdist_th')            
            cus_site_cus_name_en = request.POST.get('cus_site_cus_name_en')
            cus_site_cus_add1_en = request.POST.get('cus_site_cus_add1_en')
            cus_site_cus_add2_en = request.POST.get('cus_site_cus_add2_en')
            cus_site_cus_subdist_en = request.POST.get('cus_site_cus_subdist_en')            
            cus_site_cus_zip = request.POST.get('cus_site_cus_zip')
            if not cus_site_cus_zip:
                cus_site_cus_zip = None
            cus_site_cus_tel = request.POST.get('cus_site_cus_tel')
            cus_site_cus_fax = request.POST.get('cus_site_cus_fax')
            cus_site_cus_email = request.POST.get('cus_site_cus_email')
            cus_site_cus_zone = request.POST.get('cus_site_cus_zone')
            # customer_group_id = request.POST.get('customer_group_id')
            cus_site_cus_district_id = request.POST.get('cus_site_cus_district_id')
            # print("cus_site_cus_district_id = " + str(cus_site_cus_district_id))
            
            # Fulfill district, city, country
            cus_site_cus_district_id = None
            cus_site_city_id = None
            cus_site_country_id = None    
            cus_site_cus_district_id = request.POST.get('cus_site_cus_district_id')
            if (cus_site_cus_district_id is not None):
                if (cus_site_cus_district_id.isnumeric()):
                    try:
                        district_obj = TDistrict.objects.get(dist_id=cus_site_cus_district_id)
                        if district_obj is not None:
                            cus_site_city_id = district_obj.city_id_id
                            city_obj = TCity.objects.get(city_id=cus_site_city_id)
                            cus_site_country_id = city_obj.country_id_id
                    except TDistrict.DoesNotExist:
                        cus_site_cus_district_id = None
                        cus_site_city_id = None
                        cus_site_country_id = None
            else:
                cus_site_cus_district_id = None
                cus_site_city_id = None
                cus_site_country_id = None       

            cus_site_site_contact_id = request.POST.get('cus_site_site_contact_id')

            '''
            print("------ Print CUS_SITE data -------")
            print("cus_no = " + str(cus_no))
            print("cus_site_cus_active = " + str(cus_site_cus_active))
            print("cus_site_cus_name = " + str(cus_site_cus_name_th))
            print("cus_site_cus_district_id = " + str(cus_site_cus_district_id))
            print("cus_site_city_id = " + str(city_id))
            print("cus_site_country_id = " + str(country_id))
            print("cus_site_cus_zip = " + str(cus_site_cus_zip))
            print("cus_site_cus_zone = " + str(cus_site_cus_zone))
            print("------------------------")
            '''

            try:
                modified_records = []
                customer = Customer.objects.get(pk=cus_no)

                if customer is not None:
                    
                    # CUS_ACTIVE
                    #customer.cus_active = cus_site_cus_active
                    field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Status", int(customer.cus_active), int(cus_site_cus_active), "E", request)
                    if field_is_modified:
                        customer.cus_active = cus_site_cus_active
                        modified_records.append(record)

                        if int(cus_site_cus_active) == 1:
                            customer.cus_site = 1
                        else:
                            customer.cus_site = 0

                    # CUS_NAME_TH
                    #customer.cus_name_th = cus_site_cus_name_th
                    field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Name TH", customer.cus_name_th, cus_site_cus_name_th, "E", request)
                    if field_is_modified:
                        customer.cus_name_th = cus_site_cus_name_th
                        modified_records.append(record)

                    # CUS_ADD1_TH
                    # customer.cus_add1_th = cus_site_cus_add1_th
                    if (cus_site_cus_add1_th is not None):
                        field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Address1 TH", customer.cus_add1_th, cus_site_cus_add1_th, "E", request)
                        if field_is_modified:
                            customer.cus_add1_th = cus_site_cus_add1_th
                            modified_records.append(record)                                

                    # CUS_ADD2_TH
                    #customer.cus_add2_th = cus_site_cus_add2_th
                    if (cus_site_cus_add1_th is not None):
                        field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Address2 TH", customer.cus_add2_th, cus_site_cus_add2_th, "E", request)
                        if field_is_modified:
                            customer.cus_add2_th = cus_site_cus_add2_th
                            modified_records.append(record)                              

                    # CUS_SUBDIST_TH
                    # customer.cus_subdist_th = cus_site_cus_subdist_th
                    if (cus_site_cus_subdist_th is not None):
                        field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Sub-District TH", customer.cus_subdist_th, cus_site_cus_subdist_th, "E", request)
                        if field_is_modified:
                            customer.cus_subdist_th = cus_site_cus_subdist_th
                            modified_records.append(record)                              
                    
                    # CUS_NAME_EN
                    #customer.cus_name_en = cus_site_cus_name_en
                    field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Name EN", customer.cus_name_en, cus_site_cus_name_en, "E", request)
                    if field_is_modified:
                        customer.cus_name_en = cus_site_cus_name_en
                        modified_records.append(record)

                    # CUS_ADD1_EN
                    # customer.cus_add1_en = cus_site_cus_add1_en
                    if (cus_site_cus_add1_en is not None):
                        field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Address1 EN", customer.cus_add1_en, cus_site_cus_add1_en, "E", request)
                        if field_is_modified:
                            customer.cus_add1_en = cus_site_cus_add1_en
                            modified_records.append(record)                                

                    # CUS_ADD2_EN
                    #customer.cus_add2_en = cus_site_cus_add2_en
                    if (cus_site_cus_add1_en is not None):
                        field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Address2 EN", customer.cus_add2_en, cus_site_cus_add2_en, "E", request)
                        if field_is_modified:
                            customer.cus_add2_en = cus_site_cus_add2_en
                            modified_records.append(record)                              

                    # CUS_SUBDIST_EN
                    # customer.cus_subdist_en = cus_site_cus_subdist_en
                    if (cus_site_cus_subdist_en is not None):
                        field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Sub-District EN", customer.cus_subdist_en, cus_site_cus_subdist_en, "E", request)
                        if field_is_modified:
                            customer.cus_subdist_en = cus_site_cus_subdist_en
                            modified_records.append(record)   


                    # CUS_DISTRICT_ID
                    if (cus_site_cus_district_id is not None):
                        if (cus_site_cus_district_id.isnumeric()):
                            if customer.cus_district_id is not None:
                                field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "District ID", int(customer.cus_district_id), int(cus_site_cus_district_id), "E", request)
                            else:                                
                                field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "District ID", customer.cus_district_id, int(cus_site_cus_district_id), "E", request)
                            if field_is_modified:
                                customer.cus_district_id = cus_site_cus_district_id
                                customer.cus_city_id = cus_site_city_id
                                customer.cus_country_id = cus_site_country_id
                                modified_records.append(record)

                    # CUS_ZIP
                    if (cus_site_cus_zip is not None):
                        if customer.cus_zip is not None:
                            if cus_site_cus_zip.isnumeric():
                                field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Zip", int(customer.cus_zip), int(cus_site_cus_zip), "E", request)
                        else:
                            field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Zip", customer.cus_zip, int(cus_site_cus_zip), "E", request)

                        if field_is_modified:
                            customer.cus_zip = cus_site_cus_zip
                            modified_records.append(record)

                    # CUS_TEL
                    # customer.cus_tel = cus_site_cus_tel
                    if (cus_site_cus_tel is not None):
                        field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Telephone", customer.cus_tel, cus_site_cus_tel, "E", request)
                        if field_is_modified:
                            customer.cus_tel = cus_site_cus_tel
                            modified_records.append(record)

                    # CUS_FAX
                    # customer.cus_fax = cus_site_cus_fax
                    if (cus_site_cus_fax is not None):
                        field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Fax", customer.cus_fax, cus_site_cus_fax, "E", request)
                        if field_is_modified:
                            customer.cus_fax = cus_site_cus_fax
                            modified_records.append(record)

                    # CUS_EMAIL
                    # customer.cus_email = cus_site_cus_email
                    if (cus_site_cus_email is not None):
                        field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Email", customer.cus_email, cus_site_cus_email, "E", request)
                        if field_is_modified:
                            customer.cus_email = cus_site_cus_email
                            modified_records.append(record)

                    # CUS_TAXID
                    cus_main_cus_taxid = request.POST.get('cus_main_cus_taxid')            
                    if (cus_main_cus_taxid is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Group ID", customer.cus_taxid, cus_main_cus_taxid, "E", request)
                        if field_is_modified:
                            customer.cus_taxid = cus_main_cus_taxid
                            modified_records.append(record)

                    # CUS_ZONE
                    # customer.cus_zone_id = cus_site_cus_zone
                    if cus_site_cus_zone is not None:
                        if cus_site_cus_zone.isnumeric():
                            if customer.cus_zone_id is not None: 
                                field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Zone ID", int(customer.cus_zone_id), int(cus_site_cus_zone), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Zone ID", customer.cus_zone_id, int(cus_site_cus_zone), "E", request)
                            if field_is_modified:
                                customer.cus_zone_id = cus_site_cus_zone
                                modified_records.append(record)

                    # CUS_CONTACT
                    if cus_site_site_contact_id is not None:
                        if cus_site_site_contact_id.isnumeric():
                            if (customer.cus_contact_id is None):
                                field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Contact ID", customer.site_contact_id, int(cus_site_site_contact_id), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_SITE", cus_no, "Contact ID", int(customer.site_contact_id), int(cus_site_site_contact_id), "E", request)

                            if field_is_modified:
                                customer.site_contact_id = cus_site_site_contact_id
                                modified_records.append(record)

                    customer.upd_date = timezone.now()
                    customer.upd_by = request.user.first_name                    
                    if customer.upd_flag == 'A':
                        customer.upd_flag = 'E'

                    if customer.upd_flag == 'D':
                        customer.upd_flag = 'E'
                        
                    customer.save()

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

            except Customer.DoesNotExist:
                new_customer_site = Customer(
                    cus_active = cus_site_cus_active,
                    cus_site = cus_site,
                    cus_no = cus_no,
                    cus_id = cus_id,
                    cus_brn = cus_brn,
                    cus_name_th = cus_site_cus_name_th,
                    cus_add1_th = cus_site_cus_add1_th,
                    cus_add2_th = cus_site_cus_add2_th,
                    cus_subdist_th = cus_site_cus_subdist_th,
                    cus_district_id = cus_site_cus_district_id,
                    cus_city_id = cus_site_city_id,
                    cus_country_id = cus_site_country_id,
                    cus_name_en = cus_site_cus_name_en,
                    cus_add1_en = cus_site_cus_add1_en,
                    cus_add2_en = cus_site_cus_add2_en,
                    cus_subdist_en = cus_site_cus_subdist_en,                    
                    cus_zip = cus_site_cus_zip,
                    cus_tel = cus_site_cus_tel,
                    cus_fax = cus_site_cus_fax,
                    cus_email = cus_site_cus_email,
                    cus_taxid = cus_main_cus_taxid,
                    cus_zone_id = cus_site_cus_zone,
                    site_contact_id = cus_site_site_contact_id,
                    upd_date = timezone.now(),
                    upd_by = request.user.first_name,
                    upd_flag = 'A'
                    )
                new_customer_site.save()

                # History Log                    
                new_log = HrmsNewLog(
                    log_table = 'CUSTOMER',
                    log_key = cus_no,
                    log_field = None,
                    old_value = None,
                    new_value = None,
                    log_type = 'A',
                    log_by = request.user.username,
                    log_date = timezone.now(),
                    log_description = None
                    )
                new_log.save()    
                # ./History Log

            response_data['result'] = "Update complete."
            response_data['message'] = "ทำรายการสำเร็จ"
            response_data['form_is_valid'] = True




            # ******************************************
            # **************  CUS_BILL  ****************
            # ******************************************
            cus_bill_cus_active = request.POST.get('cus_bill_cus_active')
            cus_bill_cus_name_th = request.POST.get('cus_bill_cus_name_th')
            cus_bill_cus_add1_th = request.POST.get('cus_bill_cus_add1_th')
            cus_bill_cus_add2_th = request.POST.get('cus_bill_cus_add2_th')
            cus_bill_cus_subdist_th = request.POST.get('cus_bill_cus_subdist_th')            
            cus_bill_cus_district_id = request.POST.get('cus_bill_cus_district_id')
            # print("debug : cus_bill_cus_district_id = " + str(cus_bill_cus_district_id))

            cus_bill_cus_name_en = request.POST.get('cus_bill_cus_name_en')
            cus_bill_cus_add1_en = request.POST.get('cus_bill_cus_add1_en')
            cus_bill_cus_add2_en = request.POST.get('cus_bill_cus_add2_en')
            cus_bill_cus_subdist_en = request.POST.get('cus_bill_cus_subdist_en')
            cus_bill_cus_zip = request.POST.get('cus_bill_cus_zip')

            if not cus_bill_cus_zip:
                cus_bill_cus_zip = None

            cus_bill_cus_tel = request.POST.get('cus_bill_cus_tel')
            cus_bill_cus_fax = request.POST.get('cus_bill_cus_fax')
            cus_bill_cus_email = request.POST.get('cus_bill_cus_email')
            cus_bill_cus_zone = request.POST.get('cus_bill_cus_zone')

            # District
            # Fulfill district, city, country
            cus_bill_cus_district_id = None
            cus_bill_city_id = None
            cus_bill_country_id = None    
            cus_bill_cus_district_id = request.POST.get('cus_bill_cus_district_id')
            if (cus_bill_cus_district_id is not None):
                if (cus_bill_cus_district_id.isnumeric()):
                    try:
                        district_obj = TDistrict.objects.get(dist_id=cus_bill_cus_district_id)
                        if district_obj is not None:
                            cus_bill_city_id = district_obj.city_id_id
                            city_obj = TCity.objects.get(city_id=cus_bill_city_id)
                            cus_bill_country_id = city_obj.country_id_id
                    except TDistrict.DoesNotExist:
                        cus_bill_cus_district_id = None
                        cus_bill_city_id = None
                        cus_bill_country_id = None
            else:
                cus_bill_cus_district_id = None
                cus_bill_city_id = None
                cus_bill_country_id = None       


            # Billing Tab - Contact Information
            cus_bill_cus_contact_id = request.POST.get('cus_bill_cus_contact_id')
            if cus_bill_cus_contact_id:
                cus_bill_cus_contact_id = cus_bill_cus_contact_id
            else:
                cus_bill_cus_contact_id = None

            '''
            print("------ Print CUS_BILL data -------")
            print("cus_bill_cus_active = " + str(cus_bill_cus_active))
            print("cus_bill_cus_name_th = " + str(cus_bill_cus_name_th))
            print("cus_bill_cus_add1_th = " + str(cus_bill_cus_add1_th))
            print("cus_bill_cus_add2_th = " + str(cus_bill_cus_add2_th))
            print("cus_bill_cus_subdist_th = " + str(cus_bill_cus_subdist_th))
            print("cus_bill_cus_district_id = " + str(cus_bill_cus_district_id))
            print("cus_bill_cus_name_en = " + str(cus_bill_cus_name_en))
            print("cus_bill_cus_add1_en = " + str(cus_bill_cus_add1_en))
            print("cus_bill_cus_add2_en = " + str(cus_bill_cus_add2_en))
            print("cus_bill_cus_subdist_en = " + str(cus_bill_cus_subdist_en))
            print("cus_bill_cus_zip = " + str(cus_bill_cus_zip))
            print("cus_bill_cus_tel = " + str(cus_bill_cus_tel))
            print("cus_bill_cus_fax = " + str(cus_bill_cus_fax))
            print("cus_bill_cus_email = " + str(cus_bill_cus_email))
            print("cus_bill_cus_zone = " + str(cus_bill_cus_zone))
            print("cus_bill_cus_contact_id = " + str(cus_bill_cus_contact_id))
            '''

            try:
                cusbill = CusBill.objects.get(pk=cus_no)

                if cusbill is not None:
                    # CUS_ACTIVE
                    # cusbill.cus_active = cus_bill_cus_active
                    field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Status", int(cusbill.cus_active), int(cus_bill_cus_active), "E", request)
                    if field_is_modified:
                        print("aabbccc")
                        cusbill.cus_active = cus_bill_cus_active
                        modified_records.append(record)                    

                        if int(cus_bill_cus_active) == 1:
                            cusbill.cus_bill = 1
                        else:
                            cusbill.cus_bill = 0

                    # CUS_NAME_TH                    
                    # cusbill.cus_name_th = cus_bill_cus_name_th
                    field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Name TH", cusbill.cus_name_th, cus_bill_cus_name_th, "E", request)
                    if field_is_modified:
                        cusbill.cus_name_th = cus_bill_cus_name_th
                        modified_records.append(record)
                                
                    # CUS_ADD1_TH                    
                    # cusbill.cus_add1_th = cus_bill_cus_add1_th
                    if (cus_bill_cus_add1_th is not None):
                        field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Address1 TH", cusbill.cus_add1_th, cus_bill_cus_add1_th, "E", request)
                        if field_is_modified:
                            cusbill.cus_add1_th = cus_bill_cus_add1_th
                            modified_records.append(record)                                

                    # CUS_ADD2_TH
                    # cusbill.cus_add2_th = cus_bill_cus_add2_th
                    if (cus_bill_cus_add2_th is not None):
                        field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Address2 TH", cusbill.cus_add2_th, cus_bill_cus_add2_th, "E", request)
                        if field_is_modified:
                            cusbill.cus_add2_th = cus_bill_cus_add2_th
                            modified_records.append(record)                              

                    # CUS_SUBDIST_TH                    
                    # cusbill.cus_subdist_th = cus_bill_cus_subdist_th                    
                    if (cus_bill_cus_subdist_th is not None):
                        field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Sub-District TH", cusbill.cus_subdist_th, cus_bill_cus_subdist_th, "E", request)
                        if field_is_modified:
                            cusbill.cus_subdist_th = cus_bill_cus_subdist_th
                            modified_records.append(record)                             
                                        
                    # CUS_NAME_EN
                    # cusbill.cus_name_en = cus_bill_cus_name_en
                    field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Name EN", cusbill.cus_name_en, cus_bill_cus_name_en, "E", request)
                    if field_is_modified:
                        cusbill.cus_name_en = cus_bill_cus_name_en
                        modified_records.append(record)
                                
                    # CUS_ADD1_EN
                    # cusbill.cus_add1_en = cus_bill_cus_add1_en
                    if (cus_bill_cus_add1_en is not None):
                        field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Address1 EN", cusbill.cus_add1_en, cus_bill_cus_add1_en, "E", request)
                        if field_is_modified:
                            cusbill.cus_add1_en = cus_bill_cus_add1_en
                            modified_records.append(record)                                

                    # CUS_ADD2_EN
                    # cusbill.cus_add2_en = cus_bill_cus_add2_en
                    if (cus_bill_cus_add2_en is not None):
                        field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Address2 EN", cusbill.cus_add2_en, cus_bill_cus_add2_en, "E", request)
                        if field_is_modified:
                            cusbill.cus_add2_en = cus_bill_cus_add2_en
                            modified_records.append(record)                              

                    # CUS_SUBDIST_EN 
                    # cusbill.cus_subdist_en = cus_bill_cus_subdist_en                 
                    if (cus_bill_cus_subdist_en is not None):
                        field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Sub-District EN", cusbill.cus_subdist_en, cus_bill_cus_subdist_en, "E", request)
                        if field_is_modified:
                            cusbill.cus_subdist_en = cus_bill_cus_subdist_en
                            modified_records.append(record)                             
                    
                    # CUS_DISTRICT_ID
                    # cusbill.cus_district_id = cus_bill_cus_district_id
                    if (cus_bill_cus_district_id is not None):
                        if (cus_bill_cus_district_id.isnumeric()):
                            if cusbill.cus_district_id is not None:
                                field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "District ID", int(cusbill.cus_district_id), int(cus_bill_cus_district_id), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "District ID", cusbill.cus_district_id, int(cus_bill_cus_district_id), "E", request)
                            if field_is_modified:
                                cusbill.cus_district_id = cus_bill_cus_district_id
                                cusbill.cus_city_id = cus_bill_city_id
                                cusbill.cus_country_id = cus_bill_country_id
                                modified_records.append(record)

                    # CUS_ZIP
                    # cusbill.cus_zip = cus_bill_cus_zip
                    if (cus_bill_cus_zip is not None):
                        if cus_bill_cus_zip.isnumeric():
                            if cusbill.cus_zip is not None:                            
                                field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Zip", int(cusbill.cus_zip), int(cus_bill_cus_zip), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Zip", cusbill.cus_zip, int(cus_bill_cus_zip), "E", request)
                            if field_is_modified:
                                cusbill.cus_zip = cus_bill_cus_zip
                                modified_records.append(record)

                    # CUS_TEL
                    # cusbill.cus_tel = cus_bill_cus_tel
                    if (cus_bill_cus_tel is not None):
                        field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Telephone", cusbill.cus_tel, cus_bill_cus_tel, "E", request)
                        if field_is_modified:
                            cusbill.cus_tel = cus_bill_cus_tel
                            modified_records.append(record)

                    # CUS_FAX                    
                    # cusbill.cus_fax = cus_bill_cus_fax
                    if (cus_bill_cus_fax is not None):
                        field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Fax", cusbill.cus_fax, cus_bill_cus_fax, "E", request)
                        if field_is_modified:
                            cusbill.cus_fax = cus_bill_cus_fax
                            modified_records.append(record)

                    # CUS_EMAIL
                    # cusbill.cus_email = cus_bill_cus_email
                    if (cus_bill_cus_email is not None):
                        field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Email", cusbill.cus_email, cus_bill_cus_email, "E", request)
                        if field_is_modified:
                            cusbill.cus_email = cus_bill_cus_email
                            modified_records.append(record)


                    # CUS_TAXID
                    cus_main_cus_taxid = request.POST.get('cus_main_cus_taxid')            
                    if (cus_main_cus_taxid is not None):
                        field_is_modified, record = check_modified_field("CUS_MAIN", cus_no, "Group ID", cusbill.cus_taxid, cus_main_cus_taxid, "E", request)
                        if field_is_modified:
                            cusbill.cus_taxid = cus_main_cus_taxid
                            modified_records.append(record)

                    # CUS_ZONE
                    # cusbill.cus_zone_id = cus_bill_cus_zone
                    if cus_bill_cus_zone is not None:
                        if cus_bill_cus_zone.isnumeric():
                            if cusbill.cus_zone_id is not None: 
                                field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Zone ID", int(cusbill.cus_zone_id), int(cus_bill_cus_zone), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Zone ID", cusbill.cus_zone_id, int(cus_bill_cus_zone), "E", request)
                            if field_is_modified:
                                cusbill.cus_zone_id = cus_bill_cus_zone
                                modified_records.append(record)                                

                    # CUS_CONTACT
                    cus_bill_cus_contact_id = request.POST.get('cus_bill_cus_contact_id')                    
                    if cus_bill_cus_contact_id is not None:
                        if cus_bill_cus_contact_id.isnumeric():
                            if (cusbill.cus_contact_id is None):
                                field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Contact ID", cusbill.site_contact_id, int(cus_bill_cus_contact_id), "E", request)
                            else:
                                field_is_modified, record = check_modified_field("CUS_BILL", cus_no, "Contact ID", int(cusbill.site_contact_id), int(cus_bill_cus_contact_id), "E", request)

                            if field_is_modified:
                                cusbill.cus_contact_id = cus_bill_cus_contact_id
                                cusbill.site_contact_id = cus_bill_cus_contact_id
                                modified_records.append(record)

                    cusbill.upd_date = timezone.now()
                    cusbill.upd_by = request.user.first_name                    
                    if cusbill.upd_flag == 'A':
                        cusbill.upd_flag = 'E'

                    if cusbill.upd_flag == 'D':
                        cusbill.upd_flag = 'E'

                    cusbill.save()

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
                
                    print("update cus_bill")

            except CusBill.DoesNotExist:
                if cus_bill_cus_active == 1:
                    cus_bill = 1
                else:
                    cus_bill = 0

                new_cusbill = CusBill(
                    cus_active = cus_bill_cus_active,
                    cus_bill = cus_bill,
                    cus_no = cus_no,
                    cus_id = cus_id,
                    cus_brn = cus_brn,
                    cus_name_th = cus_bill_cus_name_th,
                    cus_add1_th = cus_bill_cus_add1_th,
                    cus_add2_th = cus_bill_cus_add2_th,
                    cus_subdist_th = cus_bill_cus_subdist_th,
                    cus_district_id = cus_bill_cus_district_id,
                    cus_city_id = cus_bill_city_id,
                    cus_country_id = cus_bill_country_id,
                    cus_name_en = cus_bill_cus_name_en,
                    cus_add1_en = cus_bill_cus_add1_en,
                    cus_add2_en = cus_bill_cus_add2_en,
                    cus_subdist_en = cus_bill_cus_subdist_en,                    
                    cus_zip = cus_bill_cus_zip,
                    cus_tel = cus_bill_cus_tel,
                    cus_fax = cus_bill_cus_fax,
                    cus_email = cus_bill_cus_email,
                    cus_taxid = cus_main_cus_taxid,
                    cus_zone_id = cus_bill_cus_zone,
                    cus_contact_id = cus_bill_cus_contact_id,
                    site_contact_id = cus_bill_cus_contact_id,
                    upd_date = timezone.now(),
                    upd_by = request.user.first_name,
                    upd_flag = 'A'                    
                    )
                new_cusbill.save()
                print("insert cus_bill")

            print("OK")
            print("****************************")

        else:
            print("form is invalid")

            response_data['form_is_valid'] = False
            response_data['message'] = ""
            if form.errors:
                for field in form:
                    for error in field.errors:
                        # response_data['message'] += field.name + " | " + error + "<br>"
                        response_data['message'] += error + "<br>"

                response_data['errors'] = form.errors
            else:
                response_data['message'] = "ไม่สามารถทำรายการได้..!"
        
            print("Error!")
            print("****************************")

        return JsonResponse(response_data)
    else:
        print("debug - found cus_main_form problem")

    context = {
        'page_title': settings.PROJECT_NAME,
        'today_date': settings.TODAY_DATE,
        'project_version': settings.PROJECT_VERSION,
        'db_server': settings.DATABASES['default']['HOST'],
        'project_name': settings.PROJECT_NAME,
        'business_type': 'abc',
    }

    return render(request, template_name, context)    


@login_required(login_url='/accounts/login/')
def get_contact_list_modal(request):

    print("**********************************")    
    print("FUNCTION: get_contact_list_modal")
    print("**********************************")

    data = []
    item_per_page = 200
    page_no = request.GET["page_no"]
    current_contact_id = request.GET["current_contact_id"]
    search_contact_option = request.GET["search_contact_option"]
    search_contact_text = request.GET["search_contact_text"]

    '''    
    print("current_contact_id = " + str(current_contact_id))
    print("search_contact_option = " + str(search_contact_option))
    print("search_contact_text = " + str(search_contact_text))
    '''

    if search_contact_option == "1":
        data = CusContact.objects.filter(con_id__exact=search_contact_text)

    if search_contact_option == "2":
        data = CusContact.objects.filter(con_fname_th__istartswith=search_contact_text)
        if not data:
            data = CusContact.objects.filter(con_fname_en__istartswith=search_contact_text)

    if search_contact_option == "3":
        data = CusContact.objects.filter(con_lname_th__istartswith=search_contact_text)
        if not data:
            data = CusContact.objects.filter(con_lname_en__istartswith=search_contact_text)

    if data:
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
                # print("debug 1")
                record = {
                    "con_id": d.con_id,
                    "con_fname_th": d.con_fname_th,
                    "con_lname_th": d.con_lname_th,
                    "con_position_th": d.con_position_th,
                    "con_position_en": d.con_position_en,
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
            response = JsonResponse(data={
                "success": False,
                "results": [],
            })
            response.status_code = 403
            return response
    else:        
        response = JsonResponse(data={
            "success": False,
            "error"
            "results": [],
        })
        response.status_code = 403
        return response


@login_required(login_url='/accounts/login/')
def get_contact_list(request):

    print("****************************")
    print("FUNCTION: get_contact_list")
    print("****************************")

    current_contact_id = request.GET.get('current_contact_id')
    
    print("*************************")    
    print("current_contact_id : " + str(current_contact_id))

    if current_contact_id:
        print("Not none")
    else:
        print("None")
    print("*************************")

    item_per_page = 100

    if request.method == "POST":

        if current_contact_id == None:
            data = CusContact.objects.all()
        else:
            data = CusContact.objects.filter(con_id__exact=current_contact_id)            

        page = 1
        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))
    else:
        print("method get")


        if request.method == 'GET' and 'current_contact_id' in request.GET:
            current_contact_id = request.GET.get('current_contact_id')
            
        if current_contact_id:
            data = CusContact.objects.filter(con_id__exact=current_contact_id)
        else:
            data = CusContact.objects.all()


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
                "con_id": d.con_id,
                "con_fname_th": d.con_fname_th,
                "con_lname_th": d.con_lname_th
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


@login_required(login_url='/accounts/login/')
def get_contact(request):

    print("****************************")
    print("FUNCTION: get_contact")
    print("****************************")

    contact_id = request.GET.get('contact_id')
    print("contact_id : " + str(contact_id))

    #data = CusContact.objects.filter(con_id__exact=contact_id)

    data = CusContact.objects.select_related('con_title').filter(con_id__exact=contact_id)

    if data:
        pickup_dict = {}
        pickup_records=[]
        
        for d in data:
            record = {
                "con_id": d.con_id,
                "con_fname_th": d.con_fname_th,
                "con_lname_th": d.con_lname_th,
                "con_position_th": d.con_position_th,
                "con_title_th": d.con_title.title_th,
            }
            pickup_records.append(record)

        response = JsonResponse(data={
            "success": True,            
            "results": list(pickup_records)        
        })
        response.status_code = 200
    else:
        print("error")
        response = JsonResponse(data={
            "success": False,
            "contact": [],
        })

        response = JsonResponse({"error": "there was an error"})
        response.status_code = 403
    
    return response        


@login_required(login_url='/accounts/login/')
def get_country(request):

    dist_id = request.GET["dist_id"]    
    
    data = TDistrict.objects.select_related('city_id').filter(dist_id__exact=dist_id).get()
    country_en = data.city_id.country_id.country_en
    country_th = data.city_id.country_id.country_th
    
    response = JsonResponse(data={"success": True, "country_en": country_en, "country_th": country_th})
    response.status_code = 200

    return response

