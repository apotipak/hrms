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
from docx import Document
from docx.shared import Cm, Mm, Pt, Inches
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE


@permission_required('dailyattendreport.can_access_gpm_422_no_of_guard_operation_by_empl_by_zone_report', login_url='/accounts/login/')
def AjaxGPM422NoOfGuardOperationByEmplByZoneReport(request, *args, **kwargs):    
    base_url = MEDIA_ROOT + '/monitoring/template/'    
    template_name = base_url + 'GPM_422.docx'
    file_name = request.user.username + "_GPM_422"

    work_date = kwargs['work_date']
    work_date = datetime.datetime.strptime(work_date, "%d/%m/%Y").date()
    dept_zone = kwargs['dept_zone']

    print("work_date : ", work_date)
    print("dept_zone : ", dept_zone)

    # TODO
    sql = "SELECT emp_fname_th, emp_lname_th, dept_en, cnt_id, emp_id, dept_id, sch_rank, absent, cus_name_th "
    sql += "FROM R_GPM422 "
    sql += ""
    sql += "ORDER BY dept_id ASC, emp_id ASC"
    print(sql)

    dly_plan_obj = None
    record = {}
    dly_plan_list = []
    error_message = ""


@permission_required('dailyattendreport.can_access_gpm403_daily_guard_performance_by_contract_report', login_url='/accounts/login/')
def AjaxGPMWorkOnDayOffReport(request, *args, **kwargs):    
    base_url = MEDIA_ROOT + '/monitoring/template/'    
    template_name = base_url + 'GPM_HDOF.docx'
    file_name = request.user.username + "_GPM_HDOF"

    start_date = kwargs['start_date']
    start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").date()

    # TODO    
    sql = "SELECT emp_fname_th, emp_lname_th, shf_desc, dept_en, cnt_id, emp_id, dly_date, dept_id, sch_rank, absent, upd_by, upd_gen, cus_name_th, dof from V_HDLYPLAN "
    sql += "Where V_HDLYPLAN.dof = 1 AND V_HDLYPLAN.absent = 0 "
    sql += "AND V_HDLYPLAN.DLY_DATE = '" + str(start_date) + "' "
    sql += "order By V_HDLYPLAN.dept_id Asc"
    print(sql)

    dly_plan_obj = None
    record = {}
    dly_plan_list = []
    error_message = ""

    try:                
        cursor = connection.cursor()
        cursor.execute(sql)
        dly_plan_obj = cursor.fetchall()        
    except db.OperationalError as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    except db.Error as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    finally:
        cursor.close()

    # TODO
    document = DocxTemplate(template_name)
    style = document.styles['Normal']
    font = style.font
    font.name = 'AngsanaUPC'
    font.size = Pt(14)

    if dly_plan_obj is not None:
        
        temp_dept_id = None
        row_count = 1

        for item in dly_plan_obj:
            emp_full_name = item[0].strip() + " " + item[1].strip()            
            shf_desc = item[2].replace("('", "")            
            dept_en = item[3].replace("('", "")        

            if (dept_en.find('SP-Zone') != -1):
                dept_en_short = dept_en.replace("SP-Zone", "").lstrip()[0]
            elif (dept_en.find('ZONE H BPI') != -1):
                dept_en_short = "H"
            elif (dept_en.find('ZONE Control') != -1):
                dept_en_short = "CR"
            elif (dept_en.find('SP-Samui') != -1):
                dept_en_short = "SM"
            elif (dept_en.find('ZONE PHUKET') != -1):
                dept_en_short = "P"
            elif (dept_en.find('Zone Khon kean') != -1):
                dept_en_short = "K"
            elif (dept_en.find('BEM') != -1):
                dept_en_short = "BEM"
            elif (dept_en.find('ZONE I') != -1):
                dept_en_short = "I"
            elif (dept_en.find('ZONE R') != -1):
                dept_en_short = "R"
            elif (dept_en.find('Zone Songkhla') != -1):
                dept_en_short = "SK"
            else:
                dept_en_short = "?"

            cnt_id = item[4]
            emp_id = item[5]            
            dly_date = item[6].strftime("%d/%m/%Y")
            dept_id = item[7]
            sch_rank = item[8]
            absent = item[9]
            upd_by = item[10]
            upd_gen = item[11]
            cus_name_th = item[12]
            dof = item[13]

            if temp_dept_id is None:
                table = document.add_table(rows=1, cols=9, style='TableGridLight')                                                
                a = table.cell(0, 0)
                b = table.cell(0, 8)
                c = a.merge(b)
                c.text = '%s' % (dept_id)
                c.paragraphs[0].runs[0].font.bold = True
                c.paragraphs[0].runs[0].font.size = Pt(15)

                row = table.add_row().cells
                row[0].text = "No."
                row[1].text = "Date"
                row[2].text = "EMP ID"
                row[3].text = "Name"
                row[4].text = "Rank"
                row[5].text = "Zone"
                row[6].text = "Shift"
                row[7].text = "POST ID"
                row[8].text = "Site Name"

                row[0].width = Cm(0.5)
                row[1].width = Cm(2)
                row[2].width = Cm(2)
                row[3].width = Cm(4)
                row[4].width = Cm(1)
                row[5].width = Cm(1)
                row[6].width = Cm(5)
                row[7].width = Cm(2)
                
                if dept_id is not None:
                    row = table.add_row().cells
                    row[0].text = str(row_count)
                    row[1].text = str(dly_date)
                    row[2].text = str(emp_id)
                    row[3].text = str(emp_full_name)
                    row[4].text = str(sch_rank)
                    row[5].text = str(dept_en_short)
                    row[6].text = str(shf_desc)
                    row[7].text = str(cnt_id)
                    row[8].text = str(cus_name_th)  

                    row[0].width = Cm(0.5)
                    row[1].width = Cm(2)
                    row[2].width = Cm(2)
                    row[3].width = Cm(4)
                    row[4].width = Cm(1)
                    row[5].width = Cm(1)
                    row[6].width = Cm(5)
                    row[7].width = Cm(2)

                    company_name = "   " + str(item[3].replace("('", ""))
                    row = table.rows[0]
                    company_name = row.cells[0].paragraphs[0].add_run(company_name)
                    company_name.font.name = 'AngsanaUPC'
                    company_name.font.size = Pt(16)
                    company_name.bold = True
            else:
                if dept_id != temp_dept_id:
                    p = document.add_paragraph()
                    runner = p.add_run('TOTAL  %s' % str(row_count - 1))
                    runner.bold = True
                    company_name.font.name = 'AngsanaUPC'
                    runner.font.size = Pt(15)

                    table = document.add_table(rows=1, cols=9, style='TableGridLight')                    

                    a = table.cell(0, 0)
                    b = table.cell(0, 1)
                    c = table.cell(0, 8)
                    d = a.merge(c)
                    d.text = '%s' % (dept_id)
                    d.paragraphs[0].runs[0].font.bold = True
                    d.paragraphs[0].runs[0].font.size = Pt(15)

                    row_count = 1                                
                    row = table.add_row().cells
                    row[0].text = str(row_count)
                    row[1].text = str(dly_date)
                    row[2].text = str(emp_id)
                    row[3].text = str(emp_full_name)
                    row[4].text = str(sch_rank)
                    row[5].text = str(dept_en_short)
                    row[6].text = str(shf_desc)
                    row[7].text = str(cnt_id)
                    row[8].text = str(cus_name_th)  

                    row[0].width = Cm(0.5)
                    row[1].width = Cm(2)
                    row[2].width = Cm(2)
                    row[3].width = Cm(4)
                    row[4].width = Cm(1)
                    row[5].width = Cm(1)
                    row[6].width = Cm(5)
                    row[7].width = Cm(2)
                    
                    company_name = "   " + str(item[3].replace("('", ""))
                    row = table.rows[0]
                    company_name = row.cells[0].paragraphs[0].add_run(company_name)
                    company_name.font.name = 'AngsanaUPC'
                    company_name.font.size = Pt(16)
                    company_name.bold = True
                else:
                    row = table.add_row().cells
                    row[0].text = str(row_count)
                    row[1].text = str(dly_date)
                    row[2].text = str(emp_id)
                    row[3].text = str(emp_full_name)
                    row[4].text = str(sch_rank)
                    row[5].text = str(dept_en_short)
                    row[6].text = str(shf_desc)
                    row[7].text = str(cnt_id)
                    row[8].text = str(cus_name_th)  

                    row[0].width = Cm(0.5)
                    row[1].width = Cm(2)
                    row[2].width = Cm(2)
                    row[3].width = Cm(4)
                    row[4].width = Cm(1)
                    row[5].width = Cm(1)
                    row[6].width = Cm(5)
                    row[7].width = Cm(2)

            temp_dept_id = dept_id
            row_count += 1
    
        if len(dly_plan_obj) > 0:
            p = document.add_paragraph()
            runner = p.add_run('TOTAL  %s' % str(row_count - 1))
            runner.bold = True            
            runner.font.size = Pt(15)

        context = {
            'start_date': start_date.strftime("%d/%m/%Y"),
        }
        
        document.render(context)
        document.save(MEDIA_ROOT + '/monitoring/download/' + file_name + ".docx")        

    else:
        context = {
            'start_date': start_date.strftime("%d/%m/%Y"),
            'end_date': end_date.strftime("%d/%m/%Y"),
        }
        
        document.render(context)
        document.save(MEDIA_ROOT + '/monitoring/download/' + file_name + ".docx")


    context = {
        'start_date': start_date.strftime("%d/%m/%Y"),
    }
    document.render(context)
    document.save(MEDIA_ROOT + '/monitoring/download/' + file_name + ".docx")    

    # TODO
    docx_file = path.abspath("media\\monitoring\\download\\" + file_name + ".docx")
    pdf_file = path.abspath("media\\monitoring\\download\\" + file_name + ".pdf")    
    convert(docx_file, pdf_file)

    return FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')


