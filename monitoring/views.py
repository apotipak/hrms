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
	    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()    
	    employee_photo = b64encode(employee_info.image).decode("utf-8")        

	if request.method == "POST":
		print("POST: ScheduleMaintenance()")
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		print("GET: ScheduleMaintenance()")
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date, 'form': form, 'employee_photo': employee_photo})


@login_required(login_url='/accounts/login/')
@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
def ajax_get_customer(request):
	cus_id = request.POST.get('cus_id')
	cus_brn = request.POST.get('cus_brn')
	cus_vol = request.POST.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	
	print("cnt_id = " + str(cnt_id))

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
				print("cus_service is found")
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
				print("cus_service is not found")
				cus_service_list=[]

			# SCH_PLAN			
			try:
				sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').order_by('-upd_date')
				print("sch_plan is found")
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
				print("sch_plan is not found")
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
			print("ajax_get_customer() - Customer Number is not found.")
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
    print("cnt_id = " + str(cnt_id))
    print("sch_active = " + str(sch_active))

    try:    	
    	print("sch_plan is found")
    	sch_plan_list = []
    	total = 0

    	if sch_active == '1':
    		sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).filter(sch_date_to='2999-12-31').exclude(upd_flag='D').order_by('-upd_date')
    		print("sch")

	    	for d in sch_plan:	
	    		print("Active - " + str(d.cnt_id) + "," + str(d.sch_rank))
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
	    		print("Pending - " + str(d.cnt_id) + "," + str(d.sch_rank))
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
	    		print("All - " + str(d.cnt_id) + "," + str(d.sch_rank))
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
	    	print("sch_plan is not found")    	
	    	sch_plan_list = []

    except SchPlan.DoesNotExist:
    	print("sch_plan is not found")    	
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
    print("sch_no = " + str(sch_no))

    try:
    	sch_plan = SchPlan.objects.filter(sch_no=sch_no).get()

    	'''
    	print("debug : " + str(sch_plan.emp_id_id) + "," + str(sch_plan.sch_rank))
    	print("sch_active = " + str(sch_plan.sch_active))
    	'''

    	employee_info = EmpPhoto.objects.filter(emp_id=sch_plan.emp_id_id).get()
    	employee_photo = b64encode(employee_info.image).decode("utf-8")

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
	print("selected_service_id = " + str(selected_service_id))

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
	print("contract_list_filter_option = " + str(contract_list_filter_option))

	sch_plan_list = []

	# Case - add new employee into customer service
	if selected_sch_no == "0":
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
		cursor.execute("select max(convert(decimal(4,0),right(rtrim(convert(char(20),sch_no)),4))) from sch_plan where cnt_id=" + cnt_id)
		max_sch_no = cursor.fetchone()[0]

		if max_sch_no is not None:
			new_sch_no = max_sch_no + 1
		else:
			new_sch_no = 1
	
		# Generate new sch_no
		new_sch_no = str(selected_service_id) + str(new_sch_no).zfill(4)
		print("new_sch_no = " + str(new_sch_no))

		# RULE-1: Check if an employee is existed in another schedule		
		# employee = SchPlan.objects.filter(emp_id=emp_id).exclude(upd_flag='D').exclude(sch_active="")
		# select * from sch_plan where emp_id=916 and sch_active=1 and upd_flag!='D'
		sch_plan_count = SchPlan.objects.filter(emp_id=emp_id).exclude(upd_flag='D').exclude(sch_active="").count()		

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
		print("update existing");
		print("selected_sch_no = " + str(selected_sch_no))

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
			sch_plan.upd_by = request.user.first_name
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
			sch_plan = SchPlan.objects.all().filter(cnt_id=cnt_id).exclude(upd_flag='D').order_by('-upd_date', 'emp_id')

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
				"message": "Saved success.",
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
	            print("debug11")
	            data = Employee.objects.all().filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').order_by('emp_id')
	        else:
	            print("debug22")
	            data = Employee.objects.all().filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').order_by('emp_id')
	    else:
	        print("debug33")
	        data = Employee.objects.all().filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').order_by('emp_id')
	else:		
		print("debug44")
		search_option = request.GET.get('search_option')
		search_key = request.GET.get('search_key')
		if search_option=="1":
			# Search employee by emp_id
			print("1111")
			if search_key.isnumeric():
				print("1111-1")
				data = Employee.objects.filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').filter(emp_id=search_key).order_by('emp_id').all()
			else:
				print("1111-2")
				data = []
			
		elif search_option=="2":
			print("2222")
			print("search_key = " + str(search_key))
			data = Employee.objects.filter(emp_type__exact='D1').filter(empstatus='A').exclude(upd_flag='D').filter(emp_fname_th__startswith=search_key).order_by('emp_id').all()
		else:
			print("3333")
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
			print("debug 1")
			current_page = paginator.get_page(page)
		except InvalidPage as e:
			print("debug 2")
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
			print("debug 3")
			print("error 403")
			response = JsonResponse({"error": "there was an error"})
			response.status_code = 403
			return response
	else:
		print("debug 4")
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

	# print(str(emp_id) + " | " + str(cus_id) + " | " + str(cus_brn) + " | " + str(cus_vol))
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)
	employee_item = []

	'''
	print("-------debug--------")
	print("_cnt_id = " + str(cnt_id))
	print("_emp_id = " + str(emp_id))
	print("_dly_date = " + str(""))
	print("_sch_shift = " + str(shf_desc))
	'''

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
				record = cursor.fetchone()
				emp_fname_th = record[0]
				emp_lname_th = record[1]
				emp_rank = record[2]
				emp_dept = record[3]
				emp_type = record[4]
				emp_join_date = "" if record[5] is None else record[5].strftime("%d/%m/%Y")
				emp_term_date = "" if record[6] is None else record[6].strftime("%d/%m/%Y")
				emp_status_id = record[7]
				emp_status_th = record[8]				
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

		employee_info = EmpPhoto.objects.filter(emp_id=emp_id).get()
		employee_photo = b64encode(employee_info.image).decode("utf-8")

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
		print("not found")
		response = JsonResponse(data={
			"success": True,
			"is_found": False,
			"class": "bg-danger",
			"message": "Employee not found.",			
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
	    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()    
	    employee_photo = b64encode(employee_info.image).decode("utf-8")        

	if request.method == "POST":
		print("POST: ScheduleMaintenance()")
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date, 'form': form, 'employee_photo': employee_photo})


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
	    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()    
	    employee_photo = b64encode(employee_info.image).decode("utf-8")        

	if request.method == "POST":
		if form.is_valid():          
			form = ScheduleMaintenanceForm(request.POST, user=request.user)
			response_data['form_is_valid'] = True            
		else:            
			response_data['form_is_valid'] = False
		return JsonResponse(response_data)     
	else:
		form = ScheduleMaintenanceForm()

	return render(request, template_name, {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date, 'form': form, 'employee_photo': employee_photo})


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

	# Show avatar
	if request.user.is_superuser:
	    employee_photo = ""
	else:
	    employee_info = EmpPhoto.objects.filter(emp_id=request.user.username).get()    
	    employee_photo = b64encode(employee_info.image).decode("utf-8")        


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
		'employee_photo': employee_photo
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
	print("period = " + str(period))

	# Get current date
	generated_date = datetime.datetime.strptime(generated_date, '%d/%m/%Y')	
	generated_date = str(generated_date)[0:10]
	print("generated_date : " + str(generated_date))

	# TODO
	cursor = connection.cursor()	
	cursor.execute("select count(*) from t_date where date_chk='" + str(generated_date) + "'")	
	tdate_count = cursor.fetchone()
	if tdate_count[0] == 0:
		try:
			cursor = connection.cursor()	
			cursor.execute("exec dbo.create_dly_plan_new %s", [generated_date])
			error_message = "Generate completed."
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
		error_message = "Daily Attendance table has been created. No need to generate again."
		response = JsonResponse(data={"success": True,"is_error": True,"class": "bg-success","error_message": error_message})


	cursor.close
	response.status_code = 200
	return response

