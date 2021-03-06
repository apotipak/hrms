from django import forms
from .models import Customer, CusMain, CusBill, CustomerOption
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _
from system.models import CusContact, ComZone, TTitle, TNation
from django.core.exceptions import ValidationError


class CustomerCodeCreateForm(forms.Form):
    # ID
    cus_id = forms.CharField()
    cus_brn = forms.CharField(required=False)

    # Customer Main Office    
    cus_main_cus_zone = forms.ModelChoiceField(queryset=None, required=False)
    customer_group_id = forms.ModelChoiceField(queryset=None, required=False)
    customer_option_btype = forms.ModelChoiceField(queryset=None, required=False)
    customer_option_op2 = forms.ModelChoiceField(queryset=None, required=False)
    customer_option_op3 = forms.ModelChoiceField(queryset=None, required=False)
    cus_main_customer_option_opn1 = forms.IntegerField(required=False)

    # Customer Site
    cus_site_cus_zone = forms.ModelChoiceField(queryset=None, required=False)

    # Customer Billing
    cus_bill_cus_zone = forms.ModelChoiceField(queryset=None, required=False)

    # amnaj
    # Contact Title
    contact_title_list = forms.ModelChoiceField(queryset=None, required=False)
    
    cus_main_cus_contact_cus_title_en = forms.CharField(required=False)
    cus_site_site_contact_cus_title_en = forms.CharField(required=False)
    cus_bill_cus_contact_cus_title_en = forms.CharField(required=False)

    # Contact Nation
    contact_nation_list = forms.ModelChoiceField(queryset=None, required=False)
    cus_main_cus_contact_nation_th = forms.CharField(required=False)
    cus_main_cus_contact_nation_en = forms.CharField(required=False)


    # Site Title
    cus_site_site_contact_cus_title_en = forms.CharField(required=False)

    # Bill Title
    cus_bill_cus_contact_cus_title_en = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerCodeCreateForm, self).__init__(*args, **kwargs)
        
        self.fields['cus_id'].widget.attrs={'class': 'form-control form-control-md'}
        self.fields['cus_brn'].widget.attrs={'class': 'form-control form-control-md'}
        self.fields['cus_main_cus_zone'].queryset=ComZone.objects.all()

        self.fields['customer_group_id'].queryset = Customer.objects.values_list('cus_taxid', flat=True).exclude(cus_taxid=None).order_by('cus_taxid').distinct()
        self.fields['customer_option_btype'].queryset = CustomerOption.objects.values_list('btype', flat=True).exclude(btype=None).order_by('btype').distinct()
        self.fields['customer_option_op2'].queryset = CustomerOption.objects.values_list('op2', flat=True).exclude(op2=None).order_by('op2').distinct()
        self.fields['customer_option_op3'].queryset = CustomerOption.objects.values_list('op3', flat=True).exclude(op2=None).order_by('op3').distinct()
        
        self.fields['cus_site_cus_zone'].queryset=ComZone.objects.all()
        self.fields['cus_bill_cus_zone'].queryset=ComZone.objects.all()

        # GP Margin
        self.fields['cus_main_customer_option_opn1'].initial = 0.00

        self.fields['customer_group_id'].empty_label = None
        self.fields['customer_option_btype'].empty_label = None
        self.fields['customer_option_op2'].empty_label = None
        self.fields['customer_option_op3'].empty_label = None


        # Contact Title        
        # self.fields['contact_title_list'].queryset=TTitle.objects.all().filter(title_id__in=[3,4,5,129,200]).order_by('-title_id')
        self.fields['contact_title_list'].queryset=TTitle.objects.all().exclude(upd_flag='D').order_by('-title_id')
        self.fields['cus_main_cus_contact_cus_title_en'].initial = "Khun"
        self.fields['cus_site_site_contact_cus_title_en'].initial = "Khun"
        self.fields['cus_bill_cus_contact_cus_title_en'].initial = "Khun"

        # Contact Nation
        # self.fields['contact_nation_list'].queryset=TNation.objects.all().exclude(upd_flag='D').filter(nation_id__in=[0,1,4,5,11,9,29,44,46,47,97,99]).order_by('-nation_id')
        self.fields['contact_nation_list'].queryset=TNation.objects.all().exclude(upd_flag='D').order_by('-nation_id')        


    def clean_cus_id(self):
        data = self.data.get('cus_id')
        if data.isnumeric():
            if len(data) > 7:
                raise ValidationError("Customer ID is not correct.")

            return int(data)
        else:
            raise ValidationError("Customer ID is not correct.")

    def clean_cus_brn(self):        
        data = self.data.get('cus_brn')        
        if data.isnumeric():
            if len(data) > 3:
                raise ValidationError("Customer Branch is not correct!")
            return data
        else:
            if data == '':
                data = 0
                return data
            else:
                raise ValidationError("Customer Branch is not correct!")