@permission_required('dailyattendreport.can_access_gpm403_daily_guard_performance_by_contract_report', login_url='/accounts/login/')
def GenerateGPM403DailyGuardPerformanceReport(request, *args, **kwargs):    
    base_url = MEDIA_ROOT + '/monitoring/template/'
    contract_number_from = kwargs['contract_number_from']
    contract_number_to = kwargs['contract_number_to']
    start_date = kwargs['start_date']
    end_date = kwargs['end_date']

    template_name = base_url + 'GPM_403.docx'
    file_name = request.user.username + "_GPM_403"

    start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
    end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").date()

    contract_number_from = 0 if contract_number_from is None else contract_number_from
    contract_number_to = 9999999999 if contract_number_to is None else contract_number_to
    today_date = settings.TODAY_DATE.strftime("%d/%m/%Y %H:%M:%S")

    sql = "select emp_fname_th, emp_lname_th, shf_desc, dept_en, cnt_id, "
    sql += "emp_id, dly_date, sch_shift, dept_id, sch_rank, "
    sql += "absent, relieft_id, tel_man, tel_paid, ot, "
    sql += "ot_hr_amt, cus_name_th, late, late_full "
    sql += "FROM V_HDLYPLAN "
    sql += "WHERE absent = 0 AND (sch_shift <> 99 OR sch_shift <> 999) "
    sql += "and (cnt_id>=" + str(contract_number_from) + " and cnt_id<=" + str(contract_number_to) + ") "
    sql += "and (dly_date>='" + str(start_date) + "' and dly_date<='" + str(end_date) + "') "
    sql += "ORDER BY cnt_id ASC, dly_date ASC, shf_desc ASC, emp_id ASC"
    print(sql)
    
    dly_plan_obj = None
    record = {}
    dly_plan_list = []
    error_message = ""

    try:                
        cursor = connection.cursor()
        cursor.execute(sql)
        dly_plan_obj = cursor.fetchall()        
    except db.OperationalError as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    except db.Error as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    finally:
        cursor.close()

    if dly_plan_obj is not None:
        if len(dly_plan_obj)>0:
            group_count = 1
            row_count = 1
            temp_cnt_id = None

            for item in dly_plan_obj:
                
                if temp_cnt_id != item[4]:
                    temp_cnt_id = item[4]
                    row_count = 1                    
                else:
                    row_count = row_count + 1

                record = {
                    "row_count": row_count,
                    "emp_full_name": item[0].strip() + " " + item[1].strip(),
                    "shf_desc": item[2],
                    "dept_en": item[3],
                    "cnt_id": item[4],
                    "emp_id": item[5],
                    "dly_date": item[6].strftime("%d/%m/%Y"),
                    "sch_shift": item[7],
                    "dept_id": item[8],
                    "sch_rank": item[9],
                    "absent": item[10],
                    "relieft_id": item[11],
                    "tel_man": item[12],
                    "tel_paid": item[13],
                    "ot": item[14],
                    "ot_hr_amt": item[15],
                    "cus_name_th": item[16],
                    "late": item[17],
                    "late_full": item[18],
                }
                # row_count = row_count + 1
                dly_plan_list.append(record)

            context = {
                'file_name': file_name,
                'docx_file_name': file_name+".docx",
                'template_name': template_name,
                'dly_plan_list': list(dly_plan_list),
                'today_date': today_date,
                'start_date': start_date.strftime("%d/%m/%Y"),
                'end_date': end_date.strftime("%d/%m/%Y"),
            }          
        else:
            context = {
                'file_name': file_name,
                'docx_file_name': file_name + ".docx",
                'template_name': template_name,
                'dly_plan_list': list(dly_plan_list),
                'today_date': today_date,
                'start_date': start_date.strftime("%d/%m/%Y"),
                'end_date': end_date.strftime("%d/%m/%Y"),
            }
        
    template_name = base_url + 'GPM_403.docx'
    file_name = 'GPM_403'
    document = DocxTemplate(template_name)
    style = document.styles['Normal']
    font = style.font
    # font.name = 'Cordia New (Body CS)'
    font.name = 'AngsanaUPC'
    font.size = Pt(14)

    if dly_plan_obj is not None:
        
        temp_cnt_id = None
        row_count = 1

        for item in dly_plan_obj:
            shf_desc = item[2].replace("('", "")
            dept_en = item[3].replace("('", "")
            cnt_id = item[4]
            emp_id = item[5]
            emp_full_name = item[0].strip() + " " + item[1].strip()
            dly_date = item[6].strftime("%d/%m/%Y")
            sch_shift = item[7]
            dept_id = item[8]
            sch_rank = item[9]
            absent = item[10]

            relieft_id = item[11] if item[11] != 0 else ""
            tel_man = "x" if item[12] else ""            
            tel_paid = "{:.2f}".format(item[13]) if item[13] > 0 else ""
            
            ot = "" if item[14] else ""
            ot_hr_amt = item[15] if item[15] else ""
            cus_name_th = item[16]
            late = "x" if item[17] else ""
            late_full = "x" if item[18] else ""

            if temp_cnt_id is None:
                table = document.add_table(rows=1, cols=13, style='TableGridLight')                                                

                a = table.cell(0, 0)
                b = table.cell(0, 12)
                c = a.merge(b)
                c.text = '%s' % (cnt_id)
                c.paragraphs[0].runs[0].font.bold = True
                c.paragraphs[0].runs[0].font.size = Pt(15)

                row = table.add_row().cells
                row[0].text = "No."
                row[1].text = "Date"
                row[2].text = "EMP ID"
                row[3].text = "Name"
                row[4].text = "Rank"
                row[5].text = "Shift"
                row[6].text = "Relief ID"
                row[7].text = "OT"
                row[8].text = "Late"
                row[9].text = "Full"
                row[10].text = "Amt.HR"
                row[11].text = "Call"
                row[12].text = "Tel Paid"
                
                row[0].width = Cm(0.5)
                row[3].width = Cm(5)
                row[5].width = Cm(8)

                if cnt_id is not None:
                    row = table.add_row().cells
                    row[0].text = str(row_count)
                    row[1].text = str(dly_date)
                    row[2].text = str(emp_id)
                    row[3].text = str(emp_full_name)
                    row[4].text = str(sch_rank)
                    row[5].text = str(shf_desc)
                    row[6].text = str(relieft_id)
                    row[7].text = str(ot)
                    row[8].text = str(late)                    
                    row[9].text = str(late_full)
                    row[10].text = str(ot_hr_amt)
                    row[11].text = str(tel_man)
                    row[12].text = str(tel_paid)

                    row[0].width = Cm(0.5)
                    row[3].width = Cm(5)
                    row[5].width = Cm(8)

                    company_name = "  " + str(cus_name_th) + "    |    " + str(dept_id) + "   " + str(dept_en)
                    row = table.rows[0]
                    company_name = row.cells[0].paragraphs[0].add_run(company_name)
                    # company_name.font.name = 'Cordia New (Body CS)'
                    company_name.font.name = 'AngsanaUPC'
                    company_name.font.size = Pt(16)
                    company_name.bold = True
            else:
                if cnt_id != temp_cnt_id:
                    # document.add_paragraph('TOTAL      %s' % str(row_count - 1)) 
                    p = document.add_paragraph()
                    runner = p.add_run('TOTAL  %s' % str(row_count - 1))
                    runner.bold = True
                    # company_name.font.name = 'Cordia New (Body CS)'
                    company_name.font.name = 'AngsanaUPC'
                    runner.font.size = Pt(15)

                    table = document.add_table(rows=1, cols=13, style='TableGridLight')                    

                    a = table.cell(0, 0)
                    b = table.cell(0, 1)
                    c = table.cell(0, 12)
                    d = a.merge(c)
                    d.text = '%s' % (cnt_id)
                    d.paragraphs[0].runs[0].font.bold = True
                    d.paragraphs[0].runs[0].font.size = Pt(15)

                    row_count = 1                                
                    row = table.add_row().cells
                    row[0].text = str(row_count)
                    row[1].text = str(dly_date)
                    row[2].text = str(emp_id)
                    row[3].text = str(emp_full_name)
                    row[4].text = str(sch_rank)
                    row[5].text = str(shf_desc)
                    row[6].text = str(relieft_id)
                    row[7].text = str(ot)
                    row[8].text = str(late)                    
                    row[9].text = str(late_full)
                    row[10].text = str(ot_hr_amt)
                    row[11].text = str(tel_man)
                    row[12].text = str(tel_paid)

                    row[0].width = Cm(0.5)
                    row[3].width = Cm(5)
                    row[5].width = Cm(8)
                    
                    company_name = "  " + str(cus_name_th) + "    |    " + str(dept_id) + "   " + str(dept_en)
                    row = table.rows[0]
                    company_name = row.cells[0].paragraphs[0].add_run(company_name)
                    # company_name.font.name = 'Cordia New (Body CS)'
                    company_name.font.name = 'AngsanaUPC'
                    company_name.font.size = Pt(16)
                    company_name.bold = True
                else:
                    row = table.add_row().cells
                    row[0].text = str(row_count)
                    row[1].text = str(dly_date)
                    row[2].text = str(emp_id)
                    row[3].text = str(emp_full_name)
                    row[4].text = str(sch_rank)
                    row[5].text = str(shf_desc)
                    row[6].text = str(relieft_id)
                    row[7].text = str(ot)
                    row[8].text = str(late)                    
                    row[9].text = str(late_full)
                    row[10].text = str(ot_hr_amt)
                    row[11].text = str(tel_man)
                    row[12].text = str(tel_paid)                    

                    row[0].width = Cm(0.5)
                    row[3].width = Cm(5)
                    row[5].width = Cm(8)

            temp_cnt_id = cnt_id
            row_count += 1
    
        if len(dly_plan_obj) > 0:
            p = document.add_paragraph()
            runner = p.add_run('TOTAL  %s' % str(row_count - 1))
            runner.bold = True            
            runner.font.size = Pt(15)

        context = {
            'start_date': start_date.strftime("%d/%m/%Y"),
            'end_date': end_date.strftime("%d/%m/%Y"),
        }
        
        document.render(context)
        document.save(MEDIA_ROOT + '/monitoring/download/' + file_name + ".docx")        

    else:
        context = {
            'start_date': start_date.strftime("%d/%m/%Y"),
            'end_date': end_date.strftime("%d/%m/%Y"),
        }
        
        document.render(context)
        document.save(MEDIA_ROOT + '/monitoring/download/' + file_name + ".docx")

    # return False

    # docx2pdf
    docx_file = path.abspath("media\\monitoring\\download\\" + file_name + ".docx")
    pdf_file = path.abspath("media\\monitoring\\download\\" + file_name + ".pdf")    
    convert(docx_file, pdf_file)

    return FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')
    # return FileResponse(open(docx_file, 'rb'), content_type='application/word')



