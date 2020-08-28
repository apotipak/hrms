from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import generic
from .models import Customer, CusMain, CusBill, CustomerOption
from .forms import CustomerCreateForm, CusMainForm, CusSiteForm, CusBillForm
from .forms import CustomerSearchForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from system.models import TDistrict, TCity, CusContact
from django.core import serializers
import json
import sys, locale


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

        print("post")
        print("POST: cus_name = " +  str(cus_name))
        print("POST: cus_id = " +  str(cus_id))
        print("POST: cus_brn = " +  str(cus_brn))

        # cus_name
        if cus_name!='' and cus_id!='' and cus_brn!='':
            print("post case 1")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).filter(cus_id=cus_id).filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_name!='' and cus_id=='' and cus_brn=='':
            print("post case 2")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).order_by('cus_id', 'cus_brn', '-cus_active')

        if cus_name!='' and cus_id=='' and cus_brn!='':
            print("post case 3")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_name=='' and cus_id!='' and cus_brn!='':
            print("post case 4")
            customer_list = Customer.objects.order_by('-cus_active','cus_id','cus_brn')

        if cus_name=='' and cus_id=='' and cus_brn=='':
            print("post case 5")
            customer_list = Customer.objects.order_by('cus_id', 'cus_brn', '-cus_active')            

        # cus_id
        if cus_id!='' and cus_name=='' and cus_brn=='':
            print("post case 6")
            customer_list = Customer.objects.filter(cus_id=cus_id).order_by('-cus_active','cus_id','cus_brn')

        if cus_id!='' and cus_name!='' and cus_brn=='':
            print("post case 7")
            customer_list = Customer.objects.filter(cus_id=cus_id).filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).order_by('-cus_active','cus_id','cus_brn')

        if cus_id!='' and cus_name=='' and cus_brn!='':
            print("post case 8")
            customer_list = Customer.objects.filter(cus_id=cus_id).filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        # cus_brn
        if cus_brn!='' and cus_name=='' and cus_id=='':
            print("post case 9")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_brn!='' and cus_name!='' and cus_id=='':
            print("post case 10")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).order_by('-cus_active','cus_id','cus_brn')

        if cus_brn!='' and cus_name=='' and cus_id!='':
            print("post case 11")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).filter(cus_id=cus_id).order_by('-cus_active','cus_id','cus_brn')

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
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).filter(cus_id=cus_id).filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_name!='' and cus_id=='' and cus_brn=='':
            print("get case 2")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).order_by('-cus_active','cus_id','cus_brn')

        if cus_name!='' and cus_id=='' and cus_brn!='':
            print("get case 3")
            customer_list = Customer.objects.filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_name=='' and cus_id!='' and cus_brn!='':
            print("get case 4")
            customer_list = Customer.objects.order_by('-cus_active','cus_id','cus_brn')

        if cus_name=='' and cus_id=='' and cus_brn=='':
            print("get case 5")
            # customer_list = Customer.objects.order_by('-cus_active','cus_id','cus_brn')
            customer_list = Customer.objects.order_by('cus_id','cus_brn','-cus_active')

        # cus_id
        if cus_id!='' and cus_name=='' and cus_brn=='':
            print("post case 6")
            customer_list = Customer.objects.filter(cus_id=cus_id).order_by('-cus_active','cus_id','cus_brn')

        if cus_id!='' and cus_name!='' and cus_brn=='':
            print("get case 7")
            customer_list = Customer.objects.filter(cus_id=cus_id).filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).order_by('-cus_active','cus_id','cus_brn')

        if cus_id!='' and cus_name=='' and cus_brn!='':
            print("get case 8")
            customer_list = Customer.objects.filter(cus_id=cus_id).filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        # cus_brn
        if cus_brn!='' and cus_name=='' and cus_id=='':
            print("post case 9")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).order_by('-cus_active','cus_id','cus_brn')

        if cus_brn!='' and cus_name!='' and cus_id=='':
            print("get case 10")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).filter(Q(cus_name_en__contains=cus_name) | Q(cus_name_th__contains=cus_name)).order_by('-cus_active','cus_id','cus_brn')

        if cus_brn!='' and cus_name=='' and cus_id!='':
            print("get case 11")
            customer_list = Customer.objects.filter(cus_brn=cus_brn).filter(cus_id=cus_id).order_by('-cus_active','cus_id','cus_brn')

        paginator = Paginator(customer_list, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False
        page = request.GET.get('page', '1') or 1

        try:
            current_page = paginator.get_page(page)
            print("current_page = " + str(current_page))
            print("current_page.number = " + str(current_page.number))        
            print("current_page.paginator.num_pages = " + str(current_page.paginator.num_pages))
            
            print("current_page.has_next = " + str(current_page.has_next))
            print("current_page.has_previous = " + str(current_page.has_previous))            
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
    template_name = 'customer/customer_update.html'
    
    customer = get_object_or_404(Customer, pk=pk)
    cus_main = None
    cus_site = None
    cus_bill = None

    if customer:
        # cus_main = CusMain.objects.filter(cus_id=customer.cus_id).get()
        # cus_site = Customer.objects.filter(cus_no=pk).get()

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
        except CusBill.DoesNotExist:
            cus_bill = None

    if request.method == 'POST':        
        cus_main_form = CusMainForm(request.POST, instance=cus_main, cus_no=pk)
        cus_site_form = CusSiteForm(request.POST, instance=cus_site)
        cus_bill_form = CusBillForm(request.POST, instance=cus_bill)
    else:
        cus_main_form = CusMainForm(instance=cus_main, cus_no=pk)    
        cus_site_form = CusSiteForm(instance=cus_site)
        cus_bill_form = CusBillForm(instance=cus_bill)

    # print("customer cus_active = " + str(customer.cus_active))
    customer_option_list = CustomerOption.objects.values_list('btype', flat=True).exclude(btype=None).order_by('btype').distinct()        

    context = {
        'page_title': settings.PROJECT_NAME,
        'today_date': settings.TODAY_DATE,
        'project_version': settings.PROJECT_VERSION,
        'db_server': settings.DATABASES['default']['HOST'],
        'project_name': settings.PROJECT_NAME,

        'cus_main_form': cus_main_form,
        'cus_main': cus_main,
        'cus_site_form': cus_site_form,
        'cus_site': cus_site,
        'cus_bill_form': cus_bill_form,
        'cus_bill': cus_bill,
        'customer': customer,        
        'request': request,
        'customer_option_list': customer_option_list,
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
    
    print("current_district_id = " + str(current_district_id))

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
        if current_district_id != "":
            district_object = TDistrict.objects.filter(dist_id__exact=current_district_id).get()                        
            print("city name th = " + str(district_object.city_id.city_en))

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
        print("current_page = " + str(current_page))
        print("current_page.number = " + str(current_page.number))        
        print("current_page.paginator.num_pages = " + str(current_page.paginator.num_pages))
        
        print("current_page.has_next = " + str(current_page.has_next))
        print("current_page.has_previous = " + str(current_page.has_previous))
    
        current_page_number = current_page.number
        current_page_paginator_num_pages = current_page.paginator.num_pages

        pickup_dict = {}
        pickup_records=[]
        
        for d in current_page:
            print("debug 1")
            record = {
                "dist_id": d.dist_id,
                "city_id": d.city_id_id,
                "dist_th": d.dist_th,
                "dist_en": d.dist_en,
                "city_th": d.city_id.city_th,
                "city_en": d.city_id.city_en,
            }
            pickup_records.append(record)

        # serialized_qs = serializers.serialize('json', current_page)
        #print(serialized_qs);
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
    print("todo : save_customer_form")
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
def CustomerCreate(request):
    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION  
    today_date = settings.TODAY_DATE
    return render(request, 'customer/customer_create.html', {'page_title': page_title, 'project_name': project_name, 'project_version': project_version, 'db_server': db_server, 'today_date': today_date})


def CustomerDelete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    data = dict()
    if request.method == 'POST':
        customer.delete()
        data['form_is_valid'] = True
        #customer_list = Customer.objects.all()
        customer_list = Customer.objects.filter(cus_id__in=[2094]).order_by('-upd_date', 'cus_id', '-cus_active')
        data['html_customer_list'] = render_to_string('customer/partial_customer_list.html', {
            'customer_list': customer_list
        })
        data['message'] = "ทำรายการสำเร็จ"
    else:
        data['message'] = "ไม่สามารถทำรายการได้..!"
        context = {'customer': customer}        
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
        print("method post")
        data = TDistrict.objects.raw("select d.dist_id,d.dist_th,d.dist_en,c.city_id,c.city_th,c.city_en from t_district d join t_city c on d.city_id = c.city_id order by c.city_th") or None

        page = 1
        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))
    else:
        print("method get")
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
            print("debug 1")
            record = {
                "dist_id": d.dist_id, 
                "city_id": d.city_id,
                "dist_th": d.dist_th,
                "dist_en": d.dist_en,
                "city_th": d.city_th
            }
            pickup_records.append(record)

        serialized_qs = serializers.serialize('json', current_page)
        print(serialized_qs);
        print("has_previous : " + str(current_page.has_previous))
        
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
    print("****************************")

    template_name = 'customer/customer_update.html'    
    response_data = {}

    if request.method == 'POST':
        form = CusMainForm(request.POST)

        if form.is_valid():
            cus_active = request.POST.get('cus_main_cus_active')
            cus_no = request.POST.get('cus_no')
            cus_id = request.POST.get('cus_id')
            cus_brn = request.POST.get('cus_brn')
            
            cus_name_th = request.POST.get('cus_main_cus_name_th')            
            cus_add1_th = request.POST.get('cus_main_cus_add1_th')
            cus_add2_th = request.POST.get('cus_main_cus_add2_th')
            cus_subdist_th = request.POST.get('cus_main_cus_subdist_th')            
            
            cus_name_en = request.POST.get('cus_main_cus_name_en')                          
            cus_add1_en = request.POST.get('cus_main_cus_add1_en')
            cus_add2_en = request.POST.get('cus_main_cus_add2_en')
            cus_subdist_en = request.POST.get('cus_main_cus_subdist_en')

            cus_zip = request.POST.get('cus_main_cus_zip')

            cus_tel = request.POST.get('cus_main_cus_tel')
            cus_fax = request.POST.get('cus_main_cus_fax')
            cus_email = request.POST.get('cus_main_cus_email')
            cus_zone = request.POST.get('cus_main_cus_zone')
            
            business_type = request.POST.get('cus_main_business_type')

            cus_main_cus_contact_id = request.POST.get('cus_main_cus_contact_id')            

            '''
            if cus_main.upd_flag == 'A':
                cus_main.upd_flag = 'E'
            
            cus_main.cus_active = cus_active
            cus_main.upd_date = timezone.now()            
            cus_main_form = CusMainForm(request.POST, instance=cus_main)
            cus_main_form.save()
            '''

            cus_main = get_object_or_404(CusMain, pk=cus_id)

            select_district_id = request.POST.get('select_district_id')
            print("cus_main_select_district_id = " + str(select_district_id))

            district_obj = TDistrict.objects.get(dist_id=select_district_id)
            if district_obj:
                city_id = district_obj.city_id_id
                old_district_id = cus_main.cus_district.dist_id
                cus_main.cus_district_id = select_district_id
                cus_main.cus_city = district_obj.city_id                
                city_obj = TCity.objects.get(city_id=city_id)
                cus_main.cus_country = city_obj.country_id

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

            cus_main.cus_contact_id = cus_main_cus_contact_id

            if cus_main.upd_flag == 'A':
                cus_main.upd_flag = 'E'
            cus_main.upd_by = request.user.first_name
            cus_main.upd_date = timezone.now()
            
            cus_main.save()

            # Business Type
            print("business_type = " + business_type)

            response_data['result'] = "Update complete."
            response_data['message'] = "ทำรายการสำเร็จ"
            response_data['form_is_valid'] = True
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


        return JsonResponse(response_data)
    else:
        print("debug - found cus_main_form problem")

    context = {
        'page_title': settings.PROJECT_NAME,
        'today_date': settings.TODAY_DATE,
        'project_version': settings.PROJECT_VERSION,
        'db_server': settings.DATABASES['default']['HOST'],
        'project_name': settings.PROJECT_NAME,
    }
    return render(request, template_name, context)    