def getPeriod(generated_date):
	generated_date = datetime.datetime.strptime(generated_date, '%d/%m/%Y')
	print(generated_date)
	try:
		period = TPeriod.objects.filter(prd_date_frm__lte=generated_date).filter(prd_date_to__gte=generated_date).filter(emp_type='D1').get()
		period = period.prd_id
	except CusContract.DoesNotExist:
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


def isGenerateDailyCreated(attendance_date):
	attendance_date = datetime.datetime.strptime(attendance_date, '%d/%m/%Y')
	cursor = connection.cursor()	
	cursor.execute("select count(*) from t_date where date_chk='" + str(attendance_date) + "'")	
	tdate_count = cursor.fetchone()
	if tdate_count[0] > 0:
		return True
	else:
		return False
	cursor.close()


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_get_attendance_information(request):

	print("********************************************")
	print("FUNCTION: ajax_get_attendance_information()")
	print("********************************************")	
	
	attendance_date = request.POST.get('attendance_date')	
	
	schedule_list = []
	employee_list = []

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

	if isGenerateDailyCreated(attendance_date):
		attendance_date = request.POST.get('attendance_date')
		attendance_date = datetime.datetime.strptime(attendance_date, '%d/%m/%Y')
		print("attendance_date = " + str(attendance_date))
		cus_id = request.POST.get('cus_id').lstrip("0")
		cus_brn = request.POST.get('cus_brn')
		cus_vol = request.POST.get('cus_vol')
				
		# Get Contract ID
		cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)		
		print("cnt_id = " + str(cnt_id))

		# Get Customer No
		cus_no = cus_id + cus_brn.zfill(3)
		print("cus_no = " + str(cus_no))

		# Get current date
		curDate = attendance_date
		print("Current date = " + str(curDate))

		# Check if daily attend is a public holiday
		# select hol_date from t_holiday where hol_date=curDate
		cursor = connection.cursor()
		cursor.execute("select hol_date from t_holiday where hol_date=%s", [curDate])		
		cursor.close
		# 99  # DAY OFF #########
		# 999  # ANOTHER SITE #

		# Get Day of Week
		dayOfWeek = curDate.weekday()
		print("Day of week = " + str(dayOfWeek))


		# Provide contract service list dropdown


		# Check Total
		# NUM_SERVICE TOTAL
		# select cnt_id,shf_type,sum(srv_wed) as srv_num, sum(srv_pub) as srv_pub from v_contract as a where cnt_id=1008000001 and srv_active=1 and cus_service_flag <> 'D' group by cnt_id,shf_type
		cursor = connection.cursor()
		cursor.execute("select cnt_id,shf_type,sum(srv_wed) as srv_num, sum(srv_pub) as srv_pub from v_contract as a where cnt_id=%s and srv_active=1 and cus_service_flag <> 'D' group by cnt_id,shf_type", [cnt_id])
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
		
		print("totalNDP=" + str(totalNDP))
		print("totalNNP=" + str(totalNNP))
		print("totalPDP=" + str(totalPDP))
		print("totalPNP=" + str(totalPNP))



		# DLY_PLAN TOTAL
		# select distinct * from v_dlyplan where cnt_id=2526000001 and dly_date=convert(datetime,'2020-12-02',20) and customer_flag<>'D' order by sch_shift, emp_id
		cursor = connection.cursor()
		cursor.execute("select distinct * from v_dlyplan where cnt_id=%s and dly_date=convert(datetime,%s,20) and customer_flag<>'D' order by sch_shift, emp_id", [cnt_id, curDate])
		rows = cursor.fetchall()
		cursor.close
		if len(rows)>0:
			for index in range(len(rows)):				
				shf_type = rows[index][2]
				absent = rows[index][21]
				print("shf_type = " + str(shf_type))
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
		sql += "Remark, ex_dof_amt, Customer_Flag "	
		sql += "from v_dlyplan "	
		sql += "where cnt_id=%s and dly_date=%s and customer_flag<>'D' order by sch_shift,emp_id "

		cursor.execute(sql, [cnt_id, attendance_date])
		rows = cursor.fetchall()
		
		for row in rows:
			print(row[6])
			if(row[6]):
				absent=1
			else:
				absent=0
		
			if row[24]==1:
				# tel_man = "<span class='text-danger'><strong>X</strong></span>"
				# tel_man = "<span class='text-success'><i class='fas fa-phone-volume'></i></span>"
				tel_man = "<span class='text-success'><i class='fas fa-phone-alt'></i></span>"
			else:
				tel_man = ""

			if row[25] is not None:
				tel_time = row[25].strftime("%d/%m/%Y %H:%M")
			else:
				tel_time = ""

			upd_date = row[45].strftime("%d/%m/%Y %H:%M")
			upd_gen = "" if row[48] is None else row[48]
			remark = "" if row[61] is None else row[61].strip("0").strip()			

			record = {
				"emp_fname_th": row[0].strip(),
				"emp_lname_th": row[1].strip(),
				"shf_type": row[2],
				"shf_desc": row[3],
				"shf_time_frm": row[4],
				"shf_time_to": row[5],
				"shf_amt_hr": row[6],
				"Remp_fname_th": row[7],
				"Remp_lname_th": row[8],
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
				"absent": row[21],
				"relieft": row[22],
				"relieft_id": row[23],
				"tel_man": tel_man,
				"tel_time": tel_time,
				"tel_amt": row[26],
				"tel_paid": row[27],
				"ot": row[28],
				"ot_reason": row[29],
				"ot_time_frm": row[30],
				"ot_time_to": row[31],
				"ot_hr_amt": row[32],
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
				"upd_by": row[46],
				"upd_flag": row[47],
				"upd_gen": upd_gen,
				"cus_name_th": row[49],
				"late": row[50],
				"sch_relieft": row[51],
				"otm_amt": row[52],
				"dof_amt": row[53],
				"dof": row[54],
				"TPA": row[55],
				"late_full": row[56],
				"DAY7": row[57],
				"cnt_sale_amt": row[58],
				"cus_name_en": row[59],
				"cnt_active": row[60],
				"remark": remark,
				"ex_dof_amt": row[62],
				"Customer_Flag": row[63],
			}
			employee_list.append(record)

		try:
			dlyplan = DlyPlan.objects.filter(cnt_id=cnt_id).all()
			is_found = True
			print(1)
		except CusContract.DoesNotExist:
			is_found = False
			print(2)

		message = ""

		print("is_found = " + str(is_found))
		cursor.close
	else:
		is_found = False
		message = ""

	response = JsonResponse(data={
	    "success": True,
	    "is_found": is_found,
	    "message": message,
	    "schedule_list": list(schedule_list),
	    "employee_list": list(employee_list),
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
	})
	
	response.status_code = 200
	return response	