@permission_required('dailyattendreport.can_access_gpm403_daily_guard_performance_by_contract_report', login_url='/accounts/login/')
def GPM403DailyGuardPerformanceReport(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    
    today_date = settings.TODAY_DATE.strftime("%d/%m/%Y")
    contract_number_from = request.POST.get('contract_number_from')
    contract_number_to = request.POST.get('contract_number_to')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    contract_number_from = 0 if contract_number_from is None else contract_number_from
    contract_number_to = 9999999999 if contract_number_to is None else contract_number_to
    start_date = today_date if start_date is None else datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
    end_date = today_date if end_date is None else datetime.datetime.strptime(end_date, "%d/%m/%Y").date()

    '''
    print("today_date = ", today_date)
    print("contract_number_from = ", contract_number_from)
    print("contract_number_to = ", contract_number_to)
    print("start_date = ", start_date)
    print("end_date = ", end_date)
    '''

    return render(request, 'dailyattendreport/gpm403_daily_guard_performance_by_contract_report.html',
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version,
        'db_server': db_server, 
        'today_date': today_date,
        'start_date': start_date,
        'end_date': end_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        'is_error': False,
        'dly_plan_list': None,
        })


@permission_required('dailyattendreport.can_access_gpm403_daily_guard_performance_by_contract_report', login_url='/accounts/login/')
def AjaxGPM403DailyGuardPerformanceReport(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    
    today_date = settings.TODAY_DATE.strftime("%d/%m/%Y")
    contract_number_from = request.POST.get('contract_number_from')
    contract_number_to = request.POST.get('contract_number_to')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    contract_number_from = 0 if contract_number_from is None else contract_number_from
    contract_number_to = 9999999999 if contract_number_to is None else contract_number_to
    start_date = today_date if start_date is None else datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
    end_date = today_date if end_date is None else datetime.datetime.strptime(end_date, "%d/%m/%Y").date()

    sql = "select emp_fname_th, emp_lname_th, shf_desc, dept_en, cnt_id, "
    sql += "emp_id, dly_date, sch_shift, dept_id, sch_rank, "
    sql += "absent, relieft_id, tel_man, tel_paid, ot, "
    sql += "ot_hr_amt, cus_name_th, late, late_full "
    sql += "FROM V_HDLYPLAN "
    sql += "WHERE absent = 0 AND (sch_shift <> 99 OR sch_shift <> 999) "
    sql += "and (cnt_id>=" + str(contract_number_from) + " and cnt_id<=" + str(contract_number_to) + ") "
    sql += "and (dly_date>='" + str(start_date) + "' and dly_date<='" + str(end_date) + "') "
    sql += "ORDER BY cnt_id ASC, dly_date ASC, shf_desc ASC, emp_id ASC"
    print(sql)
    
    dly_plan_obj = None
    record = {}
    dly_plan_list = []
    error_message = ""

    try:                
        cursor = connection.cursor()
        cursor.execute(sql)
        dly_plan_obj = cursor.fetchall()        
    except db.OperationalError as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    except db.Error as e:
        error_message = "<b>Error: please send this error to IT team</b><br>" + str(e)
    finally:
        cursor.close()

    if dly_plan_obj is not None:
        if len(dly_plan_obj)>0:           
            for item in dly_plan_obj:             
                record = {
                    "emp_fname_th": item[0],
                    "emp_lname_th": item[1],
                    "shf_desc": item[2],
                    "dept_en": item[3],
                    "cnt_id": item[4],
                    "emp_id": item[5],
                    "dly_date": item[6].strftime("%d/%m/%Y"),
                    "sch_shift": item[7],
                    "dept_id": item[8],
                    "sch_rank": item[9],
                    "absent": item[10],
                    "relieft_id": item[11],
                    "tel_man": item[12],
                    "tel_paid": item[13],
                    "ot": item[14],
                    "ot_hr_amt": item[15],
                    "cus_name_th": item[16],
                    "late": item[17],
                    "late_full": item[18],
                }
                dly_plan_list.append(record)

    response = JsonResponse(data={        
        "is_error": False,
        "error_message": error_message,
        "dly_plan_list": list(dly_plan_list),
    })

    response.status_code = 200
    return response


@login_required(login_url='/accounts/login/')
def export_gpm_403_daily_guard_performance_by_contract_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="GPM_403.xls"'

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


@permission_required('dailyattendreport.can_access_gpm_work_on_day_off_report', login_url='/accounts/login/')
def GPMWorkOnDayOffReport(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    
    today_date = settings.TODAY_DATE.strftime("%d/%m/%Y")
    contract_number_from = request.POST.get('contract_number_from')
    contract_number_to = request.POST.get('contract_number_to')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    contract_number_from = 0 if contract_number_from is None else contract_number_from
    contract_number_to = 9999999999 if contract_number_to is None else contract_number_to
    start_date = today_date if start_date is None else datetime.datetime.strptime(start_date, "%d/%m/%Y").date()
    end_date = today_date if end_date is None else datetime.datetime.strptime(end_date, "%d/%m/%Y").date()

    return render(request, 'dailyattendreport/gpm_work_on_day_off_report.html',
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version,
        'db_server': db_server, 
        'today_date': today_date,
        'start_date': start_date,
        'end_date': end_date,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        'is_error': False,
        'dly_plan_list': None,
        })




# SELECT emp_fname_th, emp_lname_th, dept_en, cnt_id, emp_id, dept_id, sch_rank, absent, cus_name_th
# FROM R_GPM422 
# ORDER BY dept_id ASC, emp_id ASC

@permission_required('dailyattendreport.can_access_gpm_422_no_of_guard_operation_by_empl_by_zone_report', login_url='/accounts/login/')
def GPM422NoOfGuardOperationByEmplByZoneReport(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    
    today_date = settings.TODAY_DATE.strftime("%d/%m/%Y")
    work_date = request.POST.get('work_date')
    dept_zone = request.POST.get('dept_zone')

    work_date = today_date if work_date is None else datetime.datetime.strptime(work_date, "%d/%m/%Y").date()
    dept_zone_obj = None

    sql = "select dept_id, dept_en from COM_DEPARTMENT where dept_zone=1;"
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        dept_zone_obj = cursor.fetchall()
    finally:
        cursor.close()

    return render(request, 'dailyattendreport/gpm_422_no_of_guard_operation_by_empl_by_zone_report.html',
        {
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version,
        'db_server': db_server, 
        'today_date': today_date,
        'work_date': work_date,
        'dept_zone': dept_zone,
        'database': settings.DATABASES['default']['NAME'],
        'host': settings.DATABASES['default']['HOST'],
        'is_error': False,
        'dept_zone_obj': dept_zone_obj,
        })

    return render_to_response('test.html', {'persons':persons}, context_instance=RequestContext(request))

