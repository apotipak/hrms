from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .models import DlyPlan, SchPlan
from customer.models import CusMain, Customer, CusBill
from contract.models import CusContract, CusService
from employee.models import Employee, EmpPhoto
from system.models import TPeriod
from .forms import ScheduleMaintenanceForm
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from django.db.models import F
from django.db import connection
from base64 import b64encode
import datetime
import django.db as db
import json
from datetime import timedelta
import time
from system.helper import *
from django.contrib.humanize.templatetags.humanize import naturalday
from hrms.settings import MEDIA_ROOT
from docxtpl import DocxTemplate
from docx2pdf import convert
from os import path
from django.http import FileResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache
import xlwt


Tpub = 11

@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ScheduleMaintenance(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE	

	template_name = 'monitoring/schedule_maintenance.html'
	response_data = {}
	modified_records = []

	if request.user.is_superuser:
	    employee_photo = ""
	else:
		if request.user.username!="CMS_SUP":
		    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()   
		    employee_photo = b64encode(employee_info.image).decode("utf-8")        
		else:
		    employee_info = None
		    employee_photo = None		

	if request.method == "POST":
		# print("POST: ScheduleMaintenance()")
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		# print("GET: ScheduleMaintenance()")
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date, 'form': form, 'employee_photo': employee_photo, 'database': settings.DATABASES['default']['NAME'], 'host': settings.DATABASES['default']['HOST'],})


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ajax_get_customer(request):
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	
	# print("cnt_id = " + str(cnt_id))

	# if cus_id is not None and cus_brn is not None:
	if cnt_id is not None:
		try:

			# Contract
			cus_contract = CusContract.objects.filter(cnt_id=cnt_id).get()
			cnt_doc_no = cus_contract.cnt_doc_no
			cnt_active = cus_contract.cnt_active
			cnt_sign_frm = cus_contract.cnt_sign_frm.strftime("%d/%m/%Y")
			cnt_sign_to = cus_contract.cnt_sign_to.strftime("%d/%m/%Y")			
			cnt_eff_frm = cus_contract.cnt_eff_frm.strftime("%d/%m/%Y")
			cnt_eff_to = cus_contract.cnt_eff_to.strftime("%d/%m/%Y")

			if cus_contract.cnt_wage_id is not None:
				if cus_contract.cnt_wage_id != "":
					cnt_wage_name_th = cus_contract.cnt_wage_id.wage_th
					cnt_wage_name_en = cus_contract.cnt_wage_id.wage_en
				else:
					cnt_wage_name_th = ""
					cnt_wage_name_en = ""	
			else:
				cnt_wage_name_th = ""
				cnt_wage_name_en = ""
			
			cnt_apr_by_name_en = cus_contract.cnt_apr_by.apr_name_en

			# Contract Services
			try:
				cus_service = CusService.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('-srv_active')				
				# print("cus_service is found")
				cus_service_list=[]
				for d in cus_service:
					if d.srv_active:
						record = {
						    "srv_id": d.srv_id,
						    "cnt_id": d.cnt_id_id,
						    "srv_rank": d.srv_rank_id,
						    "srv_shif_id": d.srv_shif_id_id,
						    "srv_shift_name": d.srv_shif_id.shf_desc,
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
						    "srv_active": "Y",
						    "upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
						    "upd_by": d.upd_by,
						}
						cus_service_list.append(record)		
			except CusService.DoesNotExist:
				# print("cus_service is not found")
				cus_service_list=[]

			# SCH_PLAN			
			try:
				sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').order_by('-upd_date')
				# print("sch_plan is found")
				sch_plan_list = []
				for d in sch_plan:
					if d.sch_active:
						if d.relief:
							relief = 1
						else:
							relief = 0 

						if d.sch_active:
							sch_active = 1
						else:
							sch_active = 0

						record = {
						    "sch_no": d.sch_no,
						    "srv_id": d.srv_id,
						    "emp_id": d.emp_id_id,
						    "emp_fname_th": d.emp_id.emp_fname_th,
						    "emp_lname_th": d.emp_id.emp_lname_th,
						    "sch_rank": d.sch_rank,
						    "sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
						    "sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
						    "sch_shf_mon": d.sch_shf_mon,
						    "sch_shf_tue": d.sch_shf_tue,
						    "sch_shf_wed": d.sch_shf_wed,
						    "sch_shf_thu": d.sch_shf_thu,
						    "sch_shf_fri": d.sch_shf_fri,
						    "sch_shf_sat": d.sch_shf_sat,
						    "sch_shf_sun": d.sch_shf_sun,
						    "sch_active": sch_active,
						    "relief": relief,
						    "upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
						    "upd_by": d.upd_by,
						    "upd_flag": d.upd_flag,
						}
						sch_plan_list.append(record)			    
			except SchPlan.DoesNotExist:
				# print("sch_plan is not found")
				sch_plan_list = []

			# CUS_MAIN
			try:
			    cus_main = CusMain.objects.filter(cus_id=cus_id).get()
			    cus_main_cus_name_th = cus_main.cus_name_th
			    cus_main_cus_name_en = cus_main.cus_name_en
			    cus_main_cus_tel = cus_main.cus_tel
			except CusMain.DoesNotExist:
				cus_main_cus_name_th = ""
				cus_main_cus_name_en = ""
				cus_main_cus_tel = ""

			# CUS_SITE
			try:
			    customer = Customer.objects.filter(cus_id=cus_id, cus_brn=cus_brn).get()
			    
			    cus_site_name_th = customer.cus_name_th
			    cus_site_sht_th = customer.cus_sht_th
			    cus_site_add1_th = customer.cus_add1_th
			    cus_site_add2_th = customer.cus_add2_th
			    cus_site_subdist_th = customer.cus_subdist_th
			    cus_site_name_en = customer.cus_name_en
			    cus_site_sht_en = customer.cus_sht_en
			    cus_site_add1_en = customer.cus_add1_en
			    cus_site_add2_en = customer.cus_add2_en
			    cus_site_subdist_en = customer.cus_subdist_en
			    cus_site_zip = customer.cus_zip

			    if customer.cus_district_id is not None:
			        cus_site_district_id = customer.cus_district_id
			        cus_site_district_th = customer.cus_district.dist_th
			        cus_site_district_en = customer.cus_district.dist_en
			    else:
			        cus_site_district_id = 0
			        cus_site_district_th = ""
			        cus_site_district_en = ""

			    if customer.cus_city_id is not None:
			        cus_site_city_th = customer.cus_city.city_th
			        cus_site_city_en = customer.cus_city.city_en
			    else:
			        cus_site_city_id = 0
			        cus_site_city_th = ""
			        cus_site_city_en = ""

			    if customer.cus_country_id is not None:
			        cus_site_country_th = customer.cus_country.country_th
			        cus_site_country_en = customer.cus_country.country_en
			    else:
			        cus_site_country_id = 0
			        cus_site_country_th = ""
			        cus_site_country_en = ""
			    
			    cus_site_tel = customer.cus_tel
			    cus_site_fax = customer.cus_fax
			    cus_site_email = customer.cus_email
			    
			    if customer.site_contact_id is not None:
			        cus_site_contact_id_th = customer.site_contact_id
			        cus_site_contact_con_fname_th = customer.site_contact.con_fname_th
			        cus_site_contact_con_lname_th = customer.site_contact.con_lname_th
			        cus_site_contact_con_position_th = customer.site_contact.con_position_th

			        cus_site_contact_id_en = customer.site_contact_id
			        cus_site_contact_con_fname_en = customer.site_contact.con_fname_en
			        cus_site_contact_con_lname_en = customer.site_contact.con_lname_en
			        cus_site_contact_con_position_en = customer.site_contact.con_position_en
			    else:
			        cus_site_contact_id_th = 0
			        cus_site_contact_con_fname_th = ""
			        cus_site_contact_con_lname_th = ""
			        cus_site_contact_con_position_th = ""

			        cus_site_contact_id_en = 0
			        cus_site_contact_con_fname_en = ""
			        cus_site_contact_con_lname_en = ""
			        cus_site_contact_con_position_en = ""


			    if customer.cus_zone_id is not None:            
			        cus_site_contact_cus_zone_id = customer.cus_zone_id
			        cus_site_contact_cus_zone_th = customer.cus_zone.zone_th
			        cus_site_contact_cus_zone_en = customer.cus_zone.zone_en
			    else:
			        cus_site_contact_cus_zone_id = 0
			        cus_site_contact_cus_zone_th = ""
			        cus_site_contact_cus_zone_en = ""

			    response = JsonResponse(data={
			        # CUS_SITE
			        "success": True,
			        "class": "bg-success",
			        "is_existed": True,

			        "cnt_doc_no": cnt_doc_no,
			        "cnt_active": cnt_active,
			        "cnt_sign_frm": cnt_sign_frm,
			        "cnt_sign_to": cnt_sign_to,			        
			        "cnt_eff_frm": cnt_eff_frm,
			        "cnt_eff_to": cnt_eff_to,
			        "cnt_wage_name_th": cnt_wage_name_th,
			        "cnt_wage_name_en": cnt_wage_name_en,
			        "cnt_apr_by_name_en": cnt_apr_by_name_en,

			        "cus_main_cus_name_th": cus_main_cus_name_th,
			        "cus_main_cus_name_en": cus_main_cus_name_en,
			        "cus_main_cus_tel": cus_main_cus_tel,

			        "cus_site_name_th": cus_site_name_th,
			        "cus_site_sht_th": cus_site_sht_th,
			        "cus_site_add_th": cus_site_add1_th + " " + cus_site_add2_th,
			        "cus_site_subdist_th": cus_site_subdist_th,
			        "cus_site_district_id": cus_site_district_id,
			        "cus_site_district_th": cus_site_district_th,
			        "cus_site_city_th": cus_site_city_th,
			        "cus_site_country_th": cus_site_country_th,
			        "cus_site_contact_id_th": cus_site_contact_id_th,
			        "cus_site_contact_name_th": str(cus_site_contact_con_fname_th) + " " + str(cus_site_contact_con_lname_th),
			        "cus_site_contact_position_th": cus_site_contact_con_position_th,
			        "cus_site_name_en": cus_site_name_en,
			        "cus_site_sht_en": cus_site_sht_en,
			        "cus_site_add_en": cus_site_add1_en + " " + cus_site_add2_en,
			        "cus_site_subdist_en": cus_site_subdist_en,
			        "cus_site_zip": cus_site_zip,
			        "cus_site_district_en": cus_site_district_en,
			        "cus_site_city_en": cus_site_city_en,
			        "cus_site_country_en": cus_site_country_en,                                                            
			        "cus_site_contact_id_en": cus_site_contact_id_en,
			        "cus_site_contact_con_en": str(cus_site_contact_id_en) + " | " + str(cus_site_contact_con_fname_en) + " " + str(cus_site_contact_con_lname_en),
			        "cus_site_contact_con_position_en": cus_site_contact_con_position_en,                
			        "cus_site_tel": cus_site_tel,
			        "cus_site_fax": cus_site_fax,
			        "cus_site_email": cus_site_email,
			        "cus_site_contact_cus_zone_id": cus_site_contact_cus_zone_id,
			        "cus_site_contact_cus_zone_th": cus_site_contact_cus_zone_th,
			        "cus_site_contact_cus_zone_en": cus_site_contact_cus_zone_en,

					"cus_service_list": list(cus_service_list),
					"sch_plan_list": list(sch_plan_list),
			    })
			    response.status_code = 200
			except Customer.DoesNotExist:            
			    response = JsonResponse(data={
			        "success": False,
			        "class": "bg-danger",
			        "is_existed": False,
			    })
			    response.status_code = 200
			    return response			    	
		except CusContract.DoesNotExist:
			# print("ajax_get_customer() - Customer Number is not found.")
			response = JsonResponse(data={
			    "success": True,
			    "class": "bg-danger",
			    "is_existed": False,
			})			
	else:
		response = JsonResponse(data={
		    "success": True,
		    "class": "bg-danger",
		    "is_existed": False,
		})

	return response



@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def get_customer_service_list(request):
    print("*************************************")
    print("FUNCTION: get_customer_service_list()")
    print("*************************************")

    cnt_id = request.GET["cnt_id"]

    data = CusService.objects.all().exclude(upd_flag='D').filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('-srv_active')
    
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
            "upd_date": d.upd_date,
            "upd_by": d.upd_by,
        }
        cus_service_list.append(record)

    response = JsonResponse(data={
        "success": True,
        "cus_service_list": list(cus_service_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ajax_get_customer_schedule_plan_list(request):
    print("*************************************")
    print("FUNCTION: ajax_get_customer_schedule_plan_list()")
    print("*************************************")

    cus_id = request.POST.get('cus_id')
    cus_brn = request.POST.get('cus_brn')
    cus_vol = request.POST.get('cus_vol')
    sch_active = request.POST.get("sch_active")	
    cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
    # print("cnt_id = " + str(cnt_id))
    # print("sch_active = " + str(sch_active))

    try:    	
    	# print("sch_plan is found")
    	sch_plan_list = []
    	total = 0

    	if sch_active == '1':
    		sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').order_by('-upd_date')
    		# print("sch")

	    	for d in sch_plan:	
	    		# print("Active - " + str(d.cnt_id) + "," + str(d.sch_rank))
	    		if d.sch_active:
	    			if d.relief:
	    				relief = 1
	    			else:
	    				relief = 0 

	    			if d.sch_active:
	    				sch_active = 1
	    			else:
	    				sch_active = 0

	    			record = {
	    				"sch_no": d.sch_no,
	    				"srv_id": d.srv_id,
	    				"emp_id": d.emp_id_id,
					    "emp_fname_th": d.emp_id.emp_fname_th,
					    "emp_lname_th": d.emp_id.emp_lname_th,	    				
	    				"sch_rank": d.sch_rank,
	    				"sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
	    				"sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
	    				"sch_shf_mon": d.sch_shf_mon,
	    				"sch_shf_tue": d.sch_shf_tue,
	    				"sch_shf_wed": d.sch_shf_wed,
	    				"sch_shf_thu": d.sch_shf_thu,
	    				"sch_shf_fri": d.sch_shf_fri,
	    				"sch_shf_sat": d.sch_shf_sat,
	    				"sch_shf_sun": d.sch_shf_sun,
	    				"sch_active": sch_active,
	    				"relief": relief,
	    				"upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
	    				"upd_by": d.upd_by,
	    				"upd_flag": d.upd_flag,
	    			}
	    			sch_plan_list.append(record)	    			
    	elif sch_active == '2':
    		sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').exclude(sch_date_to='2999-12-31').order_by('-upd_date', 'emp_id')
	    	for d in sch_plan:    		
	    		# print("Pending - " + str(d.cnt_id) + "," + str(d.sch_rank))
    			if d.relief:
    				relief = 1
    			else:
    				relief = 0 

    			if d.sch_active:
    				sch_active = 1
    			else:
    				sch_active = 0

    			record = {
    				"sch_no": d.sch_no,
    				"srv_id": d.srv_id,
    				"emp_id": d.emp_id_id,
				    "emp_fname_th": d.emp_id.emp_fname_th,
				    "emp_lname_th": d.emp_id.emp_lname_th,	    				
    				"sch_rank": d.sch_rank,
    				"sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
    				"sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
    				"sch_shf_mon": d.sch_shf_mon,
    				"sch_shf_tue": d.sch_shf_tue,
    				"sch_shf_wed": d.sch_shf_wed,
    				"sch_shf_thu": d.sch_shf_thu,
    				"sch_shf_fri": d.sch_shf_fri,
    				"sch_shf_sat": d.sch_shf_sat,
    				"sch_shf_sun": d.sch_shf_sun,
    				"sch_active": sch_active,
    				"relief": relief,
    				"upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
    				"upd_by": d.upd_by,
    				"upd_flag": d.upd_flag,
    			}
    			sch_plan_list.append(record)
    	elif sch_active == '3':
    		sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('-upd_date', 'emp_id')
	    	for d in sch_plan:
	    		# print("All - " + str(d.cnt_id) + "," + str(d.sch_rank))
    			if d.relief:
    				relief = 1
    			else:
    				relief = 0 

    			if d.sch_active:
    				sch_active = 1
    			else:
    				sch_active = 0

    			record = {
    				"sch_no": d.sch_no,
    				"srv_id": d.srv_id,
    				"emp_id": d.emp_id_id,
				    "emp_fname_th": d.emp_id.emp_fname_th,
				    "emp_lname_th": d.emp_id.emp_lname_th,    				
    				"sch_rank": d.sch_rank,
    				"sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
    				"sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
    				"sch_shf_mon": d.sch_shf_mon,
    				"sch_shf_tue": d.sch_shf_tue,
    				"sch_shf_wed": d.sch_shf_wed,
    				"sch_shf_thu": d.sch_shf_thu,
    				"sch_shf_fri": d.sch_shf_fri,
    				"sch_shf_sat": d.sch_shf_sat,
    				"sch_shf_sun": d.sch_shf_sun,
    				"sch_active": sch_active,
    				"relief": relief,
    				"upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
    				"upd_by": d.upd_by,
    				"upd_flag": d.upd_flag,
    			}
    			sch_plan_list.append(record)	    	
    	else:
	    	# print("sch_plan is not found")    	
	    	sch_plan_list = []

    except SchPlan.DoesNotExist:
    	# print("sch_plan is not found")    	
    	sch_plan_list = []

    response = JsonResponse(data={
        "success": True,
        "sch_plan_list": list(sch_plan_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ajax_get_customer_schedule_plan(request):
    print("*************************************")
    print("FUNCTION: ajax_get_customer_schedule_plan()")
    print("*************************************")

    cus_id = request.POST.get('cus_id')
    cus_brn = request.POST.get('cus_brn')
    cus_vol = request.POST.get('cus_vol')
    sch_no = request.POST.get("sch_no")	
    cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
    # print("sch_no = " + str(sch_no))

    try:
    	sch_plan = SchPlan.objects.filter(sch_no=sch_no).get()

    	'''
    	print("debug : " + str(sch_plan.emp_id_id) + "," + str(sch_plan.sch_rank))
    	print("sch_active = " + str(sch_plan.sch_active))
    	'''

    	# employee_info = EmpPhoto.objects.filter(emp_id=sch_plan.emp_id_id).get()
    	# employee_photo = b64encode(employee_info.image).decode("utf-8")
    	employee_photo = None

    	if sch_plan.relief:
    		relief = 1
    	else:
    		relief = 0 
    	if sch_plan.sch_active:
    		sch_active = 1
    	else:
    		sch_active = 0

    	if sch_plan.emp_id.emp_term_date is not None:
    		emp_term_date = sch_plan.emp_id.emp_term_date.strftime("%d/%m/%Y"),
    	else:
    		emp_term_date = ""

    	if int(sch_plan.sch_shf_sat) == 99:
    		# sch_shf_sat = "DAY OFF"
    		sch_shf_sat = sch_plan.sch_shf_sat 
    	else:
    		sch_shf_sat = sch_plan.sch_shf_sat 


    	if int(sch_plan.sch_shf_sun) == 99:
    		# sch_shf_sun = "DAY OFF"
    		sch_shf_sun = sch_plan.sch_shf_sun 
    	else:
    		sch_shf_sun = sch_plan.sch_shf_sun 

    	response = JsonResponse(data={
	        "success": True,
			"sch_no": sch_plan.sch_no,
			"emp_id": sch_plan.emp_id_id,
		    "emp_fname_th": sch_plan.emp_id.emp_fname_th,
		    "emp_lname_th": sch_plan.emp_id.emp_lname_th,
		    "emp_status_id": sch_plan.emp_id.emp_status_id,
		    "emp_status": sch_plan.emp_id.emp_status.sts_th,
		    "emp_type": sch_plan.emp_id.emp_type,
			"sch_rank": sch_plan.sch_rank,
			"emp_join_date": sch_plan.emp_id.emp_join_date.strftime("%d/%m/%Y"),
			"emp_term_date": emp_term_date,
			"sch_date_frm": sch_plan.sch_date_frm.strftime("%d/%m/%Y"),
			"sch_date_to": sch_plan.sch_date_to.strftime("%d/%m/%Y"),
			"sch_shf_mon": sch_plan.sch_shf_mon,
			"sch_shf_tue": sch_plan.sch_shf_tue,
			"sch_shf_wed": sch_plan.sch_shf_wed,
			"sch_shf_thu": sch_plan.sch_shf_thu,
			"sch_shf_fri": sch_plan.sch_shf_fri,
			"sch_shf_sat": sch_shf_sat,
			"sch_shf_sun": sch_shf_sun,
			"sch_active": sch_active,
			"relief": relief,
			"upd_date": sch_plan.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
			"upd_by": sch_plan.upd_by,
			"upd_flag": sch_plan.upd_flag,
			"employee_photo": employee_photo,
   		})					    		   
    except SchPlan.DoesNotExist:
	    response = JsonResponse(data={
	        "success": True,
	        "sch_plan": list(record),
	    })

    response.status_code = 200
    return response



@login_required(login_url='/accounts/login/')
@permission_required('monitoring.change_dlyplan', login_url='/accounts/login/')
def ajax_save_customer_schedule_plan(request):
	print("*********************************************")
	print("FUNCTION: ajax_save_customer_schedule_plan()")
	print("*********************************************")

	selected_sch_no = request.POST.get("selected_sch_no")	
	print("selected_sch_no = " + str(selected_sch_no))

	selected_service_id = request.POST.get("selected_service_id")	
	# print("selected_service_id = " + str(selected_service_id))

	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	
	emp_id = request.POST.get("emp_id")
	emp_rank = request.POST.get("emp_rank")
	sch_active = request.POST.get("sch_active")
	relief = request.POST.get("relief")
	mon_shift = request.POST.get("mon_shift")
	tue_shift = request.POST.get("tue_shift")
	wed_shift = request.POST.get("wed_shift")
	thu_shift = request.POST.get("thu_shift")
	fri_shift = request.POST.get("fri_shift")
	sat_shift = request.POST.get("sat_shift")
	sun_shift = request.POST.get("sun_shift")
	duration_from = request.POST.get("duration_from")
	duration_to = request.POST.get("duration_to")
	contract_list_filter_option = request.POST.get("contract_list_filter_option")
	# print("contract_list_filter_option = " + str(contract_list_filter_option))

	sch_plan_list = []

	# Case - add new employee into customer service
	if selected_sch_no == "0":
		print("TRUE")

		'''
		print("add new");
		print("--- debug ---")
		print("selected_sch_no = " + str(selected_sch_no))
		print("emp_id = " + str(emp_id))		
		print("duration_from = " + str(duration_from))
		print("duration_to = " + str(duration_to))
		print("sch_active = " + str(sch_active))
		print("relief = " + str(relief))
		print("mon_shift = " + str(mon_shift))
		print("tue_shift = " + str(tue_shift))
		print("wed_shift = " + str(wed_shift))
		print("thu_shift = " + str(thu_shift))
		print("fri_shift = " + str(fri_shift))
		print("sat_shift = " + str(sat_shift))
		print("sun_shift = " + str(sun_shift))
		print("--- debug ---")
		'''

		# Get latest sch_no
		cursor = connection.cursor()
		# cursor.execute("select max(convert(decimal(4,0),right(rtrim(convert(char(20),sch_no)),4))) from sch_plan where cnt_id=" + cnt_id)
		cursor.execute("select max(sch_no) from sch_plan where cnt_id=" + cnt_id + ";")
		max_sch_no = cursor.fetchone()[0]
		if max_sch_no is not None:
			new_sch_no = max_sch_no + 1
		else:
			cursor = connection.cursor()			
			cursor.execute("select top 1 srv_id from cus_service where cnt_id=" + cnt_id + ";")
			selected_service_id = cursor.fetchone()[0]			
			new_sch_no = str(selected_service_id) + str(1).zfill(4)
	
		print("max_sch_no = ",  max_sch_no)
		print("new_sch_no = ", new_sch_no)


		# Generate new sch_no
		# new_sch_no = str(selected_service_id) + str(new_sch_no).zfill(4)
		# print("new_sch_no = " + str(new_sch_no))

		# RULE-1: Check if an employee is existed in another schedule		
		# employee = SchPlan.objects.filter(emp_id=emp_id).exclude(upd_flag='D').exclude(sch_active="")
		# select * from sch_plan where emp_id=916 and sch_active=1 and upd_flag!='D'
		#  sch_plan_count = SchPlan.objects.filter(emp_id=emp_id).exclude(upd_flag='D').exclude(sch_active="").count()
		
		sch_plan_count = 0		
		sql = "select * from sch_plan where emp_id=" + emp_id + " and sch_active=1 and upd_flag!='D'"
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
				sch_plan_obj = cursor.fetchone()

			if sch_plan_obj is not None:
				if len(sch_plan_obj) > 0:
					sch_plan_count = len(sch_plan_obj)

		except db.OperationalError as e:
			is_found = False
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
		except db.Error as e:
			is_found = False
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
		finally:
			cursor.close()

		# print("sch_plan_count:", sch_plan_count)		
		if sch_plan_count > 0:
			try:
				#sch_plan = SchPlan.objects.filter(emp_id=emp_id).exclude(upd_flag='D').exclude(sch_active="").get()
				sch_plan = SchPlan.objects.filter(emp_id=emp_id).exclude(upd_flag='D').filter(sch_active__in=[1]).get()

				existed_contract_id = sch_plan.cnt_id
				employee_fullname_th = str(sch_plan.emp_id.emp_fname_th) + "  " + str(sch_plan.emp_id.emp_lname_th)
				employee_rank = sch_plan.emp_id.emp_rank

				cus_contract_info = CusContract.objects.filter(cnt_id=existed_contract_id).get()
				existed_cus_id = cus_contract_info.cus_id
				existed_cus_brn = cus_contract_info.cus_brn

				customer_info = Customer.objects.filter(cus_id=existed_cus_id).filter(cus_brn=existed_cus_brn).get()
				existed_cus_name_th = customer_info.cus_name_th

				employee_info = EmpPhoto.objects.filter(emp_id=emp_id).get()
				employee_photo = b64encode(employee_info.image).decode("utf-8")

			except SchPlan.DoesNotExist:
				existed_contract_id = "N/A"
				employee_fullname_th = "N/A"
				existed_cus_name_th = "N/A"
				employee_rank = "N/A"
				employee_photo = "N/A"

			try:
				customer = Customer.objects.filter(cus_id=cus_id).filter(cus_brn=cus_brn).get()
				cus_name_th = customer.cus_name_th				

				message = ""
				message += "<div class='card'>"				
				message += "  <div class='card-body text-dark text-center'>"
				message += "	<img src='data:image/png;base64," + employee_photo + "' style='width:120px;'/><br><br>"
				message += "    <h5 class='text-center'>" + emp_id + "&nbsp;-&nbsp;" + employee_fullname_th + "(" + employee_rank + ")" + "</h5>"
				message += "	<p class='small text-center text-danger'>ไม่สามารถลงตารางเวรใหม่ได้ เนื่องจากมีสถานะ Active ที่หน่วยงาน</p>"
				message += "    <ul class='list-group list-group-unbordered mb-3'>"				
				message += "      <li class='list-group-item'>"
				message += "        <b>" + str(existed_contract_id) + "</b>&nbsp;&nbsp;&nbsp;&nbsp;" + str(existed_cus_name_th)
				message += "      </li>"
				message += "    </ul>"			
				message += "  </div>"
				message += "</div>"				
			except Customer.DoesNotExist:				
				message = "Error! Please contact IT."

			# encoded = base64.b64encode("BinaryField as ByteArray")

			response = JsonResponse(data={
				"message": message,				
				"class": "bg-danger",
				"sch_plan_list": list(sch_plan_list),
				"is_saved": False,
			})

		else:
			cursor = connection.cursor()			
			cursor.execute("select top 1 srv_id from cus_service where cnt_id=" + cnt_id + ";")
			selected_service_id = cursor.fetchone()[0]
			if selected_service_id is None:
				selected_service_id = 0

			new_sch_plan = SchPlan(
				sch_no = new_sch_no,
				srv_id = selected_service_id,
				cnt_id = cnt_id,
				emp_id_id = emp_id,
				sch_rank = emp_rank,
				relief = relief,
				sch_date_frm = datetime.datetime.strptime(duration_from, "%d/%m/%Y").date(),
				sch_date_to = datetime.datetime.strptime(duration_to, "%d/%m/%Y").date(),
				sch_shf_mon = mon_shift,
				sch_shf_tue = tue_shift,
				sch_shf_wed = wed_shift,
				sch_shf_thu = thu_shift,
				sch_shf_fri = fri_shift,
				sch_shf_sat = sat_shift,
				sch_shf_sun = sun_shift,
				sch_active = sch_active,			
				upd_date = datetime.datetime.now(),
				# upd_by = request.user.first_name,
				upd_by = request.user.username,
				upd_flag = 'A',
			    )
			new_sch_plan.save() 

			cursor = connection.cursor()			
			cursor.execute("select count(*) from sch_plan where cnt_id=" + cnt_id + ";")
			record_count = cursor.fetchone()[0]
			if record_count is None:
				record_count = 0
			print("record_count : ", record_count)


			# print("sch_plan is found")
			sch_plan_list = []
			sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').order_by('-upd_date')
			for d in sch_plan:	
				if d.sch_active:
					if d.relief:
						relief = 1
					else:
						relief = 0 

					if d.sch_active:
						sch_active = 1
					else:
						sch_active = 0

					record = {
						"sch_no": d.sch_no,
						"srv_id": d.srv_id,
						"emp_id": d.emp_id_id,
						"emp_fname_th": d.emp_id.emp_fname_th,
						"emp_lname_th": d.emp_id.emp_lname_th,	    				
						"sch_rank": d.sch_rank,
						"sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
						"sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
						"sch_shf_mon": d.sch_shf_mon,
						"sch_shf_tue": d.sch_shf_tue,
						"sch_shf_wed": d.sch_shf_wed,
						"sch_shf_thu": d.sch_shf_thu,
						"sch_shf_fri": d.sch_shf_fri,
						"sch_shf_sat": d.sch_shf_sat,
						"sch_shf_sun": d.sch_shf_sun,
						"sch_active": sch_active,
						"relief": relief,
						"upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
						"upd_by": d.upd_by,
						"upd_flag": d.upd_flag,
					}
					sch_plan_list.append(record)

			response = JsonResponse(data={
				"message": "เพิ่มรายการสำเร็จ",
				"class": "bg-success",
				"sch_plan_list": list(sch_plan_list),
				"record_count": record_count,
				"is_saved": True,
			})

		'''
		except SchPlan.DoesNotExist:
			print("Available")
			# If RULE-1 and RULE-2 is passed, then save a new record
			new_sch_plan = SchPlan(
				sch_no = new_sch_no,
				srv_id = selected_service_id,
				cnt_id = cnt_id,
				emp_id_id = emp_id,
				sch_rank = emp_rank,
				relief = relief,
				sch_date_frm = datetime.datetime.strptime(duration_from, "%d/%m/%Y").date(),
				sch_date_to = datetime.datetime.strptime(duration_to, "%d/%m/%Y").date(),
				sch_shf_mon = mon_shift,
				sch_shf_tue = tue_shift,
				sch_shf_wed = wed_shift,
				sch_shf_thu = thu_shift,
				sch_shf_fri = fri_shift,
				sch_shf_sat = sat_shift,
				sch_shf_sun = sun_shift,
				sch_active = sch_active,			
				upd_date = datetime.datetime.now(),
				upd_by = request.user.first_name,
				upd_flag = 'A',
			    )
			new_sch_plan.save() 			
			response = JsonResponse(data={
				"message": "Added success",
				"class": "bg-success",
				"sch_plan_list": list(sch_plan_list),
				"is_saved": True,
			})
		'''

		# RULE-2: Check if select duplicated security guard	


	else:
		print("FALSE")
		# print("update existing");
		# print("selected_sch_no = " + str(selected_sch_no))

		try:
			sch_plan = SchPlan.objects.filter(sch_no=selected_sch_no).get()
			sch_plan.sch_active = sch_active
			sch_plan.relief = relief
			sch_plan.sch_shf_mon = mon_shift
			sch_plan.sch_shf_tue = tue_shift
			sch_plan.sch_shf_wed = wed_shift
			sch_plan.sch_shf_thu = thu_shift
			sch_plan.sch_shf_fri = fri_shift
			sch_plan.sch_shf_sat = sat_shift
			sch_plan.sch_shf_sun = sun_shift
			sch_plan.sch_date_frm = datetime.datetime.strptime(duration_from, "%d/%m/%Y")
			sch_plan.sch_date_to = datetime.datetime.strptime(duration_to, "%d/%m/%Y")
			sch_plan.upd_date = datetime.datetime.now()
			# sch_plan.upd_by = request.user.first_name
			sch_plan.upd_by = request.user.username
			sch_plan.upd_flag = 'E'
			sch_plan.save()


			# generate new security guard list
			'''
			if contract_list_filter_option=='1':
				sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').order_by('-upd_date')	
			elif contract_list_filter_option=='2':				
				sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').exclude(sch_date_to='2999-12-31').order_by('-upd_date', 'emp_id')
			elif contract_list_filter_option=='3':
				sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('-upd_date', 'emp_id')
			else:
				sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').order_by('-upd_date')	
			'''

			# sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').order_by('-upd_date')	
			# sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').exclude(sch_date_to='2999-12-31').order_by('-upd_date', 'emp_id')
			sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_active=1).exclude(upd_flag='D').order_by('-upd_date', 'emp_id')

			for d in sch_plan:
				# if d.sch_active:
				if d.relief:
					relief = 1
				else:
					relief = 0 

				if d.sch_active:
					sch_active = 1
				else:
					sch_active = 0

				record = {
				    "sch_no": d.sch_no,
				    "emp_id": d.emp_id_id,
				    "emp_fname_th": d.emp_id.emp_fname_th,
				    "emp_lname_th": d.emp_id.emp_lname_th,
				    "sch_rank": d.sch_rank,
				    "sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
				    "sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
				    "sch_shf_mon": d.sch_shf_mon,
				    "sch_shf_tue": d.sch_shf_tue,
				    "sch_shf_wed": d.sch_shf_wed,
				    "sch_shf_thu": d.sch_shf_thu,
				    "sch_shf_fri": d.sch_shf_fri,
				    "sch_shf_sat": d.sch_shf_sat,
				    "sch_shf_sun": d.sch_shf_sun,
				    "sch_active": sch_active,
				    "relief": relief,
				    "upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
				    "upd_by": d.upd_by,
				    "upd_flag": d.upd_flag,					 
				}
				sch_plan_list.append(record)

			response = JsonResponse(data={
				"message": "บันทึกรายการสำเร็จ",
				"class": "bg-success",
				"sch_plan_list": list(sch_plan_list),
				"is_saved": True,
			})
		except SchPlan.DoesNotExist:
			response = JsonResponse(data={
				"message": "Schedule Number not found.",
				"class": "bg-danger",
				"sch_plan_list": list(sch_plan_list),
				"is_saved": False,
			})
    
	response.status_code = 200
	return response
    


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_get_employee_list(request):

	print("***********************************")
	print("FUNCTION: ajax_get_employee_list()")
	print("***********************************")

	emp_id = request.GET.get('emp_id')
	search_option = request.GET.get('search_option')
	search_key = request.GET.get('search_key')

	# print("debug: emp_id = " + str(emp_id))

	item_per_page = 6

	if emp_id is not None:
	    if emp_id != "":
	        if emp_id.isnumeric():
	            # print("debug11")
	            data = Employee.objects.all().filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').order_by('emp_id')
	        else:
	            # print("debug22")
	            data = Employee.objects.all().filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').order_by('emp_id')
	    else:
	        # print("debug33")
	        data = Employee.objects.all().filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').order_by('emp_id')
	else:		
		# print("debug44")
		search_option = request.GET.get('search_option')
		search_key = request.GET.get('search_key')
		if search_option=="1":
			# Search employee by emp_id
			# print("1111")
			if search_key.isnumeric():
				# print("1111-1")
				data = Employee.objects.filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').filter(emp_id=search_key).order_by('emp_id').all()
			else:
				# print("1111-2")
				data = []
			
		elif search_option=="2":
			# print("2222")
			# print("search_key = " + str(search_key))
			data = Employee.objects.filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').filter(emp_fname_th__startswith=search_key).order_by('emp_id').all()
		else:
			# print("3333")
			data = Employee.objects.filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').filter(emp_fname_en__startswith=search_key).order_by('emp_id').all()

	paginator = Paginator(data, item_per_page)
	is_paginated = True if paginator.num_pages > 1 else False
	page = request.GET.get('page', 1) or 1

	try:
	    current_page = paginator.get_page(page)
	except InvalidPage as e:
	    raise Http404(str(e))    

	if current_page:
		try:
			# print("debug 1")
			current_page = paginator.get_page(page)
		except InvalidPage as e:
			# print("debug 2")
			raise Http404(str(e))

		if current_page:
		    current_page_number = current_page.number
		    current_page_paginator_num_pages = current_page.paginator.num_pages

		    pickup_dict = {}
		    pickup_records=[]

		    for d in current_page:
		    	emp_id = d.emp_id
		    	emp_fname_th = d.emp_fname_th
		    	emp_lname_th = d.emp_lname_th
		    	emp_fname_en = d.emp_fname_en
		    	emp_lname_en = d.emp_lname_en
		    	if d.emp_join_date is not None:
		    		emp_join_date = d.emp_join_date.strftime("%d/%m/%Y"),
		    	else:
		    		emp_join_date = "",

		    	if d.emp_term_date is not None:
		    		emp_term_date = d.emp_term_date.strftime("%d/%m/%Y"),
		    	else:
		    		emp_term_date = "",

		    	emp_rank = d.emp_rank
		    	emp_type = d.emp_type
		    	emp_status = str(d.emp_status_id) + " | " + str(d.emp_status.sts_th)

		    	record = {
		    		"emp_id": emp_id,
		    		"emp_fname_th": emp_fname_th,
		    		"emp_lname_th": emp_lname_th,
		    		"emp_fname_en": emp_fname_en,
		    		"emp_lname_en": emp_lname_en,
		    		"emp_join_date": emp_join_date,
		    		"emp_term_date": emp_term_date,
		    		"emp_rank": emp_rank,
		    		"emp_type": emp_type,
		    		"emp_status": emp_status,
		    	}
		    	pickup_records.append(record)

		    response = JsonResponse(data={
		    	"success": True,
		        "is_paginated": is_paginated,
		        "page" : page,
		        "next_page" : current_page_number + 1,
		        "previous_page": current_page_number - 1,
		        "current_page_number" : current_page_number,
		        "current_page_paginator_num_pages" : current_page_paginator_num_pages,
				"search_key": search_key,
				"search_option": search_option,		        
		        "results": list(pickup_records)         
		        })
		    response.status_code = 200
		    return response
		else:
			# print("debug 3")
			# print("error 403")
			response = JsonResponse({"error": "there was an error"})
			response.status_code = 403
			return response
	else:
		# print("debug 4")
		response = JsonResponse(
			data={
			"success": True,
			"error": "Data not found",
			"search_key": search_key,
			"search_option": search_option,
			})
		response.status_code = 403
		return response

	return JsonResponse(data={"success": False, "results": ""})


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_get_employee(request):

	print("********************************")
	print("FUNCTION: ajax_get_employee()")
	print("********************************")
	
	emp_id = request.GET.get('emp_id')
	shf_desc = request.GET.get('shf_desc')
	cus_id = request.GET.get('cus_id')
	cus_brn = request.GET.get('cus_brn')
	cus_vol = request.GET.get('cus_vol')

	relief_status = request.GET.get('relief_status')
	if relief_status is not None:
		relief_status = int(relief_status)

	relief_emp_id = request.GET.get('relief_emp_id')	
	
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	employee_item = []

	print("__emp_id = " + str(emp_id))
	# print("__relief_status = " + str(relief_status))
	# print("__relief_emp_id = " + str(relief_emp_id))

	if relief_status==1:
		# print("______________relief_status = 1")

		if relief_emp_id is not None:	
			try:
				with connection.cursor() as cursor:		
					# cursor.execute("select emp_fname_th,emp_lname_th,emp_rank,emp_dept,emp_type,emp_join_date,emp_term_date,emp_status,sts_th from v_employee where emp_type='D1' and upd_flag<>'D' and sch_active=1 and emp_id=%s",[relief_emp_id])
					cursor.execute("select emp_fname_th,emp_lname_th,emp_rank,emp_dept,emp_type,emp_join_date,emp_term_date,emp_status,sts_th from v_employee where upd_flag<>'D' and sch_active=1 and emp_id=%s",[relief_emp_id])
					record = cursor.fetchone()
					if record is not None:
						emp_fname_th = record[0]
						emp_lname_th = record[1]
						emp_rank = record[2]
						emp_dept = record[3]
						emp_type = record[4]
						emp_join_date = "" if record[5] is None else record[5].strftime("%d/%m/%Y")
						emp_term_date = "" if record[6] is None else record[6].strftime("%d/%m/%Y")
						emp_status_id = record[7]
						emp_status_th = record[8]

						response = JsonResponse(data={
							"success": True,
							"is_found": True,
							"class": "bg-danger",
							"message": "ข้อมูลพนักงานลงเวรแทนถูกต้อง",
							"emp_id": relief_emp_id,
							"emp_fname_th": emp_fname_th,
							"emp_lname_th": emp_lname_th,
							"emp_join_date": emp_join_date,
							"emp_term_date": emp_term_date,
							"emp_rank": emp_rank,
							"emp_dept": emp_dept,
							"emp_type": emp_type,
							"emp_status_id": emp_status_id,
							"emp_status": emp_status_th,
							"employee_photo": "",
						})
						response.status_code = 200
						return response	
					else:
						response = JsonResponse(data={
							"success": True,
							"is_found": False,
							"class": "bg-danger",
							"message": "รหัสพนักงาน <b>" + str(relief_emp_id) + "</b> ไม่มีในระบบ",
							"emp_id": "",
							"emp_fname_th": "",
							"emp_lname_th": "",
							"emp_join_date": "",
							"emp_term_date": "",
							"emp_rank": "",
							"emp_dept": "",
							"emp_type": "",
							"emp_status_id": "",
							"emp_status": "",
							"employee_photo": "",
						})
						response.status_code = 200
						return response						
			except db.OperationalError as e:
				is_found = False
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
			except db.Error as e:
				is_found = False
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)

			response = JsonResponse(data={
				"success": True,
				"is_found": is_found,
				"class": "bg-danger",
				"message": message,
				"emp_id": "",
				"emp_fname_th": "",
				"emp_lname_th": "",
				"emp_join_date": "",
				"emp_term_date": "",
				"emp_rank": "",
				"emp_dept": "",
				"emp_type": "",
				"emp_status_id": "",
				"emp_status": "",
				"employee_photo": "",
			})
			response.status_code = 200
			return response
		else:
			is_found = False
			error_message = "ข้อมูลรหัสพนักงานลงเวรแทนไม่ถูกต้อง"

			response = JsonResponse(data={
				"success": True,
				"is_found": is_found,
				"class": "bg-danger",
				"message": error_message,
				"emp_id": "",
				"emp_fname_th": "",
				"emp_lname_th": "",
				"emp_join_date": "",
				"emp_term_date": "",
				"emp_rank": "",
				"emp_dept": "",
				"emp_type": "",
				"emp_status_id": "",
				"emp_status": "",
				"employee_photo": "",
			})
			response.status_code = 200
			return response				
	else:
		# กรณีพนักงาานลาแบบไม่มีคนแทน
		# print("..........Leave without relief")	

		try:
			emp_fname_th = ""
			emp_lname_th = ""
			emp_rank = ""
			emp_dept = ""
			emp_type = ""
			emp_join_date = ""
			emp_term_date = ""
			emp_status = ""

			try:
				with connection.cursor() as cursor:		
					cursor.execute("select emp_fname_th,emp_lname_th,emp_rank,emp_dept,emp_type,emp_join_date,emp_term_date,emp_status,sts_th from v_employee where upd_flag<>'D' and sch_active=1 and emp_id=%s",[emp_id])
					# cursor.execute("select emp_fname_th,emp_lname_th,emp_rank,emp_dept,emp_type,emp_join_date,emp_term_date,emp_status,sts_th from v_employee where emp_type='D1' and upd_flag<>'D' and sch_active=1 and emp_id=%s",[emp_id])					
					record = cursor.fetchone()

					if record is not None:
						emp_fname_th = record[0]
						emp_lname_th = record[1]
						emp_rank = record[2]
						emp_dept = record[3]
						emp_type = record[4]
						emp_join_date = "" if record[5] is None else record[5].strftime("%d/%m/%Y")
						emp_term_date = "" if record[6] is None else record[6].strftime("%d/%m/%Y")
						emp_status_id = record[7]
						emp_status_th = record[8]
					else:
						response = JsonResponse(data={
							"success": True,
							"is_found": False,
							"class": "bg-danger",
							"message": "ไม่พบรหัสพนักงานนี้ในระบบ",
							"emp_id": "",
							"emp_fname_th": "",
							"emp_lname_th": "",
							"emp_join_date": "",
							"emp_term_date": "",
							"emp_rank": "",
							"emp_dept": "",
							"emp_type": "",
							"emp_status_id": "",
							"emp_status": "",
							"employee_photo": "",
						})
						response.status_code = 200
						return response						
			except db.OperationalError as e:
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
			except db.Error as e:
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)


			'''
			exclude_list = [4,5,6,8,9]
			# 4 = เลิกจ้าง
			# 5 = สูญหาย
			# 6 = เสียชีวิต
			# 8 = เกษียณ
			# 9 = ไล่ออก
			employee = Employee.objects.filter(emp_id__exact=emp_id).filter(emp_type='D1').exclude(empstatus='I').exclude(emp_status__in=exclude_list).get()
			if employee.emp_join_date is not None:
				emp_join_date = employee.emp_join_date.strftime("%d/%m/%Y")
			else:
				emp_join_date = ""
			if employee.emp_term_date is not None:
				emp_term_date = employee.emp_term_date.strftime("%d/%m/%Y")
			else:
				emp_term_date = ""
			'''
			
			'''
			employee_info = EmpPhoto.objects.filter(emp_id=emp_id).first()
			if not employee_info:
				employee_photo = None
			else:
				employee_photo = b64encode(employee_info.image).decode("utf-8")					
			'''
			employee_photo = None

			response = JsonResponse(data={
				"success": True,
				"is_found": True,
				"class": "bg-success",
				"emp_id": emp_id,
				"emp_fname_th": emp_fname_th,
				"emp_lname_th": emp_lname_th,
				"emp_join_date": emp_join_date,
				"emp_term_date": emp_term_date,
				"emp_rank": emp_rank,
				"emp_dept": emp_dept,
				"emp_type": emp_type,
				"emp_status_id": emp_status_id,
				"emp_status": str(emp_status_id) + " | " + str(emp_status_th),
				"employee_photo": employee_photo,
			    })
			response.status_code = 200
			return response

		except Employee.DoesNotExist:
			# print("not found")
			response = JsonResponse(data={
				"success": True,
				"is_found": False,
				"class": "bg-danger",
				"message": "ไม่พบรหัสพนักงานนี้ในระบบ",
				"emp_id": "",
				"emp_fname_th": "",
				"emp_lname_th": "",
				"emp_join_date": "",
				"emp_term_date": "",
				"emp_rank": "",
				"emp_dept": "",
				"emp_type": "",
				"emp_status_id": "",
				"emp_status": "",
				"employee_photo": "",
			})

		response.status_code = 200
		return response


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_get_employee_photo(request):
	print("************************************")
	print("FUNCTION: ajax_get_employee_photo()")
	print("***********************************")
	employee_item = []
	emp_id = request.GET.get('emp_id')
	employee_info = EmpPhoto.objects.filter(emp_id=emp_id).get()    
	employee_photo = b64encode(employee_info.image).decode("utf-8")
	response = JsonResponse(data={"success": True,"is_error": True,"class": "bg-success","employee_photo": employee_photo})
	response.status_code = 200	
	return response	


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@never_cache
def DailyAttendance(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE	

	template_name = 'monitoring/daily_attendance.html'
	response_data = {}
	modified_records = []

	if request.user.is_superuser:
	    employee_photo = ""
	else:
		if request.user.username!="CMS_SUP":
		    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()   
		    employee_photo = b64encode(employee_info.image).decode("utf-8")        
		else:
		    employee_info = None
		    employee_photo = None		

	if request.method == "POST":
		# print("POST: ScheduleMaintenance()")
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date, 'form': form, 'employee_photo': employee_photo,'database': settings.DATABASES['default']['NAME'],'host': settings.DATABASES['default']['HOST']})


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def DailyGuardPerformance(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE	

	template_name = 'monitoring/daily_guard_performance.html'
	response_data = {}
	modified_records = []

	if request.user.is_superuser:
	    employee_photo = ""
	else:
		if request.user.username!="CMS_SUP":
		    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()   
		    employee_photo = b64encode(employee_info.image).decode("utf-8")        
		else:
		    employee_info = None
		    employee_photo = None		

	if request.method == "POST":
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date, 'form': form, 'employee_photo': employee_photo,'database': settings.DATABASES['default']['NAME'],'host': settings.DATABASES['default']['HOST']})


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def GenerateDailyAttend(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE	

	template_name = 'monitoring/generate_daily_attend.html'
	response_data = {}
	modified_records = []

	# Check user right
	form_name = "frmD301"
	usr_id = getUSR_ID(request.user.username)
	getPriorityStatus,gUSE,gADD,gEDIT,gDEL,gPREVIEW,gPRINT,gIM,gEX,gSALARY,gType,gOLD = getPriority(usr_id, form_name)
	print("getPriorityStatus:", getPriorityStatus)
	if not getPriorityStatus:
		raise PermissionDenied()

	# Show avatar
	if request.user.is_superuser:
	    employee_photo = ""
	else:
		if request.user.username!="CMS_SUP":
		    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()   
		    employee_photo = b64encode(employee_info.image).decode("utf-8")        
		else:
		    employee_info = None
		    employee_photo = None		

	if request.method == "POST":
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 
		'project_name': project_name, 
		'project_version': project_version, 
		'db_server': db_server, 
		'today_date': today_date, 
		'form': form, 
		'employee_photo': employee_photo,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],        
		})


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def PostDailyAttend(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE	

	template_name = 'monitoring/post_daily_attend.html'
	response_data = {}
	modified_records = []

	# Check user right
	form_name = "frmD302"
	usr_id = getUSR_ID(request.user.username)
	getPriorityStatus,gUSE,gADD,gEDIT,gDEL,gPREVIEW,gPRINT,gIM,gEX,gSALARY,gType,gOLD = getPriority(usr_id, form_name)
	print("getPriorityStatus:", getPriorityStatus)
	if not getPriorityStatus:
		raise PermissionDenied()


	# Show avatar
	if request.user.is_superuser:
	    employee_photo = ""
	else:
		if request.user.username!="CMS_SUP":
		    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()   
		    employee_photo = b64encode(employee_info.image).decode("utf-8")        
		else:
		    employee_info = None
		    employee_photo = None


	if request.method == "POST":
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 
		'project_name': project_name, 
		'project_version': project_version, 
		'db_server': db_server, 
		'today_date': today_date, 
		'form': form, 
		'employee_photo': employee_photo,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],		
		})


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_sp_generate_daily_attend(request):

	print("******************************************")
	print("FUNCTION: ajax_sp_generate_daily_attend()")
	print("******************************************")

	generated_date = request.POST.get('generated_date')	

	# Get current period
	period = getPeriod(generated_date)
	# print("period = " + str(period))

	# Get current date
	generated_date = datetime.datetime.strptime(generated_date, '%d/%m/%Y')	
	generated_date = str(generated_date)[0:10]
	# print("generated_date : " + str(generated_date))

	# TODO
	cursor = connection.cursor()	
	cursor.execute("select count(*) from t_date where date_chk='" + str(generated_date) + "'")	
	tdate_count = cursor.fetchone()
	if tdate_count[0] == 0:
		try:
			cursor = connection.cursor()	
			cursor.execute("exec dbo.create_dly_plan_new %s", [generated_date])
			# error_message = "Generate completed."
			error_message = "สร้างตารางรับแจ้งเวรสำเร็จ"
			is_error = False
			response = JsonResponse(data={"success": True, "is_error": is_error, "class": "bg-success", "error_message": error_message})
		except db.OperationalError as e:
			error_message = "Error";
			is_error = True
		except db.OperationalError as e:    	
			error_message = str(e);
			is_error = True
		except db.Error as e:
			error_message = str(e);
			is_error = True
		except:
			error_message = cursor.statusmessage;		
			is_error = True

		response = JsonResponse(data={"success": True, "is_error": is_error, "class": "bg-danger", "error_message": error_message})
	else:
		# error_message = "Daily Attendance table has been created. No need to generate again."
		error_message = "ตารางรับแจ้งเวรของวันที่ <b>" + str(request.POST.get('generated_date')) + "</b> ได้สร้างไว้แล้ว"
		response = JsonResponse(data={"success": True,"is_error": True,"class": "bg-success","error_message": error_message})


	cursor.close
	response.status_code = 200
	return response


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def check_post_daily_attend_status(request):
	print("******************************************")
	print("FUNCTION: check_post_daily_attend_status()")
	print("******************************************")
	post_date = request.POST.get('post_date')
	post_date = datetime.datetime.strptime(post_date, '%d/%m/%Y')	
	post_date = str(post_date)[0:10]
	sql = "select end_chk from t_date where date_chk='" + str(post_date) + "';"
	try:				
		cursor = connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchone()
		end_chk = result[0]
	except db.OperationalError as e:
		progress_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	except db.Error as e:
		progress_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	finally:
		cursor.close()
	
	response = JsonResponse(data={"success": True, "end_chk": end_chk})
	response.status_code = 200
	return response


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def check_post_daily_attend_status_history(request):
	print("***************************************************")
	print("FUNCTION: check_post_daily_attend_status_history()")
	print("***************************************************")
	post_date = request.POST.get('post_date')
	post_date = datetime.datetime.strptime(post_date, '%d/%m/%Y')	
	post_date = str(post_date)[0:10]
	sql = "select log_emptype,log_desc,log_type,upd_by from hisdlyplan_log where log_date='" + str(post_date) + "' and log_id=1 order by log_desc;"
	print(sql)
	hisdlyplan_log_obj = None
	try:				
		cursor = connection.cursor()
		cursor.execute(sql)
		hisdlyplan_log_obj = cursor.fetchall()
		print(len(hisdlyplan_log_obj))
	except db.OperationalError as e:
		progress_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	except db.Error as e:
		progress_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	finally:
		cursor.close()

	# spiderman	
	record = {}
	history_list = []
	if hisdlyplan_log_obj is not None:
		if len(hisdlyplan_log_obj)>0:			
			for item in hisdlyplan_log_obj:				
				record = {
					"log_emptype": item[0],
					"log_desc": item[1],
					"log_type": item[2],
					"upd_by": item[3],
				}
				history_list.append(record)

	response = JsonResponse(data={"success": True, "history_list": list(history_list)})
	response.status_code = 200
	return response


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_sp_post_daily_attend_progress(request):
	print("******************************************")
	print("FUNCTION: ajax_sp_post_daily_attend()")
	print("******************************************")
	post_date = request.POST.get('post_date')
	post_date = datetime.datetime.strptime(post_date, '%d/%m/%Y')	
	post_date = str(post_date)[0:10]

	progress_message = "Posting, please wait."
	
	sql = "select top 1 log_desc from hisdlyplan_log where log_date='" + str(post_date) + "' and log_id=1  order by upd_date desc;"
	try:				
		cursor = connection.cursor()
		cursor.execute(sql)
		result = cursor.fetchone()
		progress_message = result[0]
	except db.OperationalError as e:
		progress_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	except db.Error as e:
		progress_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
	finally:
		cursor.close()
	
	response = JsonResponse(data={"success": True, "progress_message": progress_message})
	response.status_code = 200
	return response


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_sp_post_daily_attend(request):
	print("******************************************")
	print("FUNCTION: ajax_sp_post_daily_attend()")
	print("******************************************")


	# Get TcurDate
	post_date = request.POST.get('post_date')
	post_date = datetime.datetime.strptime(post_date, '%d/%m/%Y')	
	post_date = str(post_date)[0:10]

	# Get Tperiod	
	period = getPeriod(request.POST.get('post_date'))
	# print("period = " + str(period))

	# ChkValidInput() - Check date is not empty
	if len(post_date)<=0:		
		response = JsonResponse(data={"success": True, "is_error": True, "class": "bg-danger", "error_message": "เลือกวันที่ไม่ถูกต้อง"})
		response.status_code = 200
		return response

	# ChkValidInput() - Check Post Day End
	sql = "select date_chk,gen_chk,end_chk,pro_chk,im_brn1,im_brn2,im_brn3,prd_id,upd_date,upd_by,upd_flag from t_date where date_chk='" + str(post_date) + "'"	
	# print("sql", sql)
	cursor = connection.cursor()	
	cursor.execute(sql)
	record = cursor.fetchall()
	cursor.close()
	if len(record) <= 0:
		response = JsonResponse(data={"success": True, "is_error": True, "class": "bg-danger", "error_message": "วันที่ <b>" + str(request.POST.get('post_date')) + "</b> ไม่มีรายการแจ้งเวร"})
		response.status_code = 200
		return response
	else:
		# end_chk = record[]
		end_chk = record[0][2]
		# print("end_chk", end_chk)
		if end_chk:
			response = JsonResponse(data={"success": True, "is_error": True, "class": "bg-danger", "error_message": "รายการแจ้งเวรของวันที่ <b>" + str(request.POST.get('post_date')) + "</b> มีการ <b>Post Day End</b> ไปแล้ว"})
			response.status_code = 200
			return response
		
	# TODO: Call PostDayEndN
	is_error, error_message = PostDayEndN(post_date, period, request.user.username)
	
	# is_error = True
	# error_message = "TEST"

	if is_error:
		response = JsonResponse(data={"success": True, "is_error": is_error, "class": "bg-danger", "error_message": error_message})
	else:
		response = JsonResponse(data={"success": True, "is_error": False, "class": "bg-success", "error_message": error_message})

	response.status_code = 200	
	return response



