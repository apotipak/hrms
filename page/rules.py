from django.contrib.auth.models import User
from page.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


def getDefaultLanguage(username):
    # default_language = 'th'
    default_language = 'en'

    if UserProfile.objects.filter(employee_id=username).exists():
        try:
            default_language = UserProfile.objects.filter(employee_id=username).values_list('language_code', flat=True).get()
        except UserProfile.DoesNotExists:
            default_language = 'en'
    else:
        default_language = 'en'

    return default_language    


def getDateFormatDisplay(language):
    today_day = timezone.now().day
    today_month = timezone.now().strftime('%B')
    if language == "th":
    	#today_year = timezone.now().year + 543
    	today_year = timezone.now().year
    else:
    	today_year = timezone.now().year
    today_date = str(today_day) + " " + today_month + " " + str(today_year)	
    return today_date


def zone_name_display_text(zone_id):
    zone_id = str(zone_id).strip()    
    zone_name = "N/A"    
    if zone_id=="0":
        zone_name = "Zone F"
    elif zone_id=="2050":
        zone_name = "A"
    elif zone_id=="2051":
        zone_name = "B"
    elif zone_id=="2052":
        zone_name = "C1"
    elif zone_id=="2053":
        zone_name = "D"
    elif zone_id=="2054":
        zone_name = "E"
    elif zone_id=="2055":
        zone_name = "F"
    elif zone_id=="2056":
        zone_name = "G"
    elif zone_id=="2057":
        zone_name = "H"
    elif zone_id=="2058":
        zone_name = "S"
    elif zone_id=="2059":
        zone_name = "CR"
    elif zone_id=="2060":
        zone_name = "PID"
    elif zone_id=="2061":
        zone_name = "SM"
    elif zone_id=="2062":
        zone_name = "P"
    elif zone_id=="2063":
        zone_name = "Nakornsrithamrat"
    elif zone_id=="2064":
        zone_name = "Krabi"
    elif zone_id=="2065":
        zone_name = "Suratthani"
    elif zone_id=="2066":
        zone_name = "Udonthani"
    elif zone_id=="2067":
        zone_name = "SP-ZoneC2"
    elif zone_id=="2068":
        zone_name = "K"
    elif zone_id=="2069":
        zone_name = "C"
    elif zone_id=="2070":
        zone_name = "BEM"
    elif zone_id=="2071":
        zone_name = "I"
    elif zone_id=="2073":
        zone_name = "R"
    elif zone_id=="3099":
        zone_name = "ES Engineer"
    elif zone_id=="3335":
        zone_name = "SK"
    elif zone_id=="9999":
        zone_name = "Zone 0"

    return zone_name

