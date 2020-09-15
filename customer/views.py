from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import generic
from .models import Customer, CusMain, CusBill, CustomerOption
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
def CustomerCreate(request):
    template_name = 'customer/customer_create.html'
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    today_date = settings.TODAY_DATE
    response_data = dict()

    if request.method == "POST":
        if form.is_valid():          
            cus_site_form = CusSiteCreateForm(request.POST, user=request.user)
            response_data['form_is_valid'] = True            
        else:            
            response_data['form_is_valid'] = False

        return JsonResponse(response_data)     
    else:
        print("GET")
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

        '''
        print("cus_id = " + str(cus_id))
        print("cus_brn = " + str(cus_brn))
        print("**************************")
        '''

        form = CustomerCodeCreateForm(request.POST)        
        pickup_records=[]
        business_type_list = []
        group_1_list = []
        group_2_list = []
        customer_option = []

        if form.is_valid():
            # print("form is valid")            

            try:                
                cus_main = CusMain.objects.get(pk=cus_id)
                
                '''
                print("cus_main.cus_contact_id = " + str(cus_main.cus_contact_id))
                print(cus_main.cus_contact.con_title.title_en)
                print(cus_main.cus_contact.con_fname_th)
                print(cus_main.cus_contact.con_lname_th)
                print(cus_main.cus_contact.con_position_th)
                '''

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

                    if not cus_main.site_contact_id:
                        cus_main_site_contact_title_th = ""
                        cus_main_site_contact_fname_th = ""
                        cus_main_site_contact_lname_th = ""
                        cus_main_site_contact_position_th = "" 
                    else:
                        cus_main_site_contact_title_th = cus_main.site_contact.con_title.title_th
                        cus_main_site_contact_fname_th = cus_main.site_contact.con_fname_th
                        cus_main_site_contact_lname_th = cus_main.site_contact.con_lname_th,
                        cus_main_site_contact_position_th = cus_main.site_contact.con_position_th

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
                        "cus_contact_title_th": cus_main_site_contact_title_th,
                        "cus_contact_fname_th": cus_main_site_contact_fname_th,
                        "cus_contact_lname_th": cus_main_site_contact_lname_th,
                        "cus_contact_position_th": cus_main_site_contact_position_th,
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
    item_per_page = 50
    context = {
        'page_title': page_title, 
        'db_server': db_server, 'today_date': today_date,
        'project_name': project_name, 
        'project_version': project_version,         
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

def CustomerUpdate(request, pk):
    # print("check")
    # print("pk = " + str(pk))

    template_name = 'customer/customer_update.html'
    
    cus_no = pk
    customer = get_object_or_404(Customer, pk=pk)
    cus_main = None
    cus_site = None
    cus_bill = None

    if customer:
        try:
            cus_main = CusMain.objects.get(pk=customer.cus_id)
        except CusMain.DoesNotExist:
            cus_main = None

        try:
            cus_site = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            cus_site = None

        try:
            cus_bill = CusBill.objects.get(pk=pk)

            # print("check cus_subdist_th")
            # print(cus_bill.cus_subdist_th)
        except CusBill.DoesNotExist:
            cus_bill = None

    if request.method == 'POST':        
        cus_main_form = CusMainForm(request.POST, instance=cus_main, cus_no=pk)
        cus_site_form = CusSiteForm(request.POST, instance=cus_site, cus_no=pk)
        cus_bill_form = CusBillForm(request.POST, instance=cus_bill, cus_no=pk)
    else:
        cus_main_form = CusMainForm(instance=cus_main, cus_no=pk)    
        cus_site_form = CusSiteForm(instance=cus_site)
        cus_bill_form = CusBillForm(instance=cus_bill)

    # print("customer cus_active = " + str(customer.cus_active))
    business_type_list = CustomerOption.objects.values_list('btype', flat=True).exclude(btype=None).order_by('btype').distinct()
    group_1_list = CustomerOption.objects.values_list('op2', flat=True).exclude(op2=None).order_by('op2').distinct()
    group_2_list = CustomerOption.objects.values_list('op3', flat=True).exclude(op2=None).order_by('op3').distinct()

    customer_option = []
    try:
        customer_option = CustomerOption.objects.get(cus_no=pk)
        business_type = customer_option.btype
    except CustomerOption.DoesNotExist:
        business_type = ""
        print("Insert complete")


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
        'business_type_list': business_type_list,
        'group_1_list': group_1_list,
        'group_2_list': group_2_list,
    }
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
        if current_district_id:
            district_object = TDistrict.objects.filter(dist_id__exact=current_district_id).get()
            data = TDistrict.objects.select_related('city_id').filter(city_id__city_th__contains=district_object.city_id.city_th)
            if not data:
                data = TDistrict.objects.select_related('city_id').filter(city_id__city_en__contains=district_object.city_id.city_en)
        else:
            data = TDistrict.objects.select_related('city_id').all()

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