@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_delete_employee(request):
	print("********************************")
	print("FUNCTION: ajax_delete_employee()")
	print("********************************")

	cus_id = request.GET.get('cus_id').lstrip("0")
	cus_brn = request.GET.get('cus_brn')
	cus_vol = request.GET.get('cus_vol')
	cnt_id = cus_id + cus_brn.zfill(3) + cus_vol.zfill(3)		
	emp_id = request.GET.get('emp_id')
	dly_date = datetime.datetime.strptime(request.GET.get('dly_date'), '%d/%m/%Y')	
	shift_id = request.GET.get('shift_id')
	username = request.user.first_name

	'''
	print("--------debug---------")
	print("_cnt_id = " + str(cnt_id))
	print("_emp_id = " + str(emp_id))
	print("_dly_date = " + str(dly_date))
	print("_shift_id = " + str(shift_id))
	'''

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


def addRecord(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,relief_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM):
	is_pass = True
	message = ""	

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


		# *****************************************
		# RULE 4 - Validate all input
		# *****************************************				
		if is_pass:
			is_not_error, message = validateInput(dly_date, cnt_id, emp_id, shift_id, shift_type, shift_name, job_type, totalNDP, totalNDA, totalNDM, totalNNP, totalNNA, totalNNM, totalPDP, totalPDA, totalPDM, totalPNP, totalPNA, totalPNM, absent_status, late_status, phone_status, relief_status)
			if is_not_error:
				is_pass = True
				message = "Rule 4 is passed."
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
			sql += "0" + "," + "32" + "," + "'32SOY'" + "," + "NULL" + "," + "0" + "," + "0" + "," + "1" + "," + "NULL" + ",'"
			sql += str(upd_date) + "'," + "'System'" + "," + "'A'" + ",'" + remark + "')"
			# print(sql)

			try:
				with connection.cursor() as cursor:
					cursor.execute(sql)

				is_pass = True
				message = "บันทึกข้อมูลสำเร็จ"
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