def PostDayEndN(post_date, period, username):
	try:
		cursor = connection.cursor()
		cursor.execute("exec dbo.CALCULATEDAYEND %s, %s", [post_date, username])					
		is_error = False
		message = "โพสรายการแจ้งเวรสำเร็จ"
	except db.OperationalError as e:
		is_error = False
		message = "exec CALCULATEDAYEND is error - " + str(e)
		return is_error, message
	except db.Error as e:
		is_error = True
		message = "exec CALCULATEDAYEND is error - " + str(e)
		return is_error, message

	return is_error, message



@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_sp_post_daily_attend_OLD_SP(request):

	print("******************************************")
	print("FUNCTION: ajax_sp_post_daily_attend()")
	print("******************************************")

	# Get TcurDate
	post_date = request.POST.get('post_date')
	post_date = datetime.datetime.strptime(post_date, '%d/%m/%Y')	
	post_date = str(post_date)[0:10]

	# Get Tperiod	
	period = getPeriod(request.POST.get('post_date'))
	# print("period = " + str(period))

	# ChkValidInput() - Check date is not empty
	if len(post_date)<=0:		
		response = JsonResponse(data={"success": True, "is_error": True, "class": "bg-danger", "error_message": "เลือกวันที่ไม่ถูกต้อง"})
		response.status_code = 200
		return response

	# ChkValidInput() - Check Post Day End
	sql = "select date_chk,gen_chk,end_chk,pro_chk,im_brn1,im_brn2,im_brn3,prd_id,upd_date,upd_by,upd_flag from t_date where date_chk='" + str(post_date) + "'"	
	# print("sql", sql)
	cursor = connection.cursor()	
	cursor.execute(sql)
	record = cursor.fetchall()
	cursor.close()
	if len(record) <= 0:
		response = JsonResponse(data={"success": True, "is_error": True, "class": "bg-danger", "error_message": "วันที่ <b>" + str(request.POST.get('post_date')) + "</b> ไม่มีรายการแจ้งเวร"})
		response.status_code = 200
		return response
	else:
		# end_chk = record[]
		end_chk = record[0][2]
		# print("end_chk", end_chk)
		if end_chk:
			response = JsonResponse(data={"success": True, "is_error": True, "class": "bg-danger", "error_message": "รายการแจ้งเวรของวันที่ <b>" + str(request.POST.get('post_date')) + "</b> มีการ <b>Post Day End</b> ไปแล้ว"})
			response.status_code = 200
			return response
		
	# TODO: Call PostDayEndN
	is_error, error_message = PostDayEndN(post_date, period, request.user.username)

	if is_error:
		response = JsonResponse(data={"success": True, "is_error": is_error, "class": "bg-danger", "error_message": error_message})
	else:
		response = JsonResponse(data={"success": True, "is_error": False, "class": "bg-success", "error_message": error_message})

	response.status_code = 200	
	return response