@login_required(login_url='/accounts/login/')
def update_cus_site(request):
    
    print("*************************")
    print("FUNCTION: update_cus_site")
    print("*************************")

    template_name = 'customer/customer_update.html'    
    response_data = {}

    if request.method == 'POST':
        form = CusSiteForm(request.POST)
        if form.is_valid():

            cus_no = request.POST.get('cus_no')
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
            cus_tel = request.POST.get('cus_site_cus_tel')
            cus_fax = request.POST.get('cus_site_cus_fax')
            cus_email = request.POST.get('cus_site_cus_email')
            cus_zone = request.POST.get('cus_site_cus_zone')

            cus_site_cus_contact_con_sex = request.POST.get('cus_site_cus_contact_con_sex')
            #print("sex = " + str(cus_site_cus_contact_con_sex))

            cus_site_site_contact_id = request.POST.get('cus_site_site_contact_id')

            customer = get_object_or_404(Customer, pk=cus_no)
            
            select_district_id = request.POST.get('select_district_id')
            print("cus_site_select_district_id = " + str(select_district_id))

            district_obj = TDistrict.objects.get(dist_id=select_district_id)
            if district_obj:
                city_id = district_obj.city_id_id
                old_district_id = customer.cus_district.dist_id
                customer.cus_district_id = select_district_id
                customer.cus_city = district_obj.city_id
                
                # TODO
                city_obj = TCity.objects.get(city_id=city_id)                
                # print(city_obj.country_id)
                customer.cus_country = city_obj.country_id

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

            customer.site_contact_id = cus_site_site_contact_id

            if customer.upd_flag == 'A':
                customer.upd_flag = 'E'
            customer.upd_by = request.user.first_name
            customer.upd_date = timezone.now()
            
            customer.save()

            response_data['result'] = "Update complete."
            response_data['message'] = "ทำรายการสำเร็จ"
            response_data['form_is_valid'] = True
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

    else:
        response_data['result'] = "There is an error!"
        response_data['message'] = "ไม่สามารถทำรายการได้..!"
        response_data['form_is_valid'] = False        

    return JsonResponse(response_data)



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
    
    print("current_contact_id = " + str(current_contact_id))
    print("search_contact_option = " + str(search_contact_option))
    print("search_contact_text = " + str(search_contact_text))

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
    print("current_contact_id : " + str(current_contact_id))

    item_per_page = 100

    if request.method == "POST":        
        data = Contact.objects.filter(con_id__exact=current_contact_id)

        page = 1
        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))
    else:
        print("method get")
        data = CusContact.objects.filter(con_id__exact=current_contact_id)

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

    data = CusContact.objects.filter(con_id__exact=contact_id)

    if data:
        print("success")

        pickup_dict = {}
        pickup_records=[]
        
        for d in data:
            print("debug 1")
            record = {
                "con_id": d.con_id,
                "con_fname_th": d.con_fname_th,
                "con_lname_th": d.con_lname_th,
                "con_position_th": d.con_position_th,
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