def editRecord(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,relief_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM):
	is_pass = True
	message = ""	

	# Server side check
	# TODO: shift_id must be in cus_service


	# *****************************************************
	# RULE 1 - Check manpower must not more than contract
	# *****************************************************
	shift_type = shift_name.partition("#")[2][0:2].strip() # shift_type will be D or N
	
	# amnaj
	# Check Manpower
	# sql = "select count(*) from dly_plan where dly_date='%s' and emp_id=%s and absent=0 and sch_shift=%s" % (dly_date, emp_id, shift_id)
	sql = "select count(*) from v_dlyplan_shift where cnt_id='" + str(cnt_id) + "' and left(remark,2)='" + str(remark) + "' and shf_type=" + str(job_type) + "' and absent=0 and dly_date='" + str(dly_date) + "'"
	print("sql = " + str(sql))

	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchone()
	cursor.close	

	if rows is not None:
		print("no. of rows = " + str(len(rows)))
		if len(rows)==0:
			aManPower = 0
		else:
			aManPower = len(rows)
	else:		
		aManPower = 0
	
	is_error = True if aManPower>0 else False

	print("aManPower = " + str(aManPower))



	if is_error:
		is_pass = False
	else:
		is_pass = True

	if is_pass:
		message += "Rule 1 is passed.<br>"
	else:
		message += "Rule 1 is failed.<br>"


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
			print("TODO: เช็คพนักงาานเข้าเวรที่หน่วยงานอื่นไปแล้ว")
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

		print(sql)
	
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