def PostDayEndN_OLD_SP(post_date, period, username):
	Esub = False
	RowsCount = 0
	RowsResult = 0

	# 1. Insert data into DLY_PLAN_BK
	sql = "select dly_date from dly_plan_bk where dly_date='" + str(post_date) + "'"
	cursor = connection.cursor()	
	cursor.execute(sql)
	record = cursor.fetchall()
	cursor.close()
	if len(record) == 0:
		sql = "INSERT INTO DLY_PLAN_BK(cnt_id, emp_id, dly_date, sch_shift, sch_no, dept_id, sch_rank, prd_id, absent, late, late_full, sch_relieft, relieft, relieft_id, tel_man, tel_time,tel_amt, tel_paid, ot, ot_reason, ot_time_frm, ot_time_to, ot_hr_amt, ot_pay_amt,spare, wage_id, wage_no, pay_type, bas_amt, otm_amt, bon_amt, pub_amt, soc_amt,dof_amt, ex_dof_amt, soc, pub, dof, paid, TPA, DAY7, upd_date, upd_by, upd_flag,upd_gen, upd_log, Remark) SELECT cnt_id, emp_id, dly_date, sch_shift, sch_no, dept_id, sch_rank, prd_id,absent, late, late_full, sch_relieft, relieft, relieft_id, tel_man, tel_time,tel_amt, tel_paid, ot, ot_reason, ot_time_frm, ot_time_to, ot_hr_amt, ot_pay_amt,spare, wage_id, wage_no, pay_type, bas_amt, otm_amt, bon_amt, pub_amt, soc_amt,dof_amt, ex_dof_amt, soc, pub, dof, paid, TPA, DAY7, upd_date, upd_by, upd_flag,upd_gen , upd_log, Remark From DLY_PLAN WHERE DLY_DATE='" + str(post_date) + "'"
		cursor = connection.cursor()
		cursor.execute(sql)
		cursor.close()
		message = "insert data into dly_plan_bk "
	else:
		message = "TODO"


	# 2. Check number of employee in DLY_PLAN
	sql = "select count(emp_id) as empcount from dly_plan where dly_date='" + str(post_date) + "'"
	cursor = connection.cursor()
	cursor.execute(sql)	
	record_count = cursor.fetchone()
	cursor.close()
	RowsCount = 0 if record_count[0] < 0 else record_count[0]


	#TODO
	count_status = 0
	for i in range(1,101):
		count_status = i
		if not Esub:
			if i==1:
				print("**********")
				print(" step #", i)
				print("**********")
				# exec CalDayEnd_COPYDATA1
				try:
					cursor = connection.cursor()
					cursor.execute("exec dbo.CalDayEnd_COPYDATA1 %s, %s, %s", [post_date, period, username])			
					message = "exec CalDayEnd_COPYDATA1 is success"
				except db.OperationalError as e:
					is_error = False
					message = "exec CalDayEnd_COPYDATA1 is error - " + str(e)
					return is_error, message
				except db.Error as e:
					is_error = True
					message = "exec CalDayEnd_COPYDATA1 is error - " + str(e)
					return is_error, message

				if RowsCount > 100:
					RowsCount -= 100
				elif RowsCount <= 100:
					RowsResult = 1
			else:
				print("**********")
				print(" step #", i)
				print("**********")				
				if RowsCount > 100:
					RowsCount -= 100
				elif RowsCount <= 100:
					RowsResult = 1

			# exec CalDayEnd_COPYDATA2
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalDayEnd_COPYDATA2 %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalDayEnd_COPYDATA2 is done")

			# exec CAL_UPDATE_ZONE_WAGE_ID_NEW
			cursor = connection.cursor()	
			cursor.execute("exec dbo.CAL_UPDATE_ZONE_WAGE_ID_NEW %s", [post_date])
			cursor.close()
			print("# exec CAL_UPDATE_ZONE_WAGE_ID_NEW is done")

			# exec CAL_UPDATE_DEPT_SECTION_WAGE_ID_NEW
			cursor = connection.cursor()	
			cursor.execute("exec dbo.CAL_UPDATE_DEPT_SECTION_WAGE_ID_NEW %s", [post_date])
			cursor.close()
			print("exec CAL_UPDATE_DEPT_SECTION_WAGE_ID_NEW is done")
			
			# exec CAL_UPDATE_EMP_WAGE_NEW
			cursor = connection.cursor()	
			cursor.execute("exec dbo.CAL_UPDATE_EMP_WAGE_NEW %s", [post_date])
			cursor.close()
			print("exec CAL_UPDATE_EMP_WAGE_NEW is done")

			# exec CalculateDay_STEP1_NEW
			cursor = connection.cursor()	
			cursor.execute("exec dbo.CalculateDay_STEP1_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("exec CalculateDay_STEP1_NEW is done")

			# exec CalculateDay_STEP2_NEW
			cursor = connection.cursor()	
			cursor.execute("exec dbo.CalculateDay_STEP2_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP2_NEW is done")

			# exec CalculateDay_STEP3_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP3_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP3_NEW is done")

			# Update DEN_DLY_PLAN
			sql = "update A set a.sch_rank=b.emp_rank from DEN_DLY_PLAN as A left join employee as b on a.emp_id=b.emp_id where a.dly_date='" + str(post_date) + "'"
			cursor = connection.cursor()
			cursor.execute(sql)
			cursor.close()
			print("Update DEN_DLY_PLAN 1 is done")

			# Update DEN_DLY_PLAN
			sql = "update A set a.wage_no=right('00'+ltrim(str(a.wage_id)),2)+ltrim(a.sch_rank) from DEN_DLY_PLAN as A where a.dly_date='" + str(post_date) + "'"
			cursor = connection.cursor()
			cursor.execute(sql)
			cursor.close()
			print("Update DEN_DLY_PLAN 2 is done")

			# Update DEN_DLY_PLAN
			sql = "update A set a.bon_amt=b.bonus_day from DEN_DLY_PLAN a left join t_wagerank as B on a.wage_no=b.wage_no where a.dly_date='" + str(post_date) + "'  and a.prd_id='" + str(period) + "' and a.absent='0' and b.wage_active=1"
			cursor = connection.cursor()
			cursor.execute(sql)
			cursor.close()
			print("Update DEN_DLY_PLAN 3 is done")

			# exec CalculateDay_STEP4_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP4_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP4_NEW is done")

			# exec CalculateDay_STEP5_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP5_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP5_NEW is done")

			# exec CalculateDay_STEP6_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP6_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP6_NEW is done")

			# exec CalculateDay_STEP7_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP7_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP7_NEW is done")

			#exec CalculateDay_STEP8_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP8_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP8_NEW is done")

			#exec CalculateDay_STEP9_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP9_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP9_NEW is done")

			#exec CalculateDay_STEP10_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP10_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP10_NEW is done")

			#exec CalculateDay_STEP11_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP11_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP11_NEW is done")

			#exec CalculateDay_STEP12_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP12_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP12_NEW is done")

			#exec CalculateDay_STEP13_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP13_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP13_NEW is done")

			#exec CalculateDay_STEP14_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP14_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP14_NEW is done")

			#exec CalculateDay_STEP15_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP15_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP15_NEW is done")

			#exec CalculateDay_STEP16_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP16_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP16_NEW is done")

			#exec CalculateDay_STEP17_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP17_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP17_NEW is done")

			#exec CalculateDay_STEP18_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP18_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP18_NEW is done")

			#exec CalculateDay_STEP19_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP19_NEW %s, %s, %s", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP19_NEW is done")

			#exec CalculateDay_STEP20_NEW
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_STEP20_NEW %s, %s, %s, '0'", [post_date, period, username])
			cursor.close()
			print("# exec CalculateDay_STEP20_NEW is done")

			if RowsResult == 1:
				Esub = True
		else:
			break

	try:		
		sql = "select count(emp_id) as empcount from his_dly_plan where dly_date='" + str(post_date) + "'"
		cursor = connection.cursor()
		cursor.execute(sql)	
		record_count = cursor.fetchone()
		cursor.close()

		if record_count[0] > 0:
			# Update Generate Complete
			sql = "update t_date set end_chk=1, upd_date=GetDate(), upd_by='" + str(username) + "', upd_flag='E' where date_chk='" + str(post_date) + "'"
			cursor = connection.cursor()
			cursor.execute(sql)	
			cursor.close()

			# MsgBox "Post Day End for date "

			# CalculateDay_DOF
			cursor = connection.cursor()
			cursor.execute("exec dbo.CalculateDay_DOF %s", [post_date])
			cursor.close()
			print("CalculateDay_DOF is done")

			is_error = False
			# message = "Check DOF for date <b>" + str(post_date) + "</b> - Complete."
			message = "โพสรายการแจ้งเวรของวันที่ <b>" + str(post_date) + "</b> สำเร็จ"

		else:
			is_error = True
			message = "Found problem between Post Day End. Please Post DayEnd next time again."
	except db.OperationalError as e:
		message = "Error";
		is_error = True
	except db.OperationalError as e:    	
		message = str(e);
		is_error = True
	except db.Error as e:
		error_message = str(e);
		is_error = True
	
	return is_error, message


def getPeriod(generated_date):
	generated_date = datetime.datetime.strptime(generated_date, '%d/%m/%Y')
	# print(generated_date)
	try:
		period = TPeriod.objects.filter(prd_date_frm__lte=generated_date).filter(prd_date_to__gte=generated_date).filter(emp_type='D1').get()
		period = period.prd_id
	except TPeriod.DoesNotExist:
		period = ""
	
	return period


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_sp_generate_daily_attend_status(request):

	print("************************************************")
	print("FUNCTION: ajax_sp_generate_daily_attend_status()")
	print("************************************************")
	data = {'state': task.state, 'result': task.result,}
	return HttpResponse(json.dumps(data), content_type='application/json')


def isGenerateDailyCreated(attendance_date,cnt_id,getPriorityStatus,gUSE,gADD,gEDIT,gDEL,gPREVIEW,gPRINT,gIM,gEX,gSALARY,gType,gOLD):
	print("************************************")
	print("FUNCTION: isGenerateDailyCreated()")
	print("************************************")

	# Implement ChkValidInput Case 3

	is_pass = False
	error_message = ""

	# Check if date_chk is created
	attendance_date = datetime.datetime.strptime(attendance_date, '%d/%m/%Y')
	sql = "select gen_chk, end_chk, pro_chk from t_date where date_chk='" + str(attendance_date) + "'"

	cursor = connection.cursor()
	cursor.execute(sql)	
	tdate = cursor.fetchall()
	cursor.close()

	if len(tdate) <= 0:
		is_pass = False
		error_message = "ข้อมูลตารางเวรของวันที่ <b>" + str(attendance_date.strftime("%d/%m/%Y")) + "</b> ยังไม่ได้ Gen<br>กรุณา Gen ข้อมูลก่อน"
		return is_pass, error_message		
	else:
		gen_chk = 1 if tdate[0][0]==1 else 0
		end_chk = 1 if tdate[0][1]==1 else 0
		pro_chk = 1 if tdate[0][2]==1 else 0

		if end_chk == 1:
			if gOLD==False:
				is_pass = False
				error_message = "ข้อมูลวันนี้ถูก Day end ไปแล้ว ไม่สามารถเรียกดูข้อมูลย้อนหลังได้"
				return is_pass, error_message
			else:
				is_pass = True
		else:
			is_pass = True
	
	return is_pass, error_message	


def getGaray(gType):
	gPos = gType
	lAray = 0




@login_required(login_url='/accounts/login/')
def sfQuery(request):	
	print("********************************************")
	print("FUNCTION: sfQuery()")
	print("********************************************")	
	
	username = request.user.username
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	cnt_id = cnt_id.lstrip("0")

	# chkValidInput(3)
	# START
	chkOldValue = 0
	dly_date = datetime.datetime.strptime(request.POST.get('attendance_date'), '%d/%m/%Y').date()
	if (dly_date is None) or (dly_date==""):
		return False, "กรุณาป้อนวันที่"

	sql = "select date_chk,gen_chk,end_chk,pro_chk from t_date where date_chk='" + str(dly_date) + "'"
	cursor = connection.cursor()
	cursor.execute(sql)	
	t_date_obj = cursor.fetchall()
	cursor.close()
	
	gen_chk = 0	
	end_chk = 0
	pro_chk = 0

	# ตรวจสอบว่ามีการสร้างตารางรับแจ้งเวรไว้หรือยัง
	if (t_date_obj is not None):
		if len(t_date_obj)<=0:			
			return False, "ข้อมูลตารางเวรของวันที่ <b>" + str(request.POST.get('attendance_date')) + "</b> ยังไม่ได้ Gen โปรด Gen ข้อมูลก่อน"	
		else:
			message = "chkValidInput(3) is pass"
			gen_chk = t_date_obj[0][1]
			end_chk = t_date_obj[0][2]
			pro_chk = t_date_obj[0][3]
	else:
		return False, "ข้อมูลตารางเวรของวันที่ <b>" + str(request.POST.get('attendance_date')) + "</b> ยังไม่ได้ Gen โปรด Gen ข้อมูลก่อน"

	# ตรวจสอบว่า post day end ไปหรือยัง
	return False, "DEBUG 2"

	if end_chk==1:			
		return False, "ข้อมูลวันที่ <b>" + str() + "</b> ถูก DayEnd ไปแล้ว ไม่สามารถเรียกดูย้อนหลังได้"

	# ตรวจสอบว่าเลขที่สัญญาปิดไปแล้วหรือไม่
	# call GetContractActive(cnt_id)
	sql = "select cnt_active from cus_contract where cnt_id=" + str(cnt_id)
	cursor = connection.cursor()
	cursor.execute(sql)	
	cus_contract_obj = cursor.fetchall()
	cursor.close()
	cnt_active = 0
	if (cus_contract_obj is not None):
		if len(cus_contract_obj)<=0:
			return False, "ไม่พบรายละเอียดสัญญาเลขที่ <b>" + str(cnt_id) + "</b>"
		else:
			cnt_active = cus_contract_obj[0][0]
	if cnt_active!=1:
		return False, "สัญญาเลขที่ <b>" + str(cnt_id) + "</b> ถูกยกเลิก"

	# END


	# Continue sfQuery()
	# call DisplayList("NUM_SERVICE")

	# call DisplayList("CUS_SERVICE")

	# call DisplayList("DLY_PLAN")


	# call DisplayList("SCH_PLAN")


	return True, message


def showContract(cnt_id):
	print("********************************************")
	print("FUNCTION: showContract()")
	print("********************************************")	

	is_found = False
	contract_info_obj = None
	message = ""

	sql = "select "
	sql += " b.cus_name_th, b.cus_name_en, b.cus_tel,"
	sql += " i.cus_name_th as site_th, i.cus_name_en as site_en, i.cus_tel as site_tel,"
	sql += " b.cus_add1_th, b.cus_add2_th,"
	sql += " f.con_fname_th, f.con_lname_th, f.con_position_th as con_pos_th,"
	sql += " f.con_fname_en, f.con_lname_en, f.con_position_en as con_pos_en,"
	sql += " a.cnt_doc_no, a.cnt_sign_frm, a.cnt_sign_to, a.cnt_eff_frm, a.cnt_eff_to,"
	sql += " k.wage_id, k.wage_en, g.apr_name_en, a.cnt_zone, a.cnt_active,"
	sql += " c.dist_th, c.dist_en, d.city_th, d.city_en, e.country_th, e.country_en, h.zone_en,"
	sql += " g.apr_name_en, k.wage_en,"
	sql += " a.*, b.*"
	sql += " from cus_contract as a"
	sql += " left join customer as b on a.cus_id=b.cus_id and a.cus_brn=b.cus_brn"
	sql += " left join customer as i on a.cus_id=i.cus_id and i.cus_brn=0"
	sql += " left join t_district as c on b.cus_district=c.dist_id"
	sql += " left join t_city as d on b.cus_city=d.city_id"
	sql += " left join t_country as e on b.cus_country=e.country_id"
	sql += " left join cus_contact as f on b.site_contact=f.con_id"
	sql += " left join com_zone as h on b.cus_zone=h.zone_id"
	sql += " left join t_aprove as g on a.cnt_apr_by=g.apr_id"
	sql += " left join t_wagezone as k on a.cnt_wage_id=k.wage_id"
	sql += " where a.cnt_id=" + str(cnt_id)
	sql += " and a.cnt_active=1"
	# print("sql 11:", sql)

	try:				
		cursor = connection.cursor()
		cursor.execute(sql)
		contract_info_obj = cursor.fetchall()
	except db.OperationalError as e:
		return False, contract_info_obj, "<b>Please send this error to IT teamใ</b><br>" + str(e)
	except db.Error as e:
		return False, contract_info_obj, "<b>Please send this error to IT team.</b><br>" + str(e)
	finally:
		cursor.close()

	if contract_info_obj is not None:
		if len(contract_info_obj)>0:
			is_found = True
		else:
			is_found = False
			message = "ไม่พบรายละเอียดของสัญญาเลขที่ <b>" + str(cnt_id) + "</b> หรือสัญญานี้อาจถูกยกเลิกไปแล้ว"
	else:
		is_found = False
		message = "ไม่พบรายละเอียดของสัญญาเลขที่ <b>" + str(cnt_id) + "</b> หรือสัญญานี้อาจถูกยกเลิกไปแล้ว"

	return is_found, contract_info_obj, message



def getCustomerScheduleList(cnt_id):
	print("********************************************")
	print("FUNCTION: getCustomerScheduleList()")
	print("********************************************")	

	is_found = False
	schedule_list = None
	message = ""

	sql = "select b.* "
	sql += ",k.emp_fname_th,k.emp_lname_th "
	sql += ",c.shf_desc as shf_mon "
	sql += ",d.shf_desc as shf_tue "
	sql += ",e.shf_desc as shf_wed "
	sql += ",f.shf_desc as shf_thu "
	sql += ",g.shf_desc as shf_fri "
	sql += ",h.shf_desc as shf_sat "
	sql += ",i.shf_desc as shf_sun "
	sql += "from cus_contract as a left join sch_plan as b on a.cnt_id=b.cnt_id "
	sql += "left join v_employee as k on b.emp_id=k.emp_id "
	sql += "left join t_shift as c on b.sch_shf_mon=c.shf_id "
	sql += "left join t_shift as d on b.sch_shf_tue=d.shf_id "
	sql += "left join t_shift as e on b.sch_shf_wed=e.shf_id "
	sql += "left join t_shift as f on b.sch_shf_thu=f.shf_id "
	sql += "left join t_shift as g on b.sch_shf_fri=g.shf_id "
	sql += "left join t_shift as h on b.sch_shf_sat=h.shf_id "
	sql += "left join t_shift as i on b.sch_shf_sun=i.shf_id "
	sql += "where a.cnt_id=" + str(cnt_id) + " "
	sql += "and a.cnt_active=1 "
	sql += "and b.upd_flag<>'D' "
	sql += "and b.sch_active=1 "
	sql += "order by b.sch_active desc,b.emp_id"

	try:				
		cursor = connection.cursor()
		cursor.execute(sql)
		customer_schedule_list = cursor.fetchall()
	except db.OperationalError as e:
		return False, customer_schedule_list, "<b>Please send this error to IT teamใ</b><br>" + str(e)
	except db.Error as e:
		return False, customer_schedule_list, "<b>Please send this error to IT team.</b><br>" + str(e)
	finally:
		cursor.close()

	if customer_schedule_list is not None:
		if len(customer_schedule_list)>0:
			is_found = True
		else:
			is_found = False
			message = "ไม่พบรายละเอียดของรายการสัญญาเลขที่ <b>" + str(cnt_id) + "</b>"
	else:
		is_found = False
		message = "ไม่พบรายละเอียดของรายการสัญญาเลขที่ <b>" + str(cnt_id) + "</b>"

	return is_found, customer_schedule_list, message


def getCustomerContractServiceList(cnt_id):
	print("********************************************")
	print("FUNCTION: getCustomerContractServiceList()")
	print("********************************************")	

	is_found = False
	customer_contract_service_list = None
	message = ""

	# sql = "select distinct * from v_contract where cnt_id=" + str(cnt_id) + " and srv_active=1 and CUS_SERVICE_FLAG<>'D' order by srv_id"
	sql = "select distinct * from v_contract where cnt_id=" + str(cnt_id) + " and CUS_SERVICE_FLAG<>'D' order by srv_active desc, srv_id;"
	try:				
		cursor = connection.cursor()
		cursor.execute(sql)
		customer_contract_service_list = cursor.fetchall()
	except db.OperationalError as e:
		return False, customer_contract_service_list, "<b>Please send this error to IT teamใ</b><br>" + str(e)
	except db.Error as e:
		return False, customer_contract_service_list, "<b>Please send this error to IT team.</b><br>" + str(e)
	finally:
		cursor.close()

	if customer_contract_service_list is not None:
		if len(customer_contract_service_list)>0:
			is_found = True
		else:
			is_found = False
			message = "ไม่พบรายละเอียดของรายการสัญญาเลขที่ <b>" + str(cnt_id) + "</b>"
	else:
		is_found = False
		message = "ไม่พบรายละเอียดของรายการสัญญาเลขที่ <b>" + str(cnt_id) + "</b>"

	return is_found, customer_contract_service_list, message


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_get_attendance_information(request):
	print("********************************************")
	print("FUNCTION: ajax_get_attendance_information()")
	print("********************************************")	

	# กำหนดค่าเริ่มต้น
	is_pass = False			# กำหนดให้เป็น False ไว้ก่อน
	message = ""
	form_name = "frmD200"	# ค่าได้มาจากชื่อฟอร์ม D200: Daily Attendance
	username = request.user.username	# ชื่อผู้ล็อคอิน
	user_first_name = request.user.first_name
	attendance_date = request.POST.get('attendance_date')
	search_shift_option = request.POST.get('search_shift_option')	

	cus_id = request.POST.get('cus_id').lstrip("0")
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)		
	cus_no = cus_id + cus_brn.zfill(3)	
	schedule_list = []
	employee_list = []
	emp_leave_list = []
	ot_reason_list = []
	contract_info_obj = None
	customer_contract_service_list = None
	customer_schedule_list = None

	totalNDP = 0
	totalNNP = 0
	totalPDP = 0
	totalPNP = 0
	totalNDA = 0
	totalNNA = 0
	totalPDA = 0
	totalPNA = 0
	totalNDM = 0
	totalNNM = 0
	totalPDM = 0
	totalPNM = 0

	# TODO
	# call getContactID	

	# TODO
	# call ChkValidInput(3)
	# วันที่นี้ตรวจสอบตารางเวรสร้างไว้หรือไม่
	# ตรวจสอบวันที่นี้ทำการ Post Day End ไปแล้วหรือไม่
	# ตรวจสอบสัญญาถูกยกเลิกไปแล้วหรือไม่

	# Get Contract Info
	is_found,contract_info_obj,message = showContract(cnt_id)
	if is_found:
		contract_info_obj = contract_info_obj

	else:
		response = JsonResponse(data={
		    "success": True,
		    "is_found": False,
		    "message": message
		})		
		response.status_code = 200
		return response		

	# Get Contract Service
	is_found,customer_contract_service_list,message = getCustomerContractServiceList(cnt_id)
	if is_found:
		customer_contract_service_list = customer_contract_service_list


	# Get Schedule List
	is_found,customer_schedule_list,message = getCustomerScheduleList(cnt_id)
	if is_found:
		customer_schedule_list = customer_schedule_list


	#getPriorityStatus = False
	#gUSE,gADD,gEDIT,gDEL,gPREVIEW,gPRINT,gIM,gEX,gSALARY,gType,gOLD

	# ตรวจสอบวันที่ Daily Attendance มากกว่าวันที่ปัจจุบัน	
	today_date = convertStringToDate(settings.TODAY_DATE.strftime("%d/%m/%Y"))
	daily_attendance_date = convertStringToDate(attendance_date)
	
	# print("today_date", today_date)
	# print("daily_attendance_date", daily_attendance_date)

	if daily_attendance_date > today_date:
		is_pass = False
		message = "วันที่"
		response = JsonResponse(data={
		    "success": True,
		    "is_found": False,
		    "message": "วันที่ <b>Daily Attendance</b> มากกว่าวันที่ปัจจุบัน...",
		})		
		response.status_code = 200
		return response

	# ตรวจสอบวันที่ Daily Attendance น้อยกว่าวันที่ปัจจุบัน	
	'''
	if daily_attendance_date < today_date:
		is_pass = False
		message = "วันที่"
		response = JsonResponse(data={
		    "success": True,
		    "is_found": False,
		    "message": "วันที่ <b>Daily Attendance</b> น้อยกว่าวันที่ปัจจุบัน",
		})
		response.status_code = 200
		return response
	'''
	

	# ตรวจสอบสิทธิ์การใช้งานจากระบบเก่า
	usr_id = getUSR_ID(username)	
	if usr_id is None:
		response = JsonResponse(data={
		    "success": True,
		    "is_found": False,
		    "message": "ไม่พบสิทธ์การใช้งาน กรุณาติดต่อฝ่าย IT เพื่อตรวจสอบ",
		})		
		response.status_code = 200
		return response	
	else:
		is_pass = True
	
	getPriorityStatus,gUSE,gADD,gEDIT,gDEL,gPREVIEW,gPRINT,gIM,gEX,gSALARY,gType,gOLD = getPriority(usr_id, form_name)


	# getGaray(gType)
	if gType != "":
		getGaray(gType)

	# amnaj
	# is_pass, message = isGenerateDailyCreated(attendance_date,cnt_id,getPriorityStatus,gUSE,gADD,gEDIT,gDEL,gPREVIEW,gPRINT,gIM,gEX,gSALARY,gType,gOLD)
	# ไม่ตรวจสิทธิ์ดูข้อมูลการแจ้งเวรย้อนหลัง
	is_pass = True

	if is_pass:
		attendance_date = request.POST.get('attendance_date')
		attendance_date = datetime.datetime.strptime(attendance_date, '%d/%m/%Y')
		# print("attendance_date = " + str(attendance_date))

		# Get current date
		curDate = attendance_date
		# print("Current date = " + str(curDate))

		# Check if daily attend is a public holiday
		# select hol_date from t_holiday where hol_date=curDate
		cursor = connection.cursor()
		cursor.execute("select hol_date from t_holiday where hol_date=%s", [curDate])		
		cursor.close
		# 99  # DAY OFF #########
		# 999  # ANOTHER SITE #

		# Get Day of Week
		dayOfWeek = daily_attendance_date.strftime('%w')
		print("dayOfWeek:", dayOfWeek)
		print("dayOfWeek:", daily_attendance_date.strftime('%a'))

		if dayOfWeek=="0":
			DayCurDate = "SRV_SUN"
		elif dayOfWeek=="1":
			DayCurDate = "SRV_MON"
		elif dayOfWeek=="2":
			DayCurDate = "SRV_TUE"
		elif dayOfWeek=="3":
			DayCurDate = "SRV_WED"
		elif dayOfWeek=="4":
			DayCurDate = "SRV_THU"
		elif dayOfWeek=="5":
			DayCurDate = "SRV_FRI"
		elif dayOfWeek=="6":
			DayCurDate = "SRV_SAT"
		else:
			DayCurDate = "0"


		# Provide contract service list dropdown


		# Check Total
		# NUM_SERVICE TOTAL
		# select cnt_id,shf_type,sum(srv_wed) as srv_num, sum(srv_pub) as srv_pub from v_contract as a where cnt_id=1008000001 and srv_active=1 and cus_service_flag <> 'D' group by cnt_id,shf_type
		# sql = "select cnt_id,shf_type,sum(srv_wed) as srv_num, sum(srv_pub) as srv_pub from v_contract as a where cnt_id=" + str(cnt_id) + " and srv_active=1 and cus_service_flag <> 'D' group by cnt_id,shf_type"
		
		sql = "select cnt_id,shf_type,sum(" + DayCurDate + ") as srv_num, sum(srv_pub) as srv_pub "
		sql += "from v_contract as a where cnt_id=" + str(cnt_id) + " and srv_active=1 "
		sql += "and cus_service_flag <> 'D' "
		sql += "and srv_eff_frm<='" + str(curDate) + "' group by cnt_id,shf_type"
		# print("SQL debug:", sql)

		cursor = connection.cursor()
		# cursor.execute("select cnt_id,shf_type,sum(srv_wed) as srv_num, sum(srv_pub) as srv_pub from v_contract as a where cnt_id=%s and srv_active=1 and cus_service_flag <> 'D' group by cnt_id,shf_type", [cnt_id])
		cursor.execute(sql)
		rows = cursor.fetchall()
		cursor.close

		if len(rows)>0:
			for index in range(len(rows)):
				cnt_id_temp = rows[index][0]
				shf_type_temp = rows[index][1]
				srv_num_temp = rows[index][2]
				srv_pub_temp = rows[index][3]
				if shf_type_temp=='D':
					totalNDP = srv_num_temp
					totalPDP = srv_pub_temp
				else:
					totalNNP = srv_num_temp
					totalPNP = srv_pub_temp
		
		# print("totalNDP=" + str(totalNDP))
		# print("totalNNP=" + str(totalNNP))
		# print("totalPDP=" + str(totalPDP))
		# print("totalPNP=" + str(totalPNP))


		# DLY_PLAN TOTAL
		# select distinct * from v_dlyplan where cnt_id=2526000001 and dly_date=convert(datetime,'2020-12-02',20) and customer_flag<>'D' order by sch_shift, emp_id
		cursor = connection.cursor()
		
		today_date = convertStringToDate(settings.TODAY_DATE.strftime("%d/%m/%Y"))		
		selected_attendance_date = datetime.datetime.strptime(request.POST.get('attendance_date'), '%d/%m/%Y')
		# print("today_date=", today_date)
		# print("daily_attendance_date=", selected_attendance_date)

		if selected_attendance_date == today_date:
			cursor.execute("select distinct * from v_dlyplan where cnt_id=%s and dly_date=convert(datetime,%s,20) and customer_flag<>'D' order by sch_shift, emp_id", [cnt_id, curDate])
		else:
			# batman
			gen_chk = 0	
			end_chk = 0
			pro_chk = 0		
			sql = "select date_chk,gen_chk,end_chk,pro_chk from t_date where date_chk='" + str(daily_attendance_date) + "'"
			cursor1 = connection.cursor()
			cursor1.execute(sql)	
			t_date_obj = cursor1.fetchall()			
			# ตรวจสอบค่า gen_chk, end_chk, prp_chk ของวันที่ต้องการดึงข้อมูล
			if (t_date_obj is not None):
				if len(t_date_obj)>0:
					gen_chk = t_date_obj[0][1]
					end_chk = t_date_obj[0][2]
					pro_chk = t_date_obj[0][3]

			if end_chk==1:
				cursor.execute("select distinct * from v_hdlyplan where cnt_id=%s and dly_date=convert(datetime,%s,20) order by sch_shift, emp_id", [cnt_id, curDate])				
			else:
				cursor.execute("select distinct * from v_dlyplan where cnt_id=%s and dly_date=convert(datetime,%s,20) and customer_flag<>'D' order by sch_shift, emp_id", [cnt_id, curDate])
			
		rows = cursor.fetchall()
		cursor.close()
		if len(rows)>0:
			for index in range(len(rows)):				
				shf_type = rows[index][2]
				absent = rows[index][21]
				# print("shf_type = " + str(shf_type))
				if shf_type=='D':
					if absent==0:
						totalNDA = totalNDA + 1
						totalPDA = totalPDA + 1
				elif shf_type=='N':
					if absent==0:
						totalNNA = totalNNA + 1
						totalPNA = totalPNA + 1

		totalNDM = totalNDA - totalNDP
		totalNNM = totalNNA - totalNNP
		totalPDM = totalPDA - totalPDP
		totalPNM = totalPNA - totalPNP

		
		# TOTAL_Missing_Guard



		# CUS_SERVICE		
		


		# Get contract schedule list
		# ----- START -----
		cursor = connection.cursor()
		cursor.execute("select distinct(shf_id),shf_desc from cus_service a,t_shift b where a.cnt_id=%s and a.srv_active=1 and b.shf_id=a.srv_shif_id", [cnt_id])
		rows = cursor.fetchall()
		for row in rows:
			record = {
				"shf_id": row[0],
				"shf_desc": row[1],
				}
			schedule_list.append(record)		

		record = {"shf_id": 99,"shf_desc": "99   # DAY OFF ########"}
		schedule_list.append(record)
		record = {"shf_id": 999,"shf_desc": "999   # ANOTHER SITE #"}
		schedule_list.append(record)
		cursor.close()
		# ----- END -----




		# Get ot reason list
		# ----- START -----		
		cursor = connection.cursor()	
		cursor.execute("select ot_res_id,ot_res_th from t_ot_reason")
		ot_reason_obj = cursor.fetchall()
		
		# record = {"ot_res_id": 56,"ot_res_th": "มาสาย"}
		# ot_reason_list.append(record)

		if ot_reason_obj is not None:
			for row in ot_reason_obj:
				# print("row[0]", row[0])
				if row[0]==57:
					record = {
						"ot_res_id": 56,
						"ot_res_th": "มาสาย",
					}
					ot_reason_list.append(record)					
					record = {
						"ot_res_id": row[0],
						"ot_res_th": row[1],
					}					
				else:
					record = {
						"ot_res_id": row[0],
						"ot_res_th": row[1],
					}

				ot_reason_list.append(record)
		else:
			ot_reason_list = None
		cursor.close()
		# ----- END -----

		string_today_date = str(settings.TODAY_DATE.strftime("%d/%m/%Y"))
		today_date = datetime.datetime.strptime(string_today_date, "%d/%m/%Y")
		# print("today_date = " + str(today_date))

		daily_attendance_date = datetime.datetime.strptime(request.POST.get('attendance_date'), '%d/%m/%Y').date()		
		# print("daily_attendance_date = " + str(daily_attendance_date))			





		
		# ตรวจสอบว่าต้องไปดึงข้อมูลจาก v_dlyplan หรือ v_hdlyplan
		gen_chk = 0	
		end_chk = 0
		pro_chk = 0		
		sql = "select date_chk,gen_chk,end_chk,pro_chk from t_date where date_chk='" + str(daily_attendance_date) + "'"
		cursor = connection.cursor()
		cursor.execute(sql)	
		t_date_obj = cursor.fetchall()
		cursor.close()
		# ตรวจสอบค่า gen_chk, end_chk, prp_chk ของวันที่ต้องการดึงข้อมูล
		if (t_date_obj is not None):
			if len(t_date_obj)>0:
				gen_chk = t_date_obj[0][1]
				end_chk = t_date_obj[0][2]
				pro_chk = t_date_obj[0][3]

		# ตรวจสอบว่า gen_chk ไปหรือยัง
		view_name = "v_dlyplan"
		if gen_chk!=1:
			response = JsonResponse(data={"success": True, "is_found": False,"message": "ไม่มีรายการรับแจ้งเวรในวันที่ <b>" + str(request.POST.get('attendance_date')) + "</b>"})
			response.status_code = 200
			return response
		elif end_chk!=1:
			table = ", Customer_Flag from v_dlyplan where cnt_id=" + str(cnt_id) + " and dly_date='" + str(daily_attendance_date) + "' and customer_flag<>'D' "
		else:
			if daily_attendance_date==today_date.date():
				table = ", Customer_Flag from v_dlyplan where cnt_id=" + str(cnt_id) + " and dly_date='" + str(daily_attendance_date) + "' and customer_flag<>'D' "
			elif daily_attendance_date < today_date.date():
				# เช็คล็อคอินยูสเซอร์เป็น CMS_SUP หรือไม่
				if username=='CMS_SUP':							
					view_name = "v_hdlyplan"
					table = " from " + str(view_name) + " where cnt_id=" + str(cnt_id) + " and dly_date='" + str(daily_attendance_date) + "' "
				else:
					view_name = "v_hdlyplan"
					table = " from " + str(view_name) + " where cnt_id=" + str(cnt_id) + " and dly_date='" + str(daily_attendance_date) + "' "

		# Get employee schedule list (v_dlyplan)
		sql = "select distinct "
		sql += "emp_fname_th, emp_lname_th, shf_type, shf_desc, shf_time_frm, shf_time_to, "
		sql += "shf_amt_hr, Remp_fname_th, Remp_lname_th, ot_res_th, ot_res_en, "
		sql += "dept_th, dept_en, cnt_id, emp_id, dly_date, "
		sql += "sch_shift, sch_no, dept_id, sch_rank, prd_id, "
		sql += "absent, relieft, relieft_id, tel_man, tel_time, "
		sql += "tel_amt, tel_paid, ot, ot_reason, ot_time_frm, "
		sql += "ot_time_to, ot_hr_amt, ot_pay_amt, spare, wage_id, "
		sql += "wage_no, pay_type, bas_amt, bon_amt, pub_amt, "
		sql += "soc_amt, soc, pub, paid, upd_date, "
		sql += "upd_by, upd_flag, upd_gen, cus_name_th, late, "
		sql += "sch_relieft, otm_amt, dof_amt, dof, TPA, "
		sql += "late_full, DAY7, cnt_sale_amt, cus_name_en, cnt_active, "
		sql += "Remark, ex_dof_amt "
		# sql += " from v_dlyplan where cnt_id=1486000001 and dly_date='2021-01-11' order by sch_shift,emp_id"
		sql += table
		
		# print("search_shift_option:", search_shift_option)

		if search_shift_option=="2":
			sql += "and shf_type='D' "
		elif search_shift_option=="3":
			sql += "and shf_type='N' "

		sql += " order by sch_shift, emp_id"
		# print("______sql 3_____ = " + str(sql))

		cursor = connection.cursor()
		# cursor.execute(sql, [cnt_id, attendance_date])
		cursor.execute(sql)
		rows = cursor.fetchall()
		cursor.close()


		# Check Leave Status - Server side
		# print("rows:", len(rows))
		if(len(rows)>0):
			where_in = " "
			count = 0
			for row in rows:
				emp_id_temp = row[14]
				if emp_id_temp!= "":
					if count==len(rows)-1:
						where_in += str(emp_id_temp)
					else:
						where_in += str(emp_id_temp) + ","
				count += 1

			# emp_leave_list = []
			# print("where_in:", where_in)
			sql_where_in = "select emp_id from emp_leave_act where getdate() between lve_date_frm and lve_date_to and emp_id in (" + where_in + ")"
			# print("sql_where_in:", sql_where_in)
			cursor = connection.cursor()
			cursor.execute(sql_where_in)
			records = cursor.fetchall()
			cursor.close()
			if records is not None:
				for item in records:
					emp_leave_list.append(item[0])	
			# print("Number of records:", len(emp_leave_list))				


		# Check Leave Status - Client side
		'''
		if len(rows)>0:
			cursor = connection.cursor()
			for row in rows:
				emp_id_temp = row[14]
				sql = "select emp_id from emp_leave_act where getdate() between lve_date_frm and lve_date_to and emp_id=" + str(emp_id_temp)
				cursor.execute(sql)
				item = cursor.fetchone()
				if item is not None:
					record = {"emp_id": item[0]}
					emp_leave_list.append(record)
					# print("emp_id_temp", item[0])
			cursor.close()
		'''


		'''
		response = JsonResponse(data={"success": True,"is_found": False,"message": "T"})
		response.status_code = 200
		return response
		'''

		for row in rows:
			# print("____row[21] = " + str(row[21]))

			if(row[21]):
				absent=1
			else:
				absent=0
			
			# print("tel_time = " + str(row[25]))

			if row[24]==1:
				tel_status = 1
				tel_man = "<span class='text-success'><font size='1.5em;'><i class='fas fa-phone-alt'></i></font></span>"
				
				if row[25] is not None:
					tel_time = row[25].strftime("%d/%m/%Y %H:%M")
				else:
					tel_time = ""

				tel_amt = row[26] if row[26] > 0 else 0
				tel_paid = 1 if row[27] else 0 
			else:
				tel_status = 0
				tel_man = ""
				tel_time = ""
				tel_amt = 0
				tel_paid = 0
				
			'''
			if row[25] is not None:
				tel_time = row[25].strftime("%d/%m/%Y %H:%M")
			else:
				tel_time = ""
			'''

			upd_date = row[45].strftime("%d/%m/%Y %H:%M")
			upd_date_naturalday = naturalday(row[45])
			upd_date_naturaltime = row[45]

			# print("upd_date_naturalday", upd_date_naturalday)
			# print("nautraltime", nautraltime(row[45]))


			upd_gen = "" if row[48] is None else row[48]
			remark = "" if row[61] is None else row[61].strip("0").strip()

			relief = 1 if row[22]==1 else 0
			#print("relief = " + str(relief))

			relief_id = "" if row[23]==0 else row[23]			
			#print("relief_id = " + str(relief_id))

			relief_fname_th = "" if row[7] is None else row[7]
			relief_lname_th = "" if row[8] is None else row[8]

			if view_name=="v_dlyplan":
				if row[63] is not None:
					customer_flag = "" if row[63] is None else row[63]
			else:
				customer_flag = ""

			late_status = 1 if row[50]==1 else 0
			late_full_status = 1 if row[56]==1 else 0

			# OT Time From
			# print("row[30]", row[30])
			if row[30] is not None:
				if row[30] != "":
					ot_time_frm = row[30].strftime("%d/%m/%Y %H:%M")
				else:
					ot_time_frm = None
			else:
				ot_time_frm = None

			# OT Time To
			# print("row[31]", row[31])
			if row[31] is not None:
				if row[31] != "":
					ot_time_to = row[31].strftime("%d/%m/%Y %H:%M")
				else:
					ot_time_to = None
			else:
				ot_time_to = None

			# OT Hour Amount
			if row[32] is not None:
				ot_hr_amt = int(row[32])
			else:
				ot_hr_amt = 0
			
			if row[14] in emp_leave_list:
				emp_leave_status = 1
			else:
				emp_leave_status = 0

			record = {
				"emp_fname_th": row[0].strip(),
				"emp_lname_th": row[1].strip(),
				"shf_type": row[2],
				"shf_desc": row[3],
				"shf_time_frm": row[4],
				"shf_time_to": row[5],
				"shf_amt_hr": row[6],
				"Remp_fname_th": relief_fname_th.strip(),
				"Remp_lname_th": relief_lname_th.strip(),
				"ot_res_th": row[9],         
				"ot_res_en": row[10],
				"dept_th": row[11],
				"dept_en": row[12],
				"cnt_id": row[13],
				"emp_id": row[14],
				"dly_date": row[15],
				"sch_shift": row[16],
				"sch_no": row[17],
				"dept_id": row[18],
				"sch_rank": row[19],
				"prd_id": row[20],
				"absent": absent,
				"relief": relief,
				"relief_id": relief_id,
				"tel_status": tel_status,
				"tel_man": tel_man,
				"tel_time": tel_time,
				"tel_amt": tel_amt,
				"tel_paid": tel_paid,
				"ot": row[28],
				"ot_reason": row[29],
				"ot_time_frm": ot_time_frm,
				"ot_time_to": ot_time_to,
				"ot_hr_amt": ot_hr_amt,
				"ot_pay_amt": row[33],
				"spare": row[34],
				"wage_id": row[35],
				"wage_no": row[36],
				"pay_type": row[37],
				"bas_amt": row[38],
				"bon_amt": row[39],
				"pub_amt": row[40],
				"soc_amt": row[41],
				"soc": row[42],
				"pub": row[43],
				"paid": row[44],

				"upd_date": upd_date,			
				"upd_date_naturalday": upd_date_naturalday,
				"upd_date_naturaltime": upd_date_naturaltime,

				"upd_by": row[46],
				"upd_flag": row[47],
				"upd_gen": upd_gen,
				"cus_name_th": row[49],
				"late": late_status,
				"sch_relieft": row[51],
				"otm_amt": row[52],
				"dof_amt": row[53],
				"dof": row[54],
				"TPA": row[55],
				"late_full": late_full_status,
				"DAY7": row[57],
				"cnt_sale_amt": row[58],
				"cus_name_en": row[59],
				"cnt_active": row[60],
				"remark": remark,
				"ex_dof_amt": row[62],
				"Customer_Flag": customer_flag,
				"update_by_user_first_name": user_first_name,
				"emp_leave_status": emp_leave_status,
			}
			employee_list.append(record)

		try:
			dlyplan = DlyPlan.objects.filter(cnt_id=cnt_id).all()
			is_found = True
			# print(1)
		except CusContract.DoesNotExist:
			is_found = False
			# print(2)

		message = ""

		cursor.close()
	else:
		is_found = False
		message = message

	
	# ตรวจสอบการอนุญาติให้ใช้ปุ่ม
	if view_name=="v_hdlyplan":
		if request.user.username=='CMS_SUP':
			allow_crud = True
		else:
			allow_crud = False
	else:
		allow_crud = True

	print("allow_crud=", allow_crud)
	
	response = JsonResponse(data={
	    "success": True,
	    "is_found": is_found,
	    "message": message,
	    "schedule_list": list(schedule_list),
	    "customer_contract_service_list": list(customer_contract_service_list),
	    "customer_schedule_list": list(customer_schedule_list),
	    "employee_list": list(employee_list),
	    "employee_leave_list": list(emp_leave_list),
	    "ot_reason_list": list(ot_reason_list),
	    "contract_info": list(contract_info_obj),
	    "totalNDP": totalNDP,
		"totalNNP": totalNNP,
		"totalPDP": totalPDP,
		"totalPNP": totalPNP,
		"totalNDA": totalNDA,
		"totalNNA": totalNNA,
		"totalPDA": totalPDA,
		"totalPNA": totalPNA,
		"totalNDM": totalNDM,
		"totalNNM": totalNNM,
		"totalPDM": totalPDM,
		"totalPNM": totalPNM,
		"allow_crud": allow_crud,
	})
	
	response.status_code = 200
	return response	


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_delete_employee_schedule_maintenance(request):
	print("********************************")
	print("FUNCTION: ajax_delete_employee_schedule_maintenance()")
	print("********************************")
	
	is_error = True
	message = ""
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)

	sch_no = request.POST.get('sch_no')
	upd_by = request.user.username
	
	sql = "update sch_plan set Upd_by='" + str(upd_by) + "', Upd_flag='D' where sch_no=" + str(sch_no) + ";"
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)

		sch_plan_list = []
		record = {}
		sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_active=1).exclude(upd_flag='D').order_by('-upd_date', 'emp_id')
		for d in sch_plan:
			if d.relief:
				relief = 1
			else:
				relief = 0 

			if d.sch_active:
				sch_active = 1
			else:
				sch_active = 0
			record = {
				"sch_no": d.sch_no,
				"emp_id": d.emp_id_id,
				"emp_fname_th": d.emp_id.emp_fname_th,
				"emp_lname_th": d.emp_id.emp_lname_th,
				"sch_rank": d.sch_rank,
				"sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
				"sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
				"sch_shf_mon": d.sch_shf_mon,
				"sch_shf_tue": d.sch_shf_tue,
				"sch_shf_wed": d.sch_shf_wed,
				"sch_shf_thu": d.sch_shf_thu,
				"sch_shf_fri": d.sch_shf_fri,
				"sch_shf_sat": d.sch_shf_sat,
				"sch_shf_sun": d.sch_shf_sun,
				"sch_active": sch_active,
				"relief": relief,
				"upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
				"upd_by": d.upd_by,
				"upd_flag": d.upd_flag,					 
			}
			sch_plan_list.append(record)

		is_error = False
		message = "ลบรายการสำเร็จ"
	except db.OperationalError as e:
		is_error = True
		message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
	except db.Error as e:
		is_error = True
		message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
	finally:
		cursor.close()	

	response = JsonResponse(data={
	    "success": True,
		"is_error": is_error,
	    "message": message,
		"sch_plan_list": list(sch_plan_list),
	})

	response.status_code = 200
	return response


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_delete_employee(request):
	print("********************************")
	print("FUNCTION: ajax_delete_employee()")
	print("********************************")

	username = request.user.username	
	dly_date = datetime.datetime.strptime(request.GET.get('dly_date'), '%d/%m/%Y').date()
	string_today_date = str(settings.TODAY_DATE.strftime("%d/%m/%Y"))
	today_date = datetime.datetime.strptime(string_today_date, "%d/%m/%Y").date()
	gen_chk = 0	
	end_chk = 0
	pro_chk = 0		
	sql = "select date_chk,gen_chk,end_chk,pro_chk from t_date where date_chk='" + str(dly_date) + "'"
	print("SQL : ", sql)
	cursor = connection.cursor()
	cursor.execute(sql)	
	t_date_obj = cursor.fetchall()
	cursor.close()
	# ตรวจสอบว่ามีการสร้างตารางรับแจ้งเวรไว้หรือยัง
	if (t_date_obj is not None):
		if len(t_date_obj)>0:
			gen_chk = t_date_obj[0][1]
			end_chk = t_date_obj[0][2]
			pro_chk = t_date_obj[0][3]


	print()
	print("*********************** DEBUG *************************")
	print(username, dly_date, string_today_date, today_date, end_chk)
	print("*********************** DEBUG *************************")
	print()

	cus_id = request.GET.get('cus_id').lstrip("0")
	cus_brn = request.GET.get('cus_brn')
	cus_vol = request.GET.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	emp_id = request.GET.get('emp_id')
	dly_date = datetime.datetime.strptime(request.GET.get('dly_date'), '%d/%m/%Y')	
	shift_id = request.GET.get('shift_id')
	# username = request.user.first_name
	username = request.user.username

	if username=='CMS_SUP':
		if dly_date.date()==today_date:
			if cus_id=="" or cus_id is None:
				response = JsonResponse(data={"success": True, "message": "Contract Number is not correct."})
				response.status_code = 200
				return response
			
			if emp_id=="" or cus_id is None:
				response = JsonResponse(data={"success": True, "message": "Employee ID is not correct."})
				response.status_code = 200
				return response

			if dly_date=="" or cus_id is None:
				response = JsonResponse(data={"success": True, "message": "Daily Attendnace Date is not correct."})
				response.status_code = 200
				return response

			# Check if request's record is existed
			with connection.cursor() as cursor:
				cursor.execute("insert his_dly_plan_del select getdate(), %s, 'DLY_PLAN', * from dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [username, cnt_id, emp_id, dly_date, shift_id])
				cursor.execute("delete dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [cnt_id, emp_id, dly_date, shift_id])
				cursor.execute("select * from dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [cnt_id, emp_id, dly_date, shift_id])
				row = cursor.fetchone()
				cursor.close

			if row is None:
				message = "Employee ID " + emp_id + " has been deleted."
			else:
				message = "Cannot delete Employee ID " + emp_id

			response = JsonResponse(data={
				"success": True,	    
				"message": message,
			})
		elif dly_date.date() < today_date:
			if end_chk==1:
				message = "CMS_SUP ทำการลบในตาราง his_dly_plan"
				if cus_id=="" or cus_id is None:
					response = JsonResponse(data={"success": True, "message": "Contract Number is not correct."})
					response.status_code = 200
					return response
				
				if emp_id=="" or cus_id is None:
					response = JsonResponse(data={"success": True, "message": "Employee ID is not correct."})
					response.status_code = 200
					return response

				if dly_date=="" or cus_id is None:
					response = JsonResponse(data={"success": True, "message": "Daily Attendnace Date is not correct."})
					response.status_code = 200
					return response

				# Check if request's record is existed
				with connection.cursor() as cursor:
					cursor.execute("insert his_dly_plan_del select getdate(), %s, 'HIS_DLY_PLAN', * from his_dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [username, cnt_id, emp_id, dly_date, shift_id])
					cursor.execute("delete his_dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [cnt_id, emp_id, dly_date, shift_id])
					cursor.execute("select * from his_dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [cnt_id, emp_id, dly_date, shift_id])
					row = cursor.fetchone()
					cursor.close

				if row is None:
					message = "Employee ID " + emp_id + " has been deleted."
				else:
					message = "Cannot delete Employee ID " + emp_id

				response = JsonResponse(data={
					"success": True,	    
					"message": message,
				})				
			else:
				message = "ERROR : วันที่ทำรายการมากกว่าวันที่ปัจจุบัน"

	else:
		if end_chk==1:
			message = str(username) + " ไม่มีสิทธิ์ทำรายการ"			
		else:
			if dly_date==today_date:
				print(str(username) + " ทำการลบในตาราง dly_plan")
				if cus_id=="" or cus_id is None:
					response = JsonResponse(data={"success": True, "message": "Contract Number is not correct."})
					response.status_code = 200
					return response
				
				if emp_id=="" or cus_id is None:
					response = JsonResponse(data={"success": True, "message": "Employee ID is not correct."})
					response.status_code = 200
					return response

				if dly_date=="" or cus_id is None:
					response = JsonResponse(data={"success": True, "message": "Daily Attendnace Date is not correct."})
					response.status_code = 200
					return response

				# Check if request's record is existed
				with connection.cursor() as cursor:
					cursor.execute("insert his_dly_plan_del select getdate(), %s, 'DLY_PLAN', * from dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [username, cnt_id, emp_id, dly_date, shift_id])
					cursor.execute("delete dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [cnt_id, emp_id, dly_date, shift_id])
					cursor.execute("select * from dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [cnt_id, emp_id, dly_date, shift_id])
					row = cursor.fetchone()
					cursor.close

				if row is None:
					message = "Employee ID " + emp_id + " has been deleted."
				else:
					message = "Cannot delete Employee ID " + emp_id

				response = JsonResponse(data={
					"success": True,	    
					"message": message,
				})
			elif dly_date < today_date:
				message = str(username) + " ไม่มีสิทธิ์ทำรายการ"				

	response = JsonResponse(data={
	    "success": True,	    
	    "message": message,
	})

	# print("message : ", message)
	response.status_code = 200
	return response


	'''
	cus_id = request.GET.get('cus_id').lstrip("0")
	cus_brn = request.GET.get('cus_brn')
	cus_vol = request.GET.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	emp_id = request.GET.get('emp_id')
	dly_date = datetime.datetime.strptime(request.GET.get('dly_date'), '%d/%m/%Y')	
	shift_id = request.GET.get('shift_id')
	# username = request.user.first_name
	username = request.user.username

	if cus_id=="" or cus_id is None:
		response = JsonResponse(data={"success": True, "message": "Contract Number is not correct."})
		response.status_code = 200
		return response
	
	if emp_id=="" or cus_id is None:
		response = JsonResponse(data={"success": True, "message": "Employee ID is not correct."})
		response.status_code = 200
		return response

	if dly_date=="" or cus_id is None:
		response = JsonResponse(data={"success": True, "message": "Daily Attendnace Date is not correct."})
		response.status_code = 200
		return response

	# Check if request's record is existed
	with connection.cursor() as cursor:
		cursor.execute("insert his_dly_plan_del select getdate(), %s, 'DLY_PLAN', * from dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [username, cnt_id, emp_id, dly_date, shift_id])
		cursor.execute("delete dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [cnt_id, emp_id, dly_date, shift_id])
		cursor.execute("select * from dly_plan where cnt_id=%s and emp_id=%s and dly_date=%s and sch_shift=%s", [cnt_id, emp_id, dly_date, shift_id])
		row = cursor.fetchone()
		cursor.close

	if row is None:
		message = "Employee ID " + emp_id + " has been deleted."
	else:
		message = "Cannot delete Employee ID " + emp_id

	response = JsonResponse(data={
	    "success": True,	    
	    "message": message,
	})

	response.status_code = 200
	return response
	'''

def get_DLY_PLAN_OR_HIS_DLY_PLAN(dly_date):
	table_name = "DLY_PLAN"
	is_error_status = False
	error_message = "Success"

	# print("dly_date:", dly_date)
	sql = "select end_chk from t_date where date_chk='" + str(dly_date) + "'"
	cursor = connection.cursor()	
	cursor.execute(sql)	
	t_date_obj = cursor.fetchone()
	cursor.close()
	if t_date_obj is not None:		
		end_chk = t_date_obj[0]
		if end_chk==1:
			table_name = "HIS_DLY_PLAN"
	else:
		is_error_status = True
		error_message = "ตารางแจ้งเวรของวันที่ <b>" + str(dly_date) + "</b> ไม่มีในระบบ"
	return is_error_status, error_message, table_name


def addRecord_cross_site(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,
	ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,
	remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,
	allowZeroBathForPhoneAmount,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id,Tday7,Tdof,customer_wage_rate_id,customer_zone_id,Timecross):

	# print("customer_wage_rate_id : ", customer_wage_rate_id)
	# return False

	# print("Tot_hr_amt = ", Timecross)	
	# return False, Timecross

	is_pass = True
	message = ""	

	Tday7tmp = 0
	Tdoftmp = 0
	ui_ot_status = 0
	shift_type = shift_name.partition("#")[2][0:2].strip() # shift_type will be D or N or O
	string_today_date = str(settings.TODAY_DATE.strftime("%d/%m/%Y"))
	today_date = datetime.datetime.strptime(string_today_date, "%d/%m/%Y")


	# Rule 1 No person not more than contract
	# **************** START ******************
	is_error_status, error_message, table_name = get_DLY_PLAN_OR_HIS_DLY_PLAN(dly_date)	
	if is_error_status:
		return False, error_message
	else:
		sql = "select cnt_id,sch_shift from " + str(table_name)

	'''
	if dly_date > today_date.date():
		return False, "เลือกวันที่ไม่ถูกต้อง"
	if dly_date == today_date.date():
		sql = "select cnt_id,sch_shift from DLY_PLAN "
	if dly_date < today_date.date():
		sql = "select cnt_id,sch_shift from HIS_DLY_PLAN "
	'''
	
	sql += " where cnt_id=" + str(cnt_id)
	sql += " and sch_shift=" + str(shift_id)
	sql += " and absent=0 and dly_date='" + str(dly_date) + "'"
	cursor = connection.cursor()	
	cursor.execute(sql)	
	record_count = cursor.fetchall()
	cursor.close()
	informno = len(record_count) if len(record_count)>0 else 0

	sql = "select cnt_id, srv_shif_id, sum(srv_qty) as qty from cus_service where srv_active=1 and cnt_id=" + str(cnt_id) + " and srv_shif_id=" + str(shift_id) + " group by cnt_id, srv_shif_id"
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchone()
	cursor.close
	srv_qty = rows[2]

	if informno >= srv_qty:
		return False, "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา: <b>" + str(cnt_id) + "</b>"
	# **************** END ******************

	# Rule 2 Check Manpower
	# ****** START *********
	shift = shift_name.partition("#")[2][0:2].strip()
	job = job_type

	if dly_date > today_date.date():
		return False, "เลือกวันที่ไม่ถูกต้อง"

	if dly_date == today_date.date():
		sql = "select cnt_id,sch_shift from v_dlyplan_shift "
	else:
		sql = "select cnt_id,sch_shift from v_dlyplan_shift "
	sql += " where cnt_id=" + str(cnt_id)
	sql += " and left(remark,2)=" + str(job)
	sql += " and shf_type='" + str(shift) + "'"
	sql += " and absent=0 and dly_date='" + str(dly_date) + "'"
	cursor = connection.cursor()	
	cursor.execute(sql)	
	record_count = cursor.fetchall()
	cursor.close()
	amanpower = len(record_count) if len(record_count)>0 else 0	

	# return False, "Check Manpower is passed"

	# Rule 3 ChkValidInput(2)
	# ****** START **********

	is_pass, message = chkValidInput(2,dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,
		shift_name,ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,
		relief_emp_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,
		totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount,ui_ot_status,late_from,
		late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id)

	if is_pass:
		message = "PASS"
	else:
		return False, message
	# ******* END ***********	
	
	# return False, "debug111"

	# Call SetVariable("DLY_PLAN")
	Tsch_no = 0
	Temp_id = 0 if emp_id=="" else emp_id
	Tdly_date = None if dly_date=="" else dly_date
	Tsch_shift = 0 if shift_id=="" else shift_id
	Tcnt_id = 0 if cnt_id=="" else cnt_id
	
	if search_emp_id=="":
		print("Tdept_id = ใช้โซนของหน่วยงาน")
		# TODO: เลือกว่าจะใช้ค่าโซนของพนักงานหรือหน่วยงาน
		Tdept_id = emp_dept
	else:
		print("Tdept_id = ใช้โซนของพนักงาน")
		Tdept_id = emp_dept

	Tsch_rank = emp_rank
	Tabsent = ui_absent_status
	Tlate = ui_late_status
	Tlate_full = late_full_paid_status
	Trelief = ui_relief_status
	Trelief_id = '0' if relief_emp_id=="" else relief_emp_id
	
	# return False, Trelief_id

	# TELEPHONE
	if ui_phone_status==1:
		if tel_time=="":
			Ttel_time = None
		else:
			Ttel_time = datetime.datetime.strptime(tel_time, '%d/%m/%Y %H:%M')
		Ttel_amt = 0 if tel_amount=="" else tel_amount
		Ttel_paid = 5 if Ttel_amt > 5 else Ttel_amt
	else:
		Ttel_time = None
		Ttel_amt = 0
		Ttel_paid = 0

	
	# OVERTIME
	Tot = 0 if ui_ot_status==0 else 1
	if (Tot==1) or (Tlate==1):

		ot_reason = late_reason_option
		ot_time_frm = late_from
		ot_time_to = late_to

		Tot_reason = ot_reason
		Tot_time_frm = ot_time_frm
		Tot_time_to = ot_time_to
		# TODO: Tot_hr_amt
		Tot_hr_amt = float(late_hour)
		Tot_pay_amt = 0
		if Tot==1:
			Tpay_type = "BAS"
		elif Tlate==1:
			Tpay_type = "TPB"
	else:
		Tot_reason = 0
		Tot_time_frm = None
		Tot_time_to = None
		Tot_hr_amt = 0
		Tot_pay_amt = 0
		Tpay_type = ""			
	

	# Add by Somkiat 2016/02/24
	#TODO: หาค่า Rea_timecross เซ็ทเริ่มต้นมาจากที่ไหน
	'''
	Rea_timecross = 0
	if Rea_timecross==57:
		Tot_reason = 57
		Tot_time_frm = None
		Tot_time_to = None
		Tot_hr_amt = Rea_timecross
		Tot_pay_amt = 0
		Tpay_type = "TPB"			
	'''
	
	# return False, "debug"
	Rea_timecross = 57
	Tot_time_frm = None
	Tot_time_to = None
	Tot_hr_amt = int(Timecross)
	Tot_pay_amt = 0
	Tpay_type = "TPB"
	Tsoc = 1 if int(Tot_hr_amt) >= 8 else 0



	#TODO: หาค่า txtSpare มีการเซ็ทค่าเริ่มต้นมาจากที่ไหน
	txtSpare = 0
	Tspare = txtSpare
	
	#TODO: ส่งค่า wage_id จาก Customer Tab
	# wage_id = 32
	wage_id = customer_wage_rate_id

	Twage_id = wage_id
	Twage_no = str(Twage_id) + str(emp_rank)
	Tpay_type = 1 if ui_ot_status==1 else ""
	Tsoc = 1 if Tot_hr_amt>=8 else 0
	TRemark = job_type + " " + remark

	# Get Period
	try:
		Tprd_id = TPeriod.objects.filter(prd_date_frm__lte=dly_date).filter(prd_date_to__gte=dly_date).filter(emp_type='D1').get()
		Tprd_id = Tprd_id.prd_id
	except TPeriod.DoesNotExist:
		Tprd_id = ""
	
	# Check Tpub
	if getDayPub(dly_date)==1:
		Tpub = 1
	else:
		Tpub = 0


	# Call AddListName("DLY_PLAN")
	'''
	if dly_date == today_date.date():
		sql = "insert into DLY_PLAN "
	else:
		if username == "CMS_SUP":
			sql = "insert into HIS_DLY_PLAN "
		else:
			return False, "You don't have a permission to Add/Edit passed date."
	'''



	# ****************************
	# Call TotalMissGuard
	# ****************************
	# START
	'''
	totalNDP = int(request.GET.get('totalNDP'))
	totalNDA = int(request.GET.get('totalNDA'))
	totalNDM = int(request.GET.get('totalNDM'))
	totalNNP = int(request.GET.get('totalNNP'))
	totalNNA = int(request.GET.get('totalNNA'))
	totalNNM = int(request.GET.get('totalNNM'))
	totalPDP = int(request.GET.get('totalPDP'))
	totalPDA = int(request.GET.get('totalPDA'))
	totalPDM = int(request.GET.get('totalPDM'))
	totalPNP = int(request.GET.get('totalPNP'))
	totalPNA = int(request.GET.get('totalPNA'))
	totalPNM = int(request.GET.get('totalPNM'))	
	'''

	is_public_holiday, message = isPublicHoliday(dly_date)
	if is_public_holiday:
		Tpub = 1
	else:
		Tpub = 0

	DN = None
	print(shift_id)
	if (shift_id == "99" or shift_id == "999"):
		print("DN=DAY OFF/ANOTHER SITE")		
	else:
		DN = shift_name.split("#")[1].strip()[0:1]
		print("DN=", DN.strip())

	if DN is not None:
		if DN=="D":
			print("DAY")			
			if Tpub == 0:
				totalNDA = totalNDA + 1
			else:
				totalPDA = totalPDA + 1
		else:
			print("NIGHT")
			if Tpub == 0:
				totalNNA = totalNNA + 1
			else:
				totalPNA = totalPNA + 1
	else:
		print("DN is None")

	lblNDM = totalNDA - totalNDP
	lblNNM = totalNNA - totalNNP
	lblPDM = totalPDA - totalPDP
	lblPNM = totalPNA - totalPNP

	print(str(lblNDM) + " | " + str(lblNNM) + " | " + str(lblPDM) + " | " + str(lblPNM))
	if Tpub == 0:
		if lblNDM > 0:
			return False, "จำนวน รปภ.ในกะกลางวันเกินกว่าที่ระบุในสัญญา"

		if lblNNM > 0:
			return False, "จำนวน รปภ.ในกะกลางคืนเกินกว่าที่ระบุในสัญญา"
	else:
		if lblPDM > 0:
			return False, "จำนวน รปภ.ในกะกลางวันเกินกว่าที่ระบุในสัญญา"

		if lblPNM > 0:
			return False, "จำนวน รปภ.ในกะกลางคืนเกินกว่าที่ระบุในสัญญา"

	'''
	print(totalNDA)
	print(totalNDP)
	print(totalNNA)
	print(totalNNP)
	print(totalPDA)
	print(totalPDP)
	print(totalPNA)
	print(totalPNP)
	'''
	# END


	# return False, "debug"	
	is_error_status, error_message, table_name = get_DLY_PLAN_OR_HIS_DLY_PLAN(dly_date)
	if is_error_status:
		return False, error_message
	else:
		if table_name=="DLY_PLAN":
			sql = "insert into DLY_PLAN "
		else:			
			if username == "CMS_SUP":
				sql = "insert into HIS_DLY_PLAN "
			else:
				return False, "You don't have a permission to Add/Edit passed date."

	sql += "(cnt_id,emp_id,dly_date,sch_shift"
	sql += ",sch_no,dept_id,sch_rank,prd_id"
	sql += ",absent,late,late_full,relieft,relieft_id"
	sql += ",tel_man,tel_time,tel_amt,tel_paid"
	sql += ",ot,ot_reason,ot_time_frm,ot_time_to,ot_hr_amt,ot_pay_amt"
	sql += ",spare,wage_id,wage_no,pay_type,soc,pub,dof,day7"
	sql += ",upd_date,upd_by,upd_flag,remark)"
	sql += " values ("			
	sql += str(cnt_id) + "," + str(emp_id) + ",'" + str(dly_date) + "'," + str(Tsch_shift) + ","
	sql += str(Tsch_no) + "," + str(Tdept_id) + ",'" + str(Tsch_rank) + "','" + str(Tprd_id) + "',"
	sql += str(Tabsent) + "," + str(Tlate) + "," + str(Tlate_full) + "," + str(Trelief) + "," + str(Trelief_id) + ","
	sql += str(ui_phone_status) + "," 

	if (Ttel_time is None) or (Ttel_time==""):
		sql += "null,"			
	else:
		sql += "'" + str(Ttel_time) + "',"

	sql += str(Ttel_amt) + "," + str(Ttel_paid) + ","
	sql += str(Tot) + "," + str(Rea_timecross) + "," 

	if Tot_time_frm is None:
		sql += "null,"
	else:
		sql += " '" + str(Tot_time_frm) + "',"

	if Tot_time_to is None:
		sql += "null,"
	else:
		sql += " '" + str(Tot_time_to) + "',"

	sql += str(Tot_hr_amt) + "," + str(Tot_pay_amt) + ","

	sql += str(Tspare) + "," + str(Twage_id) + ",'" + str(Twage_no) + "','" + str(Tpay_type) + "'," + str(Tsoc) + "," + str(Tpub) + "," + str(Tdof) + "," + str(Tday7) + ",'"
	sql += str(str(datetime.datetime.now())[:-3]) + "','" + str(username) + "'," + "'A'" + ",'" + remark + "')"	
	
	# print("DEBUG sql: ", sql)
	# return False, "debug3"
	# return True, "TEST"

	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
		is_pass = True
		message = "รับแจ้งเวรสำเร็จ"
	except db.OperationalError as e:
		is_pass = False
		message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
	except db.Error as e:
		is_pass = False
		message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)

	return is_pass, message


	# return False, "debug"





	is_error, message = checkManPower(cnt_id, job_type, shift_type, dly_date)
	if is_error:
		is_pass = False
		message = "Rule 3 is failed."
		print(message)
		return False, 
	else:
		is_pass = True
		message = "Rule 3 is passed."
		print(message)

		is_pass = True	
	# ****** END *********


	# return True, "PASS"
	# return False, "debug"

	if shift_id!="99":
		# ************************************************
		# RULE 1 - ดักจับในกรณีที่ cnt_id มากกว่า 10 หลัก
		# ************************************************		
		if len(cnt_id) > 10:
			is_pass = False		
			message = "Rule 1 is failed."
			print(message)
		else:			
			is_pass = True
			message = "Rule 1 is passed."
			print(message)


		# ************************************************
		# RULE 2 - เช็คพนักงานที่แจ้งเวรต้องไม่เกินจำนวนที่ว่าจ้างในสัญญา
		# ************************************************		
		if is_pass:
			is_not_error, message = checkNotOverCapacity(cnt_id, shift_id, dly_date)
			if is_not_error:				
				is_pass = True
				message = "Rule 2 is passed."
				print(message)
			else:
				is_pass = False
				# message = "Rule 2 is failed."
				# print(message)


		# *****************************************
		# RULE 3 - Check Manpower
		# *****************************************
		if is_pass:
			shift_type = shift_name.partition("#")[2][0:2].strip()
			is_error, message = checkManPower(cnt_id, job_type, shift_type, dly_date)
			if is_error:
				is_pass = False
				message = "Rule 3 is failed."
				print(message)					
			else:
				is_pass = True
				message = "Rule 3 is passed."
				print(message)

			is_pass = True


		# *****************************************
		# RULE 4 - Validate all input
		# *****************************************				
		# return False, "debug"
		if is_pass:
			is_not_error, message = validateInput(dly_date, cnt_id, emp_id, shift_id, shift_type, shift_name, job_type, totalNDP, totalNDA, totalNDM, totalNNP, totalNNA, totalNNM, totalPDP, totalPDA, totalPDM, totalPNP, totalPNA, totalPNM, absent_status, late_status, phone_status, relief_status)
			if is_not_error:
				is_pass = True
				# message = "Rule 4 is passed."
				message = "รับแจ้งเวรสำเร็จ"
				print(message)							
			else:
				is_pass = False
				# message = "Rule 4 is failed."
				print(message)


		# *****************************************
		# RULE ? - New rule
		# *****************************************		
		# New rule will be added here.


		# Note: If all rules are passed, then it's ready to add.
		if is_pass:
			'''
			dly_date, cnt_id, emp_id, shift_id, shift_type, job_type, totalNDP, 
			totalNDA, totalNDM, totalNNP, totalNNA, totalNNM, totalPDP, totalPDA, 
			totalPDM, totalPNP, totalPNA, totalPNM, absent_status, late_status, 
			phone_status, relief_status
			'''

			# upd_date = str(datetime.datetime.now())
			upd_date = str(datetime.datetime.now())[:-3]
			remark = str(job_type) + " " + str(remark)

			sql = "insert into dly_plan (cnt_id,emp_id,dly_date,sch_shift"
			sql += ",sch_no,dept_id,sch_rank,prd_id"
			sql += ",absent,late,late_full,relieft,relieft_id"
			sql += ",tel_man,tel_time,tel_amt,tel_paid"
			sql += ",ot,ot_reason,ot_time_frm,ot_time_to,ot_hr_amt,ot_pay_amt"
			sql += ",spare,wage_id,wage_no,pay_type,soc,pub,dof,day7"
			sql += ",upd_date,upd_by,upd_flag,remark)"
			sql += " values ("			
			sql += str(cnt_id) + "," + str(emp_id) + ",'" + str(dly_date) + "'," + str(shift_id) + ","
			sql += "0" + "," + emp_dept + ",'" + str(emp_rank) + "'," + "'D120121'" + ","
			sql += "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + ","
			sql += "0" + "," + "NULL" + "," + "0" + "," + "0" + ","
			sql += "0" + "," + "0" + "," + "NULL" + "," + "NULL" + "," + "0" + "," + "0" + ","
			
			# sql += "0" + "," + "32" + "," + "'32SOY'" + "," + "NULL" + "," + "0" + "," + "0" + "," + "1" + "," + "NULL" + ",'"
			sql += "0" + "," + str(customer_wage_rate_id) + "," + "'32SOY'" + "," + "NULL" + "," + "0" + "," + "0" + "," + "1" + "," + "NULL" + ",'"
			

			sql += str(upd_date) + "'," + str(username) + "," + "'A'" + ",'" + remark + "')"
			# print(sql)

			try:
				with connection.cursor() as cursor:
					cursor.execute(sql)

				is_pass = True
				# message = "บันทึกข้อมูลสำเร็จ"
				# message = "บันทึกรายการแจ้งเวรสำเร็จ"
			except db.OperationalError as e:
				is_pass = False
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
			except db.Error as e:
				is_pass = False
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
	else:
		is_pass = False
		message = "Shift ID is 99 - Day Off"

	return is_pass, message


def addRecord(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,
	ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,
	remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,
	allowZeroBathForPhoneAmount,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id,Tday7,Tdof,customer_wage_rate_id,customer_zone_id):
	
	# return False, "debug"

	is_pass = True
	message = ""	

	Tday7tmp = 0
	Tdoftmp = 0
	ui_ot_status = 0
	shift_type = shift_name.partition("#")[2][0:2].strip() # shift_type will be D or N or O
	string_today_date = str(settings.TODAY_DATE.strftime("%d/%m/%Y"))
	today_date = datetime.datetime.strptime(string_today_date, "%d/%m/%Y")


	# Rule 1 No person not more than contract
	# **************** START ******************
	is_error_status, error_message, table_name = get_DLY_PLAN_OR_HIS_DLY_PLAN(dly_date)	
	if is_error_status:
		return False, error_message
	else:
		sql = "select cnt_id,sch_shift from " + str(table_name)

	'''
	if dly_date > today_date.date():
		return False, "เลือกวันที่ไม่ถูกต้อง"
	if dly_date == today_date.date():
		sql = "select cnt_id,sch_shift from DLY_PLAN "
	if dly_date < today_date.date():
		sql = "select cnt_id,sch_shift from HIS_DLY_PLAN "
	'''
	
	sql += " where cnt_id=" + str(cnt_id)
	sql += " and sch_shift=" + str(shift_id)
	sql += " and absent=0 and dly_date='" + str(dly_date) + "'"
	cursor = connection.cursor()	
	cursor.execute(sql)	
	record_count = cursor.fetchall()
	cursor.close()
	informno = len(record_count) if len(record_count)>0 else 0

	sql = "select cnt_id, srv_shif_id, sum(srv_qty) as qty from cus_service where srv_active=1 and cnt_id=" + str(cnt_id) + " and srv_shif_id=" + str(shift_id) + " group by cnt_id, srv_shif_id"
	print("SQL : ", sql)

	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchone()
	cursor.close
	srv_qty = rows[2]

	if informno >= srv_qty:
		return False, "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา: <b>" + str(cnt_id) + "</b>"
	# **************** END ******************

	# Rule 2 Check Manpower
	# ****** START *********
	shift = shift_name.partition("#")[2][0:2].strip()
	job = job_type

	if dly_date > today_date.date():
		return False, "เลือกวันที่ไม่ถูกต้อง"

	if dly_date == today_date.date():
		sql = "select cnt_id,sch_shift from v_dlyplan_shift "
	else:
		sql = "select cnt_id,sch_shift from v_dlyplan_shift "
	sql += " where cnt_id=" + str(cnt_id)
	sql += " and left(remark,2)=" + str(job)
	sql += " and shf_type='" + str(shift) + "'"
	sql += " and absent=0 and dly_date='" + str(dly_date) + "'"
	cursor = connection.cursor()	
	cursor.execute(sql)	
	record_count = cursor.fetchall()
	cursor.close()
	amanpower = len(record_count) if len(record_count)>0 else 0	

	# return False, "Check Manpower is passed"

	# Rule 3 ChkValidInput(2)
	# ****** START **********

	is_pass, message = chkValidInput(2,dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,
		shift_name,ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,
		relief_emp_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,
		totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount,ui_ot_status,late_from,
		late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id)

	if is_pass:
		message = "PASS"
	else:
		return False, message
	# ******* END ***********	
	
	# return False, "debug111"

	# Call SetVariable("DLY_PLAN")
	Tsch_no = 0
	Temp_id = 0 if emp_id=="" else emp_id
	Tdly_date = None if dly_date=="" else dly_date
	Tsch_shift = 0 if shift_id=="" else shift_id
	Tcnt_id = 0 if cnt_id=="" else cnt_id
	
	if search_emp_id=="":
		print("Tdept_id = ใช้โซนของหน่วยงาน")
		# TODO: เลือกว่าจะใช้ค่าโซนของพนักงานหรือหน่วยงาน
		Tdept_id = emp_dept
	else:
		print("Tdept_id = ใช้โซนของพนักงาน")
		Tdept_id = emp_dept

	Tsch_rank = emp_rank
	Tabsent = ui_absent_status
	Tlate = ui_late_status
	Tlate_full = late_full_paid_status
	Trelief = ui_relief_status
	Trelief_id = '0' if relief_emp_id=="" else relief_emp_id
	
	# return False, Trelief_id

	# TELEPHONE
	if ui_phone_status==1:
		if tel_time=="":
			Ttel_time = None
		else:
			Ttel_time = datetime.datetime.strptime(tel_time, '%d/%m/%Y %H:%M')
		Ttel_amt = 0 if tel_amount=="" else tel_amount
		Ttel_paid = 5 if Ttel_amt > 5 else Ttel_amt
	else:
		Ttel_time = None
		Ttel_amt = 0
		Ttel_paid = 0

	
	# OVERTIME
	Tot = 0 if ui_ot_status==0 else 1
	if (Tot==1) or (Tlate==1):

		ot_reason = late_reason_option
		ot_time_frm = late_from
		ot_time_to = late_to

		Tot_reason = ot_reason
		Tot_time_frm = ot_time_frm
		Tot_time_to = ot_time_to
		# TODO: Tot_hr_amt
		Tot_hr_amt = float(late_hour)
		Tot_pay_amt = 0
		if Tot==1:
			Tpay_type = "BAS"
		elif Tlate==1:
			Tpay_type = "TPB"
	else:
		Tot_reason = 0
		Tot_time_frm = None
		Tot_time_to = None
		Tot_hr_amt = 0
		Tot_pay_amt = 0
		Tpay_type = ""			
	

	# Add by Somkiat 2016/02/24
	#TODO: หาค่า Rea_timecross เซ็ทเริ่มต้นมาจากที่ไหน
	Rea_timecross = 0
	if Rea_timecross==57:
		Tot_reason = 57
		Tot_time_frm = None
		Tot_time_to = None
		Tot_hr_amt = Rea_timecross
		Tot_pay_amt = 0
		Tpay_type = "TPB"			

	#TODO: หาค่า txtSpare มีการเซ็ทค่าเริ่มต้นมาจากที่ไหน
	txtSpare = 0
	Tspare = txtSpare
	
	#TODO: ส่งค่า wage_id จาก Customer Tab
	# wage_id = 32
	wage_id = customer_wage_rate_id

	Twage_id = wage_id
	Twage_no = str(Twage_id) + str(emp_rank)
	Tpay_type = 1 if ui_ot_status==1 else ""
	Tsoc = 1 if Tot_hr_amt>=8 else 0
	TRemark = job_type + " " + remark

	# Get Period
	try:
		Tprd_id = TPeriod.objects.filter(prd_date_frm__lte=dly_date).filter(prd_date_to__gte=dly_date).filter(emp_type='D1').get()
		Tprd_id = Tprd_id.prd_id
	except TPeriod.DoesNotExist:
		Tprd_id = ""
	
	# Check Tpub
	if getDayPub(dly_date)==1:
		Tpub = 1
	else:
		Tpub = 0


	# Call AddListName("DLY_PLAN")
	'''
	if dly_date == today_date.date():
		sql = "insert into DLY_PLAN "
	else:
		if username == "CMS_SUP":
			sql = "insert into HIS_DLY_PLAN "
		else:
			return False, "You don't have a permission to Add/Edit passed date."
	'''



	# ****************************
	# Call TotalMissGuard
	# ****************************
	# START
	'''
	totalNDP = int(request.GET.get('totalNDP'))
	totalNDA = int(request.GET.get('totalNDA'))
	totalNDM = int(request.GET.get('totalNDM'))
	totalNNP = int(request.GET.get('totalNNP'))
	totalNNA = int(request.GET.get('totalNNA'))
	totalNNM = int(request.GET.get('totalNNM'))
	totalPDP = int(request.GET.get('totalPDP'))
	totalPDA = int(request.GET.get('totalPDA'))
	totalPDM = int(request.GET.get('totalPDM'))
	totalPNP = int(request.GET.get('totalPNP'))
	totalPNA = int(request.GET.get('totalPNA'))
	totalPNM = int(request.GET.get('totalPNM'))	
	'''

	is_public_holiday, message = isPublicHoliday(dly_date)
	if is_public_holiday:
		Tpub = 1
	else:
		Tpub = 0

	DN = None
	print(shift_id)
	if (shift_id == "99" or shift_id == "999"):
		print("DN=DAY OFF/ANOTHER SITE")		
	else:
		DN = shift_name.split("#")[1].strip()[0:1]
		print("DN=", DN.strip())

	if DN is not None:
		if DN=="D":
			print("DAY")			
			if Tpub == 0:
				totalNDA = totalNDA + 1
			else:
				totalPDA = totalPDA + 1
		else:
			print("NIGHT")
			if Tpub == 0:
				totalNNA = totalNNA + 1
			else:
				totalPNA = totalPNA + 1
	else:
		print("DN is None")

	lblNDM = totalNDA - totalNDP
	lblNNM = totalNNA - totalNNP
	lblPDM = totalPDA - totalPDP
	lblPNM = totalPNA - totalPNP

	print(str(lblNDM) + " | " + str(lblNNM) + " | " + str(lblPDM) + " | " + str(lblPNM))
	if Tpub == 0:
		if lblNDM > 0:
			return False, "จำนวน รปภ.ในกะกลางวันเกินกว่าที่ระบุในสัญญา"

		if lblNNM > 0:
			return False, "จำนวน รปภ.ในกะกลางคืนเกินกว่าที่ระบุในสัญญา"
	else:
		if lblPDM > 0:
			return False, "จำนวน รปภ.ในกะกลางวันเกินกว่าที่ระบุในสัญญา"

		if lblPNM > 0:
			return False, "จำนวน รปภ.ในกะกลางคืนเกินกว่าที่ระบุในสัญญา"

	'''
	print(totalNDA)
	print(totalNDP)
	print(totalNNA)
	print(totalNNP)
	print(totalPDA)
	print(totalPDP)
	print(totalPNA)
	print(totalPNP)
	'''
	# END


	# return False, "debug"	
	is_error_status, error_message, table_name = get_DLY_PLAN_OR_HIS_DLY_PLAN(dly_date)
	if is_error_status:
		return False, error_message
	else:
		if table_name=="DLY_PLAN":
			sql = "insert into DLY_PLAN "
		else:			
			if username == "CMS_SUP":
				sql = "insert into HIS_DLY_PLAN "
			else:
				return False, "You don't have a permission to Add/Edit passed date."

	sql += "(cnt_id,emp_id,dly_date,sch_shift"
	sql += ",sch_no,dept_id,sch_rank,prd_id"
	sql += ",absent,late,late_full,relieft,relieft_id"
	sql += ",tel_man,tel_time,tel_amt,tel_paid"
	sql += ",ot,ot_reason,ot_time_frm,ot_time_to,ot_hr_amt,ot_pay_amt"
	sql += ",spare,wage_id,wage_no,pay_type,soc,pub,dof,day7"
	sql += ",upd_date,upd_by,upd_flag,remark)"
	sql += " values ("			
	sql += str(cnt_id) + "," + str(emp_id) + ",'" + str(dly_date) + "'," + str(Tsch_shift) + ","
	sql += str(Tsch_no) + "," + str(Tdept_id) + ",'" + str(Tsch_rank) + "','" + str(Tprd_id) + "',"
	sql += str(Tabsent) + "," + str(Tlate) + "," + str(Tlate_full) + "," + str(Trelief) + "," + str(Trelief_id) + ","
	sql += str(ui_phone_status) + "," 

	if (Ttel_time is None) or (Ttel_time==""):
		sql += "null,"			
	else:
		sql += "'" + str(Ttel_time) + "',"

	sql += str(Ttel_amt) + "," + str(Ttel_paid) + ","
	sql += str(Tot) + "," + str(Tot_reason) + "," 

	if Tot_time_frm is None:
		sql += "null,"
	else:
		sql += " '" + str(Tot_time_frm) + "',"

	if Tot_time_to is None:
		sql += "null,"
	else:
		sql += " '" + str(Tot_time_to) + "',"

	sql += str(Tot_hr_amt) + "," + str(Tot_pay_amt) + ","

	sql += str(Tspare) + "," + str(Twage_id) + ",'" + str(Twage_no) + "','" + str(Tpay_type) + "'," + str(Tsoc) + "," + str(Tpub) + "," + str(Tdof) + "," + str(Tday7) + ",'"
	sql += str(str(datetime.datetime.now())[:-3]) + "','" + str(username) + "'," + "'A'" + ",'" + remark + "')"	

	
	print("DEBUG sql: ", sql)
	# return False, "debug3"

	# return True, "TEST"

	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
		is_pass = True
		message = "รับแจ้งเวรสำเร็จ"
	except db.OperationalError as e:
		is_pass = False
		message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
	except db.Error as e:
		is_pass = False
		message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)

	return is_pass, message


	# return False, "debug"





	is_error, message = checkManPower(cnt_id, job_type, shift_type, dly_date)
	if is_error:
		is_pass = False
		message = "Rule 3 is failed."
		print(message)
		return False, 
	else:
		is_pass = True
		message = "Rule 3 is passed."
		print(message)

		is_pass = True	
	# ****** END *********


	# return True, "PASS"
	# return False, "debug"

	if shift_id!="99":
		# ************************************************
		# RULE 1 - ดักจับในกรณีที่ cnt_id มากกว่า 10 หลัก
		# ************************************************		
		if len(cnt_id) > 10:
			is_pass = False		
			message = "Rule 1 is failed."
			print(message)
		else:			
			is_pass = True
			message = "Rule 1 is passed."
			print(message)


		# ************************************************
		# RULE 2 - เช็คพนักงานที่แจ้งเวรต้องไม่เกินจำนวนที่ว่าจ้างในสัญญา
		# ************************************************		
		if is_pass:
			is_not_error, message = checkNotOverCapacity(cnt_id, shift_id, dly_date)
			if is_not_error:				
				is_pass = True
				message = "Rule 2 is passed."
				print(message)
			else:
				is_pass = False
				# message = "Rule 2 is failed."
				# print(message)


		# *****************************************
		# RULE 3 - Check Manpower
		# *****************************************
		if is_pass:
			shift_type = shift_name.partition("#")[2][0:2].strip()
			is_error, message = checkManPower(cnt_id, job_type, shift_type, dly_date)
			if is_error:
				is_pass = False
				message = "Rule 3 is failed."
				print(message)					
			else:
				is_pass = True
				message = "Rule 3 is passed."
				print(message)

			is_pass = True


		# *****************************************
		# RULE 4 - Validate all input
		# *****************************************				
		# return False, "debug"
		if is_pass:
			is_not_error, message = validateInput(dly_date, cnt_id, emp_id, shift_id, shift_type, shift_name, job_type, totalNDP, totalNDA, totalNDM, totalNNP, totalNNA, totalNNM, totalPDP, totalPDA, totalPDM, totalPNP, totalPNA, totalPNM, absent_status, late_status, phone_status, relief_status)
			if is_not_error:
				is_pass = True
				# message = "Rule 4 is passed."
				message = "รับแจ้งเวรสำเร็จ"
				print(message)							
			else:
				is_pass = False
				# message = "Rule 4 is failed."
				print(message)


		# *****************************************
		# RULE ? - New rule
		# *****************************************		
		# New rule will be added here.


		# Note: If all rules are passed, then it's ready to add.
		if is_pass:
			'''
			dly_date, cnt_id, emp_id, shift_id, shift_type, job_type, totalNDP, 
			totalNDA, totalNDM, totalNNP, totalNNA, totalNNM, totalPDP, totalPDA, 
			totalPDM, totalPNP, totalPNA, totalPNM, absent_status, late_status, 
			phone_status, relief_status
			'''

			# upd_date = str(datetime.datetime.now())
			upd_date = str(datetime.datetime.now())[:-3]
			remark = str(job_type) + " " + str(remark)

			sql = "insert into dly_plan (cnt_id,emp_id,dly_date,sch_shift"
			sql += ",sch_no,dept_id,sch_rank,prd_id"
			sql += ",absent,late,late_full,relieft,relieft_id"
			sql += ",tel_man,tel_time,tel_amt,tel_paid"
			sql += ",ot,ot_reason,ot_time_frm,ot_time_to,ot_hr_amt,ot_pay_amt"
			sql += ",spare,wage_id,wage_no,pay_type,soc,pub,dof,day7"
			sql += ",upd_date,upd_by,upd_flag,remark)"
			sql += " values ("			
			sql += str(cnt_id) + "," + str(emp_id) + ",'" + str(dly_date) + "'," + str(shift_id) + ","
			sql += "0" + "," + emp_dept + ",'" + str(emp_rank) + "'," + "'D120121'" + ","
			sql += "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + ","
			sql += "0" + "," + "NULL" + "," + "0" + "," + "0" + ","
			sql += "0" + "," + "0" + "," + "NULL" + "," + "NULL" + "," + "0" + "," + "0" + ","
			
			# sql += "0" + "," + "32" + "," + "'32SOY'" + "," + "NULL" + "," + "0" + "," + "0" + "," + "1" + "," + "NULL" + ",'"
			sql += "0" + "," + str(customer_wage_rate_id) + "," + "'32SOY'" + "," + "NULL" + "," + "0" + "," + "0" + "," + "1" + "," + "NULL" + ",'"
			

			sql += str(upd_date) + "'," + str(username) + "," + "'A'" + ",'" + remark + "')"
			# print(sql)

			try:
				with connection.cursor() as cursor:
					cursor.execute(sql)

				is_pass = True
				# message = "บันทึกข้อมูลสำเร็จ"
				# message = "บันทึกรายการแจ้งเวรสำเร็จ"
			except db.OperationalError as e:
				is_pass = False
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
			except db.Error as e:
				is_pass = False
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
	else:
		is_pass = False
		message = "Shift ID is 99 - Day Off"

	return is_pass, message


def editRecord(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,ui_absent_status,
	ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,remark,
	totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,
	allowZeroBathForPhoneAmount,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id,Tday7,
	Tdof,customer_wage_rate_id,customer_zone_id):

	# return False, "TODO"

	# print("tel_time BBBB:", tel_time)

	# message = str(late_from) + " | " + str(late_to) + " | " + str(late_hour) + " | " + str(job_type)
	# return False, message

	# set hardcode value
	ui_ot_status = 0

	#                                                          
	# set default value
	Tday7tmp = 0
	Tdoftmp = 0
	shift_type = shift_name.partition("#")[2][0:2].strip() # shift_type will be D or N or O
	# job_type - get from parameter

	# CheckNoSpare
	#TODO: check chkAbsent, chkLate, chkOT, chkCall
	if (ui_absent_status==0) and (ui_late_status==0) and (ui_ot_status==0) and (ui_phone_status==0):
		CheckNoSpare = True
	else:
		CheckNoSpare = False

	# RULE 1 - Check Manpower
	string_today_date = str(settings.TODAY_DATE.strftime("%d/%m/%Y"))
	today_date = datetime.datetime.strptime(string_today_date, "%d/%m/%Y")

	if dly_date == today_date.date():
		sql = "select count(*) from v_dlyplan_shift "

	if dly_date < today_date.date():
		sql = "select count(*) from v_dlyplan_shift "

	# sql += "where cnt_id=" + str(cnt_id) + " and left(remark, 2)=" + str(job_type) + " and shf_type='" + shift_type + "'" + " and absent=0 and dly_date='" + str(dly_date) + "'"
	sql += "where cnt_id=" + str(cnt_id) + " and shf_type='" + shift_type + "'" + " and absent=0 and dly_date='" + str(dly_date) + "'"

	cursor = connection.cursor()	
	cursor.execute(sql)	
	record_count = cursor.fetchone()
	cursor.close()
	AmanPower = 0 if record_count[0] == 0 else record_count[0]

	# Check #4 - To check No person not more than contract
	'''
	if dly_date == today_date.date():
		sql = "select cnt_id,emp_id,absent,late,tel_man,relieft from dly_plan "
	if dly_date < today_date.date():
		sql = "select cnt_id,emp_id,absent,late,tel_man,relieft from his_dly_plan "
	sql += " where cnt_id=" + str(cnt_id) + " and dly_date='" + str(dly_date) + "' and emp_id=" + str(emp_id)
	
	print("sql:", sql)
	return False, "TODO"
	'''	

	# Check #4
	if dly_date == today_date.date():
		sql = "select cnt_id,emp_id,absent,late,tel_man,relieft from dly_plan "

	if dly_date < today_date.date():
		sql = "select cnt_id,emp_id,absent,late,tel_man,relieft from his_dly_plan "	
	# sql = "select cnt_id,emp_id,absent,late,tel_man,relieft from dly_plan "
	sql += " where cnt_id=" + str(cnt_id) + " and sch_shift=" + shift_id + " and dly_date='" + str(dly_date) + "' and emp_id=" + str(emp_id)

	print("SQL debug1:", sql)
	print("DEBUG shift_id : ", shift_id)

	cursor = connection.cursor()	
	cursor.execute(sql)	
	record_count = cursor.fetchone()
	cursor.close()

	# return False, "TODO2"

	if(record_count is not None):
		if len(record_count)>0:
			db_cnt_id = record_count[0]
			db_emp_id = record_count[1]
			db_absent_status = 1 if record_count[2] else 0
			db_late_status = 1 if record_count[3] else 0
			db_phone_status = 1 if record_count[4] else 0
			db_relief_status = 1 if record_count[5] else 0
			# return False, str(db_absent_status) + "," + str(db_late_status) + "," + str(db_phone_status) + "," + str(db_relief_status)
		else:
			return False, "Employee not found"


		'''
		if ui_phone_status==db_phone_status:
			if ui_late_status==db_late_status:
				if (db_absent_status==1) and (db_relief_status==1):
					# TODO
					# return False, "TODO11"
					return True, "Implement Check #4"	
		'''


		# Check #5 - ค่าโทรต้องมีค่ามากกว่า 0 บาท
		if (ui_phone_status==1) and (tel_amount<=0):
			if allowZeroBathForPhoneAmount==0:
				is_pass = False
				message = "ค่าโทรมีค่าเป็น 0 กรุณาตรวจสอบ"
				return is_pass, message


		print("ui_phone_status = ", ui_phone_status)
		print("db_phone_status = ", db_phone_status)

		# return False, "TODO3"

		# Check #6
		if ui_phone_status==db_phone_status:
			if ui_late_status==db_late_status:
				if ui_absent_status==0:
					if shift_id != 99:				
						if dly_date == today_date.date():
							sql = "select count(*) from dly_plan "

						if dly_date < today_date.date():
							sql = "select count(*) from his_dly_plan "

						
						sql += "where cnt_id=" + str(cnt_id) + " and sch_shift=" + str(shift_id) + " and absent=0 and dly_date='" + str(dly_date) + "'"
						# sql += "where cnt_id=" + str(cnt_id) + " and absent=0 and dly_date='" + str(dly_date) + "'"

						print("DEBUG 09 sql: ", sql)
						cursor = connection.cursor()
						cursor.execute(sql)
						rows = cursor.fetchone()
						cursor.close	
						informNo = rows[0] if rows[0]>0 else 0

						# get srv_qty
						sql = "select cnt_id, srv_shif_id, sum(srv_qty) as qty from cus_service where srv_active=1 and cnt_id=" + str(cnt_id) + " and srv_shif_id=" + str(shift_id) + " group by cnt_id, srv_shif_id"
						print("DEBUG 10 sql: ", sql)
						cursor = connection.cursor()
						cursor.execute(sql)
						rows = cursor.fetchone()
						cursor.close
						srv_qty = rows[2]

						print("cnt_id_1 = ", int(rows[0]))
						print("cnt_id_2 = ", int(cnt_id))
						print("informNo = ", informNo)
						print("srv_qty = ", srv_qty)
						print("tel_amount = ", tel_amount)

						if informNo >= srv_qty:
							if(int(rows[0])==int(cnt_id)):
								is_pass = True
								message = ""
							else:
								is_pass = False					
								message = "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา: <b>" + str(cnt_id) + "</b>"

							# return is_pass, message
						else:
							is_pass = True # แจ้งเวรยังไม่เกินจำนวนที่อยู่ในสัญญา
							message = "Check #6 is passed."
		
		
		'''				
		else:
			if ui_absent_status==0:
				if shift_id != 99:				
					if dly_date == today_date.date():
						sql = "select count(*) from dly_plan "
					if dly_date < today_date.date():
						sql = "select count(*) from his_dly_plan "
					sql += "where cnt_id=" + str(cnt_id) + " and sch_shift=" + str(shift_id) + " and absent=0 and dly_date='" + str(dly_date) + "'"
					cursor = connection.cursor()
					cursor.execute(sql)
					rows = cursor.fetchone()
					cursor.close	
					informNo = rows[0] if rows[0]>0 else 0
					# get srv_qty
					sql = "select cnt_id, srv_shif_id, sum(srv_qty) as qty from cus_service where srv_active=1 and cnt_id=" + str(cnt_id) + " and srv_shif_id=" + str(shift_id) + " group by cnt_id, srv_shif_id"
					cursor = connection.cursor()
					cursor.execute(sql)
					rows = cursor.fetchone()
					cursor.close
					srv_qty = rows[2]
					if informNo >= srv_qty:
						is_pass = False					
						message = "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา: <b>" + str(cnt_id) + "</b>"
						return is_pass, message
					else:
						is_pass = True # แจ้งเวรยังไม่เกินจำนวนที่อยู่ในสัญญา
						message = "Check #6 is passed."
		'''

	# return False, "TODO3"

	# debug
	# Check #7
	# print("AAAA")
	is_pass, message = chkValidInput(2,dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount,ui_ot_status,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id)
	
	# return False, message

	# YODA
	# return False, message

	if is_pass:
		


		# ****************************
		# Call TotalMissGuard
		# ****************************
		# START
		'''
		totalNDP = int(request.GET.get('totalNDP'))
		totalNDA = int(request.GET.get('totalNDA'))
		totalNDM = int(request.GET.get('totalNDM'))
		totalNNP = int(request.GET.get('totalNNP'))
		totalNNA = int(request.GET.get('totalNNA'))
		totalNNM = int(request.GET.get('totalNNM'))
		totalPDP = int(request.GET.get('totalPDP'))
		totalPDA = int(request.GET.get('totalPDA'))
		totalPDM = int(request.GET.get('totalPDM'))
		totalPNP = int(request.GET.get('totalPNP'))
		totalPNA = int(request.GET.get('totalPNA'))
		totalPNM = int(request.GET.get('totalPNM'))	
		'''

		'''
		is_public_holiday, message = isPublicHoliday(dly_date)
		if is_public_holiday:
			Tpub = 1
		else:
			Tpub = 0
		DN = None
		print(shift_id)
		if (shift_id == "99" or shift_id == "999"):
			print("DN=DAY OFF/ANOTHER SITE")		
		else:
			DN = shift_name.split("#")[1].strip()[0:1]
			print("DN=", DN.strip())
		if DN is not None:
			if DN=="D":
				print("DAY")			
				if Tpub == 0:
					totalNDA = totalNDA + 1
				else:
					totalPDA = totalPDA + 1
			else:
				print("NIGHT")
				if Tpub == 0:
					totalNNA = totalNNA + 1
				else:
					totalPNA = totalPNA + 1
		else:
			print("DN is None")
		lblNDM = totalNDA - totalNDP
		lblNNM = totalNNA - totalNNP
		lblPDM = totalPDA - totalPDP
		lblPNM = totalPNA - totalPNP
		print(str(lblNDM) + " | " + str(lblNNM) + " | " + str(lblPDM) + " | " + str(lblPNM))
		if Tpub == 0:
			if lblNDM > 0:
				return False, "จำนวน รปภ.ในกะกลางวันเกินกว่าที่ระบุในสัญญา"
			if lblNNM > 0:
				return False, "จำนวน รปภ.ในกะกลางคืนเกินกว่าที่ระบุในสัญญา"
		else:
			if lblPDM > 0:
				return False, "จำนวน รปภ.ในกะกลางวันเกินกว่าที่ระบุในสัญญา"
			if lblPNM > 0:
				return False, "จำนวน รปภ.ในกะกลางคืนเกินกว่าที่ระบุในสัญญา"
		'''

		'''
		print(totalNDA)
		print(totalNDP)
		print(totalNNA)
		print(totalNNP)
		print(totalPDA)
		print(totalPDP)
		print(totalPNA)
		print(totalPNP)
		'''
		# END




		# return False, "PASS"

		if (cnt_id=="") and (emp_id==""):
			return False, "ข้อมูลไม่ถูกต้อง"

		# Call SetVariable("DLY_PLAN")
		Tsch_no = 0
		Temp_id = 0 if emp_id=="" else emp_id
		Tdly_date = None if dly_date=="" else dly_date
		Tsch_shift = 0 if shift_id=="" else shift_id
		Tcnt_id = 0 if cnt_id=="" else cnt_id
		
		if search_emp_id=="":
			# print("Tdept_id = ใช้โซนของหน่วยงาน")
			# TODO: เลือกว่าจะใช้ค่าโซนของพนักงานหรือหน่วยงาน
			Tdept_id = emp_dept
		else:
			# print("Tdept_id = ใช้โซนของพนักงาน")
			Tdept_id = emp_dept

		Tsch_rank = emp_rank
		Tabsent = ui_absent_status
		Tlate = ui_late_status
		Tlate_full = late_full_paid_status
		Trelief = ui_relief_status
		Trelief_id = '0' if relief_emp_id=="" else relief_emp_id

		# return False, Trelief_id

		# TELEPHONE
		if ui_phone_status==1:
			if tel_time=="":
				Ttel_time = None
			else:
				Ttel_time = datetime.datetime.strptime(tel_time, '%d/%m/%Y %H:%M')
			Ttel_amt = 0 if tel_amount=="" else tel_amount
			Ttel_paid = 5 if Ttel_amt > 5 else Ttel_amt
		else:
			Ttel_time = None
			Ttel_amt = 0
			Ttel_paid = 0		


		# print("AAAA")

		# OVERTIME
		# late_from, late_to,late_reason_option, late_hour, late_full_paid_status
		Tot = 0 if ui_ot_status==0 else 1
		if (Tot==1) or (Tlate==1):
			Tot_reason = late_reason_option
			Tot_time_frm = late_from
			Tot_time_to = late_to
			# TODO: Tot_hr_amt
			Tot_hr_amt = late_hour
			Tot_pay_amt = 0
			if Tot==1:
				Tpay_type = "BAS"
			elif Tlate==1:
				Tpay_type = "TPB"
		else:
			Tot_reason = 0
			Tot_time_frm = None
			Tot_time_to = None
			Tot_hr_amt = 0
			Tot_pay_amt = 0
			Tpay_type = ""			


		# Add by Somkiat 2016/02/24
		#TODO: หาค่า Rea_timecross เซ็ทเริ่มต้นมาจากที่ไหน
		Rea_timecross = 0
		if Rea_timecross==57:
			Tot_reason = 57
			Tot_time_frm = None
			Tot_time_to = None
			Tot_hr_amt = Rea_timecross
			Tot_pay_amt = 0
			Tpay_type = "TPB"			

		#TODO: หาค่า txtSpare มีการเซ็ทค่าเริ่มต้นมาจากที่ไหน
		txtSpare = 0
		Tspare = txtSpare

		Twage_id = customer_wage_rate_id
		Twage_no = str(Twage_id) + str(emp_rank)
		Tpay_type = 1 if ui_ot_status==1 else ""
		Tsoc = 1 if float(Tot_hr_amt)>=8 else 0
		TRemark = job_type + " " + remark

		#message = "%s, %s, %s, %s, %s" % (Twage_id, Twage_no, Tpay_type, Tsoc, TRemark)

		# TODO: ถ้าหากขาดงานและมีคนมาแทน คนที่ขาดจะตั้ง Tday7=0 แต่คนที่มาแทนจะตั้ง Tday7=1
		if (ui_absent_status==1) and (ui_relief_status==1) and (relief_emp_id!=""):
			Tday7tmp = Tday7
			Tday7 = 0
 
		# return False, Tday7

		# return True, "TODO1"

		# ทำการบันทึกข้อมูลกรณีแก้ไขข้อมูลเก่า
		# Call UpdListName("DLY_PLAN")
		# aeiou
		# ตรวจสอบว่าต้องไปอัพเดทข้อมูลในตาราง DLY_PLAN หรือ HIS_DLY_PLAN
		gen_chk = 0	
		end_chk = 0
		pro_chk = 0		
		sql = "select date_chk,gen_chk,end_chk,pro_chk from t_date where date_chk='" + str(dly_date) + "'"
		cursor = connection.cursor()
		cursor.execute(sql)	
		t_date_obj = cursor.fetchall()
		cursor.close()
		# ตรวจสอบว่ามีการสร้างตารางรับแจ้งเวรไว้หรือยัง
		if (t_date_obj is not None):
			if len(t_date_obj)>0:
				gen_chk = t_date_obj[0][1]
				end_chk = t_date_obj[0][2]
				pro_chk = t_date_obj[0][3]
		
		# ตรวจสอบว่า post day end ไปหรือยัง
		'''
		if end_chk==1:
			return False, "ข้อมูลวันที่ <b>" + str() + "</b> ถูก DayEnd ไปแล้ว ไม่สามารถเรียกดูย้อนหลังได้"
		else:
			if dly_date==today_date.date():
				sql = "update dly_plan set "
			elif dly_date < today_date.date():
				# เช็คล็อคอินยูสเซอร์เป็น CMS_SUP หรือไม่				
				if username=='CMS_SUP':
					if end_chk==1:
						sql = "update his_dly_plan set "
					else:
						sql = "update dly_plan set "
				else:
					sql = "update dly_plan set "
			else:
				return False, "เลือกวันที่ทำรายการไม่ถูกต้อง"		
		'''

		# return False, "Debug 1"
		if username=='CMS_SUP':
			if dly_date==today_date.date():
				sql = "update dly_plan set "
			elif dly_date < today_date.date():
				# เช็คล็อคอินยูสเซอร์เป็น CMS_SUP หรือไม่				
				if username=='CMS_SUP':
					if end_chk==1:
						sql = "update his_dly_plan set "
					else:
						sql = "update dly_plan set "
				else:
					sql = "update dly_plan set "
			else:
				return False, "เลือกวันที่ทำรายการไม่ถูกต้อง"		
		else:
			if end_chk==1:
				return False, "ข้อมูลวันที่ <b>" + str(string_today_date) + "</b> ถูก DayEnd ไปแล้ว ไม่สามารถเรียกดูย้อนหลังได้"
			else:
				if dly_date==today_date.date():
					sql = "update dly_plan set "
				elif dly_date < today_date.date():
					# เช็คล็อคอินยูสเซอร์เป็น CMS_SUP หรือไม่				
					if username=='CMS_SUP':
						if end_chk==1:
							sql = "update his_dly_plan set "
						else:
							sql = "update dly_plan set "
					else:
						sql = "update dly_plan set "
				else:
					return False, "เลือกวันที่ทำรายการไม่ถูกต้อง"			

		# Get Period
		try:
			Tprd_id = TPeriod.objects.filter(prd_date_frm__lte=dly_date).filter(prd_date_to__gte=dly_date).filter(emp_type='D1').get()
			Tprd_id = Tprd_id.prd_id
		except TPeriod.DoesNotExist:
			Tprd_id = ""
		
		# Check Tpub
		if getDayPub(dly_date)==1:
			Tpub = 1
		else:
			Tpub = 0

		sql += "sch_no=" + str(Tsch_no) + ","
		sql += "dept_id=" + str(Tdept_id) + ","
		sql += "sch_rank='" + str(Tsch_rank) + "',"		
		sql += "prd_id='" + str(Tprd_id) + "',"
		sql += "absent=" + str(Tabsent) + ","
		sql += "late=" + str(Tlate) + ","
		sql += "late_full=" + str(Tlate_full) + ","		

		
		#sql += "relieft=" + str(Trelief) + ","
		# TODO
		# if (ui_absent_status==0) and (ui_late_status==0) and (ui_phone_status==1):
		if ui_relief_status==1:
			sql += "relieft=1" + ","
		else:
			sql += "relieft=0" + ","

		sql += "relieft_id=" + str(Trelief_id) + ","		
		sql += "tel_man=" + str(tel_man) + ","

		'''
		if (Ttel_time is None):
			sql += "tel_time=null,"			
		else:
			sql += "tel_time='" + str(Ttel_time) + "',"
		'''
		sql += "tel_time='" + str(datetime.datetime.now())[:-10] + "',"

		sql += "tel_amt=" + str(Ttel_amt) + ","
		sql += "tel_paid=" + str(Ttel_paid) + ","
		sql += "ot=" + str(Tot) + ","
		sql += "ot_reason=" + str(Tot_reason) + ","
		
		if Tot_time_frm is None:
			sql += "ot_time_frm=null,"
		else:
			sql += "ot_time_frm='" + str(Tot_time_frm) + "',"

		if Tot_time_to is None:
			sql += "ot_time_to=null,"
		else:
			sql += "ot_time_to='" + str(Tot_time_to) + "',"

		sql += "ot_hr_amt=" + str(Tot_hr_amt) + ","
		sql += "ot_pay_amt=" + str(Tot_pay_amt) + ","
		sql += "spare=" + str(Tspare) + ","
		sql += "wage_id=" + str(Twage_id) + ","		
		sql += "wage_no='" + str(Twage_no) + "',"
		sql += "pay_type='" + str(Tpay_type) + "',"
		sql += "soc=" + str(Tsoc) + ","
		sql += "pub=" + str(Tpub) + ","
		sql += "dof=" + str(Tdof) + ","		
		sql += "day7=" + str(Tday7) + ","		
		sql += "upd_date='" + str(datetime.datetime.now())[:-10] + "',"
		sql += "upd_by='" + str(username) + "',"
		sql += "upd_flag='E'" + ","
		sql += "remark='" + str(job_type) + "' "		
		sql += "where cnt_id=" + str(cnt_id) + " "
		sql += "and dly_date='" + str(dly_date) + "' "
		sql += "and emp_id=" + str(emp_id) + " "
		sql += "and sch_shift=" + str(shift_id)

		print("DEBUG sql check:", sql)

		
		# return False, "DEBUG1"


		try:
			with connection.cursor() as cursor:
				cursor.execute(sql)
			is_pass = True
			message = "รับแจ้งเวรสำเร็จ"

			# กรณีรับแจ้งเวรสำเร็จ
			if is_pass:
				print('Update spaydate table')
				# Update spaydate table		

				job_type_split = job_type.split("|")
				
				if len(job_type_split) == 2:
					srv_id_temp = job_type_split[0]
					position_temp = job_type_split[1]
					sql = "update spaydate set Upd_by='" + str(username) + "', Upd_flag='A' where cnt_id=" + str(cnt_id) + " and srv_id=" + str(srv_id_temp) + " and position='" + str(position_temp) + "';"
					print("SQL:", sql)
					try:
						with connection.cursor() as cursor:
							cursor.execute(sql)					
					except db.OperationalError as e:
						is_pass = False
						message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
					except db.Error as e:
						is_pass = False
						message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
					finally:
						cursor.close()	

		except db.OperationalError as e:
			is_pass = False
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
		except db.Error as e:
			is_pass = False
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
		finally:
			cursor.close()


		# print("sql test: ", sql)
		# return False, "A2"

		# message = "%s,%s,%s,%s" %(Temp_id,Tabsent,Trelief,Trelief_id)
		# return False, message		

		if (Temp_id!="") and (Tabsent==1) and (Trelief==1) and (Trelief_id!=""):
			# TODO: ถ้าหากขาดงานและมีคนมาแทนจะต้องเพิ่ม รายการคนที่แทนอีก 1 รายการ
			Temp_id = 0 if relief_emp_id=="" else relief_emp_id
			Tsch_rank = "SOY" #TODO ส่งค่า relief_emp_id_rank มา

			# คนที่ขาดจะตั้ง Tday7=0 แต่คนมาแทนต้องตั้ง Tday7=1
			Tday7 = Tday7tmp
			# 632036,SOY,0


			# Call AddListName("DLY_PLAN")
			if dly_date==today_date.date():
				sql = "insert into dly_plan "
			elif dly_date < today_date.date():
				if username=="CMS_SUP":
					sql = "insert into his_dly_plan "
				else:
					is_pass = False
					message = "ไม่มีสิทธิ์ทำรายการ"
					return is_pass, message
			else:
				is_pass = False
				message = "เลือกวันที่ทำรายการไม่ถูกต้อง"
				return is_pass, message
			
			sql += "(cnt_id,emp_id,dly_date,sch_shift"
			sql += ",sch_no,dept_id,sch_rank,prd_id"
			sql += ",absent,late,late_full,relieft,relieft_id"
			sql += ",tel_man,tel_time,tel_amt,tel_paid"
			sql += ",ot,ot_reason,ot_time_frm,ot_time_to,ot_hr_amt,ot_pay_amt"
			sql += ",spare,wage_id,wage_no,pay_type,soc,pub,dof,day7"
			sql += ",upd_date,upd_by,upd_flag,remark)"
			sql += " values ("			
			sql += str(Tcnt_id) + "," + str(Temp_id) + ",'" + str(Tdly_date) + "'," + str(Tsch_shift) + ","
			sql += str(Tsch_no) + "," + str(Tdept_id) + ",'" + str(Tsch_rank) + "','" + str(Tprd_id) + "',"
			# sql += str(Tabsent) + "," + str(Tlate) + "," + str(Tlate_full) + "," + str(Trelief) + "," + str(Trelief_id) + ","
			# sql += str("0") + "," + str(Tlate) + "," + str(Tlate_full) + "," + str(Trelief) + "," + str(Trelief_id) + ","
			sql += str("0") + "," + str(Tlate) + "," + str(Tlate_full) + "," + str(Trelief) + "," + str("0") + ","
			sql += str(ui_phone_status) + "," 
			
			print("SQL : ", sql)
			# return False, sql

			if (Ttel_time is None) or (Ttel_time==""):
				sql += "null" + "," 
			else:
				sql += str(Ttel_time)

			sql += str(Ttel_amt) + "," + str(Ttel_paid) + "," + str(Tot) + "," + str(Tot_reason) + "," 

			if (Tot_time_frm is None) or (Tot_time_frm==""):
				sql += "null" + "," 
			else:
				sql += str(Tot_time_frm) + ","

			if (Tot_time_to is None) or (Tot_time_to==""):
				sql += "null" + "," 
			else:
				sql += str(Tot_time_to) + ","

			sql += str(Tot_hr_amt) + "," + str(Tot_pay_amt) + ","
			sql += str(Tspare) + "," + str(Twage_id) + ",'" + str(Twage_no) + "','" + str(Tpay_type) + "'," + str(Tsoc) + "," + str(Tpub) + "," + str(Tdof) + "," + str(Tday7) + ",'"
			sql += str(str(datetime.datetime.now())[:-3]) + "','" + str(username) + "'," + "'A'" + ",'" + str(TRemark) + "')"
			
			# print("sql 2 " + str(sql))
			# return False, "Test"

			try:
				with connection.cursor() as cursor:
					cursor.execute(sql)
				is_pass = True
				message = "รับแจ้งเวรสำเร็จ"
			except db.OperationalError as e:
				is_pass = False
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
			except db.Error as e:
				is_pass = False
				message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
			finally:
				cursor.close()			

	return is_pass, message
	
	

def editRecord_temp(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,relief_status,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM):
	is_pass = False
	message = ""

	string_today_date = str(settings.TODAY_DATE.strftime("%d/%m/%Y"))
	today_date = datetime.datetime.strptime(string_today_date, "%d/%m/%Y")
	
	# Check #1
	checkNoSpare = False
	if absent_status==0 and late_status==0 and late_status==0 and ot_status==0 and phone_status==0:
		checkNoSpare = True
	is_pass = True
	message += "Check #1 is passed.<br>" if is_pass else "Check #1 is failed.<br>"
	# print(message)


	print("PASS CHECK #1")
	# Check #2 - check shift not empty	
	# skip
	if is_pass:
		is_pass = True
		message += "Check #2 is passed.<br>" if is_pass else "Check #2 is failed.<br>"
		# print(message)
	

	print("PASS CHECK #2")
	# Check #3 - check manpower
	if is_pass:
		sql = "select count(*) from v_dlyplan_shift where cnt_id='" + str(cnt_id) + "' and left(remark,2)='" + str(remark) + "' and shf_type=" + str(job_type) + " and absent=0 and dly_date='" + str(dly_date) + "'"
		# print("sql = " + str(sql))
		cursor = connection.cursor()
		cursor.execute(sql)
		rows = cursor.fetchone()
		cursor.close	
		# print("aManPower = " + str(rows[0]))
		is_pass = True if rows[0]>=0 else False
		message += "Check #3 is passed.<br>" if is_pass else "Check #3 is failed.</br>"
		# print(message)


	print("PASS CHECK #3")
	# Check #4 - 
	if is_pass:
		if phone_status==0:
			if late_status==0:
				if absent_status==1 and relief_status==1:
					print("TODO check #4")
		is_pass = True
		message += "Check #4 is passed.<br>" if is_pass else "Check #4 is failed.</br>"


	print("PASS CHECK #4")
	# Check #5 - ค่าโทราต้องมีค่ามากกว่า 0 บาท
	if is_pass:
		is_pass = True
		message += "Check #5 is passed.<br>" if is_pass else "Check #5 is failed.</br>"


	print("PASS CHECK #5")
	# Check #6 - กรณีพนักงานไม่ได้หยุดและต้องการแจ้งเวรให้ตรวจสอบจำนวนคนแจ้งเวรต้องไม่เกินจากที่จำนวนที่แจ้งในสัญญา
	if is_pass:
		if phone_status==0:
			if late_status==0:
				if absent_status==0:
					if shift_id != "99":

						if dly_date > today_date.date():
							is_pass = False
							message += "Check #6 is failed - Daily attendance date is greater than today date.</br>"
						else:
							is_pass = True

						if is_pass:
							if dly_date == today_date.date():
								sql = "select count(*) from dly_plan "

							if dly_date < today_date.date():
								sql = "select count(*) from his_dly_plan "

							sql += "where cnt_id=" + str(cnt_id) + " and sch_shift=" + str(shift_id) + " and absent=0 and dly_date='" + str(dly_date) + "'"
							cursor = connection.cursor()
							cursor.execute(sql)
							rows = cursor.fetchone()
							cursor.close	
							informNo = rows[0] if rows[0]>0 else 0
							# print("informNo = " + str(informNo))

							# get srv_qty
							sql = "select cnt_id, srv_shif_id, sum(srv_qty) as qty from cus_service where srv_active=1 and cnt_id=" + str(cnt_id) + " and srv_shif_id=" + str(shift_id) + " group by cnt_id, srv_shif_id"
							cursor = connection.cursor()
							cursor.execute(sql)
							rows = cursor.fetchone()
							cursor.close
							contractNo = rows[2]
							# print("contractNo = " + str(contractNo))

							if informNo >= contractNo:
								is_pass = False
								message += "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา"
								return is_pass, message
							else:
								is_pass = True								
						

	print("PASS CHECK #6")

	# Check #7 - check valid input
	is_pass, message = chkValidInput(2,dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,relief_status,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM)		
	is_pass = True
	message += "Ready to save record"

	'''
	if is_pass:
		# setVariable()		
		# dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,
		# relief_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM
		upd_date = str(datetime.datetime.now())[:-3]
		sql = "update dly_plan set cnt_id=" + str(cnt_id) + ","		
		sql += "sch_no=0,"
		sql += "dept_id=" + str(emp_dept) + ","
		sql += "sch_rank='" + str(emp_rank) + "',"
		sql += "prd_id='D120121',"
		sql += "absent=" + str(absent_status) + ","
		sql += "late=" + str(late_status) + ","
		sql += "late_full=0,"
		sql += "relieft=" + str(relief_status) + ","
		sql += "relieft_id=0,"
		sql += "tel_man=0,"
		sql += "tel_time=NULL,"
		sql += "tel_amt=0,"
		sql += "tel_paid=0,"
		sql += "ot=0,"
		sql += "ot_reason=0,"
		sql += "ot_time_frm=NULL,"
		sql += "ot_time_to=NULL,"
		sql += "ot_hr_amt=0,"
		sql += "ot_pay_amt=0,"
		sql += "spare=0,"
		sql += "wage_id=32,"
		sql += "wage_no='32SOY',"
		sql += "pay_type='',"
		sql += "soc=0,"
		sql += "pub=0,"
		sql += "dof=0,"
		sql += "day7=0,"
		sql += "upd_date='" + str(upd_date) + "',"
		sql += "upd_by='System',"
		sql += "upd_flag='A',"
		sql += "remark='" + str(job_type) + " " + str(remark) + "' "
		sql += "where cnt_id=" + str(cnt_id)
		sql += " and dly_date='" + str(dly_date) + "'"
		sql += " and emp_id=" + str(emp_id)
		sql += " and sch_shift=" + str(shift_id)
		# print(sql)
	
		try:
			with connection.cursor() as cursor:
				cursor.execute(sql)
			is_pass = True
			message = "Edit complete."
		except db.OperationalError as e:
			is_pass = False
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
		except db.Error as e:
			is_pass = False
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
	return is_pass, message
	'''

	return is_pass, message


def chkValidInput(check_type,dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,ui_absent_status,
	ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,remark,totalNDP,
	totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount,
	ui_ot_status,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id):

	# Initial value for booking cross site
	# START
	Timecross = 0
	# END

	#print(cus_id + cus_brn + cus_vol)
	#return False, "DEBUG"

	# Case 2
	if check_type==2:

		# เช็ครหัสพนักงานต้องมีค่า
		if emp_id=="" or emp_id is None:
			return False, "กรุณาป้อนรหัสพนักงาน"
		
		# เช็คกะการทำงานต้องมีค่า
		if shift_id=="" or shift_id is None:
			return False, "กรุณาป้อนกะการทำงานของพนักงาาน"

		# เช็คห้ามคีย์รหัสที่ไม่มีสิทธ์ลงเวร
		sql = "select emp_id,upd_flag,emp_term_date,sch_active from v_employee where emp_id=" + str(emp_id)
		print("SQL: ", sql)

		cursor = connection.cursor()
		cursor.execute(sql)
		employeeobj = cursor.fetchone()
		cursor.close()


		if employeeobj is not None:

			# ตรวจสอบว่าพนักงานถูกลบออกจากระบบไปแล้วหรือไม่
			if employeeobj[1] == 'D' and employeeobj[3] != 1:
				return False, "พนักงานคนนี้ไม่สามารถนำมาจัดตารางเวรได้เนื่องจากพนักงานโดนลบจากระบบ"

			# batman
			# ตรวจสอบว่าพนักงานลาออกหรือไม่
			# if employeeobj[2] is not None: #and employeeobj[3] != 1:
			#	return False, "พนักงานคนนี้ไม่สามารถนำมาจัดตารางเวรได้เนื่องจากลาออกตั้งแต่วันที่ <b>" + str(employeeobj[2].strftime("%d/%m/%Y")) + "</b>"

			if employeeobj[2] is not None:
				emp_term_date = employeeobj[2].strftime("%Y-%m-%d")
				daily_attendance_date = dly_date.strftime("%Y-%m-%d")

				print("emp_term_date : ", emp_term_date)
				print("daily_attendance_date : ", daily_attendance_date)

				if datetime.datetime.strptime(emp_term_date, '%Y-%m-%d') <= datetime.datetime.strptime(daily_attendance_date, '%Y-%m-%d'):				
					return False, "พนักงานคนนี้ไม่สามารถนำมาจัดตารางเวรได้เนื่องจากลาออกตั้งแต่วันที่ <b>" + str(employeeobj[2].strftime("%d/%m/%Y")) + "</b>"


			# return False, "TEST1"

			# กรณีไม่มีคนเข้าเวรแทนให้ดูจากไม่มีการเลือกทั้ง Absent และ Relief หรือไม่ ถ้าใช่ให้ตรวจสอบว่าพนักงานลาออกหรือยัง
			if (ui_absent_status==0) and (ui_relief_status==0):
				if employeeobj[1] == 'D':
					return False, "พนักงานคนนี้ไม่สามารถนำมาจัดตารางเวรได้เนื่องจากพนักงานโดนลบจากระบบ"

			# กรณีมีการเข้าเวรแทน
			if (ui_absent_status==1) and (ui_relief_status==1):
				if relief_emp_id is not None:					
					sql = "select emp_id,upd_flag,emp_term_date from v_employee where emp_id=" + str(relief_emp_id)				
					cursor = connection.cursor()
					cursor.execute(sql)
					employeeobj = cursor.fetchone()
					cursor.close()
					if employeeobj is not None:
						# เช็คว่าพนักงานถูกลบออกจากระบบไปแล้วหรือไม่
						if employeeobj[1] == 'D':
							return False, "พนักงานคนนี้ไม่สามารถเข้าเวรแทนได้เนื่องจากพนักงานโดนลบจากระบบ"

						# เช็คว่าพนักงานลาออกหรือไม่
						if employeeobj[2] is not None:
							return False, "พนักงานคนนี้ไม่สามารถนำเข้าเวรแทนได้เนื่องจาก" + " <u>ลาออก</u> " + "ตั้งแต่วันที่ <b>" + str(employeeobj[2].strftime("%d/%m/%Y")) + "</b>"
				else:
					is_pass = False
					message = "พนักงานคนนี้ไม่สามารถนำมาเข้าเวรแทนได้เนื่องจากรหัสพนักงานไม่มีอยู่ในระบบ!"			

			# ตรวจสอบค่าโทร
			if ui_phone_status==1:
				if tel_amount==0:
					if allowZeroBathForPhoneAmount==0:
						return False, "กรุณาป้อนค่าโทรศัพท์"

			# ตรวจสอบเงื่อนไขเข้างานสาย หรือ ตรวจสอบช่วงเวลาได้โอที
			if (ui_late_status==1) or (ui_ot_status==1):
				# ตรวจสอบการป้อนรหัสพนักงานที่เข้าเวรแทนช่วงมาสาย
				if ui_late_status==1:
					if (relief_emp_id=="") or (relief_emp_id is None):
						return False, "กรุณาป้อนรหัสพนังานที่เข้าเวรแทน"

				# ตรวจสอบเวลาเริ่มโอที
				# late_from,late_to,late_reason_option,late_hour,late_full_paid_status
				if (late_from=="") or (late_to==""):
					return False, "กรุณาป้อนเวลาที่เริ่มและเวลาสิ้นสุดโอที"

				# ตรวจสอบเวลาสิ้นสุดโอทีต้องน้อยกว่าเวลาเริ่มโอที
				if late_from > late_to:
					return False, "เวลาสิ้นสุดโอทีต้องมากกว่าเวลาเริ่มโอที"

				# ตรวจสอบเหตุผลที่ได้โอที
				if (late_reason_option=="") or (late_reason_option==0):
					return False, "กรุณาเลือกเหตุผลที่ได้โอที"

				# ตรวจสอบจำนวนชั่วโมงที่ได้โอที
				if (late_hour=="") or (late_hour==0):
					return False, "กรุณาระบุจำนวนชั่วโมงที่ได้โอที"

				# ตรวจสอบจำนวนชั่วโมงที่ได้โอทีต้องไม่เกิน 2 ชั่วโมง
				if float(late_hour) > 2:
					return False, "จำนวนชั่วโมงควงรอเกิน 2 ชั่วโมง"



			# ห้ามลงงานที่อื่นในเวลาที่คร่อมกัน วันเดียวกัน
			# ตรวจสอบห้ามลงงานที่อื่นในกะเดียวกัน วันเดียวกัน
			# TODO - CheckBetweenShift()
			# START			

			# END


			# ป้องกันการกลับมาแก้ไข Absent หากรปภ.เข้าเวรอื่นอยู่และเวลาคร่อมกับหน่วยงานอื่น
			'''
			if ui_relief_status==1:
				sql = "select a.*,b.shf_type,b.shf_time_frm,b.shf_time_to"
				sql += " from dly_plan a left join t_shift b on a.sch_shift=b.shf_id"
				sql += " where a.dly_date='" + str(dly_date) + "'"
				sql += " and a.emp_id=" + str(relief_emp_id)
				sql += " and a.absent=0"
				cursor = connection.cursor()
				cursor.execute(sql)
				record = cursor.fetchone()
				cursor.close()
				
				if record is not None:
					# TODO: ตรวจสอบกรณียอมให้พนักงานเข้าเวรคร่อมกับหน่วยงานที่เข้าเวรอยู่ล้ว
					return False, "พนักงานเข้าเวรคร่อมกับหน่วยงาน..."			
			'''			


			# ห้ามลงรายการซ้ำ ถ้าเพิ่มรายการใหม่ สำหรับคนที่มาแทน แทนหลายคนในหน่วยเดียวกันไม่ได้
			if (ui_relief_status==1) and (relief_emp_id!="") and (relief_emp_id is not None):
				
				# GetShiftOrder
				getShiftOrder = 0
				sql = "select shf_order from t_shift where shf_id=" + shift_id
				cursor = connection.cursor()
				cursor.execute(sql)
				record = cursor.fetchone()
				cursor.close()
				if record is not None:
					getShiftOrder = record[0]


				# เช็คห้ามคนที่มาแทนลงงานที่อื่นในกะเดียวกัน วันเดียวกัน
				checkDupDly = 0
				sql = "select * from dly_plan where dly_date='" + str(dly_date) + "'"
				sql += " and emp_id=" + str(relief_emp_id)
				sql += " and absent=0"
				sql += " and dbo.shforder(sch_shift)=" + str(getShiftOrder)
				# print("___sql = " + str(sql))
				cursor = connection.cursor()
				cursor.execute(sql)
				record = cursor.fetchone()
				cursor.close()
				# if record is not None:
				#	return False, "พนักงานรหัส <b>" + str(relief_emp_id) + "</b> เข้าเวรที่หน่วยงานอื่น1"

				# สำหรับ Relief Employee ID ห้ามลงรายการซ้ำ ในสัญญาเดียวกัน วันเดียวกัน กะเดียวกัน
				sql = "select * from dly_plan where cnt_id=" + str(cnt_id) + " and dly_date='" + str(dly_date) + "' and emp_id=" + str(relief_emp_id) + " and sch_shift=" + str(shift_id)
				cursor = connection.cursor()
				cursor.execute(sql)
				record = cursor.fetchone()
				cursor.close()
				
				'''
				if record is not None:
					# ถ้าเป็นการมาสายให้บันทึกได้
					if ui_late_status!=1:
						return False, "พนักงานรหัส <b>" + str(relief_emp_id) + "</b> เข้าเวรที่หน่วยงานอื่น2"		
				'''

			# เช็คห้ามพนักงานทำงานในวัน Day Off จากตาราง SYS_GPMDOF
			# พนักงานปกติ
			if (emp_id!="") and (ui_absent_status==0):
				sql = "select * from sys_gpmdof where emp_id=" + str(emp_id) + " and dly_date='" + str(dly_date) + "'"
				cursor = connection.cursor()
				cursor.execute(sql)
				record = cursor.fetchone()
				cursor.close()
				if record is not None:
					return False, "พนักงานทำงานในวัน Day Off จากตาราง SYS_GPMDOF"

			
			# เช็คห้ามพนักงานที่เข้าเวรแทนทำงานในวัน Day Off จากตาราง SYS_GPMDOF
			if (relief_emp_id!="") and (ui_absent_status==1):
				sql = "select * from sys_gpmdof where emp_id=" + str(relief_emp_id) + " and dly_date='" + str(dly_date) + "'"
				# print("sql 1:", sql)
				cursor = connection.cursor()
				cursor.execute(sql)
				record = cursor.fetchone()
				cursor.close()
				if record is not None:
					return False, "พนักงานที่จะลงเวรแทนทำงานในวัน Day Off จากตาราง SYS_GPMDOF"


			# ***********************************************************
			# เช็คจำนวนคนห้ามคีย์เกินในรายการสัญญา กรณีนี้ให้เช็คจาก Missing Record		
			# ***********************************************************
			# spidy


			is_pass = True
			message = "ChkValidInput is true"
		else:
			return False, "พนักงานคนนี้ไม่สามารถนำมาจัดตารางเวรได้เนื่องจากรหัสพนักงานไม่มีอยู่ในระบบ"
	else:
		is_pass = False
		message = "Error: check_type value is not 2."

	return is_pass, message


# def chkValidInput(check_type,dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,relief_status,relief_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM):
def chkValidInput_bk(check_type,dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,tel_man,tel_time,tel_amount,relief_status,relief_emp_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount):
	is_pass = False
	message = ""

	# Case 1
	if check_type==1:
		is_pass = False
		message = "check_type = 1 is not implemented."
		return is_pass, message
	

	# Case 2
	if check_type==2:

		# เช็ครหัสพนักงานต้องมีค่า
		if emp_id=="" or emp_id is None:
			is_pass = False
			message = "กรุณาป้อนรหัสพนักงาน"
			return is_pass, message
		
		# เช็คกะการทำงานต้องมีค่า
		if shift_id=="" or shift_id is None:
			is_pass = False
			message = "กรุณาป้อนกะการทำงานของพนักงาาน"
			return is_pass, message


		# เช็คห้ามคีย์รหัสที่ไม่มีสิทธ์ลงเวร
		sql = "select emp_id,upd_flag,emp_term_date from v_employee where emp_id=" + str(emp_id)
		cursor = connection.cursor()
		cursor.execute(sql)
		employeeobj = cursor.fetchone()
		cursor.close
		if employeeobj is not None:

			# เช็คว่าพนักงานถูกลบออกจากระบบไปแล้วหรือไม่
			if employeeobj[1] == 'D':
				is_pass = False
				message = "พนักงานคนนี้ไม่สามารถนำมาจัดตารางเวรได้เนื่องจากพนักงานโดนลบจากระบบ"
				return is_pass, message

			# เช็คว่าพนักงานลาออกหรือไม่
			if employeeobj[2] is not None:
				is_pass = False
				message = "พนักงานคนนี้ไม่สามารถนำมาจัดตารางเวรได้เนื่องจากลาออกตั้งแต่วันที่ <b>" + str(employeeobj[0][2]) + "</b>"
				return is_pass, message

			# หากไม่ติดเงื่อนไขข้างต้นให้ทำการอัพเดทข้อมูล
			is_pass = True
			message = "Pass"
		else:
			is_pass = False
			message = "พนักงานคนนี้ไม่สามารถนำมาจัดตารางเวรได้เนื่องจากรหัสพนักงานไม่มีอยู่ในระบบ"
			return is_pass, message

		# เช็คกรณีมีการเข้าเวรแทน
		# print("____relief_id = " + str(relief_id))
		if absent_status==1 and relief_status==1:
			# print("___Relief__=Y")
			if relief_emp_id is not None:
				

				sql = "select emp_id,upd_flag,emp_term_date from v_employee where emp_id=" + str(relief_emp_id)				
				cursor = connection.cursor()
				cursor.execute(sql)
				employeeobj = cursor.fetchone()
				cursor.close
				if employeeobj is not None:
					# เช็คว่าพนักงานถูกลบออกจากระบบไปแล้วหรือไม่
					if employeeobj[1] == 'D':
						is_pass = False
						message = "พนักงานคนนี้ไม่สามารถเข้าเวรแทนได้เนื่องจากพนักงานโดนลบจากระบบ"
						return is_pass, message

					# เช็คว่าพนักงานลาออกหรือไม่
					if employeeobj[2] is not None:
						is_pass = False
						message = "พนักงานคนนี้ไม่สามารถนำเข้าเวรแทนได้เนื่องจาก" + " <u>ลาออก</u> " + "ตั้งแต่วันที่ <b>" + str(employeeobj[2].strftime("%d/%m/%Y")) + "</b>"
						return is_pass, message					

					# หากไม่ติดเงื่อนไขข้างต้นให้ทำการอัพเดทข้อมูล
					is_pass = True
					message = "Pass - สามารถลงหน่วยงานแทนได้"

					# print(message)

			else:
				is_pass = False
				message = "พนักงานคนนี้ไม่สามารถนำมาเข้าเวรแทนได้เนื่องจากรหัสพนักงานไม่มีอยู่ในระบบ!"
		

		# เช็คห้ามลงงานที่อื่นในกะเดียวกัน วันเดียวกัน
		if is_pass:
			if phone_status==1:
				print("Do nothing")
			elif late_status==1:				
				print("Do nothing")
			elif absent_status==0:
				# TODO: 
				table_name = "dly_plan"
				sql = "select * from " + table_name + " where dly_date='" + str(dly_date) + "' and emp_id=" + str(emp_id) + " and absent=0" + " and sch_shift=" + str(shift_id) + " and cnt_id<>" + str(cnt_id)
				cursor = connection.cursor()
				cursor.execute(sql)
				record = cursor.fetchone()
				cursor.close()
				if record is None:
					is_pass = True
				else:
					is_pass = False
					message = "พนักงานรหัส <b>" + str(emp_id) + "</b> เข้าเวรที่หน่วยงานอื่น กรุณาตรวจสอบ"
					return is_pass, message


		# เช็คป้องกันการกลับมาแก้ไข Absent หากรปภ.เข้าเวรอื่นอยู่และเวลาคร่อมกับหน่วยงานอื่น
		if relief_status==1:

			rea_timecross = 0

			# Check between shift
			sql = "select a.*,b.shf_type,b.shf_time_frm,b.shf_time_to"
			sql += " from dly_plan a left join t_shift b on a.sch_shift=b.shf_id"
			sql += " where a.dly_date='" + str(dly_date) + "'"
			sql += " and a.emp_id=" + str(relief_emp_id)
			sql += " and a.absent=0"
			# print("____sql=" + str(sql))			
			cursor = connection.cursor()
			cursor.execute(sql)
			record = cursor.fetchone()
			cursor.close()
			if record is None:
				is_pass = True
			else:
				is_pass = False
				message = "พนักงานเข้าเวรคร่อมกับหน่วยงาน..."
				return is_pass, message
				

		# ห้ามลงรายการซ้ำ ถ้าเพิ่มรายการใหม่ สำหรับคนที่มาแทน แทนหลายคนในหน่วยเดียวกันไม่ได้
		if relief_status==1 and relief_emp_id is not None:
			# GetShiftOrder
			getShiftOrder = 0
			sql = "select shf_order from t_shift where shf_id=" + shift_id
			cursor = connection.cursor()
			cursor.execute(sql)
			record = cursor.fetchone()
			cursor.close
			if record is not None:
				getShiftOrder = record[0]


			# เช็คห้ามคนที่มาแทนลงงานที่อื่นในกะเดียวกัน วันเดียวกัน
			checkDupDly = 0
			sql = "select * from dly_plan where dly_date='" + str(dly_date) + "'"
			sql += " and emp_id=" + str(relief_emp_id)
			sql += " and absent=0"
			sql += " and dbo.shforder(sch_shift)=" + str(getShiftOrder)
			# print("___sql = " + str(sql))
			cursor = connection.cursor()
			cursor.execute(sql)
			record = cursor.fetchone()
			cursor.close
			if record is not None:				
				# หากมีการแก้ไขเปลี่ยนแปลง Phone, OT, Late ให้สามารถบันทึกได้
				if late_status==1 or phone_status==1:
					gphone = 0

				checkDupDly = 1
				is_pass = False
				message = "พนักงานเข้าเวรที่หน่วยงานอื่น"
				return is_pass, message
			else:
				checkDupDly = 0
				message = ""

			# สำหรับ Relief Employee ID ห้ามลงรายการซ้ำในสัญญาเดียวกัน วันเดียวกัน กะเดียวกัน
			checkDupDly = 0
			sql = "select * from dly_plan where cnt_id=" + str(cnt_id) + " and dly_date='" + str(dly_date) + "'"
			sql += " and emp_id=" + str(relief_emp_id)
			sql += " and sch_shift=" + str(shift_id)
			cursor = connection.cursor()
			cursor.execute(sql)
			record = cursor.fetchone()
			cursor.close
			if record is not None:				
				# หากมีการแก้ไขเปลี่ยนแปลง Phone, OT, Late ให้สามารถบันทึกได้
				if late_status==1 or phone_status==1:
					gphone = 0

				checkDupDly = 1
				is_pass = False
				message = "พนักงานเข้าเวรที่หน่วยงานอื่น"
				return is_pass, message
			else:
				checkDupDly = 0
				message = ""

			# เช็คห้ามพนักงานทำงานในวัน Day Off จากตาราง SYS_GPMDOF
			if emp_id is not None and absent_status==0:
				print("TODO: ChkDOF")
				chkDOF = False
				sql = "select * from sys_gpmdof where emp_id=" + str(emp_id) + " and dly_date='" + str(dly_date) + "'"
				cursor = connection.cursor()
				cursor.execute(sql)
				record = cursor.fetchone()
				cursor.close
				if record is not None:
					chkDOF = True
					is_pass = False
					message = "พนักงานทำงานในวัน Day Off จากตาราง SYS_GPMDOF"
					return is_pass, message
				else:
					is_pass = True
					chkDOF = False

				if chkDOF:
					print("TODO: CheckEmpDOF()")
						
			if relief_emp_id is not None and absent_status==1:
				print("TODO: ChkDOF()")
				print("TODO: CheckEmpDOF()")
				print("TODO: ChkDOF")
				chkDOF = False
				sql = "select * from sys_gpmdof where emp_id=" + str(relief_emp_id) + " and dly_date='" + str(dly_date) + "'"
				cursor = connection.cursor()
				cursor.execute(sql)
				record = cursor.fetchone()
				cursor.close
				if record is not None:
					chkDOF = True
					is_pass = False
					message = "พนักงานที่จะลงเวรแทนทำงานในวัน Day Off จากตาราง SYS_GPMDOF"
					return is_pass, message
				else:
					is_pass = True
					chkDOF = False

				if chkDOF:
					print("TODO: CheckEmpDOF()")

		# TODO: checkCall
		if phone_status==1:
			if tel_amount <= 0:
				is_pass = False
				message = "ยังไม่ได้ป้อนค่าโทรศัพท์"
				return is_pass, message

		# TODO: checkLate
		# if late_status==1 or ot_status==1:	# ot_status ???
		if late_status==1:
			if relief_emp_id=="" or relief_emp_id is None:
				return False, "กรุณาป้อนรหัสพนังานที่เข้าเวรแทน"	
		
		return is_pass, message

	# Case 3
	if check_type==3:
		is_pass = False
		message = "check_type = 3 is not implemented."
		return is_pass, message
	
	return False, "Validation is failed! Please contact admin"



'''
def editRecord_old(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,relief_status,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM):
	is_pass = True
	message = ""	

	# Server side check
	# TODO: shift_id must be in cus_service

	# ป้องกันความผิดพลาดของการคีย์ค่า spare zone
	checkNoSpare = False
	if absent_status==0 and late_status==0 and late_status==0 and ot_status==0 and phone_status==0:
		checkNoSpare = True

	# *****************************************************
	# RULE 1 - Check manpower must not more than contract
	# *****************************************************
	shift_type = shift_name.partition("#")[2][0:2].strip() # shift_type will be D or N or O
		
	# Check Manpower
	# sql = "select count(*) from v_dlyplan_shift where cnt_id='" + str(cnt_id) + "' and left(remark,2)='" + str(remark) + "' and shf_type=" + str(job_type) + " and absent=0 and dly_date='" + str(dly_date) + "'"
	# print("sql = " + str(sql))
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchone()
	cursor.close	
	# print("aManPower = " + str(rows[0]))
	is_pass = True if rows[0]>=0 else False
	# print("Rule 1 is passed." if is_pass else "Rule 1 is failed.")
	# print("absent_status = " + str(absent_status))
	# print("shift_id = " + str(shift_id))
     

	# กรณีพนักงานลาและมีการส่งคนใหม่เข้าเวรแทน
	if absent_status==1 and relief_status==1:
				
		today_date = settings.TODAY_DATE.strftime("%Y-%m-%d")
		daily_attendance_date = dly_date.strftime("%Y-%m-%d")

		# print("today_date = " + str(today_date))
		# print("daily_attendance_date = " + str(daily_attendance_date))

		# d1 = time.strptime(settings.TODAY_DATE, "%d/%m/%Y")
		# d2 = time.strptime(dly_date, "%d/%m/%Y")

		if daily_attendance_date == today_date:
			sql = "select cnt_id, sch_shift from dly_plan "
			message = "DLY_PLAN"
		else:
			sql = "select cnt_id, sch_shift from his_dly_plan "
			message = "HIS_DLY_PLAN"

		sql += "where cnt_id=" + str(cnt_id) + " and sch_shift=" + str(shift_id) + " and absent=0 and dly_date='" + str(dly_date) + "'"
		print(sql)

		is_pass = False
		# message = "TEST"




	if phone_status==0:
		if late_status==0:
			if absent_status==0:
				print("TODO")


	# กรณีพนักงานมาทำงาน
	if absent_status==0: 
		if shift_id!="99":			
			# sql = "select cnt_id, sch_shift from dly_plan where cnt_id=" + str(cnt_id) + " and sch_shift=" + str(shift_id) + " and absent=" + str(absent_status) + " and dly_date='" + str(dly_date) + "'"
			sql = "select count(*) from dly_plan where cnt_id=" + str(cnt_id) + " and sch_shift=" + str(shift_id) + " and absent=" + str(absent_status) + " and dly_date='" + str(dly_date) + "'"
			# print("sql 1 = " + str(sql))
			cursor = connection.cursor()
			cursor.execute(sql)
			rows = cursor.fetchone()				
			informedNumber = rows[0]

			sql = "select cnt_id, srv_shif_id, sum(srv_qty) as qty from cus_service where srv_active=1 and cnt_id=" + str(cnt_id) + " and srv_shif_id=" + str(shift_id) + " group by cnt_id, srv_shif_id"
			# print("sql 2 = " + str(sql))
			cursor = connection.cursor()
			cursor.execute(sql)
			rows = cursor.fetchone()
			contractNumber = rows[2]
					
			cursor.close

			# print("informed_number = " + str(informedNumber))
			# print("contract_number = " + str(contractNumber))

			if(informedNumber >= contractNumber):
				is_pass = False
				message += "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา: <b>" + str(cnt_id) + "</b>"
			else:
				is_pass = True
				message += "Rule 1 is passed.<br>"

	else: # กรณีไม่มาทำงาน
		print("todo: employee takes absent")



	# *****************************************
	# RULE 2 - Check phone call status
	# *****************************************
	# TODO
	if is_pass:

		if phone_status:
			if late_status:
				if absent_status and relief_status:
					if shift_id != "99":
						print("")
					else:
						print("")

			is_pass = True # ***Hardcode***


		# TODO: ค่าโทรเป็น 0 ให้ตรวจสอบ
		# if phone_status and phone_amount>0:

		if is_pass:
			message += "Rule 2 is passed.<br>"
		else:
			message += "Rule 2 is failed.<br>"
		

	# ***********************************************
	# RULE 3 - Check valid input
	# ***********************************************
	if is_pass:			
		
		# ***********************************************
		# RULE 3 เช็คห้ามคีย์รหัสที่ไม่มีสิทธ์ลงเวร
		# ตรวจ 3 เงื่อนไข 1.ไม่มีรหัสในระบบ 2.มีแต่สถานะ upd_flag='D' 3. ยังไม่ลาออก emp_term_date=null
		# ***********************************************
		try:
			with connection.cursor() as cursor:		
				cursor.execute("select emp_id, emp_term_date from v_employee where emp_id=%s and upd_flag<>'D'", [emp_id])
				employee = cursor.fetchone()				

		except db.OperationalError as e:
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
		except db.Error as e:
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)

		# is_pass = True if employee[0]>0 else False
		if len(employee)>0:			
			emp_term_date = employee[1]
			# print("emp_term_date = " + str(emp_term_date))
			# print("absent_status = " + str(absent_status))
			# print("relief_status = " + str(relief_status))

			# กรณีพนักงานมาเข้าเวรปกติ
			if absent_status==1 and relief_status==0:
				# ตรวจสอบสถานะการลาออก emp_term_date
				# ถ้าลาออกค่า emp_term_date จะไม่ใช่ค่า Null แต่ใส่เป็นวันที่ที่ลาออก
				if emp_term_date is not None:
					emp_term_date = employee[1].strftime('%d/%m/%Y')
					# print("emp_term_date = " + str(emp_term_date))
					is_pass = False
					message += "Rule 3 is failed: พนักงานคนนี้ไม่สามารถจัดตารางเวรได้ เนื่องจากลาออกตั้งแต่วันที่ " + str(emp_term_date)
				else:
					is_pass = True


			# กรณีพนักงานลาและมีคนลงเวรแทน
			if absent_status==1 and relief_status==1:
				print("TODO")

		else:
			is_pass = False


		if is_pass:
			message += "Rule 3 is passed.<br>"



	# ***********************************************
	# RULE 4 - เช็คจำนวนคนห้ามคีย์เกินในรายการสัญญา กรณีนี้ให้เช็คจาก Missing Record		
	# ***********************************************
	if is_pass:
		if phone_status==1:
			if phone_amount <= 0:
				is_pass = False
				message = "Rule 4 is faled: แจ้งโทรลงบันทึกการเข้าเวร แต่ค่าโทรยังเป็น 0 บาท."

		ot_status = 0 # Hardcode
		if late_status==1 or ot_status:
			print("TODO")

		is_pass = True


	# ***********************************************
	# RULE 5 - ห้ามลงงานที่อื่นในกะเดียวกัน วันเดียวกัน
	# และป้องกันการแก้ไข ปลด Absent รปภ.ที่ขาดหน่วยงานที่นึงแล้วไปอยู่อีกหน่วยงานนึง หากจะปลด Absent ต้องออกจากหน่วยงานที่สองก่อน
	# ***********************************************
	if is_pass:
		if phone_status==1:
			# print("TODO: เช็คพนักงาานเข้าเวรที่หน่วยงานอื่นไปแล้ว")
			is_pass = False


		sql = ""
		#is_error, message = checkBetweenShift(sql)
		#if is_error:
		#	print("TODO: พนักงานเข้าเวรคร่อมกับหน่วยงาน")

		# Hardcode
		is_pass = True
		message += "Rule 5 is passed.<br>"




	# ***********************************************
	# RULE 6 - 	ป้องกันการกลับมาแก้ไข Absent หากรปภ.เข้าเวรอื่นอยู่และเวลาคร่อมกับหน่วยงานอื่น
	# ***********************************************
	if is_pass:
		if relief_status==1:
			print("TODO")

		# Hardcode
		is_pass = True
		message += "Rule 6 is passed.<br>"		


	# ***********************************************
	# RULE 7 - 	ห้ามลงรายการซ้ำ ถ้าเพิ่มรายการใหม่สำหรับคนที่มาแทน แทนหลายคนในหน่วยงานเดียวกันไม่ได้
	# ***********************************************
	if is_pass:
		print("TODO")

		# Hardcode
		is_pass = True
		message += "Rule 7 is passed.<br>"


	# ***********************************************
	# RULE 8 - ห้ามพนักงานทำงานในวัน Day Off จากตาราง SYS_GPMDOF
	# ***********************************************
	# TODO
	# "select cnt_id,sch_shift from v_dlyplan_shift where cnt_id=1486000001 and left(remark,2)=00 and shf_type='D' and absent=0 and dly_date='2020-12-01'"
	if is_pass:
		print("TODO")

		# Hardcode
		is_pass = True
		message += "Rule 8 is passed.<br>"


	# All rules are good then it's good to go
	# *** Not allow CMS_SUP Add/Edit passed day ***

	if is_pass:
		# setVariable()		
		# dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,
		# relief_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM
		upd_date = str(datetime.datetime.now())[:-3]
		sql = "update dly_plan set cnt_id=" + str(cnt_id) + ","		
		sql += "sch_no=0,"
		sql += "dept_id=" + str(emp_dept) + ","
		sql += "sch_rank='" + str(emp_rank) + "',"
		sql += "prd_id='D120121',"
		sql += "absent=" + str(absent_status) + ","
		sql += "late=" + str(late_status) + ","
		sql += "late_full=0,"
		sql += "relieft=" + str(relief_status) + ","
		sql += "relieft_id=0,"
		sql += "tel_man=0,"
		sql += "tel_time=NULL,"
		sql += "tel_amt=0,"
		sql += "tel_paid=0,"
		sql += "ot=0,"
		sql += "ot_reason=0,"
		sql += "ot_time_frm=NULL,"
		sql += "ot_time_to=NULL,"
		sql += "ot_hr_amt=0,"
		sql += "ot_pay_amt=0,"
		sql += "spare=0,"
		sql += "wage_id=32,"
		sql += "wage_no='32SOY',"
		sql += "pay_type='',"
		sql += "soc=0,"
		sql += "pub=0,"
		sql += "dof=0,"
		sql += "day7=0,"
		sql += "upd_date='" + str(upd_date) + "',"
		sql += "upd_by='System',"
		sql += "upd_flag='A',"
		sql += "remark='" + str(job_type) + " " + str(remark) + "' "
		sql += "where cnt_id=" + str(cnt_id)
		sql += " and dly_date='" + str(dly_date) + "'"
		sql += " and emp_id=" + str(emp_id)
		sql += " and sch_shift=" + str(shift_id)

		# print(sql)
	
		try:
			with connection.cursor() as cursor:
				cursor.execute(sql)

			is_pass = True
			message = "บันทึกรายการสำเร็จ"
		except db.OperationalError as e:
			is_pass = False
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
		except db.Error as e:
			is_pass = False
			message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)

	return is_pass, message
'''


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_save_daily_attendance_cross_site(request):
	print("***************************************************")
	print("FUNCTION: ajax_save_daily_attendance_cross_site()")
	print("***************************************************")

	username = request.user.username

	# Initial values
	AEdly = int(request.GET.get("AEdly"))
	Tday7 = 0
	Tdof = 0

	message = ""
	allowZeroBathForPhoneAmount = int(request.GET.get("allowZeroBathForPhoneAmount"))	
	dly_date = datetime.datetime.strptime(request.GET.get('dly_date'), '%d/%m/%Y').date()

	cus_id = request.GET.get('cus_id')
	cus_brn = request.GET.get('cus_brn')
	cus_vol = request.GET.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	cnt_id = cnt_id.lstrip("0")
	emp_id = request.GET.get('emp_id')
	emp_rank = request.GET.get('emp_rank')
	emp_dept = request.GET.get('emp_dept')
	shift_id = request.GET.get('shift_id')
	shift_name = request.GET.get('shift_name')
	
	ui_absent_status = int(request.GET.get('ui_absent_status'))	
	ui_late_status = int(request.GET.get('ui_late_status'))
	ui_phone_status = int(request.GET.get('ui_phone_status'))
	ui_relief_status = int(request.GET.get('ui_relief_status'))

	late_from = request.GET.get('late_from')
	late_to = request.GET.get('late_to')
	late_reason_option = request.GET.get('late_reason_option')
	late_hour = request.GET.get('late_hour')
	late_full_paid_status = request.GET.get('late_full_paid_status')

	if ui_late_status==1:
		late_from = datetime.datetime.strptime(late_from, '%d/%m/%Y %H:%M')
		late_to = datetime.datetime.strptime(late_to, '%d/%m/%Y %H:%M')


	tel_man = request.GET.get('tel_man')
	# print("tel_man:", tel_man)
	# print("ui_phone_status:", ui_phone_status)

	tel_time = request.GET.get('tel_time')
	tel_amount = int(request.GET.get('tel_amount'))	
	
	relief_emp_id = request.GET.get('relief_emp_id')

	ot_status = 0

	job_type = request.GET.get('job_type_option')	

	remark = request.GET.get('remark')
	totalNDP = int(request.GET.get('totalNDP'))
	totalNDA = int(request.GET.get('totalNDA'))
	totalNDM = int(request.GET.get('totalNDM'))
	totalNNP = int(request.GET.get('totalNNP'))
	totalNNA = int(request.GET.get('totalNNA'))
	totalNNM = int(request.GET.get('totalNNM'))
	totalPDP = int(request.GET.get('totalPDP'))
	totalPDA = int(request.GET.get('totalPDA'))
	totalPDM = int(request.GET.get('totalPDM'))
	totalPNP = int(request.GET.get('totalPNP'))
	totalPNA = int(request.GET.get('totalPNA'))
	totalPNM = int(request.GET.get('totalPNM'))	
	search_emp_id = request.GET.get('search_emp_id')

	customer_wage_rate_id = request.GET.get('customer_wage_rate_id')
	customer_zone_id = request.GET.get('customer_zone_id')
	Timecross = request.GET.get('Timecross')	

	if AEdly == 0: # EDIT MODE
		print("Edit Mode")
		
		# print("DEBUG job_type:", job_type)

		is_edit_record_success, message = editRecord(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id,Tday7,Tdof,customer_wage_rate_id,customer_zone_id)
		if is_edit_record_success:
			success_status = True
			title = "Success"
			type_status = "green"
		else:
			success_status = False
			title = "Error"
			type_status = "red"

	elif AEdly == 1: # ADD MODE
		# print("Add Mode")
		
		is_add_record_success, message = addRecord_cross_site(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id,Tday7,Tdof,customer_wage_rate_id,customer_zone_id, Timecross)

		if is_add_record_success:
			success_status = True
			title = "Success"
			type_status = "green"
		else:
			success_status = False
			title = "Error"
			type_status = "red"	
	elif AEdly == 2: # DELETE MODE
		# print("Delete Mode")
		success_status = True
		title = "Success"
		type_status = "green"
		message = "TODO: Delete record"
	else: # UNKNOWN MODE
		# print("Error! unknown mode")
		success_status = False
		title = "Error"
		type_status = "red"
		message = "Unknown request! Please contact IT team."

	response = JsonResponse(data={		
	    "success": success_status,
	    "title": title,
	    "type": type_status,
	    "message": message,
	})

	response.status_code = 200

	# print("LUFY")

	return response




@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_save_daily_attendance(request):
	print("***************************************")
	print("FUNCTION: ajax_save_daily_attendance()")
	print("***************************************")

	username = request.user.username

	# Initial values
	AEdly = int(request.GET.get("AEdly"))
	Tday7 = 0
	Tdof = 0

	message = ""
	allowZeroBathForPhoneAmount = int(request.GET.get("allowZeroBathForPhoneAmount"))

	# Get requested parameters
	# dly_date = request.GET.get('dly_date')
	# dly_date = datetime.datetime.strptime(request.GET.get('dly_date'), '%d/%m/%Y')
	
	dly_date = datetime.datetime.strptime(request.GET.get('dly_date'), '%d/%m/%Y').date()
	# print("dly_date = " + str(dly_date))

	cus_id = request.GET.get('cus_id')
	cus_brn = request.GET.get('cus_brn')
	cus_vol = request.GET.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	cnt_id = cnt_id.lstrip("0")
	emp_id = request.GET.get('emp_id')
	emp_rank = request.GET.get('emp_rank')
	emp_dept = request.GET.get('emp_dept')
	shift_id = request.GET.get('shift_id')
	shift_name = request.GET.get('shift_name')
	
	ui_absent_status = int(request.GET.get('ui_absent_status'))	
	ui_late_status = int(request.GET.get('ui_late_status'))
	ui_phone_status = int(request.GET.get('ui_phone_status'))
	ui_relief_status = int(request.GET.get('ui_relief_status'))

	late_from = request.GET.get('late_from')
	late_to = request.GET.get('late_to')
	late_reason_option = request.GET.get('late_reason_option')
	late_hour = request.GET.get('late_hour')
	late_full_paid_status = request.GET.get('late_full_paid_status')

	if ui_late_status==1:
		late_from = datetime.datetime.strptime(late_from, '%d/%m/%Y %H:%M')
		late_to = datetime.datetime.strptime(late_to, '%d/%m/%Y %H:%M')


	tel_man = request.GET.get('tel_man')
	# print("tel_man:", tel_man)
	# print("ui_phone_status:", ui_phone_status)

	tel_time = request.GET.get('tel_time')
	tel_amount = int(request.GET.get('tel_amount'))	
	
	relief_emp_id = request.GET.get('relief_emp_id')

	ot_status = 0

	job_type = request.GET.get('job_type_option')	

	remark = request.GET.get('remark')
	totalNDP = int(request.GET.get('totalNDP'))
	totalNDA = int(request.GET.get('totalNDA'))
	totalNDM = int(request.GET.get('totalNDM'))
	totalNNP = int(request.GET.get('totalNNP'))
	totalNNA = int(request.GET.get('totalNNA'))
	totalNNM = int(request.GET.get('totalNNM'))
	totalPDP = int(request.GET.get('totalPDP'))
	totalPDA = int(request.GET.get('totalPDA'))
	totalPDM = int(request.GET.get('totalPDM'))
	totalPNP = int(request.GET.get('totalPNP'))
	totalPNA = int(request.GET.get('totalPNA'))
	totalPNM = int(request.GET.get('totalPNM'))	
	search_emp_id = request.GET.get('search_emp_id')

	customer_wage_rate_id = request.GET.get('customer_wage_rate_id')
	customer_zone_id = request.GET.get('customer_zone_id')

	if AEdly == 0: # EDIT MODE
		print("Edit Mode")
		
		# print("DEBUG job_type:", job_type)

		is_edit_record_success, message = editRecord(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id,Tday7,Tdof,customer_wage_rate_id,customer_zone_id)
		if is_edit_record_success:
			success_status = True
			title = "Success"
			type_status = "green"
		else:
			success_status = False
			title = "Error"
			type_status = "red"

	elif AEdly == 1: # ADD MODE
		print("Add Mode")

		is_add_record_success, message = addRecord(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id,Tday7,Tdof,customer_wage_rate_id,customer_zone_id)

		if is_add_record_success:
			success_status = True
			title = "Success"
			type_status = "green"
		else:
			success_status = False
			title = "Error"
			type_status = "red"	
	elif AEdly == 2: # DELETE MODE
		# print("Delete Mode")
		success_status = True
		title = "Success"
		type_status = "green"
		message = "TODO: Delete record"
	else: # UNKNOWN MODE
		# print("Error! unknown mode")
		success_status = False
		title = "Error"
		type_status = "red"
		message = "Unknown request! Please contact IT team."

	response = JsonResponse(data={		
	    "success": success_status,
	    "title": title,
	    "type": type_status,
	    "message": message,
	})

	response.status_code = 200

	print("___END___")

	return response


# ******************************************************
# RULE 1 - เช็คพนักงานที่แจ้งเวรต้องไม่เกินจำนวนอัตราที่ว่าจ้างในสัญญา
# ******************************************************
def checkNotOverCapacity(cnt_id, shift_id, dly_date):
	isPass = False
	message = ""

	cursor = connection.cursor()
	cursor.execute("select count(*) from dly_plan where cnt_id=%s and sch_shift=%s and absent=0 and dly_date=%s", [cnt_id, shift_id, dly_date])
	informCount = cursor.fetchone()
	if informCount[0] == 0:
		informCount = 0
	else:
		informCount = informCount[0]

	cursor.execute("select cnt_id, srv_shif_id, sum(srv_qty) as qty from cus_service where srv_active=1 and cnt_id=%s and srv_shif_id=%s group by cnt_id, srv_shif_id", [cnt_id, shift_id])
	rows = cursor.fetchone()
	cursor.close

	if rows is not None:
		if len(rows)==0:
			srv_qty = 0
		else:
			srv_qty = rows[2]
	else:
		srv_qty = 0

	scheduleCount = srv_qty

	if informCount >= scheduleCount:
		isPass = False
		# message = "พนักงานที่แจ้งเวรมากกว่าที่อยู่ในสัญญา : <b>" + str(cnt_id)[3:] + "</b>"
		message = "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา : <b>" + str(cnt_id) + "</b>"
	else:
		isPass = True
		message = "Pass rule 2"

	return isPass, message


# *****************************************
# RULE 2 - Check Manpower
# *****************************************
def checkManPower(cnt_id, job_type, shift_type, dly_date):
	print(str(cnt_id) + "," + str(job_type) + "," + str(shift_type) + "," + str(dly_date))

	is_error = False
	message = ""
	
	cursor = connection.cursor()
	cursor.execute("select cnt_id, sch_shift from v_dlyplan_shift where cnt_id=%s and left(remark,2)=%s and shf_type=%s and absent=0 and dly_date=%s", [cnt_id, job_type, shift_type, dly_date])
	rows = cursor.fetchone()
	cursor.close	

	if rows is not None:
		# print("no. of rows = " + str(len(rows)))
		if len(rows)==0:
			aManPower = 0
		else:
			aManPower = len(rows)
	else:		
		aManPower = 0
	
	is_error = True if aManPower>0 else False

	# print("is_error = " + str(is_error))
	
	return is_error, message



# *******************************************************************
# RULE 3 - Validate Input
# *******************************************************************
def validateInput(dly_date, cnt_id, emp_id, shift_id, shift_type, shift_name, job_type, totalNDP, totalNDA, totalNDM, totalNNP, totalNNA, totalNNM, totalPDP, totalPDA, totalPDM, totalPNP, totalPNA, totalPNM, absent_status, late_status, phone_status, relief_status):
	isPass = True
	message = ""

	# return True, "AA"

	is_public_holiday, message = isPublicHoliday(dly_date)

	if shift_type=='D':
		if is_public_holiday:
			totalNDA = totalNDA + 1
		else:
			totalPDA = totalPDA + 1
	
	if shift_type=='N':
		if is_public_holiday:
			totalNNA = totalNNA + 1
		else:
			totalPNA = totalPNA + 1

	# Call TOTAL MISS GUARD
	totalNDM, totalNNM, totalPDM, totalPNM = totalMissGuard(totalNDP, totalNDA, totalNNP, totalNNA, totalPDP, totalPDA, totalPNP, totalPNA)

	if is_public_holiday:
		if totalPDM > 0:
			isPass = False
			message = "PD - จำนวน รปภ.ในกะกลางวัน เกินว่าที่ระบุในสัญญา"
			totalPDA = totalPDA - 1
			totalNDM, totalNNM, totalPDM, totalPNM = totalMissGuard(totalNDP, totalNDA, totalNNP, totalNNA, totalPDP, totalPDA, totalPNP, totalPNA)			

		if totalPNM > 0:
			isPass = False
			message = "PD - จำนวน รปภ.ในกะกลางคืน เกินว่าที่ระบุในสัญญา"
			totalPNA = totalPNA - 1
			totalNDM, totalNNM, totalPDM, totalPNM = totalMissGuard(totalNDP, totalNDA, totalNNP, totalNNA, totalPDP, totalPDA, totalPNP, totalPNA)
	else:
		if totalNDM > 0:
			isPass = False
			message = "ND - จำนวน รปภ.ในกะกลางวัน เกินว่าที่ระบุในสัญญา"
			totalNDA = totalNDA - 1
			totalNDM, totalNNM, totalPDM, totalPNM = totalMissGuard(totalNDP, totalNDA, totalNNP, totalNNA, totalPDP, totalPDA, totalPNP, totalPNA)			

		if totalNNM > 0:
			isPass = False
			message = "NN - จำนวน รปภ.ในกะกลางคืน เกินว่าที่ระบุในสัญญา"
			totalNNA = totalNNA - 1
			totalNDM, totalNNM, totalPDM, totalPNM = totalMissGuard(totalNDP, totalNDA, totalNNP, totalNNA, totalPDP, totalPDA, totalPNP, totalPNA)			


	# TODO: checkCall()

	# TODO: checkLate()

	# TODO: ห้ามลงงานที่อื่นในกะเดียวกัน วันเดียวกัน
	# ทำเคสนี้ถ้าเป็นการ Edit


	# TODO: พนักงานเข้าเวรที่หน่วยงานอื่น ต้องการลบออกจากหน่วยงานเดิมหรือไม่
	sql = "select count(*) from dly_plan where dly_date='%s' and emp_id=%s and absent=0 and sch_shift=%s" % (dly_date, emp_id, shift_id)
	is_duplicated, message = checkDupDly(sql)
	if is_duplicated:
		isPass = False
		message = "เข้าเวรที่หน่วยงานอื่นไปแล้วแต่สามารถให้ย้ายมาเข้าเวรที่ใหม่ได้"
	else:
		isPass = True

	# TODO: ห้ามลงงานที่อื่นในเวลาที่คร่อมกัน วันเดียวกัน
	# print("Check 1: checkBetweenShift()")
	sql = "select a.*, b.shf_type, b.shf_time_frm, b.shf_time_to from dly_plan a left join t_shift b on a.sch_shift = b.shf_id where a.dly_date=%s and a.emp_id=%s and a.absent=0" % (dly_date, emp_id)
	is_duplicated, message = checkBetweenShift(sql)
	if is_duplicated:
		isPass = False
		message = ""
	else:
		isPass = True

	# TODO: สำหรับ Employee ID ห้ามลงรายการซ้ำถ้าเพิ่มรายการใหม่	
	if not is_duplicated:
		# print("Check 2: checkDupDly()")
		sql = "select count(*) from dly_plan where cnt_id=%s and dly_date='%s' and emp_id=%s and sch_shift=%s" % (cnt_id, dly_date, emp_id, shift_id)
		is_duplicated, message = checkDupDly(sql)
		if is_duplicated:
			isPass = False
			message = "รหัส : <b>" + str(emp_id) + "</b><br>ตารางเวร : <b>" + shift_name + "</b><br>เป็นรายการซ้ำ กรุณาตรวจสอบอีกครั้ง"
		else:
			isPass = True	
	
	# TODO: ห้ามลงรายการซ้ำ ถ้าเพิ่มรายการใหม่ สำหรับคนที่มาแทน แทนหลายคนในหน่วยเดียวกันไม่ได้
	if not is_duplicated:
		# print("Check 3: checkDupDly()")
		# sql will be revised	
		sql = "select count(*) from dly_plan where cnt_id=%s and dly_date='%s' and emp_id=%s and sch_shift=%s" % (cnt_id, dly_date, emp_id, shift_id)
		is_duplicated, message = checkDupDly(sql)
		if is_duplicated:
			isPass = False
			message = "3) พนักงานรหัส <b>" + str(emp_id) + "</b> มีการแจ้งเวรไปแล้ว กรุณาตรวจสอบอีกครั้ง"
		else:
			isPass = True

	# **** Process takes too long at this step
	# TODO: เช็คห้ามพนักงานทำงานในวัน Day Off จากตาราง SYS_GPMDOF
	'''
	if not is_duplicated:
		if len(emp_id)>0 and int(emp_id)>0 and absent_status==0:
			is_day_off = checkDayOff(emp_id, dly_date)
			if is_day_off:
				isPass = False
				message = "ห้ามพนักงานทำงานในวัน Day Off"
			else:
				isPass = True
	'''


	# TODO: เช็คห้ามพนักงาน Relief ทำงานในวัน Day Off จากตาราง SYS_GPMDOF

	return isPass, message


# **************************
# **** Helper functions ****
# **************************
def isPublicHoliday(curDate):
	isPublicHoliday = False

	cursor = connection.cursor()
	cursor.execute("select count(*) from t_holiday where hol_date=%s", [curDate])
	row_count = cursor.fetchone()
	cursor.close

	if row_count[0] == 0:
		isPublicHoliday = False
		message = str(curDate) + " is public holiday."
	else:
		isPublicHoliday = True
		message = str(curDate) + " is not public holiday."

	return isPublicHoliday, message

def totalMissGuard(totalNDP, totalNDA, totalNNP, totalNNA, totalPDP, totalPDA, totalPNP, totalPNA):
	totalNDM = 0
	totalNNM = 0
	totalPDM = 0
	totalPNM = 0
	totalNDM = totalNDA - totalNDP
	totalNNM = totalNNA - totalNNP
	totalPDM = totalPDA - totalPDP
	totalPNM = totalPNA - totalPNP

	return totalNDM, totalNNM, totalPDM, totalPNM

# def checkDupDly(dly_date, cnt_id, emp_id, shift_id):
def checkDupDly(sql):
	isDuplicated = False
	message = ""

	cursor = connection.cursor()
	cursor.execute(sql)

	duplicateCount = cursor.fetchone()

	if duplicateCount[0] == 0:
		isDuplicated = False
	else:
		isDuplicated = True

	cursor.close

	return isDuplicated, message


# CheckBetweenShift
def checkBetweenShift(sql):
	isDuplicated = True
	message = ""

	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()

	if len(rows) == 0:
		isDuplicated = False
	else:
		isDuplicated = True

	cursor.close

	return isDuplicated, message


def checkDayOff(emp_id, dly_date):
	is_day_off = True
	message = ""

	cursor = connection.cursor()
	cursor.execute("select * from sys_gpmdof where emp_id=%s and dly_date=%s", [emp_id, dly_date])
	rows = cursor.fetchall()

	if len(rows) == 0:
		is_day_off = False
	else:
		is_day_off = True

	cursor.close

	return is_day_off, message



@login_required(login_url='/accounts/login/')
def ajax_is_scheduled_between_site(request):

	'''
	response = JsonResponse(data={"success": True,"is_error": True,"message": "TODO"})
	response.status_code = 200
	return response
	'''

	is_scheduled = True
	message = ""
	Tpub = 0
	DayCurDate = ""
	is_error = False
	shift_status_list = ["0","1"]
	TContractShift = 0
	TDailyShift = 0
	attendance_date = datetime.datetime.strptime(request.POST.get('attendance_date'), '%d/%m/%Y').date()
	CurDate = attendance_date
	shift_id = request.POST.get('shift_id')
	shift_status = request.POST.get('shift_status')
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	username = request.user.username
	upd_date = datetime.datetime.now()
	
	message = "%s,%s,%s,%s,%s" %(attendance_date,shift_id,cus_id,cus_brn,cus_vol)
	print("message:", message)
	print("shift_status:", shift_status)
	print("attendance_date:", attendance_date)

	# Field validation
	if shift_status not in shift_status_list:
		response = JsonResponse(data={"success": True, "is_error": True, "is_scheduled:": is_scheduled , "message": "เลือกสถานะการลาไม่ถูกต้อง"})
		response.status_code = 200
		return response
	else:
		if shift_status=="0": # Not Absent
			TContractShift = 0
			TDailyShift = 0
			
			Tpub = 1 if getDayPub(attendance_date)==1 else 0
			DateOfWeek = int(attendance_date.strftime('%w'))
			# Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.

			if DateOfWeek==0:
				DayCurDate = "SRV_SUN"
			elif DateOfWeek==1:
				DayCurDate = "SRV_MON"
			elif DateOfWeek==2:
				DayCurDate = "SRV_TUE"
			elif DateOfWeek==3:
				DayCurDate = "SRV_WED"
			elif DateOfWeek==4:
				DayCurDate = "SRV_THU"
			elif DateOfWeek==5:
				DayCurDate = "SRV_FRI"
			elif DateOfWeek==6:
				DayCurDate = "SRV_SAT"
			else:
				DayCurDate = 99

			print("DayCurDate:", DayCurDate)

			if DayCurDate==99:
				response = JsonResponse(data={"success": True, "is_error": True,  "is_scheduled:": True, "message": "วันที่ทำงานไม่ถูกต้อง กรุณาตรวจสอบ"})
				response.status_code = 200
				return response
			
			sql = "select cnt_id,srv_shif_id, sum(" + str(DayCurDate) + ") as srv_num"
			sql += " from cus_service where cnt_id=" + str(cnt_id)
			sql += " and srv_shif_id=" + str(shift_id)
			sql += " and srv_active=1 and upd_flag<>'D' "
			sql += " group by cnt_id, srv_shif_id"
			print("SQL TContractShift:", sql)

			try:
				with connection.cursor() as cursor:		
					cursor.execute(sql)
					cus_service_obj = cursor.fetchone()

				if cus_service_obj is not None:					
					TContractShift = cus_service_obj[2] # get srv_num value								
			except db.OperationalError as e:
				response = JsonResponse(data={"success": True, "is_error": True, "is_scheduled:": True, "message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response
			except db.Error as e:
				response = JsonResponse(data={"success": True,"is_error": True,  "is_scheduled:": True, "message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response

			sql = "select cnt_id,sch_shift,count(emp_id) as srv_num from dly_plan"
			sql += " where cnt_id=" + str(cnt_id)
			sql += " and sch_shift=" + str(shift_id)
			sql += " group by cnt_id, sch_shift"
			print("SQL TContractShift:", sql)
			try:
				with connection.cursor() as cursor:		
					cursor.execute(sql)
					dly_plan_obj = cursor.fetchone()

				if dly_plan_obj is not None:					
					TDailyShift = dly_plan_obj[2] # get srv_num value
			except db.OperationalError as e:
				response = JsonResponse(data={"success": True, "is_error": True, "is_scheduled:": True, "message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response
			except db.Error as e:
				response = JsonResponse(data={"success": True, "is_error": True, "is_scheduled:": True, "message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response


			print("TContractShift=", TContractShift)
			print("TDailyShift=", TDailyShift)

			if int(TContractShift) >= int(TDailyShift):				
				sql = "select cnt_id,emp_id,sch_shift,shf_type from v_dlyplan "
				sql += " where cnt_id=" + str(cnt_id)
				sql += " and sch_shift=" + str(shift_id)
				print("sql11:", sql)

				try:
					with connection.cursor() as cursor:		
						cursor.execute(sql)
						v_dlyplan_obj = cursor.fetchall()
						cursor.close()

					if v_dlyplan_obj is not None:					
						number_of_record = len(v_dlyplan_obj)						

						# Begin tran
						for i in range(0,number_of_record):
							tmp_cnt_id = v_dlyplan_obj[i][0]
							tmp_emp_id = v_dlyplan_obj[i][1]
							tmp_shf_type = v_dlyplan_obj[i][3]

							message = "%s,%s,%s" %(tmp_cnt_id, tmp_emp_id, tmp_shf_type)

							sql = "select * from v_dlyplan where emp_id=" + str(tmp_emp_id) + " and absent=0 and shf_type='" + str(tmp_shf_type) + "'"
							# print("DEBUG sql 11: ", sql)
							cursor = connection.cursor()
							cursor.execute(sql)
							v_dlyplan_obj = cursor.fetchone()
							cursor.close()

							if v_dlyplan_obj is not None:

								# DlyPerRs[i][38]
								message = "พนักงานรหัส <b>" + str(tmp_emp_id) + "</b> ได้แจ้งเวรเข้าหน่วยงาน <b>" + str(v_dlyplan_obj[13]) + "</b> ในกะ <b>" + str(v_dlyplan_obj[3]) + "</b> ไว้แล้ว "
								message += "ระบบไม่อนุญาติให้ทำรายการของพนังงานท่านนี้<br>"
								message += "<hr>หากต้องการบันทึกการแจ้งเวรของพนักงานที่เหลือ กรุณากดปุ่มยืนยัน"
								
								response = JsonResponse(data={"success": True, "is_error": True, "is_over_capacity": False, "is_scheduled:": True, "message": message})
								response.status_code = 200
								return response
							else:
								response = JsonResponse(data={"success": True,"is_error": False, "is_over_capacity": False, "is_scheduled:": False, "message": "Good to go"})
								response.status_code = 200
								return response								
				except db.OperationalError as e:
					response = JsonResponse(data={"success": True,"is_error": True, "is_over_capacity": False, "is_scheduled:": True, "message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
					response.status_code = 200
					return response
				except db.Error as e:
					response = JsonResponse(data={"success": True,"is_error": True, "is_over_capacity": False, "is_scheduled:": True, "message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
					response.status_code = 200
					return response
			else:
				# response = JsonResponse(data={"success": True, "is_error": True, "is_scheduled:": True, "message": "ไม่สามารถทำรายการได้เนื่องจาก <b>จำนวนพนักงานทำงานมากกว่าสัญญาการให้บริการ</b>"})
				
				message = "ไม่สามารถทำรายการได้เนื่องจาก <b>จำนวนพนักงานเกินสัญญาการให้บริการ</b> "
				message += "(จำนวนพนักงาน <b>" + str(TDailyShift) + "</b> อัตรา | จำนวนในสัญญา <b> " + str(TContractShift) + "</b> อัตรา)"
				response = JsonResponse(data={"success": True, "is_error": True, "is_over_capacity": True, "is_scheduled:": True, "message": message})
				response.status_code = 200
				return response
			
		else: # Absent

			sql = "update dly_plan set "
			sql += "absent=1, "
			sql += "late=0, "
			sql += "late_full=0, "
			sql += "relieft=0, "
			sql += "relieft_id=0, "
			sql += "tel_man=0, "
			sql += "tel_time=null, "
			sql += "tel_amt=0, "
			sql += "tel_paid=0, "
			sql += "ot=0, "
			sql += "ot_reason=0, "
			sql += "ot_time_frm=null, "
			sql += "ot_time_to=null, "
			sql += "ot_hr_amt=0, "
			sql += "ot_pay_amt=0, "

			sql += "upd_by='" + str(username) + "'"
			sql += ",upd_date='" + str(upd_date)[:-10] + "'"
			sql += ",upd_flag='E'"
			sql += " where dly_date='" + str(CurDate) + "'"
			sql += " and sch_shift=" + str(shift_id)
			sql += " and cnt_id=" + str(cnt_id)
			# print("sql:", sql)

			try:
				with connection.cursor() as cursor:		
					cursor.execute(sql)					
				message = "ปรับสถานะการเข้างานเป็น <b>Absent</b> สำเร็จ"

			except db.OperationalError as e:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response
			except db.Error as e:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response		
			finally:
				cursor.close()

	response = JsonResponse(data={"success": True,"is_error": is_error,"message": message})
	response.status_code = 200
	return response



@login_required(login_url='/accounts/login/')
def ajax_bulk_update_absent_status(request):

	'''
	response = JsonResponse(data={"success": True,"is_error": True,"message": "TODO"})
	response.status_code = 200
	return response
	'''

	message = ""
	Tpub = 0
	DayCurDate = ""
	is_error = False
	shift_status_list = ["0","1"]
	TContractShift = 0
	TDailyShift = 0
	attendance_date = datetime.datetime.strptime(request.POST.get('attendance_date'), '%d/%m/%Y').date()
	CurDate = attendance_date
	shift_id = request.POST.get('shift_id')
	shift_status = request.POST.get('shift_status')
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	skip_is_scheduled_record = request.POST.get('skip_is_scheduled_record')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	username = request.user.username
	upd_date = datetime.datetime.now()
	
	print("skip_is_scheduled_record : ", skip_is_scheduled_record)

	# message = "%s,%s,%s,%s,%s" %(attendance_date,shift_id,cus_id,cus_brn,cus_vol)
	# print("message:", message)
	# print("shift_status:", shift_status)
	# print("attendance_date:", attendance_date)

	# Field validation
	if shift_status not in shift_status_list:
		response = JsonResponse(data={"success": True,"is_error": True,"message": "เลือกสถานะการลาไม่ถูกต้อง"})
		response.status_code = 200
		return response
	else:
		if shift_status=="0": # Not Absent
			TContractShift = 0
			TDailyShift = 0
			
			Tpub = 1 if getDayPub(attendance_date)==1 else 0
			DateOfWeek = int(attendance_date.strftime('%w'))
			# Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.

			print("Attendance Date:", attendance_date)
			print("DateOfWeek:", DateOfWeek)

			if DateOfWeek==0:
				DayCurDate = "SRV_SUN"
			elif DateOfWeek==1:
				DayCurDate = "SRV_MON"
			elif DateOfWeek==2:
				DayCurDate = "SRV_TUE"
			elif DateOfWeek==3:
				DayCurDate = "SRV_WED"
			elif DateOfWeek==4:
				DayCurDate = "SRV_THU"
			elif DateOfWeek==5:
				DayCurDate = "SRV_FRI"
			elif DateOfWeek==6:
				DayCurDate = "SRV_SAT"
			else:
				DayCurDate = 99

			print("DayCurDate:", DayCurDate)

			if DayCurDate==99:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "วันที่ทำงานไม่ถูกต้อง กรุณาตรวจสอบ"})
				response.status_code = 200
				return response
			
			# print("attendance_date:", attendance_date)
			# print("DateOfWeek:", DateOfWeek)
			# print("DayCurDate:", DayCurDate)

			sql = "select cnt_id,srv_shif_id, sum(" + str(DayCurDate) + ") as srv_num"
			sql += " from cus_service where cnt_id=" + str(cnt_id)
			sql += " and srv_shif_id=" + str(shift_id)
			sql += " and srv_active=1 and upd_flag<>'D' "
			sql += " group by cnt_id, srv_shif_id"
			print("SQL TContractShift:", sql)

			try:
				with connection.cursor() as cursor:		
					cursor.execute(sql)
					cus_service_obj = cursor.fetchone()

				if cus_service_obj is not None:					
					TContractShift = cus_service_obj[2] # get srv_num value								
			except db.OperationalError as e:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response
			except db.Error as e:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response

			sql = "select cnt_id,sch_shift,count(emp_id) as srv_num from dly_plan"
			sql += " where cnt_id=" + str(cnt_id)
			sql += " and sch_shift=" + str(shift_id)
			sql += " group by cnt_id, sch_shift"
			print("SQL TContractShift:", sql)
			try:
				with connection.cursor() as cursor:		
					cursor.execute(sql)
					dly_plan_obj = cursor.fetchone()

				if dly_plan_obj is not None:					
					TDailyShift = dly_plan_obj[2] # get srv_num value
			except db.OperationalError as e:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response
			except db.Error as e:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response


			print("TContractShift=", TContractShift)
			print("TDailyShift=", TDailyShift)

			if int(TContractShift) >= int(TDailyShift):				
				sql = "select cnt_id,emp_id,sch_shift,shf_type from v_dlyplan "
				sql += " where cnt_id=" + str(cnt_id)
				sql += " and sch_shift=" + str(shift_id)
				print("sql11:", sql)

				try:
					with connection.cursor() as cursor:		
						cursor.execute(sql)
						v_dlyplan_obj = cursor.fetchall()
						cursor.close()

					if v_dlyplan_obj is not None:					
						number_of_record = len(v_dlyplan_obj)						
						skip_emp_id = None

						# Begin tran
						for i in range(0,number_of_record):
							tmp_cnt_id = v_dlyplan_obj[i][0]
							tmp_emp_id = v_dlyplan_obj[i][1]
							tmp_shf_type = v_dlyplan_obj[i][3]

							message = "%s,%s,%s" %(tmp_cnt_id, tmp_emp_id, tmp_shf_type)

							# sql = "select emp_id from v_dlyplan where emp_id=" + str(tmp_emp_id) + " and absent=1 and shf_type='" + str(tmp_shf_type) + "'"
							sql = "select emp_id from v_dlyplan where emp_id=" + str(tmp_emp_id) + " and absent=0 and shf_type='" + str(tmp_shf_type) + "'"
							print("SQL : ", sql)
							cursor = connection.cursor()
							cursor.execute(sql)
							emp_obj = cursor.fetchone()
							cursor.close()

							
							'''
							if count>0:
								message = "พนักงานรหัส <b>" + str(tmp_emp_id) + "</b> ทำงานที่หน่วยงาน <b>" + str(tmp_cnt_id) + "</b> ในกะ <b>" + str(tmp_shf_type) + "</b> เรียบร้อยแล้ว กรุณาตรวจสอบอีกครั้ง"
								response = JsonResponse(data={"success": True,"is_error": True,"message": message})
								response.status_code = 200
								return response
							'''

							# print("tmp_emp_id = ", tmp_emp_id)
							# print("skip_emp_id = ", emp_obj[0])
							
							# skip_is_scheduled_record
							if emp_obj is not None:
								skip_emp_id = emp_obj[0]

							# print("skip_emp_id = ", emp_obj[0])

							if skip_is_scheduled_record=="1":

								print("tmp_emp_id = " + str(tmp_emp_id) + " | skip_emp_id = " + str(skip_emp_id))

								if skip_emp_id==tmp_emp_id:
									print("Skip emp id : ", tmp_emp_id)
								else:
									print("Not skip emp id : ", tmp_emp_id)
									sql = "update dly_plan set "
									sql += "absent=0, "

									sql += "late=0, "
									sql += "late_full=0, "
									sql += "relieft=0, "
									sql += "relieft_id=0, "
									sql += "tel_man=0, "
									sql += "tel_time=null, "
									sql += "tel_amt=0, "
									sql += "tel_paid=0, "
									sql += "ot=0, "
									sql += "ot_reason=0, "
									sql += "ot_time_frm=null, "
									sql += "ot_time_to=null, "
									sql += "ot_hr_amt=0, "
									sql += "ot_pay_amt=0, "

									sql += "upd_by='" + str(username) + "'"
									sql += ",upd_date='" + str(upd_date)[:-10] + "'"
									sql += ",upd_flag='E'"
									sql += " where dly_date='" + str(CurDate) + "'"
									sql += " and sch_shift=" + str(shift_id)
									sql += " and emp_id=" + str(tmp_emp_id)
									sql += " and cnt_id=" + str(tmp_cnt_id)

									print("DEBUG SQL:", sql)
									cursor = connection.cursor()
									cursor.execute(sql)
									cursor.close()

							else:
								print("UPDATE ALL")
								sql = "update dly_plan set "
								sql += "absent=0, "

								sql += "late=0, "
								sql += "late_full=0, "
								sql += "relieft=0, "
								sql += "relieft_id=0, "
								sql += "tel_man=0, "
								sql += "tel_time=null, "
								sql += "tel_amt=0, "
								sql += "tel_paid=0, "
								sql += "ot=0, "
								sql += "ot_reason=0, "
								sql += "ot_time_frm=null, "
								sql += "ot_time_to=null, "
								sql += "ot_hr_amt=0, "
								sql += "ot_pay_amt=0, "

								sql += "upd_by='" + str(username) + "'"
								sql += ",upd_date='" + str(upd_date)[:-10] + "'"
								sql += ",upd_flag='E'"
								sql += " where dly_date='" + str(CurDate) + "'"
								sql += " and sch_shift=" + str(shift_id)
								sql += " and emp_id=" + str(tmp_emp_id)
								sql += " and cnt_id=" + str(tmp_cnt_id)

								print("DEBUG SQL:", sql)
								cursor = connection.cursor()
								cursor.execute(sql)
								cursor.close()

						message = "ปรับสถานะการเข้างานเป็น <b>Not Absent</b> สำเร็จ"
						response = JsonResponse(data={"success": True, "is_error": False, "message": message})
						response.status_code = 200
						return response

				except db.OperationalError as e:
					response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
					response.status_code = 200
					return response
				except db.Error as e:
					response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
					response.status_code = 200
					return response
			else:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "จำนวนพนักงานทำงานมากกว่าสัญญาการให้บริการ"})
				response.status_code = 200
				return response
				
			
		else: # Absent

			sql = "update dly_plan set "
			sql += "absent=1, "
			sql += "late=0, "
			sql += "late_full=0, "
			sql += "relieft=0, "
			sql += "relieft_id=0, "
			sql += "tel_man=0, "
			sql += "tel_time=null, "
			sql += "tel_amt=0, "
			sql += "tel_paid=0, "
			sql += "ot=0, "
			sql += "ot_reason=0, "
			sql += "ot_time_frm=null, "
			sql += "ot_time_to=null, "
			sql += "ot_hr_amt=0, "
			sql += "ot_pay_amt=0, "

			sql += "upd_by='" + str(username) + "'"
			sql += ",upd_date='" + str(upd_date)[:-10] + "'"
			sql += ",upd_flag='E'"
			sql += " where dly_date='" + str(CurDate) + "'"
			sql += " and sch_shift=" + str(shift_id)
			sql += " and cnt_id=" + str(cnt_id)
			# print("sql:", sql)

			try:
				with connection.cursor() as cursor:		
					cursor.execute(sql)					
				message = "ปรับสถานะการเข้างานเป็น <b>Absent</b> สำเร็จ"
			except db.OperationalError as e:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response
			except db.Error as e:
				response = JsonResponse(data={"success": True,"is_error": True,"message": "<b>Please send this error to IT team or try again.</b><br>" + str(e)})
				response.status_code = 200
				return response		
			finally:
				cursor.close()

	response = JsonResponse(data={"success": True,"is_error": is_error,"message": message})
	response.status_code = 200
	return response



def DropTable(table_name):
	is_success = False
	message = ""

	sql = "if exists (select * from sysobjects where id=object_id('" + str(table_name) + "')) drop table " + str(table_name)
	try:
		with connection.cursor() as cursor:		
			cursor.execute(sql)

		# print("Log: drop table " + str(table_name) + " success")
		is_success = True
		message = "Drop table success"
	except db.OperationalError as e:
		is_success = False
		message = "<b>Please send this error to IT team.</b><br>" + str(e)
	except db.Error as e:
		is_success = False
		message = "<b>Please send this error to IT team.</b><br>" + str(e)
	finally:
		cursor.close()
	
	return is_success, message


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def SearchDailyGurdPerformance(request):
	is_error = True
	message = ""
	emp_id = request.POST.get('emp_id')
	user_first_name = request.user.first_name
	
	search_date_from = datetime.datetime.strptime(request.POST.get('search_date_from'), '%d/%m/%Y').date()
	search_date_to = datetime.datetime.strptime(request.POST.get('search_date_to'), '%d/%m/%Y').date()

	performance_list = None
	overtime_list = None
	schedule_list = None
	substitue_list = None
	leave_list = None
	emp_leave_plan_list = None
	absent_dly_plan_list = None
	
	'''
	message = "%s | %s | %s" %(emp_id, search_date_from, search_date_to)	
	response = JsonResponse(data={"success": True,"is_error": is_error,"message": message})
	response.status_code = 200
	return response	
	'''

	# Call ChkValidInput(1)
	if (emp_id=="") or (search_date_from=="") or (search_date_to==""):
		message = "ป้อนข้อมูลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง"
		response = JsonResponse(data={"success": True,"is_error": True,"message": message})
		response.status_code = 200
		return response	

	# TODO: validate Start Date must not over than End Date

	# TODO: validate emp_id is existed
	sql = "select count(*) from v_hdlyplan where emp_id=" + str(emp_id)
	try:
		with connection.cursor() as cursor:		
			cursor.execute(sql)
			count = cursor.fetchone()[0]

		if count <= 0:
			is_error = True
			message = "รหัสพนักงาน <b>" + str(emp_id) + "</b> ไม่มีอยู่ในระบบ"
		else:
			is_error = False
			message = "Pass"

	except db.OperationalError as e:
		response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
		response.status_code = 200
		return response
	except db.Error as e:
		response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
		response.status_code = 200
		return response		
	finally:
		cursor.close()

	# if emp_id is existed
	# TODO: drop all 5 user tables (usertable, usertable1, usertable2, usertable3, usertable4)
	is_drop_table_success, message = DropTable(user_first_name)

	if is_drop_table_success:		
		DropTable(user_first_name + "1")
		DropTable(user_first_name + "2")
		DropTable(user_first_name + "3")
		DropTable(user_first_name + "4")

		sql = "select distinct * into " + str(user_first_name + "1") + " from v_hdlyplan "
		sql += "where emp_id=" + str(emp_id) + " "
		sql += "and dly_date>='" + str(search_date_from) + "' "
		sql += "and dly_date<='" + str(search_date_to) + "'"
		
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		except db.Error as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		finally:
			cursor.close()


		sql = "alter table " + str(user_first_name + "1") + " add Customer_Flag nvarchar(1) NULL"
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		except db.Error as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		finally:
			cursor.close()


		sql = "select distinct * into " + str(user_first_name + "2") + " from v_dlyplan "
		sql += "where emp_id=" + str(emp_id) + " "
		sql += "and dly_date>='" + str(search_date_from) + "' "
		sql += "and dly_date<='" + str(search_date_to) + "'"
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		except db.Error as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		finally:
			cursor.close()


		sql = "select distinct * into " + str(user_first_name + "3") + " from v_dlyplan "
		sql += "where relieft_id=" + str(emp_id) + " "
		sql += "and dly_date>='" + str(search_date_from) + "' "
		sql += "and dly_date<='" + str(search_date_to) + "'"
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		except db.Error as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		finally:
			cursor.close()


		sql = "select distinct * into " + str(user_first_name + "4") + " from v_hdlyplan "
		sql += "where relieft_id=" + str(emp_id) + " "
		sql += "and dly_date>='" + str(search_date_from) + "' "
		sql += "and dly_date<='" + str(search_date_to) + "'"
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		except db.Error as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		finally:
			cursor.close()

		sql = "alter table " + str(user_first_name + "4") + " add Customer_Flag nvarchar(1) NULL"
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		except db.Error as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		finally:
			cursor.close()


		sql = "select * into " + str(user_first_name) + " " 
		sql += "from " + str(user_first_name + "1") + " "
		sql += "union select * from " + str(user_first_name + "2") + " "
		sql += "union select * from " + str(user_first_name + "3") + " "
		sql += "union select * from " + str(user_first_name + "4") + " "
		# print("SQL:", sql)

		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		except db.Error as e:
			response = JsonResponse(data={"success": True, "is_error": True, "message": "<b>Please send this error to IT team.</b><br>" + str(e)})
			response.status_code = 200
			return response
		finally:
			cursor.close()


		# TODO: Call DisplayList("DLY_PLAN")
		is_error, error_message, performance_list, income_list = DisplayList("DLY_PLAN", user_first_name, emp_id, search_date_from, search_date_to)
		if is_error:
			is_error = True
			message = error_message
		else:
			is_error = False
			message = error_message


		# TODO: Call DisplayList("DLY_OT")		
		is_error, error_message, overtime_list = DisplayList("DLY_OT", user_first_name, emp_id, search_date_from, search_date_to)
		if is_error:
			is_error = True
			message = error_message
		else:
			is_error = False
			message = error_message


		# TODO: Call DisplayList("DLY_SUB")
		is_error, error_message, substitute_list = DisplayList("DLY_SUB", user_first_name, emp_id, search_date_from, search_date_to)
		if is_error:
			is_error = True
			message = error_message
		else:
			is_error = False
			message = error_message



		# TODO: Call DisplayList("SCH_PLAN")
		is_error, error_message, schedule_list = DisplayList("SCH_PLAN", user_first_name, emp_id, search_date_from, search_date_to)
		if is_error:
			is_error = True
			message = error_message
		else:
			is_error = False
			message = error_message



		# TODO: Call DisplayList("EMP_LEAVE_ACT")
		is_error, error_message, leave_list = DisplayList("EMP_LEAVE_ACT", user_first_name, emp_id, search_date_from, search_date_to)
		if is_error:
			is_error = True
			message = error_message
		else:
			is_error = False
			message = error_message



		# TODO: Call DisplayList("EMP_LEAVE_PLAN")
		is_error, error_message, emp_leave_plan_list = DisplayList("EMP_LEAVE_PLAN", user_first_name, emp_id, search_date_from, search_date_to)
		if is_error:
			is_error = True
			message = error_message
		else:
			is_error = False
			message = error_message



		# TODO: Call DisplayList("ABSENT_DLY_PLAN")
		is_error, error_message, absent_dly_plan_list = DisplayList("ABSENT_DLY_PLAN", user_first_name, emp_id, search_date_from, search_date_to)
		if is_error:
			is_error = True
			message = error_message
		else:
			is_error = False
			message = error_message


		'''
		DropTable(user_first_name)
		DropTable(user_first_name + "1")
		DropTable(user_first_name + "2")
		DropTable(user_first_name + "3")
		DropTable(user_first_name + "4")		
		'''
	else:
		is_error = True
		message = "Can't drop table " + str(user_first_name)

	response = JsonResponse(data={"success": True,"is_error": is_error,"message": message, 
		"performance_list": performance_list, "income_list": income_list, "overtime_list":overtime_list, 
		"schedule_list": schedule_list, "substitute_list":substitute_list, "leave_list":leave_list, 
		"emp_leave_plan_list": emp_leave_plan_list, "absent_dly_plan_list": absent_dly_plan_list})

	response.status_code = 200
	return response	


def DisplayList(table_name, user_first_name, emp_id, search_date_from, search_date_to):

	# ABSENT_DLY_PLAN
	if(table_name=="ABSENT_DLY_PLAN"):
		is_error = True
		message = "<b>ABSENT_DLY_PLAN</b>: "
		DlyPerRs_ABSENTDLYPLAN = None
		sql = "select emp_id,dly_date,cnt_id,sch_shift,shf_desc,upd_date,upd_by,upd_flag from " + str(user_first_name) + " "		
		sql += "where emp_id=" + str(emp_id) + " "
		sql += "and absent=1 and sch_shift<>99 and year(dly_date)=year(getdate()) "
		sql += "order by dly_date desc"
		# print("ABSENT_DLY_PLAN SQL:", sql)
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
				DlyPerRs_ABSENTDLYPLAN = cursor.fetchall()
			message += "Success"
			is_error = False
		except db.OperationalError as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		finally:
			cursor.close()		
		return is_error, message, DlyPerRs_ABSENTDLYPLAN


	# EMP_LEAVE_PLAN
	if(table_name=="EMP_LEAVE_PLAN"):
		is_error = True
		message = "<b>EMP_LEAVE_PLAN</b>: "
		DlyPerRs_EMPLEAVEPLAN = None
		sql = "select b.*,c.lve_th from v_employee as a left join emp_leave_plan as b on a.emp_id=b.emp_id "
		sql += "left join t_leave as c on b.lve_id=c.lve_id "
		sql += "where a.emp_id= " + str(emp_id) + " "
		sql += "and b.lve_year>=year(getdate())"
		# print("EMP_LEAVE_PLAN SQL:", sql)

		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
				DlyPerRs_EMPLEAVEPLAN = cursor.fetchall()
			message += "Success"
			is_error = False
		except db.OperationalError as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		finally:
			cursor.close()		
		return is_error, message, DlyPerRs_EMPLEAVEPLAN


	# EMP_LEAVE_ACT
	if(table_name=="EMP_LEAVE_ACT"):
		is_error = True
		message = "<b>EMP_LEAVE_ACT</b>: "
		DlyPerRs_EMPLEAVEACT = None

		sql = "select b.*,c.lve_th from v_employee as a left join emp_leave_act as b on a.emp_id=b.emp_id "
		sql += "left join t_leave as c on b.lve_id=c.lve_id "		
		sql += "where a.emp_id= " + str(emp_id) + " and b.lve_date_frm>='" + str(search_date_from) + "' "	
		# print("EMP_LEAVE_ACT SQL:", sql)
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
				DlyPerRs_EMPLEAVEACT = cursor.fetchall()
			message += "Success"
			is_error = False
		except db.OperationalError as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		finally:
			cursor.close()		
		return is_error, message, DlyPerRs_EMPLEAVEACT


	# DLY_SUB
	if(table_name=="DLY_SUB"):
		is_error = True
		message = "<b>DLY_SUB</b>: "
		DlyPerRs_DLYSUB = None
		sql = "select distinct * from " + str(user_first_name) + " where relieft_id=" + str(emp_id) + " "
		sql += "and dly_date>='" + str(search_date_from) + "' "
		sql += "and dly_date<='" + str(search_date_to) + "' "
		sql += "order by sch_shift"
		# print("DLY_SUB SQL:", sql)
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
				DlyPerRs_DLYSUB = cursor.fetchall()
			message += "Success"
			is_error = False
		except db.OperationalError as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		finally:
			cursor.close()		
		return is_error, message, DlyPerRs_DLYSUB


	# SCH_PLAN
	if(table_name=="SCH_PLAN"):
		is_error = True
		message = "<b>SCH_PLAN</b>: "
		DlyPerRs_SCHPLAN = None

		sql = "select b.*,k.emp_fname_th,k.emp_lname_th,"
		sql += "c.shf_desc as shf_mon,"
		sql += "d.shf_desc as shf_tue,"
		sql += "e.shf_desc as shf_wed,"
		sql += "f.shf_desc as shf_thu,"
		sql += "g.shf_desc as shf_fri,"
		sql += "h.shf_desc as shf_sat,"
		sql += "i.shf_desc as shf_sun "
		sql += "from cus_contract as a left join sch_plan as b on a.cnt_id=b.cnt_id "
		sql += "left join v_employee as k on b.emp_id=k.emp_id "		
		sql += "left join t_shift as c on b.sch_shf_mon=c.shf_id "
		sql += "left join t_shift as d on b.sch_shf_tue=d.shf_id "
		sql += "left join t_shift as e on b.sch_shf_wed=e.shf_id "
		sql += "left join t_shift as f on b.sch_shf_thu=f.shf_id "
		sql += "left join t_shift as g on b.sch_shf_fri=g.shf_id "
		sql += "left join t_shift as h on b.sch_shf_sat=h.shf_id "
		sql += "left join t_shift as i on b.sch_shf_sun=i.shf_id "		
		sql += "where b.emp_id=" + str(emp_id) + " "
		sql += "and b.upd_flag<>'D' "
		sql += "order by sch_date_frm desc, sch_no asc"
		# print("SQL debug:", sql)
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
				DlyPerRs_SCHPLAN = cursor.fetchall()
			message += "Success"
			is_error = False
		except db.OperationalError as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		finally:
			cursor.close()

		return is_error, message, DlyPerRs_SCHPLAN


	# DLY_OT
	if(table_name=="DLY_OT"):
		is_error = True
		message = "<b>DLY_OT</b>: "
		DlyPerRs_DLYOT = None
		sql = "select distinct "
		sql += "absent,sch_no,emp_id,dly_date,emp_fname_th,sch_rank,shf_desc,prd_id,cnt_id,relieft,relieft_id,remp_fname_th,remp_lname_th,tel_man,"
		sql += "tel_time,tel_amt,tel_paid,ot,ot_reason,ot_res_th,ot_time_frm,ot_time_to,ot_hr_amt,ot_pay_amt,spare,wage_id,pay_type,soc,pub,paid,shf_type,remark,sch_shift "
		sql += "from " + str(user_first_name) + " where emp_id=" + str(emp_id) + " and ot_hr_amt>0 "
		sql += "and dly_date>='" + str(search_date_from) + "' "
		sql += "and dly_date<='" + str(search_date_to) + "' "
		sql += "order by sch_shift"
		# print("DLY_OT SQL:", sql)
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
				DlyPerRs_DLYOT = cursor.fetchall()
			message += "Success"
			is_error = False
		except db.OperationalError as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message += message + "Error! Please send this error to IT team.<br>" + str(e)
			return is_error, message
		finally:
			cursor.close()
		return is_error, message, DlyPerRs_DLYOT


	# DLY_PLAN
	if (table_name=="DLY_PLAN"):
		is_error = True
		message = "<b>DLY_PLAN</b>: "
		DlyPerRs = None
		income_list = []

		# UPDATE 1
		sql = "update " + str(user_first_name) + " "
		sql += "set shf_amt_hr = ot_hr_amt "
		sql += "where (ot_hr_amt<>0 and relieft_id<>0) "
		sql += "or (ot_hr_amt<>0 and pay_type='TPA')"
		# print("SQL:", sql)
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		finally:
			cursor.close()
		
		#return is_error, message, DlyPerRs, income_list


		# UPDATE 2
		sql = "update "	+ str(user_first_name) + " "
		sql += "set shf_amt_hr = (shf_amt_hr + ot_hr_amt) "
		sql += "where (ot_hr_amt<>0 and relieft_id<>0) "
		sql += "or (ot_hr_amt<>0 and pay_type<>'TPA')"
		try:
			with connection.cursor() as cursor:
				cursor.execute(sql)
		except db.OperationalError as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		finally:
			cursor.close()


		# UPDATE 3
		sql = "update " + str(user_first_name) + " "
		sql += "set shf_amt_hr='0' "
		sql += "where left(ltrim(shf_desc),3)='999' "
		sql += "and absent='1'"
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		finally:
			cursor.close()

		# DlyPerRs		
		sql = "select distinct * from " + str(user_first_name) + " "
		sql += "where emp_id=" + str(emp_id) + " "
		sql += "and dly_date>='" + str(search_date_from) + "' "
		sql += "and dly_date<='" + str(search_date_to) + "' "
		sql += "order by dly_date, sch_shift"
		# print("sql DlyPerRs: ", sql)
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
				DlyPerRs = cursor.fetchall()			
		except db.OperationalError as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		finally:
			cursor.close()

		sql = "if exists (select * from dbo.sysobjects where id=object_id(N'[dbo].[R_D500]') and OBJECTPROPERTY(id,N'IsUserTable')=1) "
		sql += "drop table [dbo].[R_D500]"
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		finally:
			cursor.close()



		sql = "select distinct emp_id,rtrim(emp_fname_th)+' ' + rtrim(emp_lname_th) as fname,cnt_id,dly_date,sch_shift, "
		sql += "shf_desc,sch_rank,pay_type,bas_amt,bon_amt,pub_amt,otm_amt,dof_amt+ex_dof_amt as dof,spare, "
		sql += "tel_amt,wage_id,shf_amt_hr,ot_hr_amt,absent,remark "
		sql += "into R_D500 from " + str(user_first_name) + " "
		sql += "where emp_id=" + str(emp_id) + " "
		sql += "and dly_date>='" + str(search_date_from) + "' "
		sql += "and dly_date<='" + str(search_date_to) + "' "
		sql += "and pay_type<>'ABS' order by dly_date,sch_shift"
		# print("SQL:", sql)
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
		except db.OperationalError as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		finally:
			cursor.close()

		A1 = 0
		A2 = 0
		A3 = 0
		A4 = 0
		A5 = 0
		A6 = 0
		A7 = 0
		A8 = 0

		DropTable(user_first_name + "_TMPC")
		sql = "select distinct * into " + str(user_first_name + "_TMPC") + " "
		sql += "from " + str(user_first_name) + " "
		sql += "where emp_id=" + str(emp_id) + " "
		sql += "and dly_date>='" + str(search_date_from) + "' "
		sql += "and dly_date<='" + str(search_date_to) + "' "
		sql += "order by dly_date,sch_shift"
		# print("DEBUG SQL:", sql)
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)

		except db.OperationalError as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		except db.Error as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
			return is_error, message
		finally:
			cursor.close()

		print("DEBUG message = ", message)

		if DlyPerRs is not None:
			if len(DlyPerRs) > 0:
				for i in range(0, len(DlyPerRs)):
					absent = DlyPerRs[i][21]
					shf_amt_hr = DlyPerRs[i][6]
					
					if  DlyPerRs[i][38] is not None:
						bas_amt = DlyPerRs[i][38] if DlyPerRs[i][38]>0 else 0
					else:
						bas_amt = 0
					
					if  DlyPerRs[i][52] is not None:
						otm_amt = DlyPerRs[i][52] if DlyPerRs[i][52]>0 else 0
					else:
						otm_amt = 0

					if  DlyPerRs[i][39] is not None:
						bon_amt = DlyPerRs[i][39] if DlyPerRs[i][39]>0 else 0
					else:
						bon_amt = 0

					if  DlyPerRs[i][40] is not None:
						pub_amt = DlyPerRs[i][40] if DlyPerRs[i][40]>0 else 0
					else:
						pub_amt = 0

					if  DlyPerRs[i][53] is not None:
						dof_amt = DlyPerRs[i][53] if DlyPerRs[i][53]>0 else 0
					else:
						dof_amt = 0

					if  DlyPerRs[i][62] is not None:
						ex_dof_amt = DlyPerRs[i][62] if DlyPerRs[i][62]>0 else 0
					else:
						ex_dof_amt = 0

					if absent==int(1):
						print("absent = true")
					else:
						# print("shf_amt_hr =", shf_amt_hr)
						A1 = A1 + shf_amt_hr
						A2 = A2 + 1
						A3 = A3 + bas_amt
						A4 = A4 + otm_amt
						A5 = A5 + bon_amt
						A6 = A6 + pub_amt
						A7 = A7 + dof_amt
						A7 = A7 + ex_dof_amt					
					# print("absent:", absent)

				'''
				print("A1:", A1)
				print("A2:", A2)
				print("A3:", A3)
				print("A4:", A4)
				print("A5:", A5)
				print("A6:", A6)
				print("A7:", A7)
				'''

				income_list = [A1,A2,A3,A4,A5,A6,A7]

		is_error = False
		message = "DisplayList('DLY_PLAN') is pass."

	# is_error, error_message, performance_list, income_list = DisplayList("DLY_PLAN", user_first_name, emp_id, search_date_from, search_date_to)
	return is_error, message, DlyPerRs, income_list


def SearchDailyGurdPerformanceEmployeeInformation(request):
	is_error = True
	message = ""
	employee_information = None

	emp_id = request.POST.get('emp_id')
	if (emp_id=="") or (emp_id is None):
		is_error = True
		message = "ข้อมูลรหัสพนักงานไม่ถูกต้อง กรุณาตรวจสอบ"
		response = JsonResponse(data={"success": True,"is_error": is_error,"message": message, "employee_information": employee_information})
		response.status_code = 200
		return response
	else:
		sql = "select a.*,b.dept_en,c.sts_en from employee as a "
		sql += "left join com_department as b on a.emp_dept=b.dept_id "
		sql += "left join t_empsts as c on a.emp_status=c.sts_id "
		sql += "where a.emp_id=" + str(emp_id)
		
		try:
			with connection.cursor() as cursor:		
				cursor.execute(sql)
				employee_information = cursor.fetchall()
			
			is_error = False
			message = "PASS"				
		except db.OperationalError as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)			
		except db.Error as e:
			is_error = True
			message = "<b>Please send this error to IT team.</b><br>" + str(e)
		finally:			
			cursor.close()

	response = JsonResponse(data={"success": True,"is_error": is_error,"message": message, "employee_information": employee_information})
	response.status_code = 200
	return response


@login_required(login_url='/accounts/login/')
def generate_dgp_500(request, *args, **kwargs):    

	r_d500_obj = []
	pickup_record = []
	context = {}
	emp_id = ""
	fname = ""
	fname = ""
	cnt_id = ""
	dly_date = ""
	shf_desc = ""
	sch_rank = ""
	pay_type = ""
	bas_amt = ""
	bon_amt = ""
	pub_amt = ""
	otm_amt = ""
	dof = ""
	spare = ""
	tel_amt = ""
	wage_id = ""
	shf_amt_hr = ""
	ot_hr_amt = ""
	absent = ""
	sum_otm_amt = 0
	sum_shf_amt_hr = 0
	sum_bas_amt = 0
	sum_ot_hr_amt = 0
	sum_bon_amt = 0
	sum_pub_amt = 0
	sum_tel_amt = 0
	sum_dof = 0
	sum_spare = 0	

	base_url = MEDIA_ROOT + '/monitoring/template/'
	emp_id = kwargs['emp_id']
	search_date_from = kwargs['search_date_from'] 
	search_date_to = kwargs['search_date_to'] 
	template_name = base_url + 'DGP_500.docx'
	file_name = "DGP_500"

	sql = "select R_D500.EMP_ID,R_D500.FNAME,R_D500.CNT_ID,R_D500.DLY_DATE,"
	sql += "R_D500.SHF_DESC,R_D500.SCH_RANK,R_D500.PAY_TYPE,R_D500.BAS_AMT,"
	sql += "R_D500.BON_AMT,R_D500.PUB_AMT,R_D500.OTM_AMT,R_D500.DOF,R_D500.SPARE,"
	sql += "R_D500.TEL_AMT,R_D500.WAGE_ID,R_D500.SHF_AMT_HR,R_D500.OT_HR_AMT,R_D500.ABSENT "
	sql += "FROM HRMS.dbo.R_D500 R_D500 "
	sql += "ORDER BY R_D500.EMP_ID ASC"
	print("SQL report:", sql)
	try:
		cursor = connection.cursor()
		cursor.execute(sql)
		r_d500_obj = cursor.fetchall()
		counter = 1

		if r_d500_obj is not None:
			if len(r_d500_obj)>0:

				for row in r_d500_obj:
					number = counter
					fname = row[1]
					cnt_id = row[2]
					dly_date = row[3].strftime("%d/%m/%Y")
					dly_date_week_day = datetime.datetime.strptime(dly_date, '%d/%m/%Y').strftime('%a')
					shf_desc = row[4]
					sch_rank = row[5]
					pay_type = row[6]
					
					if row[10] is not None:
						otm_amt = row[10]
					else:
						otm_amt = 0						

					if pay_type!="LWO":
						sum_otm_amt += otm_amt
						
					shf_amt_hr = row[15]
					if pay_type!="LWO":
						sum_shf_amt_hr += shf_amt_hr

					if row[7] is not None:
						bas_amt = row[7]
					else:
						bas_amt =0

					sum_bas_amt += bas_amt

					if row[16] is not None:
						ot_hr_amt = row[16]
					else:
						ot_hr_amt = 0

					sum_ot_hr_amt += ot_hr_amt

					if row[8] is not None:
						bon_amt = row[8]
					else:
						bon_amt = 0
					sum_bon_amt += bon_amt

					if row[9] is not None:
						pub_amt = row[9]
					else:
						pub_amt = 0
					sum_pub_amt += pub_amt
					
					if row[13] is not None:
						tel_amt = row[13]
					else:
						tel_amt = 0
					sum_tel_amt += tel_amt

					if row[11] is not None:
						dof = row[11]
					else:
						dof = 0

					sum_dof += dof

					spare = row[12]
					sum_spare += spare

					wage_id = row[14]					
					absent = row[17]

					record = {
						"number": number,
					    "fname": fname,
					    "cnt_id": cnt_id,
					    "dly_date": dly_date,
					    "dly_date_week_day": dly_date_week_day,
					    "shf_desc": shf_desc,			    
					    "sch_rank": sch_rank,
					    "pay_type": pay_type,
					    "otm_amt": otm_amt,					   
					    "bas_amt": bas_amt,					    
					    "bon_amt": bon_amt,					    
					    "pub_amt": pub_amt,					    
					    "dof": dof,
					    "spare": spare,					    
					    "tel_amt": tel_amt,					    
					    "wage_id": wage_id,
					    "shf_amt_hr": shf_amt_hr,
					    "ot_hr_amt": ot_hr_amt,
					    "absent": absent,			    
					}

					counter = counter + 1
					pickup_record.append(record)
	finally:
		cursor.close()

	counter = counter -1
	if counter>0:
		total_row = str(counter) + str(" Days")
	else:
		total_row = str(counter) + str(" Day")

	current_datetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

	print("sum_pub_amt:", sum_pub_amt)

	context = {
	'search_date_from': search_date_from,
	'search_date_to': search_date_to,
	'emp_id': emp_id,
	'fname': fname,
	'cnt_id': cnt_id,
	'dly_date': dly_date,
	'shf_desc': shf_desc,
	'sch_rank': sch_rank,
	'pay_type': pay_type,
	'bas_amt': bas_amt,
	'bon_amt': bon_amt,
	'pub_amt': pub_amt,
	'otm_amt': otm_amt,
	'dof': dof,
	'spare': spare,
	'tel_amt': tel_amt,
	'wage_id': wage_id,
	'shf_amt_hr': shf_amt_hr,
	'ot_hr_amt': ot_hr_amt,
	'absent': absent,
	'daily_guard_performance_list': list(pickup_record),
	'current_datetime': current_datetime,
	"sum_ot_hr_amt": sum_ot_hr_amt,
    "sum_otm_amt": sum_otm_amt,
    "sum_tel_amt": sum_tel_amt,
    "sum_bas_amt": sum_bas_amt,
    "sum_bon_amt": sum_bon_amt,
    "sum_pub_amt": sum_pub_amt,	    
    "sum_spare": sum_spare,
    "sum_shf_amt_hr": sum_shf_amt_hr,
    "sum_dof": sum_dof,
    "total_row": total_row,
	}

	tpl = DocxTemplate(template_name)
	tpl.render(context)
	tpl.save(MEDIA_ROOT + '/monitoring/download/' + file_name + ".docx")

	# docx2pdf
	docx_file = path.abspath("media\\monitoring\\download\\" + file_name + ".docx")
	pdf_file = path.abspath("media\\monitoring\\download\\" + file_name + ".pdf")    
	convert(docx_file, pdf_file)

	return FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')


@login_required(login_url='/accounts/login/')
def export_dgp_500_xls(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="DGP_500.xls"'

	r_d500_obj = []
	pickup_record = []
	context = {}
	emp_id = ""
	fname = ""
	cnt_id = ""
	dly_date = ""
	shf_desc = ""
	sch_rank = ""
	pay_type = ""
	bas_amt = ""
	bon_amt = ""
	pub_amt = ""
	otm_amt = ""
	dof = ""
	spare = ""
	tel_amt = ""
	wage_id = ""
	shf_amt_hr = ""
	ot_hr_amt = ""
	absent = ""
	sum_otm_amt = 0
	sum_shf_amt_hr = 0
	sum_bas_amt = 0
	sum_ot_hr_amt = 0
	sum_bon_amt = 0
	sum_pub_amt = 0
	sum_tel_amt = 0
	sum_dof = 0
	sum_spare = 0

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('DGP_500')

	sql = "select "
	sql += "0 as col0, "
	sql += "R_D500.CNT_ID, R_D500.DLY_DATE, 3 as col3, R_D500.SHF_DESC, R_D500.OTM_AMT, R_D500.SHF_AMT_HR,"
	sql += "R_D500.BAS_AMT, R_D500.OT_HR_AMT, R_D500.BON_AMT, R_D500.PUB_AMT, R_D500.TEL_AMT,"
	sql += "R_D500.DOF, R_D500.SPARE, R_D500.WAGE_ID, R_D500.PAY_TYPE, R_D500.EMP_ID,"
	sql += "R_D500.FNAME, R_D500.SCH_RANK, R_D500.ABSENT "
	sql += "FROM HRMS.dbo.R_D500 R_D500 "
	sql += "ORDER BY R_D500.EMP_ID ASC"
	# print("SQL: ", sql)
	try:
		cursor = connection.cursor()
		cursor.execute(sql)
		r_d500_obj = cursor.fetchall()
	finally:
		cursor.close()

	if r_d500_obj is not None:
		if len(r_d500_obj)>0:
			emp_id = r_d500_obj[0][16]
			fullname_th = r_d500_obj[0][17]
			sch_rank = r_d500_obj[0][18]
			search_date_from = r_d500_obj[0][2].strftime('%d/%m/%Y')
			search_date_to = r_d500_obj[len(r_d500_obj)-1][2].strftime('%d/%m/%Y')
			

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	# First Row, First Column
	font_style = xlwt.easyxf('font: bold 1,height 280;')
	ws.write(1, 5, "Daily Guard Performance", font_style)

	font_style = xlwt.XFStyle()
	font_style = xlwt.easyxf('font: height 180;')
	ws.write(3, 0, "Employee ID : " + str(emp_id))
	ws.write(4, 0, "Employee Name : " + str(fullname_th))
	ws.write(5, 0, "Employee Rank : " + str(sch_rank))

	ws.write(2, 14, "From Date : " + str(search_date_from))
	ws.write(3, 14, "To Date : " + str(search_date_to))	
	ws.write(4, 14, "Print Date : " + str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M')))

	ws.col(1).width = int(13*260)
	ws.col(3).width = int(10*260)
	ws.col(4).width = int(25*260)
	ws.col(15).width = int(10*260)

	columns = ['', 'CONTRACT', 'DATE', 'DAY', 'SHIFT', 'OT', 'HOURS', 'BAS', 'GOT', 'BON', 'PUB', 'TEL', 'DOF', 'SPARE', 'WAGE', 'PAY TYPE', 'REMARK']
	for col_num in range(len(columns)):
		ws.write(7, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()
	font_style = xlwt.easyxf('font: height 180;')

	# Sheet header, first row
	row_num = 8
	counter = 1

	for row in r_d500_obj:
		number = counter
		fname = row[17]
		cnt_id = str(row[2])
		dly_date = str(row[2].strftime("%d/%m/%Y"))		
		dly_date_week_day = datetime.datetime.strptime(dly_date, '%d/%m/%Y').strftime('%a')
		# print("dly_date_week_day:", dly_date_week_day)
		dly_date_str = str(dly_date)
		shf_desc = row[4]
		sch_rank = row[18]
		pay_type = row[15]

		if row[5] is not None:
			otm_amt = row[5]
		else:
			otm_amt = 0

		if pay_type!="LWO":			
			sum_otm_amt += otm_amt
			
		shf_amt_hr = row[6]
		if pay_type!="LWO":
			sum_shf_amt_hr += shf_amt_hr

		if row[7] is not None:
			bas_amt = row[7]
		else:
			bas_amt = 0
		sum_bas_amt += bas_amt

		if row[8] is not None:
			ot_hr_amt = row[8]
		else:
			ot_hr_amt = 0
		sum_ot_hr_amt += ot_hr_amt

		if row[9] is not None:
			bon_amt = row[9]
		else:
			bon_amt = 0
		sum_bon_amt += bon_amt

		if row[10] is not None:
			pub_amt = row[10]
		else:
			pub_amt = 0
		sum_pub_amt += pub_amt
		
		if row[11] is not None:
			tel_amt = row[11]
		else:
			tel_amt = 0
		sum_tel_amt += tel_amt

		if row[12] is not None:
			dof = row[12]
		else:
			dof = 0
		sum_dof += dof

		spare = row[13]
		sum_spare += spare

		wage_id = row[13]					
		absent = row[19]
		
		for col_num in range(len(row)):
			if(col_num==0):
				ws.write(row_num, 0, counter, font_style)
			elif(col_num==2):
				ws.write(row_num, 2, dly_date_week_day.upper(), font_style)
			elif(col_num==3):
				ws.write(row_num, 3, dly_date_str, font_style)
			elif (col_num==16) or (col_num==17) or (col_num==18) or (col_num==19):
				ws.write(row_num, col_num, "", font_style)
			else:
				ws.write(row_num, col_num, row[col_num], font_style)

		row_num += 1
		counter += 1

	# Sum
	font_style = xlwt.XFStyle()
	font_style = xlwt.easyxf('font: height 180;')
	
	font_style.font.bold = True
	for col_num in range(len(row)):
		if(col_num==0):
			ws.write(row_num, 0, counter-1, font_style)
		elif(col_num==1):
			ws.write(row_num, 1, "Days", font_style)			
		elif(col_num==5):
			ws.write(row_num, 5, sum_otm_amt, font_style)
		elif(col_num==6):
			ws.write(row_num, 6, sum_shf_amt_hr, font_style)
		elif(col_num==7):
			ws.write(row_num, 7, sum_bas_amt, font_style)
		elif(col_num==8):
			ws.write(row_num, 8, sum_ot_hr_amt, font_style)
		elif(col_num==9):
			ws.write(row_num, 9, sum_bon_amt, font_style)
		elif(col_num==10):
			ws.write(row_num, 10, sum_pub_amt, font_style)
		elif(col_num==11):
			ws.write(row_num, 11, sum_tel_amt, font_style)			
		elif(col_num==12):
			ws.write(row_num, 12, sum_dof, font_style)
		elif(col_num==13):
			ws.write(row_num, 13, sum_spare, font_style)

	wb.save(response)
	return response


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def DailyMonitoringReports(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE	

	template_name = 'monitoring/daily_monitoring_reports.html'
	response_data = {}
	modified_records = []

	if request.user.is_superuser:
	    employee_photo = ""
	else:
		if request.user.username!="CMS_SUP":
		    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()   
		    employee_photo = b64encode(employee_info.image).decode("utf-8")        
		else:
		    employee_info = None
		    employee_photo = None		

	if request.method == "POST":
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date, 'form': form, 'employee_photo': employee_photo,'database': settings.DATABASES['default']['NAME'],'host': settings.DATABASES['default']['HOST']})



# TEST
'''
from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time
@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    # progress_recorder.set_progress(i + 1, seconds, description='my progress description')
    result = 0
    for i in range(seconds):
        time.sleep(1)
        result += i
        progress_recorder.set_progress(i + 1, seconds)
    return result
def progress_view(request):
    result = my_task.delay(10)
    return render(request, 'post_daily_attend.html', context={'task_id': result.task_id})
'''

def progress_view(request):
    result = my_task.delay(10)
    return render(request, 'monitoring/display_progress.html', context={'task_id': result.task_id})


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ajax_get_job_type_list(request):
    print("*************************************")
    print("FUNCTION: ajax_get_job_type_list()")
    print("*************************************")

    cus_id = request.POST.get('cus_id')
    cus_brn = request.POST.get('cus_brn')
    cus_vol = request.POST.get('cus_vol')
    cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
    # print("cnt_id:", cnt_id)
    shift_id = request.POST.get('shift_id')
    # print("shift_id:", shift_id)

    job_type_object = None
    job_type_list = []
   
    sql = "select srv_id,spay1,spay2,spay3,spay4,spay5,spay6,spay7,spay8,spay9,Position,Spay_detail from spaydate where cnt_id=" + str(cnt_id) + " and srv_shif_id=" + str(shift_id) + " and upd_flag='';"
    print("SQL:", sql)

    try:
        with connection.cursor() as cursor:     
            cursor.execute(sql)
            job_type_object = cursor.fetchall()
    except db.OperationalError as e:
        is_found = False
        message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
    except db.Error as e:
        is_found = False
        message = "<b>Please send this error to IT team or try again.</b><br>" + str(e)
    finally:
        cursor.close()
    
    if job_type_object is not None:
    	print("1")
    	for item in job_type_object:
	        record = {
	        	"srv_id": item[0],
	            "spay1": item[1],
	            "spay2": item[2],
	            "spay3": item[3],
	            "spay4": item[4],
	            "spay9": item[9],
	            "position": item[10],
	            "spay_detail": item[11],
	        }	        

	        job_type_list.append(record)
    else:
    	print("2")

    response = JsonResponse(data={"success": True, "is_error": False, "message": "", "job_type_list": job_type_list})
    response.status_code = 200
    return response    


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def is_scheduled(request):
	print("*****************************************************")
	print("FUNCTION: is_scheduled()")
	print("*****************************************************")
	username = request.user.username	
	dly_date = datetime.datetime.strptime(request.POST.get('dly_date'), '%d/%m/%Y').date()
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	emp_id = request.POST.get('emp_id')
	shift_id = request.POST.get('shift_id')
	
	is_scheduled = True
	message = ""

	sql = "select a.*,b.shf_type,b.shf_time_frm,b.shf_time_to"
	sql += " from dly_plan a left join t_shift b on a.sch_shift=b.shf_id"
	sql += " where a.dly_date='" + str(dly_date) + "'"
	sql += " and a.emp_id=" + str(emp_id)
	sql += " and a.absent=0 "
	sql += " and a.sch_shift=" + str(shift_id)
	print("DEBUG SQL: ", sql)

	cursor = connection.cursor()
	cursor.execute(sql)
	record = cursor.fetchone()
	cursor.close()			

	if record is not None:				
		messcross = str(record[0]) + " Shift No =" + str(record[3])
		dup_cnt_id = record[0]
		dup_shift_number = record[3]
		Shp = shift_id
		Gtype = record[47]
		Gfrom = record[48]
		Gto = record[49]

		print("cnt_id = ", int(cnt_id))
		print("dup_cnt_id = ", dup_cnt_id)
		print("emp_id : ", emp_id)
		print("emp_id_temp : ", record[1])

		if int(cnt_id)!=int(dup_cnt_id):
			if Shp != 0:
				sql = "Select SHF_TYPE, SHF_TIME_FRM, SHF_TIME_TO, shf_desc from t_shift where shf_id=" + str(Shp)
				
				cursor = connection.cursor()
				cursor.execute(sql)
				check_dup_record = cursor.fetchone()
				cursor.close()	
				if check_dup_record is not None:
					Stype = check_dup_record[0]
					Sfrom = check_dup_record[1]
					Sto = check_dup_record[2]
					shf_desc = check_dup_record[3]
			
			message = "พนักงานรหัส  <b>" + str(emp_id) + "</b> "
			message += "ได้แจ้งเวรไว้แล้วที่หน่วยงาน <b>" + str(dup_cnt_id) + "</b> "
			message += "ในกะ <b>" + str(shf_desc) + "</b><br><hr>"
			message += "กรุณาตรวจสอบข้อมูลอีกครั้ง"

			is_scheduled = True			
		else:
			# is_scheduled = False
			# message = "ไม่คร่อมหน่วยงาน"

			# get srv_qty
			string_today_date = str(settings.TODAY_DATE.strftime("%d/%m/%Y"))
			today_date = datetime.datetime.strptime(string_today_date, "%d/%m/%Y")
			if dly_date == today_date.date():
				sql = "select count(*) from dly_plan "
			if dly_date < today_date.date():
				sql = "select count(*) from his_dly_plan "		
			sql += "where cnt_id=" + str(cnt_id) + " and sch_shift=" + str(shift_id) + " and absent=0 and dly_date='" + str(dly_date) + "'"
			print("SQL 1 : ", sql)

			cursor = connection.cursor()
			cursor.execute(sql)
			rows = cursor.fetchone()
			cursor.close	
			informNo = rows[0] if rows[0]>0 else 0
			sql = "select cnt_id, srv_shif_id, sum(srv_qty) as qty from cus_service where srv_active=1 and cnt_id=" + str(cnt_id) + " and srv_shif_id=" + str(shift_id) + " group by cnt_id, srv_shif_id"
			print("SQL 2 : ", sql)
			cursor = connection.cursor()
			cursor.execute(sql)
			rows = cursor.fetchone()
			cursor.close
			srv_qty = rows[2]
			
			print("cnt_id_1 = ", int(rows[0]))
			print("cnt_id_2 = ", int(cnt_id))
			print("informNo = ", informNo)
			print("srv_qty = ", srv_qty)

			if informNo > srv_qty:
				if(int(rows[0])==int(cnt_id)):
					is_scheduled = True
					message = "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา: <b>" + str(int(cnt_id)) + "</b>"			
				else:
					is_scheduled = True
					message = "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา: <b>" + str(cnt_id) + "</b>"			
			else:
				is_scheduled = False # แจ้งเวรยังไม่เกินจำนวนที่อยู่ในสัญญา
				message = "ทำรายการได้"


	else:
		# get srv_qty
		string_today_date = str(settings.TODAY_DATE.strftime("%d/%m/%Y"))
		today_date = datetime.datetime.strptime(string_today_date, "%d/%m/%Y")
		if dly_date == today_date.date():
			sql = "select count(*) from dly_plan "
		if dly_date < today_date.date():
			sql = "select count(*) from his_dly_plan "		
		sql += "where cnt_id=" + str(cnt_id) + " and sch_shift=" + str(shift_id) + " and absent=0 and dly_date='" + str(dly_date) + "'"
		print("SQL 1 : ", sql)

		cursor = connection.cursor()
		cursor.execute(sql)
		rows = cursor.fetchone()
		cursor.close	
		informNo = rows[0] if rows[0]>0 else 0
		sql = "select cnt_id, srv_shif_id, sum(srv_qty) as qty from cus_service where srv_active=1 and cnt_id=" + str(cnt_id) + " and srv_shif_id=" + str(shift_id) + " group by cnt_id, srv_shif_id"
		print("SQL 2 : ", sql)
		cursor = connection.cursor()
		cursor.execute(sql)
		rows = cursor.fetchone()
		cursor.close
		srv_qty = rows[2]
		print("cnt_id_1 = ", int(rows[0]))
		print("cnt_id_2 = ", int(cnt_id))
		print("informNo = ", informNo)
		print("srv_qty = ", srv_qty)
		if informNo >= srv_qty:
			if(int(rows[0])==int(cnt_id)):
				is_scheduled = True
				message = "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา: <b>" + str(int(cnt_id)) + "</b>"			
			else:
				is_scheduled = True
				message = "พนักงานที่แจ้งเวรมากกว่าที่มีอยู่ในสัญญา: <b>" + str(cnt_id) + "</b>"			
		else:
			is_scheduled = False # แจ้งเวรยังไม่เกินจำนวนที่อยู่ในสัญญา
			message = "ทำรายการได้"
		

	print("MESSAGE : ", message)

	response = JsonResponse(data={"success": True, "is_scheduled": is_scheduled, "message": message})
	response.status_code = 200
	return response    


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_save_daily_attendance_check_rule_1(request):
	print("*****************************************************")
	print("FUNCTION: ajax_save_daily_attendance_check_rule_1()")
	print("*****************************************************")
	username = request.user.username	
	dly_date = datetime.datetime.strptime(request.POST.get('dly_date'), '%d/%m/%Y').date()
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	emp_id = request.POST.get('emp_id')
	shift_id = request.POST.get('shift_id')
	
	Timecross = 0	
	is_cross_site = True
	message = ""


	sql = "select a.*,b.shf_type,b.shf_time_frm,b.shf_time_to"
	sql += " from dly_plan a left join t_shift b on a.sch_shift=b.shf_id"
	sql += " where a.dly_date='" + str(dly_date) + "'"
	sql += " and a.emp_id=" + str(emp_id)
	sql += " and a.absent=0"
	cursor = connection.cursor()
	cursor.execute(sql)
	record = cursor.fetchone()
	cursor.close()			

	if record is not None:					
		messcross = str(record[0]) + " Shift No =" + str(record[3])
		dup_cnt_id = record[0]
		dup_shift_number = record[3]
		Shp = shift_id
		Gtype = record[47]
		Gfrom = record[48]
		Gto = record[49]

		if Shp != 0:
			sql = "Select SHF_TYPE, SHF_TIME_FRM, SHF_TIME_TO, shf_desc from t_shift where shf_id=" + str(Shp)
			cursor = connection.cursor()
			cursor.execute(sql)
			check_dup_record = cursor.fetchone()
			cursor.close()			
			if check_dup_record is not None:
				Stype = check_dup_record[0]
				Sfrom = check_dup_record[1]
				Sto = check_dup_record[2]
				shf_desc = check_dup_record[3]

			'''
			if Sfrom != 0 and Gfrom != 0:
				print("???")
			else:
				print("Exit Function")
			'''

		Gto = str(Gto).zfill(4)
		Sfrom = str(Sfrom).zfill(4)
		
		Hst = str(Gto)[:2] + ":" + str(Gto)[2:]
		# print("Hst = ", Hst)

		Hen = str(Sfrom)[:2] + ":" + str(Sfrom)[2:]
		# print("Hen = ", Hen)

		HDiff = datetime.datetime.strptime(Hst, '%H:%M') - datetime.datetime.strptime(Hen, '%H:%M')
		# print("HDiff 1 = ", HDiff)

		mdiff = int(HDiff.total_seconds() % 60)					
		mmdiff = 0.5 if mdiff >= 30 else 0

		HDiff = str(HDiff)[:2]
		if HDiff.isdigit():
			print("HDiff 2 = ", HDiff)
		else:
			HDiff = str(HDiff)[:1]
			# print("HDiff 3 = ", HDiff)	

		HDiff = abs(int(str(HDiff)[:2]))

		Timecross = HDiff + mmdiff
		
		if int(Gfrom) < int(Sfrom):
			sql = "SELECT TIME_VALUE FROM "
			sql += "( "
			sql += "SELECT TIME_VALUE FROM T_TIME "
			sql += " WHERE TIME_VALUE BETWEEN " + str(Gfrom) + " AND " + str(Gto)
			if int(Sto) > int(Sfrom):
				sql += ") a WHERE TIME_VALUE BETWEEN " + str(Sfrom) + " AND " + str(Sto)
			else:
				sql += ") a WHERE TIME_VALUE BETWEEN " + str(Sfrom) + " AND  2400"
		elif int(Gfrom) > int(Sfrom):
			sql = "SELECT TIME_VALUE FROM "
			sql += "( "
			sql += "SELECT TIME_VALUE FROM T_TIME "
			sql += " WHERE TIME_VALUE BETWEEN " + str(Sfrom) + " AND " + str(Sto)
			if int(Gto) > int(Gfrom):
				sql += ") a WHERE TIME_VALUE BETWEEN " + str(Gfrom) + " AND " + str(Gto)
			else:
				sql += ") a WHERE TIME_VALUE BETWEEN " + str(Gfrom) + " AND  2400"
		else:
			print("Exit Function")
		
		cursor = connection.cursor()
		cursor.execute(sql)
		check_dup_record = cursor.fetchone()
		cursor.close()

		if check_dup_record is None:
			is_cross_site = False
			message = "ไม่คร่อมหน่วยงาน"
		else:
			if Gto == Sfrom:
				is_cross_site = False
				message = "ไม่คร่อมหน่วยงาน"
			else:
				is_cross_site = True
				message = "รหัสพนักงาน  <b>" + str(emp_id) + "</b> "
				message += "เข้าเวรกะ  <b>" + str(shf_desc) + "</b> "
				message += "ที่หน่วยงาน  <b>" + str(dup_cnt_id) + "</b> ไปแล้ว "							
				# message += "จำนวนชั่วโมงที่โดนหัก <b>" + str(Timecross) + "</b> ชั่วโมง"
				message += " | กรุณาตรวจสอบข้อมูลอีกครั้ง"
				# message += " | ถ้าต้องการบันทึกกดปุ่มยืนยัน"
	else:
		is_cross_site = False
		message = "ไม่คร่อมหน่วยงาน"


	response = JsonResponse(data={"success": True, "is_cross_site": is_cross_site, "Timecross": Timecross, "message": message})
	response.status_code = 200
	return response    


def checkBetweenShiftNew(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,ui_absent_status,ui_late_status,ui_phone_status,tel_man,tel_time,tel_amount,ui_relief_status,relief_emp_id,ot_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM,username,allowZeroBathForPhoneAmount,late_from,late_to,late_reason_option,late_hour,late_full_paid_status,search_emp_id,Tday7,Tdof,customer_wage_rate_id,customer_zone_id):
	is_cross_site = True
	message = ""

	table_name = "dly_plan"
	sql = "select * from " + table_name + " where dly_date='" + str(dly_date) + "' and emp_id=" + str(emp_id) + " and absent=0" + " and sch_shift=" + str(shift_id) + " and cnt_id<>" + str(cnt_id)
	cursor = connection.cursor()
	cursor.execute(sql)
	record = cursor.fetchone()
	cursor.close()
	if record is not None:
		is_cross_site = True
		return is_cross_site, "พนักงานเข้างานที่หน่วยงานอื่น"

	# CheckBetweenShift()
	CheckBetweenShift = False
	
	# return False, "TODO: CheckBetweenShift()"

	sql = "select a.*,b.shf_type,b.shf_time_frm,b.shf_time_to"
	sql += " from dly_plan a left join t_shift b on a.sch_shift=b.shf_id"
	sql += " where a.dly_date='" + str(dly_date) + "'"
	sql += " and a.emp_id=" + str(emp_id)
	sql += " and a.absent=0"
	print("SQL:", sql)
	cursor = connection.cursor()
	cursor.execute(sql)
	record = cursor.fetchone()
	cursor.close()			
	if record is not None:					
		# TODO: ตรวจสอบกรณียอมให้พนักงานเข้าเวรคร่อมกับหน่วยงานที่เข้าเวรอยู่ล้ว
		messcross = str(record[0]) + " Shift No =" + str(record[3])
		print(messcross)

		dup_cnt_id = record[0]
		dup_shift_number = record[3]

		Shp = shift_id
		# print(Shp)
		Gtype = record[47]
		# print(Gtype)
		Gfrom = record[48]
		# print(Gfrom)
		Gto = record[49]
		# print(Gto)
		if Shp != 0:
			sql = "Select SHF_TYPE, SHF_TIME_FRM, SHF_TIME_TO from t_shift where shf_id=" + str(Shp)
			print("SQL: ", sql)
			cursor = connection.cursor()
			cursor.execute(sql)
			check_dup_record = cursor.fetchone()
			cursor.close()			
			if check_dup_record is not None:
				Stype = check_dup_record[0]
				Sfrom = check_dup_record[1]
				Sto = check_dup_record[2]

			if Sfrom != 0 and Gfrom != 0:
				print("???")
			else:
				print("Exit Function")

		
		Gto = str(Gto).zfill(4)
		Sfrom = str(Sfrom).zfill(4)
		Hst = str(Gto)[:2] + ":" + str(Gto)[2:]
		Hen = str(Sfrom)[:2] + ":" + str(Sfrom)[2:]
		HDiff = datetime.datetime.strptime(Hst, '%H:%M') - datetime.datetime.strptime(Hen, '%H:%M')					
		mdiff = int(HDiff.total_seconds() % 60)					
		mmdiff = 0.5 if mdiff >= 30 else 0
		HDiff = abs(int(str(HDiff)[:2]))
		Timecross = HDiff + mmdiff
		
		print("Hst:", Hst)					
		print("Hen:", Hen)					
		print("HDiff:", HDiff)
		print("mdiff:", mdiff)
		print("Timecross:", Timecross)

		# return False, "TEST"
	

		# เปลี่ยนการคร่อมเวลากะ
		print("Gfrom: ", Gfrom)
		print("Sfrom: ", Sfrom)
		# return False, "TEST"


		if int(Gfrom) < int(Sfrom):
			sql = "SELECT TIME_VALUE FROM "
			sql += "( "
			sql += "SELECT TIME_VALUE FROM T_TIME "
			sql += " WHERE TIME_VALUE BETWEEN " + str(Gfrom) + " AND " + str(Gto)
			if int(Sto) > int(Sfrom):
				sql += ") a WHERE TIME_VALUE BETWEEN " + str(Sfrom) + " AND " + str(Sto)
			else:
				sql += ") a WHERE TIME_VALUE BETWEEN " + str(Sfrom) + " AND  2400"
		elif int(Gfrom) > int(Sfrom):
			sql = "SELECT TIME_VALUE FROM "
			sql += "( "
			sql += "SELECT TIME_VALUE FROM T_TIME "
			sql += " WHERE TIME_VALUE BETWEEN " + str(Sfrom) + " AND " + str(Sto)
			if int(Gto) > int(Gfrom):
				sql += ") a WHERE TIME_VALUE BETWEEN " + str(Gfrom) + " AND " + str(Gto)
			else:
				sql += ") a WHERE TIME_VALUE BETWEEN " + str(Gfrom) + " AND  2400"
		else:
			print("Exit Function")

		
		# print("SQLL:", sql)
		# return False, sql
		
		cursor = connection.cursor()
		cursor.execute(sql)
		check_dup_record = cursor.fetchone()
		cursor.close()


		print("DEBUG Gto: ", Gto)
		print("DEUBG Sfrom: ", Sfrom)

		if check_dup_record is None:
			CheckBetweenShift = False
			is_cross_site = False
			message = "TEST11"
		else:
			if Gto == Sfrom:
				CheckBetweenShift = False
				is_cross_site = False
				message = "ไม่คร่อมหน่วยงาน"
			else:
				CheckBetweenShift = True
				is_cross_site = True
				message = "รหัสหนักงาน  <b>" + str(emp_id) + "</b> "
				message += "เข้าเวรกะ  <b>" + str(dup_shift_number) + "</b> "
				message += "ที่หน่วยงาน  <b>" + str(dup_cnt_id) + "</b> ไปแล้ว<br>"							
				message += "กรุณาตรวจสอบข้อมูลอีกครั้ง"
				# message += "จำนวนชั่วโมงที่โดนหัก  <b>" + str(Timecross) + "</b>"				
	else:
		is_cross_site = False
		message = ""

	return is_cross_site, message


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_end_all_active_status(request):
	cus_id = request.POST.get('cus_id').lstrip("0")
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	end_all_date = datetime.datetime.strptime(request.POST.get('end_all_date'), "%d/%m/%Y").strftime("%Y-%m-%d")
	print("end_all_date = ", end_all_date)

	try:
		sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').update(
			sch_active=False, sch_date_to=end_all_date, upd_by=request.user.username, upd_date=datetime.datetime.now(), upd_flag='E'
			)

		# Return refresh SCH_PLAN			
		try:
			sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').order_by('-upd_date')
			sch_plan_list = []
			for d in sch_plan:
				if d.sch_active:
					if d.relief:
						relief = 1
					else:
						relief = 0 

					if d.sch_active:
						sch_active = 1
					else:
						sch_active = 0

					record = {
						"sch_no": d.sch_no,
						"srv_id": d.srv_id,
						"emp_id": d.emp_id_id,
						"emp_fname_th": d.emp_id.emp_fname_th,
						"emp_lname_th": d.emp_id.emp_lname_th,
						"sch_rank": d.sch_rank,
						"sch_date_frm": d.sch_date_frm.strftime("%d/%m/%Y"),
						"sch_date_to": d.sch_date_to.strftime("%d/%m/%Y"),
						"sch_shf_mon": d.sch_shf_mon,
						"sch_shf_tue": d.sch_shf_tue,
						"sch_shf_wed": d.sch_shf_wed,
						"sch_shf_thu": d.sch_shf_thu,
						"sch_shf_fri": d.sch_shf_fri,
						"sch_shf_sat": d.sch_shf_sat,
						"sch_shf_sun": d.sch_shf_sun,
						"sch_active": sch_active,
						"relief": relief,
						"upd_date": d.upd_date.strftime("%d/%m/%Y %H:%M:%S"),
						"upd_by": d.upd_by,
						"upd_flag": d.upd_flag,
					}
					sch_plan_list.append(record)			    
		except SchPlan.DoesNotExist:
			sch_plan_list = []

		is_error = False
		message = "ทำรายการสำเร็จ"
	except db.OperationalError as e:
		is_error = True
		message = "Please send this error to IT team or try again | " + str(e)                    
	except db.Error as e:
		is_error = True
		message = "Please send this error to IT team or try again | " + str(e)


	response = JsonResponse(data={"success": True, "is_error": is_error, "message": message, "sch_plan_list": sch_plan_list})
	response.status_code = 200
	return response


