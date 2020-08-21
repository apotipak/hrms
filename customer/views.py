from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import generic
from .models import Customer, CusMain
from .forms import CustomerCreateForm, CusMainForm, CusSiteForm
# from .forms import CustomerUpdateForm
from .forms import CustomerSearchForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from system.models import TDistrict, TCity
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


@login_required(login_url='/accounts/login/')
def get_district_list_modal(request):

    '''
    queryset = TDistrict.objects.select_related('tcity').all()
    districts = []
    for district in queryset:
        district.append({'dist_id': district.dist_id})
    '''

    queryset = CusMain.objects.select_related('cus_city').all()
    cusmain = []
    for cus in queryset:
        cusmain.append({'cus_id': cus.cus_id})

    item_per_page = 8
    page_no = request.GET["page_no"]
    city_name = request.GET["city_name"]
    print("GET_DISTRICT_LIST_MODAL: city_name = ")
    print(city_name)
    
    # city_name = 'จันทบุรี'
    if city_name != '':
        #data = TDistrict.objects.raw("select d.dist_id,d.dist_th,d.dist_en,c.city_id,c.city_th,c.city_en from t_district d join t_city c on d.city_id = c.city_id where c.city_en = %s", [u'bangkok']) or None
        data = TDistrict.objects.raw("select d.dist_id,d.dist_th,d.dist_en,c.city_id,c.city_th,c.city_en from t_district d join t_city c on d.city_id = c.city_id order by c.city_th") or None
    else:
        data = TDistrict.objects.raw("select d.dist_id,d.dist_th,d.dist_en,c.city_id,c.city_th,c.city_en from t_district d join t_city c on d.city_id = c.city_id order by c.city_th") or None


    '''
    if city_name:
        data = TDistrict.objects.raw("select d.dist_id,d.dist_th,d.dist_en,c.city_id,c.city_th,c.city_en from t_district d join t_city c on d.city_id = c.city_id where c.city_name like '%'" + city_name + "'" + " order by c.city_th") or None
    else:
        data = TDistrict.objects.raw("select d.dist_id,d.dist_th,d.dist_en,c.city_id,c.city_th,c.city_en from t_district d join t_city c on d.city_id = c.city_id order by c.city_th") or None
    '''

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
                "city_id": d.city_id,
                "dist_th": d.dist_th,
                "dist_en": d.dist_en,
                "city_th": d.city_th
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
            "next_page" : next_page,
            "previous_page" : previous_page,
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

    '''
    response = JsonResponse(data={
        "test" : "test"
    })

    response.status_code = 200
    return response
    '''

@login_required(login_url='/accounts/login/')
def get_district_list(request):        
    item_per_page = 8

    if request.method == "POST":
        print("method post")
        data = TDistrict.objects.raw("select d.dist_id,d.dist_th,d.dist_en,c.city_id,c.city_th,c.city_en \
            from t_district d join t_city c on d.city_id = c.city_id order by c.city_th") or None

        page = 1
        paginator = Paginator(data, item_per_page)
        is_paginated = True if paginator.num_pages > 1 else False        

        try:
            current_page = paginator.get_page(page)
        except InvalidPage as e:
            raise Http404(str(e))

    else:
        print("method get")
        data = TDistrict.objects.raw("select d.dist_id as dist_id, d.dist_th as dist_th, d.dist_en as dist_en, c.city_id as city_id, c.city_th as city_th, c.city_en as city_en \
            from t_district d join \
            t_city c on d.city_id = c.city_id order by c.city_th") or None

        #data = TDistrict.objects.raw("select * from t_district")
        data = TDistrict.objects.select_related('city_id')

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
                "dist_id": d.dist_id, #d.dist_id, 
                "city_id": d.city_id_id, #d.city_id,
                "dist_th": d.dist_th, #d.dist_th,
                "dist_en": d.dist_en, #d.dist_en,
                "city_th": d.city_id.city_th, #d.city_th
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


def CustomerUpdate(request, pk):
    template_name = 'customer/customer_update.html'
    
    customer = get_object_or_404(Customer, pk=pk)
    cus_main = []
    if customer:
        cus_main = CusMain.objects.filter(cus_id=customer.cus_id).get()

    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=customer)
        cus_main_form = CusMainUpdateForm(instance=cus_main)
    else:
        form = CustomerUpdateForm(instance=customer)
        cus_main_form = CusMainUpdateForm(instance=cus_main)

    data = dict()
    form_is_valid = False
    update_message = ""

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            
            if request.user.is_superuser:
                obj.upd_by = 'Superuser'
            else:
                obj.upd_by = request.user.first_name

            if obj.upd_flag == 'A':
                obj.upd_flag = 'E'

            obj.upd_date = timezone.now()

            obj.save()
            form_is_valid = True            
            update_message = "ทำรายการสำเร็จ"
        else:
            form_is_valid = False
            update_message = "ไม่สามารถทำรายการได้..!"

    context = {
        'page_title': settings.PROJECT_NAME,
        'today_date': settings.TODAY_DATE,
        'project_version': settings.PROJECT_VERSION,
        'db_server': settings.DATABASES['default']['HOST'],
        'project_name': settings.PROJECT_NAME,
        'form': form, 
        'cus_main_form': cus_main_form,
        'customer': customer,
        'cus_main': cus_main,
        'request': request,
        'form_is_valid': form_is_valid,
        'update_message': update_message,   
    }
    return render(request, template_name, context)


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