@login_required(login_url='/accounts/login/')
def update_all_cus_tabs(request):

    print("****************************")
    print("FUNCTION: update_all_cus_tabs")
    # print("****************************")

    template_name = 'customer/customer_update.html'    
    response_data = {}

    if request.method == 'POST':
        form = CusAllTabsForm(request.POST)

        if form.is_valid():            
            cus_id = request.POST.get('cus_id')
            cus_brn = request.POST.get('cus_brn').zfill(3)
            cus_no = str(cus_id) + str(cus_brn)

            # ******************************************
            # **************  CUS_MAIN  ****************
            # ******************************************            
            cus_main_cus_active = request.POST.get('cus_main_cus_active')
            cus_main_cus_name_th = request.POST.get('cus_main_cus_name_th')            
            cus_main_cus_add1_th = request.POST.get('cus_main_cus_add1_th')
            cus_main_cus_add2_th = request.POST.get('cus_main_cus_add2_th')
            cus_main_cus_subdist_th = request.POST.get('cus_main_cus_subdist_th')                        
            cus_main_cus_name_en = request.POST.get('cus_main_cus_name_en')                          
            cus_main_cus_add1_en = request.POST.get('cus_main_cus_add1_en')
            cus_main_cus_add2_en = request.POST.get('cus_main_cus_add2_en')
            cus_main_cus_district_id = request.POST.get('id_cus_main_cus_district_id')
            cus_main_cus_subdist_en = request.POST.get('cus_main_cus_subdist_en')
            cus_main_cus_zip = request.POST.get('cus_main_cus_zip')
            if not cus_main_cus_zip:
                cus_main_cus_zip = None
            cus_main_cus_tel = request.POST.get('cus_main_cus_tel')
            cus_main_cus_fax = request.POST.get('cus_main_cus_fax')
            cus_main_cus_email = request.POST.get('cus_main_cus_email')
            cus_main_cus_zone = request.POST.get('cus_main_cus_zone')                

            cus_main_cus_district_id = request.POST.get('cus_main_cus_district_id')
            if cus_main_cus_district_id:
                try:
                    district_obj = TDistrict.objects.get(dist_id=cus_main_cus_district_id)
                    if district_obj:
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

            cus_main_business_type = request.POST.get('cus_main_business_type')
            cus_main_customer_option_op1 = request.POST.get('cus_main_customer_option_op1')
            cus_main_customer_option_op2 = request.POST.get('cus_main_customer_option_op2')
            cus_main_customer_option_op3 = request.POST.get('cus_main_customer_option_op3')
            cus_main_customer_option_op4 = request.POST.get('cus_main_customer_option_op4')
            cus_main_cus_contact_id = request.POST.get('cus_main_cus_contact_id')
            if cus_main_cus_contact_id:
                cus_main_cus_contact_id = cus_main_cus_contact_id
            else:
                cus_main_cus_contact_id = None

            print("------ Print CUS_MAIN data -------")
            print("cus_main_business_type = " + str(cus_main_business_type))
            print("cus_main_customer_option_op1 = " + str(cus_main_customer_option_op1))
            print("cus_main_customer_option_op2 = " + str(cus_main_customer_option_op2))
            print("cus_main_customer_option_op3 = " + str(cus_main_customer_option_op3))
            print("cus_main_customer_option_op4 = " + str(cus_main_customer_option_op4))
            
            try:
                cus_main = CusMain.objects.get(pk=cus_id)
                if cus_main:
                    cus_main.cus_active = cus_main_cus_active
                    cus_main.cus_name_th = cus_main_cus_name_th
                    cus_main.cus_add1_th = cus_main_cus_add1_th
                    cus_main.cus_add2_th = cus_main_cus_add2_th
                    cus_main.cus_subdist_th = cus_main_cus_subdist_th
                    cus_main.cus_name_en = cus_main_cus_name_en
                    cus_main.cus_add1_en = cus_main_cus_add1_en
                    cus_main.cus_add2_en = cus_main_cus_add2_en
                    cus_main.cus_subdist_en = cus_main_cus_subdist_en
                    cus_main.cus_zip = cus_main_cus_zip
                    cus_main.cus_tel = cus_main_cus_tel
                    cus_main.cus_fax = cus_main_cus_fax
                    cus_main.cus_email = cus_main_cus_email
                    cus_main.cus_zone_id = cus_main_cus_zone
                    cus_main.cus_contact_id = cus_main_cus_contact_id
                    if cus_main.upd_flag == 'A':
                        cus_main.upd_flag = 'E'
                    cus_main.upd_by = request.user.first_name
                    cus_main.upd_date = timezone.now()        
                    cus_main.save()

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
                            op4 = cus_main_customer_option_op4)   # A/R Code
                        c.save()

            except CusMain.DoesNotExist:
                new_customer_main = CusMain(
                    cus_active = cus_main_cus_active,
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
                    cus_zone_id = cus_main_cus_zone,
                    site_contact_id = cus_main_cus_contact_id,
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
                        op4 = cus_main_customer_option_op4)   # A/R Code
                    c.save()



            # ******************************************
            # **************  CUS_SITE  ****************
            # ******************************************
            cus_site_cus_active = request.POST.get('cus_site_cus_active')            
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
            
            cus_site_cus_district_id = request.POST.get('cus_site_cus_district_id')
            if cus_site_cus_district_id:
                print("debug 1")
                try:
                    district_obj = TDistrict.objects.get(dist_id=cus_site_cus_district_id)
                    if district_obj:
                        print("debug 2")
                        city_id = district_obj.city_id_id
                        city_obj = TCity.objects.get(city_id=city_id)
                        country_id = city_obj.country_id_id
                except TDistrict.DoesNotExist:
                    print("debug 3")
                    cus_site_cus_district_id = None
                    city_id = None
                    country_id = None
            else:
                cus_site_cus_district_id = None
                city_id = None
                country_id = None

            cus_site_site_contact_id = request.POST.get('cus_site_site_contact_id')
            if cus_site_site_contact_id:
                cus_site_site_contact_id = cus_site_site_contact_id
            else:
                cus_site_site_contact_id = None

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
                customer = Customer.objects.get(pk=cus_no)
                customer.cus_active = cus_site_cus_active
                customer.cus_name_th = cus_site_cus_name_th
                customer.cus_add1_th = cus_site_cus_add1_th
                customer.cus_add2_th = cus_site_cus_add2_th
                customer.cus_subdist_th = cus_site_cus_subdist_th
                customer.cus_district_id = cus_site_cus_district_id
                customer.cus_city_id = city_id
                customer.cus_country_id = country_id
                customer.cus_name_en = cus_site_cus_name_en
                customer.cus_add1_en = cus_site_cus_add1_en
                customer.cus_add2_en = cus_site_cus_add2_en
                customer.cus_subdist_en = cus_site_cus_subdist_en
                customer.cus_zip = cus_site_cus_zip
                customer.cus_tel = cus_site_cus_tel
                customer.cus_fax = cus_site_cus_fax
                customer.cus_email = cus_site_cus_email
                customer.cus_zone_id = cus_site_cus_zone
                customer.site_contact_id = cus_site_site_contact_id

                if customer.upd_flag == 'A':
                    customer.upd_flag = 'E'

                if customer.upd_flag == 'D':
                    customer.upd_flag = 'E'
                    
                customer.save()                
            except Customer.DoesNotExist:                
                new_customer_site = Customer(
                    cus_active = cus_site_cus_active,
                    cus_no = cus_no,
                    cus_id = cus_id,
                    cus_brn = cus_brn,
                    cus_name_th = cus_site_cus_name_th,
                    cus_add1_th = cus_site_cus_add1_th,
                    cus_add2_th = cus_site_cus_add2_th,
                    cus_subdist_th = cus_site_cus_subdist_th,
                    cus_district_id = cus_site_cus_district_id,
                    cus_city_id = city_id,
                    cus_country_id = country_id,
                    cus_name_en = cus_site_cus_name_en,
                    cus_add1_en = cus_site_cus_add1_en,
                    cus_add2_en = cus_site_cus_add2_en,
                    cus_subdist_en = cus_site_cus_subdist_en,                    
                    cus_zip = cus_site_cus_zip,
                    cus_tel = cus_site_cus_tel,
                    cus_fax = cus_site_cus_fax,
                    cus_email = cus_site_cus_email,
                    cus_zone_id = cus_site_cus_zone,
                    site_contact_id = cus_site_site_contact_id,
                    )
                new_customer_site.save()                
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

            cus_bill_cus_district_id = request.POST.get('cus_bill_cus_district_id')
            if cus_bill_cus_district_id:
                try:
                    district_obj = TDistrict.objects.get(dist_id=cus_bill_cus_district_id)
                    if district_obj:
                        city_id = district_obj.city_id_id
                        city_obj = TCity.objects.get(city_id=city_id)
                        country_id = city_obj.country_id_id
                except TDistrict.DoesNotExist:
                    cus_bill_cus_district_id = None
                    city_id = None
                    country_id = None
            else:
                cus_bill_cus_district_id = None
                city_id = None
                country_id = None

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

                cusbill.cus_active = cus_bill_cus_active
                cusbill.cus_name_th = cus_bill_cus_name_th
                cusbill.cus_add1_th = cus_bill_cus_add1_th
                cusbill.cus_add2_th = cus_bill_cus_add2_th
                cusbill.cus_subdist_th = cus_bill_cus_subdist_th
                cusbill.cus_district_id = cus_bill_cus_district_id
                cusbill.cus_city_id = city_id
                cusbill.cus_country_id = country_id
                cusbill.cus_name_en = cus_bill_cus_name_en
                cusbill.cus_add1_en = cus_bill_cus_add1_en
                cusbill.cus_add2_en = cus_bill_cus_add2_en
                cusbill.cus_subdist_en = cus_bill_cus_subdist_en
                cusbill.cus_zip = cus_bill_cus_zip
                cusbill.cus_tel = cus_bill_cus_tel
                cusbill.cus_fax = cus_bill_cus_fax
                cusbill.cus_email = cus_bill_cus_email
                cusbill.cus_zone_id = cus_bill_cus_zone
                cusbill.cus_contact_id = cus_bill_cus_contact_id
                cusbill.site_contact_id = cus_bill_cus_contact_id
                cusbill.save()
                print("update cus_bill")
            except CusBill.DoesNotExist:
                new_cusbill = CusBill(
                    cus_active = cus_bill_cus_active,
                    cus_no = cus_no,
                    cus_id = cus_id,
                    cus_brn = cus_brn,
                    cus_name_th = cus_bill_cus_name_th,
                    cus_add1_th = cus_bill_cus_add1_th,
                    cus_add2_th = cus_bill_cus_add2_th,
                    cus_subdist_th = cus_bill_cus_subdist_th,
                    cus_district_id = cus_bill_cus_district_id,
                    cus_city_id = city_id,
                    cus_country_id = country_id,
                    cus_name_en = cus_bill_cus_name_en,
                    cus_add1_en = cus_bill_cus_add1_en,
                    cus_add2_en = cus_bill_cus_add2_en,
                    cus_subdist_en = cus_bill_cus_subdist_en,                    
                    cus_zip = cus_bill_cus_zip,
                    cus_tel = cus_bill_cus_tel,
                    cus_fax = cus_bill_cus_fax,
                    cus_email = cus_bill_cus_email,
                    cus_zone_id = cus_bill_cus_zone,
                    cus_contact_id = cus_bill_cus_contact_id,
                    site_contact_id = cus_bill_cus_contact_id,
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

