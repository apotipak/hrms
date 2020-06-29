from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from page.rules import *
from django.utils import translation
from django.utils.translation import ugettext as _


@login_required(login_url='/accounts/login/')
def index(request):
	page_title = settings.PROJECT_NAME
	db_server = settings.DATABASES['default']['HOST']
	project_name = settings.PROJECT_NAME
	project_version = settings.PROJECT_VERSION
	today_date = settings.TODAY_DATE

	return render(request, 'index.html', {
		'page_title': page_title, 
		'project_name': project_name, 
		'project_version': project_version, 
		'db_server': db_server, 
		'today_date': today_date
	})


@login_required(login_url='/accounts/login/')
def userprofile(request):
    user_language = getDefaultLanguage(request.user.username)
    translation.activate(user_language)

    page_title = settings.PROJECT_NAME
    db_server = settings.DATABASES['default']['HOST']
    project_name = settings.PROJECT_NAME
    project_version = settings.PROJECT_VERSION
    today_date = getDateFormatDisplay(user_language)   

    '''
    if user_language == "th":
        username_display = LeaveEmployee.objects.filter(emp_id=request.user.username).values_list('emp_fname_th', flat=True).get()
    else:
        username_display = LeaveEmployee.objects.filter(emp_id=request.user.username).values_list('emp_fname_en', flat=True).get()
    '''
    
    username_display = "en"

    return render(request, 'page/user_profile.html', {
        'form': form,
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'username_display': username_display,
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

            if not UserProfile.objects.filter(username=username).exists():
                print("debug 1")
                UserProfile.objects.create(language=language_code, updated_by_id=userid, username=username)
            else:
                print("debug 2")
                employee = UserProfile.objects.get(username=username)
                employee.language = language_code
                employee.updated_by_id = userid
                employee.username = username
                employee.save()
            
            messages.success(request, _('A new language has been set.'))
            return HttpResponseRedirect('/staff-language')
    else:
        form = LanguageForm(user=request.user)    

    if user_language == "th":
        username_display = LeaveEmployee.objects.filter(emp_id=request.user.username).values_list('emp_fname_th', flat=True).get()
    else:
        username_display = LeaveEmployee.objects.filter(emp_id=request.user.username).values_list('emp_fname_en', flat=True).get()

    return render(request, 'page/user_language.html', {
        'form': form,
        'page_title': page_title, 
        'project_name': project_name, 
        'project_version': project_version, 
        'db_server': db_server, 
        'today_date': today_date,
        'username_display': username_display,
    })
