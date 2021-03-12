from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.static import serve
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils import translation
from django.utils.translation import ugettext as _
import django.db as db
from django.db import connection
from page.rules import *
import datetime
from django.utils import timezone
from system.models import ComZone
from django.http import JsonResponse
from hrms.settings import MEDIA_ROOT
from django.http import FileResponse
from docxtpl import DocxTemplate
from docx2pdf import convert
import xlwt
from os import path


@permission_required('customerreport.can_access_export_customer_address_main_report', login_url='/accounts/login/')
def ExportCustomerMainAddressReport(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    today_date = settings.TODAY_DATE
    
    zone_list = ComZone.objects.all().order_by('zone_id')

    return render(request, 'customerreport/export_customer_main_address_report.html',
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        "zone_list": zone_list,
        })


def AjaxSearchCustomerMainAddress(request):
    is_error = False
    error_message = ""
    customer_main_address_list = []
    customer_zone = request.POST.get('customer_zone')

    sql = "select cus_id, cus_name_th, cus_add1_th, cus_add2_th, cus_subdist_th, cus_name_en, cus_add1_en, cus_add2_en, cus_subdist_en, cus_zip, cus_tel, "
    sql += "cus_fax, cus_email, cus_active, con_fname_th, con_lname_th, con_position_th, con_fname_en, con_lname_en, con_position_en, dist_th, dist_en, city_en, city_th, dept_en "
    sql += "from EX_MAIN EX_MAIN where cus_active = 1 "
    if customer_zone!="":
        sql += "and cus_zone=" + str(customer_zone) + ";"
    else:
        sql += ";"
    print("SQL = ", sql)

    try:
        with connection.cursor() as cursor:     
            cursor.execute(sql)
            customer_main_address_obj = cursor.fetchall()

    except db.OperationalError as e:
        is_error = True
        error_message = "Error message: " + str(e)
    except db.Error as e:
        is_error = True
        error_message = "Error message: " + str(e)
    finally:
        cursor.close()

    if customer_main_address_obj is not None:
        if len(customer_main_address_obj) > 0:
            for row in customer_main_address_obj:                
                record = {
                    "cus_id": row[0],
                    "cus_name_th": row[1],
                    "cus_add1_th": row[2],
                    "cus_add2_th": row[3],
                    "cus_subdist_th": row[4],
                    "dist_th": row[20],
                    "city_th": row[23],

                    "cus_name_en": row[5],
                    "cus_add1_en": row[6],
                    "cus_add2_en": row[7],
                    "cus_subdist_en": row[8],
                    "dist_en": row[21],
                    "city_en": row[22],
                    
                    "cus_zip": row[9],
                    "cus_tel": row[10],
                    "cus_fax": row[11],
                    "cus_zone": row[24],

                    "con_fname_th": row[14],
                    "con_lname_th": row[15],
                    "con_position_th": row[16],

                    "con_fname_en": row[17],
                    "con_lname_en": row[18],
                    "con_position_en": row[19],

                    "cus_email": row[12],

                }
                customer_main_address_list.append(record)
        else:
            is_error = True
    else:
        is_error = True

    response = JsonResponse(data={        
        "is_error": False,
        "error_message": error_message,
        "customer_main_address_list": list(customer_main_address_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
def export_customer_main_address(request, *args, **kwargs):
    base_url = MEDIA_ROOT + '/contract/template/'
    customer_zone = kwargs['customer_zone']

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Customer_Main_Address_List.xls"'

    customer_list_obj = []
    pickup_record = []
    context = {}

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Customer Main Address')

    # TITLE
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style = xlwt.easyxf('font: bold 1,height 280;')
    ws.write(0, 0, "Customer Main Address", font_style)

    # COLUMN WIDTH
    ws.col(0).width = int(5*260)    # NO    
    ws.col(1).width = int(10*260)   # CUS_ID

    ws.col(2).width = int(50*260)   # NAME (TH)
    ws.col(3).width = int(50*260)   # ADD1 (TH)
    ws.col(4).width = int(30*260)   # ADD2 (TH)
    ws.col(5).width = int(15*260)   # SUB DIST (TH)
    ws.col(6).width = int(15*260)   # DIST (TH)
    ws.col(7).width = int(15*260)   # CITY (TH)

    ws.col(8).width = int(50*260)
    ws.col(9).width = int(50*260)
    ws.col(10).width = int(30*260)
    ws.col(11).width = int(20*260)
    ws.col(12).width = int(20*260)
    ws.col(13).width = int(20*260)

    ws.col(14).width = int(20*260)
    ws.col(15).width = int(20*260)
    ws.col(16).width = int(20*260)

    ws.col(17).width = int(20*260)
    ws.col(18).width = int(20*260)
    ws.col(19).width = int(20*260)
    ws.col(20).width = int(20*260)
    ws.col(21).width = int(20*260)
    ws.col(22).width = int(20*260)
    ws.col(23).width = int(20*260)
    ws.col(24).width = int(20*260)

    # COLUMN NAME
    font_style = xlwt.XFStyle()
    font_style = xlwt.easyxf('font: bold 1, height 180;')   
    font_style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; align: vert centre, horiz centre;')

    ws.write(2, 0, "NO.", font_style)
    ws.write(2, 1, "CUS ID", font_style)
    ws.write(2, 2, "NAME (TH)", font_style)
    ws.write(2, 3, "ADDRESS 1 (TH)", font_style)
    ws.write(2, 4, "ADDRESS 2 (TH)", font_style)
    ws.write(2, 5, "SUB DISTRICT (TH)", font_style)
    ws.write(2, 6, "DISTRICT (TH)", font_style)
    ws.write(2, 7, "CITY (TH)", font_style)

    ws.write(2, 8, "NAME (EN)", font_style)
    ws.write(2, 9, "ADDRESS 1 (EN)", font_style)
    ws.write(2, 10, "ADDRESS 2 (EN)", font_style)
    ws.write(2, 11, "SUB DISTRICT (EN)", font_style)
    ws.write(2, 12, "DISTRICT (EN)", font_style)
    ws.write(2, 13, "CITY (EN)", font_style)

    ws.write(2, 14, "ZIP", font_style)
    ws.write(2, 15, "TEL", font_style)
    ws.write(2, 16, "FAX", font_style)
    ws.write(2, 17, "ZONE", font_style)
    ws.write(2, 18, "FNAME (TH)", font_style)
    ws.write(2, 19, "LNAME (TH)", font_style)
    ws.write(2, 20, "POS (TH)", font_style)
    ws.write(2, 21, "FNAME (EN)", font_style)
    ws.write(2, 22, "LNAME (EN)", font_style)
    ws.write(2, 23, "POS (EN)", font_style)
    ws.write(2, 24, "EMAIL", font_style)


    customer_main_address_obj = None
    customer_main_address_list = None

    sql = "select cus_id, cus_name_th, cus_add1_th, cus_add2_th, cus_subdist_th, cus_name_en, cus_add1_en, cus_add2_en, cus_subdist_en, cus_zip, cus_tel, "
    sql += "cus_fax, cus_email, cus_active, con_fname_th, con_lname_th, con_position_th, con_fname_en, con_lname_en, con_position_en, dist_th, dist_en, city_en, city_th, dept_en "
    sql += "from EX_MAIN EX_MAIN where cus_active = 1 "
    if customer_zone!="":
        sql += "and cus_zone=" + str(customer_zone) + ";"
    else:
        sql += ";"

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        customer_main_address_obj = cursor.fetchall()
    finally:
        cursor.close()

    font_style = xlwt.XFStyle()
    font_style = xlwt.easyxf('font: bold 1, height 180;')
    font_style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; align: vert centre, horiz left;')

    if customer_main_address_obj is not None:
        if len(customer_main_address_obj)>0:
            row_num = 3
            row_count = 1
            for item in customer_main_address_obj:
                cus_id = item[0]
                cus_name_th = item[1]
                cus_add1_th = item[2]
                cus_add2_th = item[3]
                cus_subdist_th = item[4]
                cus_name_en = item[5]
                cus_add1_en = item[6]
                cus_add2_en = item[7]
                cus_subdist_en = item[8]
                cus_zip = item[9]
                cus_tel = item[10]
                cus_fax = item[11]
                cus_email = item[12]                
                cus_active = item[13]
                con_fname_th = item[14]
                con_lname_th = item[15]
                con_position_th = item[16]
                con_fname_en = item[17]
                con_lname_en = item[18]
                con_position_en = item[19]
                dist_th = item[20]
                dist_en = item[21]
                city_en = item[22]
                city_th = item[23]
                dept_en = item[24]

                for col_num in range(25):
                    if(col_num==0):
                        ws.write(row_num, 0, row_count, font_style)                    
                    elif(col_num==1):
                        ws.write(row_num, 1, cus_id, font_style)
                    
                    elif(col_num==2):
                        ws.write(row_num, 2, cus_name_th, font_style)
                    elif(col_num==3):
                        ws.write(row_num, 3, cus_add1_th, font_style)
                    elif(col_num==4):
                        ws.write(row_num, 4, cus_add2_th, font_style)
                    elif(col_num==5):
                        ws.write(row_num, 5, cus_subdist_th, font_style)                        
                    elif(col_num==6):
                        ws.write(row_num, 6, dist_th, font_style)
                    elif(col_num==7):
                        ws.write(row_num, 7, city_th, font_style)

                    elif(col_num==8):
                        ws.write(row_num, 8, cus_name_en, font_style)
                    elif(col_num==9):
                        ws.write(row_num, 9, cus_add1_en, font_style)
                    elif(col_num==10):
                        ws.write(row_num, 10, cus_add2_en, font_style)
                    elif(col_num==11):
                        ws.write(row_num, 11, cus_subdist_en, font_style)
                    elif(col_num==12):
                        ws.write(row_num, 12, dist_en, font_style)                        
                    elif(col_num==13):
                        ws.write(row_num, 13, city_en, font_style)

                    elif(col_num==14):
                        ws.write(row_num, 14, cus_zip, font_style)
                    elif(col_num==15):
                        ws.write(row_num, 15, cus_tel, font_style)
                    elif(col_num==16):
                        ws.write(row_num, 16, cus_fax, font_style)
                    elif(col_num==17):
                        ws.write(row_num, 17, dept_en, font_style)
                    elif(col_num==18):
                        ws.write(row_num, 18, con_fname_th, font_style)
                    elif(col_num==19):
                        ws.write(row_num, 19, con_lname_th, font_style)                        
                    elif(col_num==20):
                        ws.write(row_num, 20, con_position_th, font_style)
                    elif(col_num==21):
                        ws.write(row_num, 21, con_fname_en, font_style)
                    elif(col_num==22):
                        ws.write(row_num, 22, con_lname_en, font_style)
                    elif(col_num==23):
                        ws.write(row_num, 23, con_position_en, font_style)
                    elif(col_num==24):
                        ws.write(row_num, 24, cus_email, font_style)
                    else:
                        print("ERROR")

                row_num += 1
                row_count += 1

    wb.save(response)
    return response 


@permission_required('customerreport.can_access_export_customer_address_main_report', login_url='/accounts/login/')
def ExportCustomerSiteAddressReport(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    today_date = settings.TODAY_DATE
    
    zone_list = ComZone.objects.all().order_by('zone_id')

    return render(request, 'customerreport/export_customer_site_address_report.html',
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        "zone_list": zone_list,
        })


def AjaxSearchCustomerSiteAddress(request):
    is_error = False
    error_message = ""
    customer_site_address_list = []
    customer_zone = request.POST.get('customer_zone')

    sql = "select cus_id, cus_name_th, cus_add1_th, cus_add2_th, cus_subdist_th, cus_name_en, cus_add1_en, cus_add2_en, cus_subdist_en, cus_zip, cus_tel, "
    sql += "cus_fax, cus_email, cus_active, con_fname_th, con_lname_th, con_position_th, con_fname_en, con_lname_en, con_position_en, dist_th, dist_en, city_en, city_th, dept_en "
    sql += "from EX_SITE where cus_active = 1 "
    if customer_zone!="":
        sql += "and cus_zone=" + str(customer_zone) + ";"
    else:
        sql += ";"
    print("SQL = ", sql)

    try:
        with connection.cursor() as cursor:     
            cursor.execute(sql)
            customer_site_address_obj = cursor.fetchall()

    except db.OperationalError as e:
        is_error = True
        error_message = "Error message: " + str(e)
    except db.Error as e:
        is_error = True
        error_message = "Error message: " + str(e)
    finally:
        cursor.close()

    if customer_site_address_obj is not None:
        if len(customer_site_address_obj) > 0:
            for row in customer_site_address_obj:                
                record = {
                    "cus_id": row[0],
                    "cus_name_th": row[1],
                    "cus_add1_th": row[2],
                    "cus_add2_th": row[3],
                    "cus_subdist_th": row[4],
                    "dist_th": row[20],
                    "city_th": row[23],

                    "cus_name_en": row[5],
                    "cus_add1_en": row[6],
                    "cus_add2_en": row[7],
                    "cus_subdist_en": row[8],
                    "dist_en": row[21],
                    "city_en": row[22],
                    
                    "cus_zip": row[9],
                    "cus_tel": row[10],
                    "cus_fax": row[11],
                    "cus_zone": row[24],

                    "con_fname_th": row[14],
                    "con_lname_th": row[15],
                    "con_position_th": row[16],

                    "con_fname_en": row[17],
                    "con_lname_en": row[18],
                    "con_position_en": row[19],

                    "cus_email": row[12],

                }
                customer_site_address_list.append(record)
        else:
            is_error = True
    else:
        is_error = True

    response = JsonResponse(data={        
        "is_error": False,
        "error_message": error_message,
        "customer_site_address_list": list(customer_site_address_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
def export_customer_site_address(request, *args, **kwargs):
    base_url = MEDIA_ROOT + '/contract/template/'
    customer_zone = kwargs['customer_zone']

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Customer_Site_Address_List.xls"'

    customer_list_obj = []
    pickup_record = []
    context = {}

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Customer Site Address')

    # TITLE
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style = xlwt.easyxf('font: bold 1,height 280;')
    ws.write(0, 0, "Customer Main Address", font_style)

    # COLUMN WIDTH
    ws.col(0).width = int(5*260)    # NO    
    ws.col(1).width = int(10*260)   # CUS_ID

    ws.col(2).width = int(50*260)   # NAME (TH)
    ws.col(3).width = int(50*260)   # ADD1 (TH)
    ws.col(4).width = int(30*260)   # ADD2 (TH)
    ws.col(5).width = int(15*260)   # SUB DIST (TH)
    ws.col(6).width = int(15*260)   # DIST (TH)
    ws.col(7).width = int(15*260)   # CITY (TH)

    ws.col(8).width = int(50*260)
    ws.col(9).width = int(50*260)
    ws.col(10).width = int(30*260)
    ws.col(11).width = int(20*260)
    ws.col(12).width = int(20*260)
    ws.col(13).width = int(20*260)

    ws.col(14).width = int(20*260)
    ws.col(15).width = int(20*260)
    ws.col(16).width = int(20*260)

    ws.col(17).width = int(20*260)
    ws.col(18).width = int(20*260)
    ws.col(19).width = int(20*260)
    ws.col(20).width = int(20*260)
    ws.col(21).width = int(20*260)
    ws.col(22).width = int(20*260)
    ws.col(23).width = int(20*260)
    ws.col(24).width = int(20*260)

    # COLUMN NAME
    font_style = xlwt.XFStyle()
    font_style = xlwt.easyxf('font: bold 1, height 180;')   
    font_style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; align: vert centre, horiz centre;')

    ws.write(2, 0, "NO.", font_style)
    ws.write(2, 1, "CUS ID", font_style)
    ws.write(2, 2, "NAME (TH)", font_style)
    ws.write(2, 3, "ADDRESS 1 (TH)", font_style)
    ws.write(2, 4, "ADDRESS 2 (TH)", font_style)
    ws.write(2, 5, "SUB DISTRICT (TH)", font_style)
    ws.write(2, 6, "DISTRICT (TH)", font_style)
    ws.write(2, 7, "CITY (TH)", font_style)

    ws.write(2, 8, "NAME (EN)", font_style)
    ws.write(2, 9, "ADDRESS 1 (EN)", font_style)
    ws.write(2, 10, "ADDRESS 2 (EN)", font_style)
    ws.write(2, 11, "SUB DISTRICT (EN)", font_style)
    ws.write(2, 12, "DISTRICT (EN)", font_style)
    ws.write(2, 13, "CITY (EN)", font_style)

    ws.write(2, 14, "ZIP", font_style)
    ws.write(2, 15, "TEL", font_style)
    ws.write(2, 16, "FAX", font_style)
    ws.write(2, 17, "ZONE", font_style)
    ws.write(2, 18, "FNAME (TH)", font_style)
    ws.write(2, 19, "LNAME (TH)", font_style)
    ws.write(2, 20, "POS (TH)", font_style)
    ws.write(2, 21, "FNAME (EN)", font_style)
    ws.write(2, 22, "LNAME (EN)", font_style)
    ws.write(2, 23, "POS (EN)", font_style)
    ws.write(2, 24, "EMAIL", font_style)


    customer_site_address_obj = None    

    sql = "select cus_id, cus_name_th, cus_add1_th, cus_add2_th, cus_subdist_th, cus_name_en, cus_add1_en, cus_add2_en, cus_subdist_en, cus_zip, cus_tel, "
    sql += "cus_fax, cus_email, cus_active, con_fname_th, con_lname_th, con_position_th, con_fname_en, con_lname_en, con_position_en, dist_th, dist_en, city_en, city_th, dept_en "
    sql += "from EX_SITE where cus_active = 1 "
    if customer_zone!="":
        sql += "and cus_zone=" + str(customer_zone) + ";"
    else:
        sql += ";"

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        customer_site_address_obj = cursor.fetchall()
    finally:
        cursor.close()

    font_style = xlwt.XFStyle()
    font_style = xlwt.easyxf('font: bold 1, height 180;')
    font_style = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white; align: vert centre, horiz left;')

    if customer_site_address_obj is not None:
        if len(customer_site_address_obj)>0:
            row_num = 3
            row_count = 1
            for item in customer_site_address_obj:
                cus_id = item[0]
                cus_name_th = item[1]
                cus_add1_th = item[2]
                cus_add2_th = item[3]
                cus_subdist_th = item[4]
                cus_name_en = item[5]
                cus_add1_en = item[6]
                cus_add2_en = item[7]
                cus_subdist_en = item[8]
                cus_zip = item[9]
                cus_tel = item[10]
                cus_fax = item[11]
                cus_email = item[12]                
                cus_active = item[13]
                con_fname_th = item[14]
                con_lname_th = item[15]
                con_position_th = item[16]
                con_fname_en = item[17]
                con_lname_en = item[18]
                con_position_en = item[19]
                dist_th = item[20]
                dist_en = item[21]
                city_en = item[22]
                city_th = item[23]
                dept_en = item[24]

                for col_num in range(25):
                    if(col_num==0):
                        ws.write(row_num, 0, row_count, font_style)                    
                    elif(col_num==1):
                        ws.write(row_num, 1, cus_id, font_style)
                    
                    elif(col_num==2):
                        ws.write(row_num, 2, cus_name_th, font_style)
                    elif(col_num==3):
                        ws.write(row_num, 3, cus_add1_th, font_style)
                    elif(col_num==4):
                        ws.write(row_num, 4, cus_add2_th, font_style)
                    elif(col_num==5):
                        ws.write(row_num, 5, cus_subdist_th, font_style)                        
                    elif(col_num==6):
                        ws.write(row_num, 6, dist_th, font_style)
                    elif(col_num==7):
                        ws.write(row_num, 7, city_th, font_style)

                    elif(col_num==8):
                        ws.write(row_num, 8, cus_name_en, font_style)
                    elif(col_num==9):
                        ws.write(row_num, 9, cus_add1_en, font_style)
                    elif(col_num==10):
                        ws.write(row_num, 10, cus_add2_en, font_style)
                    elif(col_num==11):
                        ws.write(row_num, 11, cus_subdist_en, font_style)
                    elif(col_num==12):
                        ws.write(row_num, 12, dist_en, font_style)                        
                    elif(col_num==13):
                        ws.write(row_num, 13, city_en, font_style)

                    elif(col_num==14):
                        ws.write(row_num, 14, cus_zip, font_style)
                    elif(col_num==15):
                        ws.write(row_num, 15, cus_tel, font_style)
                    elif(col_num==16):
                        ws.write(row_num, 16, cus_fax, font_style)
                    elif(col_num==17):
                        ws.write(row_num, 17, dept_en, font_style)
                    elif(col_num==18):
                        ws.write(row_num, 18, con_fname_th, font_style)
                    elif(col_num==19):
                        ws.write(row_num, 19, con_lname_th, font_style)                        
                    elif(col_num==20):
                        ws.write(row_num, 20, con_position_th, font_style)
                    elif(col_num==21):
                        ws.write(row_num, 21, con_fname_en, font_style)
                    elif(col_num==22):
                        ws.write(row_num, 22, con_lname_en, font_style)
                    elif(col_num==23):
                        ws.write(row_num, 23, con_position_en, font_style)
                    elif(col_num==24):
                        ws.write(row_num, 24, cus_email, font_style)
                    else:
                        print("ERROR")

                row_num += 1
                row_count += 1

    wb.save(response)
    return response