def CusMainUpdate(request, pk):
    template_name = 'customer/customer_update.html'
    
    customer = get_object_or_404(Customer, pk=pk)
    cus_main = []

    if customer:
        cus_main = CusMain.objects.filter(cus_id=customer.cus_id).get()

    if request.method == 'POST':
        # form = CustomerUpdateForm(request.POST, instance=customer)
        cus_main_form = CusMainForm(request.POST, instance=cus_main)
    else:
        # form = CustomerUpdateForm(instance=customer)
        cus_main_form = CusMainForm(instance=cus_main)        
        print("test - update cus_main")
        print(cus_main.cus_active)


    data = dict()
    form_is_valid = False
    cus_main_form_is_valid = False
    update_message = ""

    if request.method == 'POST':
        if cus_main_form.is_valid():            
            print("cus_main_form is valid")
            obj = cus_main_form.save(commit=False)
            obj.upd_by = request.user.first_name
            obj.upd_date = timezone.now()
            obj.save()

            '''
            obj = form.save(commit=False)
            
            if request.user.is_superuser:
                obj.upd_by = 'Superuser'
            else:
                obj.upd_by = request.user.first_name

            if obj.upd_flag == 'A':
                obj.upd_flag = 'E'

            obj.upd_date = timezone.now()

            obj.save()
            form_is_valid = True            
            '''
            cus_main_form_is_valid = True
            message = "ทำรายการสำเร็จ"
            data['message'] = "ทำรายการสำเร็จ"
        else:
            print("cus_main_form is not valid")
            cus_main_form_is_valid = False
            message = "ไม่สามารถทำรายการได้..!"
            data['message'] = "ทำรายการสำเร็จ"

    print("customer cus_active = " + str(customer.cus_active))

    context = {
        'page_title': settings.PROJECT_NAME,
        'today_date': settings.TODAY_DATE,
        'project_version': settings.PROJECT_VERSION,
        'db_server': settings.DATABASES['default']['HOST'],
        'project_name': settings.PROJECT_NAME,
        'cus_main_form': cus_main_form,
        'customer': customer,
        'cus_main': cus_main,
        'request': request,
        'cus_main_form_is_valid': cus_main_form_is_valid,
        'form_is_valid': form_is_valid,
        'update_message': update_message,   
    }
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def update_cus_main(request):

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
            
            # cus_main = CusMain.objects.get(cus_id=cus_id)            
            # cus_main.upd_by = request.user.first_name

            '''
            if cus_main.upd_flag == 'A':
                cus_main.upd_flag = 'E'
            
            cus_main.cus_active = cus_active
            cus_main.upd_date = timezone.now()            
            cus_main_form = CusMainForm(request.POST, instance=cus_main)
            cus_main_form.save()
            '''

            cus_main = get_object_or_404(CusMain, pk=cus_id)
            cus_main.cus_active = cus_active
            cus_main.cus_name_th = cus_name_th
            cus_main.cus_add1_th = cus_add1_th
            cus_main.cus_add2_th = cus_add2_th
            cus_main.cus_subdist_th = cus_subdist_th
            
            cus_main.cus_name_en = cus_name_en
            cus_main.cus_add1_en = cus_add1_en
            cus_main.cus_add2_en = cus_add2_en
            cus_main.cus_subdist_en = cus_subdist_en

            if cus_main.upd_flag == 'A':
                cus_main.upd_flag = 'E'
            cus_main.upd_by = request.user.first_name
            cus_main.upd_date = timezone.now()
            
            cus_main.save()

            response_data['result'] = "Save customer main office success."
            response_data['message'] = "ทำรายการสำเร็จ"
            response_data['form_is_valid'] = True
        else:
            response_data['form_is_valid'] = False
            response_data['message'] = ""
            if form.errors:
                for field in form:
                    for error in field.errors:
                        response_data['message'] += error + "<br>"
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
    
    print("todo: update_cus_site")

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

            # print(str(cus_no) + ", " + str(cus_id) + ", " + str(cus_brn))
            # print(str(cus_active) + ", " + str(cus_name_th) + ", " + str(cus_add1_th) + ", " + str(cus_add2_th) + ", " + str(cus_subdist_th))
            # print(str(cus_active) + ", " + str(cus_name_en) + ", " + str(cus_add1_en) + ", " + str(cus_add2_en) + ", " + str(cus_subdist_en))            

            customer = get_object_or_404(Customer, pk=cus_no)

            # TODO
            select_district_id = request.POST.get('select_district_id')
            district = TDistrict.objects.get(dist_id=select_district_id)
            old_district_id = customer.cus_district.dist_id
            customer.cus_district_id = select_district_id
            #print("old cus_district = " + str(old_district_id) + " | new = " + str(select_district_id))

            customer.cus_active = cus_active
            customer.cus_name_th = cus_name_th
            customer.cus_add1_th = cus_add1_th
            customer.cus_add2_th = cus_add2_th
            customer.cus_subdist_th = cus_subdist_th
            customer.cus_name_en = cus_name_en
            customer.cus_add1_en = cus_add1_en
            customer.cus_add2_en = cus_add2_en
            customer.cus_subdist_en = cus_subdist_en

            if customer.upd_flag == 'A':
                customer.upd_flag = 'E'
            customer.upd_by = request.user.first_name
            customer.upd_date = timezone.now()
            
            customer.save()

            response_data['result'] = "Save customer main office success."
            response_data['message'] = "ทำรายการสำเร็จ"
            response_data['form_is_valid'] = True
        else:
            response_data['form_is_valid'] = False
            response_data['message'] = ""
            if form.errors:
                for field in form:
                    for error in field.errors:
                        response_data['message'] += error + "<br>"
            else:
                response_data['message'] = "ไม่สามารถทำรายการได้..!"
    else:
        response_data['result'] = "There is an error!"
        response_data['message'] = "ไม่สามารถทำรายการได้..!"
        response_data['form_is_valid'] = False        

    return JsonResponse(response_data)