@permission_required('monitoring.view_dlyplan', login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def ajax_save_daily_attendance(request):
	print("***************************************")
	print("FUNCTION: ajax_save_daily_attendance()")
	print("***************************************")

	# Initial values
	AEdly = int(request.GET.get("AEdly"))
	message = ""

	# Get requested parameters
	# dly_date = request.GET.get('dly_date')
	# dly_date = datetime.datetime.strptime(request.GET.get('dly_date'), '%d/%m/%Y')
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
	absent_status = int(request.GET.get('absent_status'))
	late_status = int(request.GET.get('late_status'))
	phone_status = int(request.GET.get('phone_status'))
	relief_status = int(request.GET.get('relief_status'))
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
	
	'''
	print("debug 1")
	print("------------------")
	print(str(absent_status) + "," + str(late_status) + "," + str(phone_status) + "," + str(relief_status))
	print("------------------")
	print("debug 2")
	print("------------------")
	print(str(job_type) + "," + str(job_type) + "," + str(totalNDP) + "," + str(totalNDA) + "," + str(totalNDM) + "," + str(totalNNP) + "," + str(totalNNA) + "," + str(totalNNM))
	print("------------------")	
	'''
	print("remark : " + str(remark))


	if AEdly == 0: # EDIT MODE
		print("Edit")		
		is_edit_record_success, message = editRecord(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,relief_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM)
		if is_edit_record_success:
			success_status = True
			title = "Success"
			type_status = "green"
		else:
			success_status = False
			title = "Error"
			type_status = "red"

	elif AEdly == 1: # ADD MODE
		print("Add")		
		is_add_record_success, message = addRecord(dly_date,cus_id,cus_brn,cus_vol,cnt_id,emp_id,emp_rank,emp_dept,shift_id,shift_name,absent_status,late_status,phone_status,relief_status,job_type,remark,totalNDP,totalNDA,totalNDM,totalNNP,totalNNA,totalNNM,totalPDP,totalPDA,totalPDM,totalPNP,totalPNA,totalPNM)
		if is_add_record_success:
			success_status = True
			title = "Success"
			type_status = "green"
		else:
			success_status = False
			title = "Error"
			type_status = "red"	
	elif AEdly == 2: # DELETE MODE
		print("Delete")
		success_status = True
		title = "Success"
		type_status = "green"
		message = "TODO: Delete record"
	else: # UNKNOWN MODE
		print("Error!")
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
		print("no. of rows = " + str(len(rows)))
		if len(rows)==0:
			aManPower = 0
		else:
			aManPower = len(rows)
	else:		
		aManPower = 0
	
	is_error = True if aManPower>0 else False

	print("is_error = " + str(is_error))
	
	return is_error, message



# *******************************************************************
# RULE 3 - Validate Input
# *******************************************************************
def validateInput(dly_date, cnt_id, emp_id, shift_id, shift_type, shift_name, job_type, totalNDP, totalNDA, totalNDM, totalNNP, totalNNA, totalNNM, totalPDP, totalPDA, totalPDM, totalPNP, totalPNA, totalPNM, absent_status, late_status, phone_status, relief_status):
	isPass = True
	message = ""

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
	print("Check 1: checkBetweenShift()")
	sql = "select a.*, b.shf_type, b.shf_time_frm, b.shf_time_to from dly_plan a left join t_shift b on a.sch_shift = b.shf_id where a.dly_date=%s and a.emp_id=%s and a.absent=0" % (dly_date, emp_id)
	is_duplicated, message = checkBetweenShift(sql)
	if is_duplicated:
		isPass = False
		message = ""
	else:
		isPass = True

	# TODO: สำหรับ Employee ID ห้ามลงรายการซ้ำถ้าเพิ่มรายการใหม่	
	if not is_duplicated:
		print("Check 2: checkDupDly()")
		sql = "select count(*) from dly_plan where cnt_id=%s and dly_date='%s' and emp_id=%s and sch_shift=%s" % (cnt_id, dly_date, emp_id, shift_id)
		is_duplicated, message = checkDupDly(sql)
		if is_duplicated:
			isPass = False
			message = "รหัส : <b>" + str(emp_id) + "</b><br>ตารางเวร : <b>" + shift_name + "</b><br>เป็นรายการซ้ำ กรุณาตรวจสอบอีกครั้ง"
		else:
			isPass = True	
	
	# TODO: ห้ามลงรายการซ้ำ ถ้าเพิ่มรายการใหม่ สำหรับคนที่มาแทน แทนหลายคนในหน่วยเดียวกันไม่ได้
	if not is_duplicated:
		print("Check 3: checkDupDly()")
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
