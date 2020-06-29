from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from page.rules import *
from .forms import ChangePasswordForm, LanguageForm
from django.utils import translation
from django.contrib import messages
from django.utils.translation import ugettext as _


@login_required(login_url='/accounts/login/')
def index(request):
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE

	return render(request, 'index.html', {
		'project_name': project_name, 
		'project_version': project_version, 
		'db_server': db_server, 
		'today_date': today_date
	})


@login_required(login_url='/accounts/login/')
def userprofile(request):
    user_language = getDefaultLanguage(request.user.username)
    translation.activate(user_language)

    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = getDateFormatDisplay(user_language)   

    return render(request, 'page/user_profile.html', {
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
    })


@login_required(login_url='/accounts/login/')
def userpassword(request):
    user_language = getDefaultLanguage(request.user.username)
    translation.activate(user_language)

    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = getDateFormatDisplay(user_language)   

    form = ChangePasswordForm(request.POST, user=request.user)
    
    if request.method == "POST":
        if form.is_valid():            
            new_password = form.cleaned_data['new_password']
            u = User.objects.get(username__exact=request.user)
            u.set_password(new_password)
            u.save()            
            return HttpResponseRedirect('/staff-profile')
    else:
        form = ChangePasswordForm(user=request.user)   

    return render(request, 'page/user_password.html', {
        'form': form,
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
    })


@login_required(login_url='/accounts/login/')
def userlanguage(request):
    user_language = getDefaultLanguage(request.user.username)
    translation.activate(user_language)

    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = getDateFormatDisplay(user_language)   

    form = LanguageForm(request.POST, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            language_code = form.cleaned_data['language_code']
            username = request.user.username
            userid = request.user.id

            print("language_code = " + str(language_code))

            if not UserProfile.objects.filter(employee_id=username).exists():
                print("debug 1")
                UserProfile.objects.create(language_code=language_code, updated_by_id=userid, employee_id=username)
            else:
                print("debug 2")
                employee = UserProfile.objects.get(employee_id=username)
                employee.language_code = language_code
                employee.updated_by_id = userid
                employee.employee_id = username
                employee.save()
            
            messages.success(request, _('ตั้งค่าใหม่สำเร็จ'))
            return HttpResponseRedirect('/user-language')
    else:
        form = LanguageForm(user=request.user)    

    return render(request, 'page/user_language.html', {
        'form': form,
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
    })