class CusSiteCreateForm(forms.ModelForm):
    cus_site_cus_id = forms.CharField()

    class Meta:
        model = CusMain
        exclude = ['cus_no','cus_id','cus_brn','cus_zone','cus_contact','site_contact','cus_district','cus_country','cus_city']

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user')
        super(CusSiteCreateForm, self).__init__(*args, **kwargs)
        self.fields['cus_site_cus_id'].widget.attrs={'class': 'form-control form-control-sm'}
        
    def clean_cus_site_cus_id(self):
        data = self.data.get('cus_site_cus_id')
        if data.isnumeric():
            return data
        else:
            raise ValidationError("Customer ID is not correct!")

        
class CustomerCreateForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('cus_id', 'cus_brn', 'cus_name_th', 'cus_name_en', 'cus_add1_th', 'cus_add1_en', 'cus_add2_th', 'cus_add2_en', 'cus_subdist_en', 'cus_subdist_th')

        widgets = {
            'cus_no': forms.HiddenInput(),
            'upd_by': forms.HiddenInput(),
            'upd_flag': forms.HiddenInput(),
        }
        error_messages = {
            'cus_no': {
                'required': _("This field is required"),
            },
            'cus_id': {
                'required': _("This field is required"),
                'max_digits': _("รหัสลูกค้า ป้อนค่าได้ระหว่าง 0 - 9999999"),
            },
            'cus_brn': {
                'required': _("This field is required"),
                'max_digits': _("รหัสสาขา ป้อนค่าได้ระหว่าง 0 - 999"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(CustomerCreateForm, self).__init__(*args, **kwargs)
        self.fields['cus_id'].label = "Customer ID"
        self.fields['cus_id'].widget.attrs={'class': 'form-control', 'placeholder': _('Customer Code')}
        self.fields['cus_brn'].label = "Branch Code"
        self.fields['cus_brn'].widget.attrs={'class': 'form-control', 'placeholder': _('Branch Code')}
        self.fields['cus_name_th'].label = "Customer Name (TH)"
        self.fields['cus_name_th'].widget.attrs={'class': 'form-control', 'placeholder': _('Company Name (TH)')}
        self.fields['cus_name_en'].label = "Customer Name (EN)"
        self.fields['cus_name_en'].widget.attrs={'class': 'form-control', 'placeholder': _('Company Name (EN)')}
        self.fields['cus_add1_th'].label = "Address 1 (TH)"
        self.fields['cus_add1_th'].widget.attrs={'class': 'form-control', 'placeholder': _('Address 1 (TH)')}
        self.fields['cus_add1_en'].label = "Address 1 (EN)"
        self.fields['cus_add1_en'].widget.attrs={'class': 'form-control', 'placeholder': _('Address 1 (EN)')}
        self.fields['cus_add2_th'].label = "Address 2 (TH)"
        self.fields['cus_add2_th'].widget.attrs={'class': 'form-control', 'placeholder': _('Address 2 (TH)')}
        self.fields['cus_add2_en'].label = "Address 2 (EN)"
        self.fields['cus_add2_en'].widget.attrs={'class': 'form-control', 'placeholder': _('Address 2 (EN)')}

        self.fields['cus_subdist_th'].label = "Sub-District (TH)"
        self.fields['cus_subdist_th'].widget.attrs={'class': 'form-control', 'placeholder': _('Sub-Distict (TH)')}
        self.fields['cus_subdist_en'].label = "Sub-District (EN)"
        self.fields['cus_subdist_en'].widget.attrs={'class': 'form-control', 'placeholder': _('Sub-Distict (EN)')}

        #fields = ('cus_district', 'cus_city', 'cus_country', 'cus_zip', 'cus_tel', 'cus_fax', 'cus_email', 'cus_taxid', 'cus_active', 'cus_bill', 'cus_main', 'cus_site', 'cus_zone', 'cus_contact', 'site_contact', 'last_contact', 'upd_date', 'upd_by', 'upd_flag')

        #self.initial['cus_brn'] = 0
        self.initial['cus_active'] = 1
        self.initial['upd_flag'] = 'A'
        self.initial['upd_by'] = 'Superadmin'

    def clean(self):
        cleaned_data = self.cleaned_data
        cus_no = str(cleaned_data.get('cus_id')) + str(cleaned_data.get('cus_brn')).zfill(3)
        
        try:
            customer = Customer.objects.get(cus_no=cus_no)
        except Customer.DoesNotExist:
            customer = None

        if customer:
            error_message = u"รหัสลูกค้าและสาขาซ้ำ"
            self._errors['cus_no'] = self.error_class([error_message])
            return cleaned_data
        else:
            return self.cleaned_data

    def clean_cus_name_th(self):
        cleaned_data = self.cleaned_data['cus_name_th']
        if cleaned_data == None:
            error_message = u"กรุณาป้อนชื่อบริษัท (TH)"
            self._errors['cus_name_th'] = self.error_class([error_message])

        return cleaned_data

    def clean_cus_name_en(self):
        cleaned_data = self.cleaned_data['cus_name_en']
        if cleaned_data == None:
            error_message = u"กรุณาป้อนชื่อบริษัท (EN)"
            self._errors['cus_name_en'] = self.error_class([error_message])

        return cleaned_data

    def _remove_leading_zero(value, string):
        if 1 > value > -1:
            string = string.replace('0', '', 1)
        return string


class CustomerSearchForm(forms.ModelForm):
    cus_id = forms.CharField(label=_('Customer ID'), max_length=7, required=False, error_messages={'max_length': _('Too long')}, widget=forms.TextInput(attrs={'autocomplete':'off', 'type':'number'}))
    cus_brn = forms.CharField(label=_('Customer Branch'), max_length=3, required=False, error_messages={'max_length': _('Too long')}, widget=forms.TextInput(attrs={'autocomplete':'off','type':'number'}))
    cus_name = forms.CharField(label=_('Customer Name'), max_length=120, required=False, widget=forms.TextInput(attrs={'autocomplete':'off'}))
    
    class Meta:
        model = Customer
        fields = ['cus_id', 'cus_brn']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')      
        super(CustomerSearchForm, self).__init__(*args, **kwargs)
        self.fields['cus_name'].widget.attrs['placeholder'] = _("Name")
        self.fields['cus_id'].widget.attrs={'class': 'form-control form-control-sm'}
        self.fields['cus_id'].widget.attrs['placeholder'] = _("Code")
        self.fields['cus_brn'].widget.attrs={'class': 'form-control form-control-sm'}
        self.fields['cus_brn'].widget.attrs['placeholder'] = _("Branch")

    def clean_cus_id(self):        
        cus_id = self.data.get('cus_id')
        if len(cus_id) > 7:
            raise forms.ValidationError('Maximum 7 characters required')
        data = self.cleaned_data['cus_id']        
        return data

    def clean_cus_brn(self):        
        cus_brn = self.data.get('cus_brn')
        if len(cus_brn) > 3:
            raise forms.ValidationError('Maximum 3 characters required')
        data = self.cleaned_data['cus_brn']        
        return data


class CusAllTabsForm(forms.ModelForm):
    # Customer Main Office
    cus_main_cus_name_th = forms.CharField(required=True)
    cus_main_cus_name_en = forms.CharField(required=False)    
    cus_main_cus_active = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput())
    cus_main_cus_city_th = forms.CharField(required=False)
    cus_main_cus_country_th = forms.CharField(required=False)    
    cus_main_cus_city_en = forms.CharField(required=False)
    cus_main_cus_district_en = forms.CharField(required=False)
    cus_main_cus_country_en = forms.CharField(required=False)
    cus_main_cus_zone = forms.ModelChoiceField(queryset=None, required=False)
    cus_main_cus_zip = forms.CharField(required=False)
    cus_main_customer_option_op1 = forms.CharField(required=False)    
    cus_main_customer_option_op4 = forms.CharField(required=False)
    cus_main_customer_option_opn1 = forms.DecimalField(required=False)

    # Customer Site
    #cus_site_cus_name_th = forms.CharField(required=True)
    #cus_site_cus_name_en = forms.CharField(required=True)
    
    # District ID
    cus_main_cus_district_id = forms.CharField(required=False)
    # cus_site_cus_district_id = forms.CharField(required=False)
    #cus_site_cus_zone = forms.CharField(required=True)
    #cus_site_cus_zip = forms.CharField(required=True)

    class Meta:
        model = CusMain
        fields = '__all__'        
        exclude = ['cus_no','cus_id','cus_city','cus_country','cus_zip','cus_district','cus_zone','cus_contact','site_contact','dist_en']
    
    def __init__(self, *args, **kwargs):
        if 'cus_no' in kwargs:
            cus_no = kwargs.pop('cus_no')
        else:
            cus_no = None

        super(CusAllTabsForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)        
        instance = getattr(self, 'instance', None)

        # self.fields['cus_main_cus_name_th'].error_messages = {'required': _('Main Office - Customer Name is required'), 'max_value': _('รหัสสัญญาเกิน 7 หลัก')}
        self.fields['cus_main_cus_name_th'].error_messages = {'required': _('Main Office - Customer Name (TH) is required.')}
        # self.fields['cus_main_cus_name_en'].error_messages = {'required': _('Main Office - Customer Name (EN) is required.')}
        self.fields['cus_main_cus_zone'].error_messages = {'required': _('Main Office - Zone is required.')}
        self.fields['cus_main_cus_zip'].error_messages = {'required': _('Main Office - Zip is required.')}

        # self.fields['cus_site_cus_name_th'].error_messages = {'required': _('Site - Customer Name (TH) is required.')}
        # self.fields['cus_site_cus_name_en'].error_messages = {'required': _('Site - Customer Name (EN) is required.')}
        # self.fields['cus_site_cus_zone'].error_messages = {'required': _('Site - Zone is required.')}
        # self.fields['cus_site_cus_zip'].error_messages = {'required': _('Site - Zip is required.')}
        self.fields['cus_main_cus_district_id'].error_messages = {'required': _('Main Office - District is required.')}
        # self.fields['cus_site_cus_district_id'].error_messages = {'required': _('Site - District is required.')}

        self.initial['cus_main_cus_active'] = instance.cus_active

        self.initial['cus_zip'] = instance.cus_zip

        cus_main_cus_city_th = forms.CharField(required=False)
        self.initial['cus_main_cus_city_th'] = instance.cus_city
        self.fields['cus_main_cus_city_th'].widget.attrs['readonly'] = True

        cus_main_cus_country_th = forms.CharField(required=False)
        self.fields['cus_main_cus_country_th'].initial = instance.cus_country        
        self.fields['cus_main_cus_country_th'].widget.attrs['readonly'] = True

        cus_main_cus_city_en = forms.CharField(required=False)
        self.fields['cus_main_cus_city_en'].widget.attrs['readonly'] = True
        if instance.cus_city is not None:
            self.initial['cus_main_cus_city_en'] = instance.cus_city.city_en
        else:
            self.initial['cus_main_cus_city_en'] = ""
        
        cus_main_cus_district_en = forms.CharField(required=False)
        self.fields['cus_main_cus_district_en'].widget.attrs['readonly'] = True
        if instance.cus_district is not None:
            self.initial['cus_main_cus_district_en'] = instance.cus_district.dist_en
        else:
            self.initial['cus_main_cus_district_en'] = ""
        
        cus_main_cus_country_en = forms.CharField(required=False)
        self.fields['cus_main_cus_country_en'].widget.attrs['readonly'] = True
        if instance.cus_district is not None:
            self.fields['cus_main_cus_country_en'].initial = instance.cus_country.country_en
        else:
            self.fields['cus_main_cus_country_en'].initial = ""

        self.fields['cus_main_cus_zone'].queryset=ComZone.objects.all()
        self.initial['cus_main_cus_zone'] = instance.cus_zone_id

        self.fields['cus_main_customer_option_op1'].strip = False
        self.fields['cus_main_customer_option_op4'].strip = False


    def clean_cus_main_cus_district_id(self):
        data = self.data.get('cus_main_cus_district_id')        
        if len(data) > 0:
            return data
        else:
            return None
            #raise ValidationError("Main Office - District is required.")

    def clean_cus_main_customer_option_op1(self):
        data = self.data.get('cus_main_customer_option_op1')
        if len(data) > 10:
            raise ValidationError("Status is too long.")
        else:
            return data

    def clean_cus_main_customer_option_op4(self):
        data = self.data.get('cus_main_customer_option_op4')
        if len(data) > 100:
            raise ValidationError("A/R Code is too long.")
        else:
            return data            

    def clean_cus_active(self):
        data = self.data.get('cus_main_cus_active')
        if data != "1":
            return 0
        return 1

    '''
    def clean_cus_main_cus_name_th(self):
        data = self.data.get('cus_main_cus_name_th')        
        if len(data) > 0:
            return data
        else:
            raise ValidationError("Main Office - Customer Name (TH) is required.")
    '''

    def clean_cus_add1_th(self):
        data = self.data.get('cus_main_cus_add1_th')
        if len(data) > 150:
            raise ValidationError("Address 1 (TH) is too long.")
        else:
            return data

    def clean_cus_add2_th(self):
        data = self.data.get('cus_main_cus_add2_th')
        if len(data) > 70:
            raise ValidationError("Address 2 (TH) is too long.")
        else:
            return data

    def clean_cus_subdist_th(self):
        data = self.data.get('cus_main_cus_subdist_th')
        if len(data) > 50:
            raise ValidationError("Sub-District is too long.")
        else:
            return data

    '''
    def clean_cus_main_cus_name_en(self):
        data = self.data.get('cus_main_cus_name_en')
        if len(data) > 0:
            return data
        else:
            raise ValidationError("Customer Name (EN) is required.")
    '''
    
    def clean_cus_add1_en(self):
        data = self.data.get('cus_main_cus_add1_en')
        if len(data) > 150:
            raise ValidationError("Address 1 (EN) is too long.")
        else:
            return data

    def clean_cus_add2_en(self):
        data = self.data.get('cus_main_cus_add2_en')
        if len(data) > 70:
            raise ValidationError("Address 2 (EN) is too long.")
        else:
            return data

    def clean_cus_subdist_en(self):
        data = self.data.get('cus_main_cus_subdist_en')
        if len(data) > 50:
            raise ValidationError("Sub-District (EN) is too long.")
        else:
            return data

    def clean_cus_main_customer_option_opn1(self):
        data = self.data.get('cus_main_customer_option_opn1')
        if data:
            if data.isnumeric():            
                if float(data) < 0:
                    raise ValidationError("GP Margin is less than zero.")
                else:
                    return 1
        else:
            return 0


class CusMainForm(forms.ModelForm):
    # Customer Main Office
    cus_main_cus_name_th = forms.CharField(required=False)
    cus_main_cus_active = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput())
    cus_main_cus_city_th = forms.CharField(required=False)
    cus_main_cus_country_th = forms.CharField(required=False)    
    cus_main_cus_city_en = forms.CharField(required=False)
    cus_main_cus_district_en = forms.CharField(required=False)
    cus_main_cus_country_en = forms.CharField(required=False)
    cus_main_cus_zone = forms.ModelChoiceField(queryset=None, required=False)
    cus_main_cus_zip = forms.CharField(required=False)
    cus_main_customer_option_op1 = forms.CharField(required=False)
    cus_main_customer_option_op4 = forms.CharField(required=False)

    # amnaj
    contact_title_list = forms.ModelChoiceField(queryset=None, required=False)
    contact_nation_list = forms.ModelChoiceField(queryset=TNation.objects.all().exclude(upd_flag='D').order_by('-nation_id'), required=False)

    cus_main_cus_contact_cus_title_en = forms.CharField(required=False)
    # cus_main_cus_contact_nation_th = forms.CharField(required=False)
    # cus_main_cus_contact_nation_en = forms.CharField(required=False)

    class Meta:
        model = CusMain
        fields = '__all__'        
        exclude = ['cus_no','cus_id','cus_city','cus_country','cus_zip','cus_district','cus_zone','cus_contact','site_contact','dist_en']
    
    def __init__(self, *args, **kwargs):
        if 'cus_no' in kwargs:
            cus_no = kwargs.pop('cus_no')
        else:
            cus_no = None

        super(CusMainForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)        
        instance = getattr(self, 'instance', None)

        self.initial['cus_main_cus_active'] = instance.cus_active
        self.initial['cus_zip'] = instance.cus_zip

        cus_main_cus_city_th = forms.CharField(required=False)                
        self.fields['cus_main_cus_city_th'].widget.attrs['readonly'] = True
        if (instance.cus_city is not None):
            self.initial['cus_main_cus_city_th'] = instance.cus_city.city_th
        else:
            self.initial['cus_main_cus_city_th'] = None

        cus_main_cus_country_th = forms.CharField(required=False)
        self.fields['cus_main_cus_country_th'].initial = instance.cus_country
        self.fields['cus_main_cus_country_th'].widget.attrs['readonly'] = True

        cus_main_cus_city_en = forms.CharField(required=False)
        self.fields['cus_main_cus_city_en'].widget.attrs['readonly'] = True
        if instance.cus_city is not None:
            self.initial['cus_main_cus_city_en'] = instance.cus_city.city_en
        else:
            self.initial['cus_main_cus_city_en'] = None
        
        cus_main_cus_district_en = forms.CharField(required=False)
        self.fields['cus_main_cus_district_en'].widget.attrs['readonly'] = True
        if instance.cus_district is not None:
            self.initial['cus_main_cus_district_en'] = instance.cus_district.dist_en
        else:
            self.initial['cus_main_cus_district_en'] = ""
                
        self.fields['cus_main_cus_country_en'].widget.attrs['readonly'] = True
        if (instance.cus_district is not None):
            self.fields['cus_main_cus_country_en'].initial = instance.cus_country.country_en
        else:
            self.initial['cus_main_cus_country_en'] = ""

        self.fields['cus_main_cus_zone'].queryset=ComZone.objects.all()
        self.initial['cus_main_cus_zone'] = instance.cus_zone_id

        self.fields['cus_main_customer_option_op1'].strip = False
        self.fields['cus_main_customer_option_op4'].strip = False

        self.fields['contact_title_list'].queryset=TTitle.objects.all().exclude(upd_flag='D').order_by('-title_id')

        self.fields['cus_main_cus_contact_cus_title_en'].initial = "Khun"

    def clean_cus_main_customer_option_op1(self):
        data = self.data.get('cus_main_customer_option_op1')
        if len(data) > 10:
            raise ValidationError("Status is too long.")
        else:
            return data

    def clean_cus_main_customer_option_op4(self):
        data = self.data.get('cus_main_customer_option_op4')
        if len(data) > 100:
            raise ValidationError("A/R Code is too long.")
        else:
            return data            

    def clean_cus_active(self):
        data = self.data.get('cus_main_cus_active')
        if data != "1":
            return 0
        return 1

    def clean_cus_add1_th(self):
        data = self.data.get('cus_main_cus_add1_th')
        if len(data) > 150:
            raise ValidationError("Address 1 (TH) is too long.")
        else:
            return data

    def clean_cus_add2_th(self):
        data = self.data.get('cus_main_cus_add2_th')
        if len(data) > 70:
            raise ValidationError("Address 2 (TH) is too long.")
        else:
            return data

    def clean_cus_subdist_th(self):
        data = self.data.get('cus_main_cus_subdist_th')
        if len(data) > 50:
            raise ValidationError("Sub-District is too long.")
        else:
            return data

    def clean_cus_add1_en(self):
        data = self.data.get('cus_main_cus_add1_en')
        if len(data) > 150:
            raise ValidationError("Address 1 (EN) is too long.")
        else:
            return data

    def clean_cus_add2_en(self):
        data = self.data.get('cus_main_cus_add2_en')
        if len(data) > 70:
            raise ValidationError("Address 2 (EN) is too long.")
        else:
            return data

    def clean_cus_subdist_en(self):
        data = self.data.get('cus_main_cus_subdist_en')
        if len(data) > 50:
            raise ValidationError("Sub-District (EN) is too long.")
        else:
            return data

    '''
    def clean_cus_site_cus_name_th(self):
        data = self.data.get('cus_site_cus_name_th')        
        if len(data) > 0:
            return data
        else:
            raise ValidationError("Site Tab - Customer Name (TH) is required.")
    '''


class CusSiteForm(forms.ModelForm):    
    cus_site_cus_name_th = forms.CharField(required=False)
    cus_site_cus_zip = forms.CharField(required=False)
    cus_site_cus_tel = forms.CharField(required=False)
    cus_site_cus_fax = forms.CharField(required=False)
    cus_site_cus_email = forms.CharField(required=False)
    cus_site_cus_zone = forms.ModelChoiceField(queryset=None, required=False)    

    # Contact Information
    cus_site_cus_contact = forms.CharField(required=False)
    sex_choices=[('M','Male'), ('F','Female')]    
    cus_site_cus_contact_con_sex = forms.ChoiceField(choices=sex_choices, widget=forms.RadioSelect(attrs={'class': 'inline'}), required=False)
    cus_site_cus_contact_cus_title = forms.ModelChoiceField(queryset=None, required=False)

    contact_title_list = forms.ModelChoiceField(queryset=TTitle.objects.all().exclude(upd_flag='D').order_by('-title_id'), required=False)
    contact_nation_list = forms.ModelChoiceField(queryset=TNation.objects.all().exclude(upd_flag='D').order_by('-nation_id'), required=False)

    cus_site_site_contact_cus_title_en = forms.CharField(required=False)

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['cus_no','cus_id','cus_brn','cus_city','cus_country','cus_zip','cus_district','cus_zone','cus_contact','site_contact','dist_en']
    
    def __init__(self, *args, **kwargs):        
        super(CusSiteForm, self).__init__(*args, **kwargs)        
        instance = getattr(self, 'instance', None)

        self.initial['cus_zip'] = instance.cus_zip

        self.fields['cus_site_cus_zone'].queryset=ComZone.objects.all()
        self.initial['cus_site_cus_zone'] = instance.cus_zone_id
        
        self.initial['cus_site_cus_contact'] = instance.cus_contact

        self.fields['cus_site_site_contact_cus_title_en'].initial = "Khun"

    def clean_cus_active(self):
        data = self.data.get('cus_site_cus_active')
        if data != "1":
            return 0
        return 1     

    '''
    def clean_cus_site_cus_name_th(self):
        data = self.data.get('cus_site_cus_name_th')        
        if len(data) > 0:
            return data
        else:
            raise ValidationError("Customer Name (TH) is required.")
    '''


    def clean_cus_add1_th(self):
        data = self.data.get('cus_site_cus_add1_th')
        if len(data) > 150:
            raise ValidationError("Address 1 (TH) is too long.")
        else:
            return data

    def clean_cus_add2_th(self):
        data = self.data.get('cus_site_cus_add2_th')
        if len(data) > 70:
            raise ValidationError("Address 2 (TH) is too long.")
        else:
            return data

    def clean_cus_subdist_th(self):
        data = self.data.get('cus_site_cus_subdist_th')
        if len(data) > 50:
            raise ValidationError("Sub-District is too long.")
        else:
            return data

    '''
    def clean_cus_name_en(self):
        data = self.data.get('cus_site_cus_name_en')
        if len(data) > 0:
            return data
        else:
            raise ValidationError("Customer Name (EN) is required.")
    '''

    def clean_cus_add1_en(self):
        data = self.data.get('cus_site_cus_add1_en')
        if len(data) > 150:
            raise ValidationError("Address 1 (EN) is too long.")
        else:
            return data

    def clean_cus_add2_en(self):
        data = self.data.get('cus_site_cus_add2_en')
        if len(data) > 70:
            raise ValidationError("Address 2 (EN) is too long.")
        else:
            return data

    def clean_cus_subdist_en(self):
        data = self.data.get('cus_site_cus_subdist_en')
        if len(data) > 50:
            raise ValidationError("Sub-District (EN) is too long.")
        else:
            return data

    '''
    def clean_cus_site_cus_zip(self):
        data = self.data.get('cus_site_cus_zip')
        if len(data) != 5:
            raise ValidationError("Zip is not correct.")
        else:
            return data

        if data.isnumeric():
            return data
        else:
            raise ValidationError("Zip is not correct.")
    '''

    def clean_cus_site_cus_tel(self):
        data = self.data.get('cus_site_cus_tel')
        return data

    def clean_cus_site_cus_fax(self):
        data = self.data.get('cus_site_cus_fax')
        return data

    def clean_cus_site_cus_email(self):
        data = self.data.get('cus_site_cus_email')
        return data

    def clean_cus_site_cus_zone(self):
        data = self.data.get('cus_site_cus_zone')
        return data

    def clean_cus_site_cus_contact(self):
        data = self.data.get('cus_site_cus_contact')
        return data

    def clean_cus_site_cus_contact_con_sex(self):
        data = self.data.get('cus_site_cus_contact_con_sex')
        data = "F"
        return data        


class CusBillForm(forms.ModelForm):    
    cus_bill_cus_name_th = forms.CharField(required=False)
    cus_bill_cus_zip = forms.CharField(required=False)
    cus_bill_cus_tel = forms.CharField(required=False)
    cus_bill_cus_fax = forms.CharField(required=False)
    cus_bill_cus_email = forms.CharField(required=False)
    cus_bill_cus_zone = forms.ModelChoiceField(queryset=None, required=False)    

    contact_title_list = forms.ModelChoiceField(queryset=TTitle.objects.all().exclude(upd_flag='D').order_by('-title_id'), required=False)
    contact_nation_list = forms.ModelChoiceField(queryset=TNation.objects.all().exclude(upd_flag='D').order_by('-nation_id'), required=False)
    
    cus_bill_cus_contact_cus_title_en = forms.CharField(required=False)

    class Meta:
        model = CusBill
        fields = '__all__'
        exclude = ['cus_no','cus_id','cus_brn','cus_city','cus_country','cus_zip','cus_district','cus_zone','cus_contact','site_contact','dist_en']
    
    def __init__(self, *args, **kwargs):        
        super(CusBillForm, self).__init__(*args, **kwargs)     
        instance = getattr(self, 'instance', None)

        self.initial['cus_zip'] = instance.cus_zip

        self.fields['cus_bill_cus_zone'].queryset=ComZone.objects.all()
        self.initial['cus_bill_cus_zone'] = instance.cus_zone_id
        self.initial['cus_bill_cus_contact'] = instance.cus_contact

        self.fields['cus_bill_cus_contact_cus_title_en'].initial = "Khun"

    def clean_cus_active(self):
        data = self.data.get('cus_bill_cus_active')
        if data != "1":
            return 0
        return 1 


class ContactSearchForm(forms.Form):
    cus_id = forms.CharField(max_length=4, required=False, error_messages={'max_length': _('This Customer ID is too long.')}, widget=forms.TextInput(attrs={'autocomplete':'off', 'type':'number'}))
    # con_id = forms.CharField(max_length=4, required=False, error_messages={'max_length': _('This Contact ID is too long.')}, widget=forms.TextInput(attrs={'autocomplete':'off','type':'number'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')      
        super(ContactSearchForm, self).__init__(*args, **kwargs)
        self.fields['cus_id'].widget.attrs={'class': 'form-control', 'placeholder': _('Enter Customer ID')}
        # self.fields['con_id'].widget.attrs={'class': 'form-control', 'placeholder': _('Contact ID')}
        

    def clean_cus_id(self):        
        cus_id = self.data.get('cus_id')
        if len(cus_id) > 4:
            raise forms.ValidationError('Maximum 4 characters required')
        data = self.cleaned_data['cus_id']        
        return data

    '''
    def clean_con_id(self):
        con_id = self.data.get('con_id')
        if len(con_id) > 4:
            raise forms.ValidationError('Maximum 4 characters required')
        data = self.cleaned_data['con_id']        
        return data
    '''