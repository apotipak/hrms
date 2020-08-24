from django import forms
from .models import Customer, CusMain
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _
from system.models import CusContact, ComZone, TTitle
from django.core.exceptions import ValidationError


class CustomerCreateForm(forms.ModelForm):

    class Meta:
        model = Customer
        #fields = '__all__'
        #fields = ('cus_id', 'cus_brn', 'cus_name_th', 'cus_name_en', 'cus_add1_th', 'cus_add1_en', 'cus_add2_th', 'cus_add2_en')
        fields = ('cus_id', 'cus_brn', 'cus_name_th', 'cus_name_en', 'cus_add1_th', 'cus_add1_en', 'cus_add2_th', 'cus_add2_en', 'cus_subdist_en', 'cus_subdist_th')
        #, 'cus_district', 'cus_city', 'cus_country', 'cus_zip', 'cus_tel', 'cus_fax', 'cus_email', 'cus_taxid', 'cus_active', 'cus_bill', 'cus_main', 'cus_site', 'cus_zone', 'cus_contact', 'site_contact', 'last_contact', 'upd_date', 'upd_by', 'upd_flag')


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


class CustomerUpdateForm1(forms.ModelForm):    
    # contract status    
    cus_active = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput())
    cus_site_active = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput())
    cus_billing_active = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput())

    cus_district_th_text = forms.CharField(required=False)
    cus_district_en_text = forms.CharField(required=False)
    cus_city_th_text = forms.CharField(required=False)
    cus_city_en_text = forms.CharField(required=False)
    cus_country_th_text = forms.CharField(required=False)
    cus_country_en_text = forms.CharField(required=False)

    class Meta:
        model = Customer        
        fields = '__all__'
        # fields = ['cus_name_th', 'cus_add1_th', 'cus_add2_th', 'cus_name_en', 'cus_subdist_th', 'cus_sht_en', 'cus_name_en', 'cus_add1_en', 'cus_add2_en', 'cus_subdist_en', 'cus_district', 'cus_city', 'cus_country', 'cus_zip', 'cus_tel', 'cus_fax', 'cus_email', 'cus_taxid', 'cus_active', 'cus_bill', 'cus_main', 'cus_site', 'cus_zone', 'cus_contact', 'site_contact', 'last_contact', 'upd_date', 'upd_by', 'upd_flag']        
        exclude = ['cus_no','cus_id','cus_brn','cus_city','cus_country','cus_zip','cus_district','cus_contact','site_contact']

    def __init__(self, *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)        
        instance = getattr(self, 'instance', None)
        # print("country = " + str(instance.cus_country.pk))

        # contactobj = CusContact.objects.exclude(upd_flag='D')
        # customer_list = Customer.objects.filter(cus_id__in=[2094]).order_by('-upd_date', 'cus_id', '-cus_active')
        # cus_contact = forms.ModelChoiceField(label=_('Select contact person'), queryset=contactobj, required=False)

        cus_district = forms.ModelChoiceField(queryset=None, required=False)
        cus_main_district = forms.ModelChoiceField(queryset=None, required=False)

        #cus_city = forms.ModelChoiceField(queryset=None, required=False)
        #self.fields['cus_city'].widget.attrs['readonly'] = True

        #cus_country = forms.ModelChoiceField(queryset=None, required=False)
        #self.fields['cus_country'].widget.attrs['readonly'] = True

        cus_zone = forms.ModelChoiceField(queryset=None, required=False)
        cus_bill = forms.ModelChoiceField(queryset=None, required=False)

        cus_district_th_text = forms.CharField(required=False)
        if instance.cus_district.dist_th:
            self.initial['cus_district_th_text'] = instance.cus_district.dist_th
        else:
            self.initial['cus_district_th_text'] = ""
        self.fields['cus_district_th_text'].widget.attrs['readonly'] = True

        cus_district_en_text = forms.CharField(required=False)
        self.initial['cus_district_en_text'] = instance.cus_district.dist_en
        self.fields['cus_district_en_text'].widget.attrs['readonly'] = True

        cus_city_th_text = forms.CharField(required=False)
        self.initial['cus_city_th_text'] = instance.cus_city.city_th
        self.fields['cus_city_th_text'].widget.attrs['readonly'] = True

        cus_city_en_text = forms.CharField(required=False)
        self.initial['cus_city_en_text'] = instance.cus_city.city_en
        self.fields['cus_city_en_text'].widget.attrs['readonly'] = True

        cus_country_th_text = forms.CharField(required=False)
        self.initial['cus_country_th_text'] = instance.cus_country.country_th
        self.fields['cus_country_th_text'].widget.attrs['readonly'] = True

        cus_country_en_text = forms.CharField(required=False)
        self.initial['cus_country_en_text'] = instance.cus_country.country_en
        self.fields['cus_country_en_text'].widget.attrs['readonly'] = True

    def clean_cus_zip(self):
        cus_zip = self.data.get('cus_zip')
        if cus_zip is not None:
            if len(cus_zip) <= 0:
                raise forms.ValidationError(_('Invalid post code.'))        
        data = self.data['cus_zip']
        return data

    def clean_cus_add1_th(self):
        data = self.data.get('cus_add1_th')
        if data is None:
            data = None
        return data

    def clean_cus_add2_th(self):
        data = self.data.get('cus_add2_th')
        if data is None:
            data = None
        return data

    def clean_cus_add1_en(self):
        data = self.data.get('cus_add1_en')
        if data is None:
            data = None
        return data

    def clean_cus_add2_en(self):
        data = self.data.get('cus_add2_en')
        if data is None:
            data = None
        return data

    def clean_cus_subdist_th(self):
        data = self.data.get('cus_subdist_th')
        if data is None:
            data = None
        return data

    def clean_cus_subdist_en(self):
        data = self.data.get('cus_subdist_en')
        if data is None:
            data = None
        return data

    def clean_cus_email(self):
        data = self.data.get('cus_email')
        if data is None:
            data = None
        return data

    def clean_cus_active(self):
        data = self.data.get('cus_active')
        if data=="on":
            data=1
        else:
            data=0
        return data


class CusMainForm(forms.ModelForm):            
    cus_main_cus_active = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput())
    cus_main_cus_city_th = forms.CharField(required=False)
    cus_main_cus_country_th = forms.CharField(required=False)    
    cus_main_cus_city_en = forms.CharField(required=False)
    cus_main_cus_district_en = forms.CharField(required=False)
    cus_main_cus_country_en = forms.CharField(required=False)

    class Meta:
        model = CusMain
        fields = '__all__'        
        exclude = ['cus_id','cus_city','cus_country','cus_zip','cus_district','cus_zone','cus_contact','site_contact','dist_en']
    
    def __init__(self, *args, **kwargs):
        super(CusMainForm, self).__init__(*args, **kwargs)        
        instance = getattr(self, 'instance', None)        
                
        self.initial['cus_main_cus_active'] = instance.cus_active

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

    def clean_cus_active(self):
        data = self.data.get('cus_main_cus_active')
        if data != "1":
            return 0
        return 1     

    def clean_cus_name_th(self):
        data = self.data.get('cus_main_cus_name_th')        
        if len(data) > 0:
            return data
        else:
            raise ValidationError("Customer Name (TH) is required.")

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

    def clean_cus_name_en(self):
        data = self.data.get('cus_main_cus_name_en')
        if len(data) > 0:
            return data
        else:
            raise ValidationError("Customer Name (EN) is required.")

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


class CusSiteForm(forms.ModelForm):    
    cus_site_cus_name_th = forms.CharField(required=False)
    cus_site_cus_zip = forms.CharField(required=False)
    cus_site_cus_tel = forms.CharField(required=False)
    cus_site_cus_fax = forms.CharField(required=False)
    cus_site_cus_email = forms.CharField(required=False)
    cus_site_cus_zone = forms.ModelChoiceField(queryset=None, required=True)    

    # Contact Information
    cus_site_cus_contact = forms.CharField(required=False)
    sex_choices=[('M','Male'), ('F','Female')]    
    cus_site_cus_contact_con_sex = forms.ChoiceField(choices=sex_choices, widget=forms.RadioSelect(attrs={'class': 'inline'}), required=False)
    cus_site_cus_contact_cus_title = forms.ModelChoiceField(queryset=None, required=False)


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
        print("cus_contact = " + str(instance.cus_contact_id))

        # sex_object = CusContact.objects.filter(con_id=instance.cus_contact_id).get()
        sex_object = CusContact.objects.filter(con_id=0).get()

        print("sex = " + str(sex_object.con_sex))
        # self.fields['cus_site_cus_contact_con_sex'].widget.attrs={'class': 'radio-inline'}
        self.initial['cus_site_cus_contact_con_sex'] = sex_object.con_sex

    def clean_cus_active(self):
        data = self.data.get('cus_site_cus_active')
        if data != "1":
            return 0
        return 1     

    def clean_cus_site_cus_name_th(self):
        data = self.data.get('cus_site_cus_name_th')        
        if len(data) > 0:
            return data
        else:
            raise ValidationError("Customer Name (TH) is required.")

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

    def clean_cus_name_en(self):
        data = self.data.get('cus_site_cus_name_en')
        if len(data) > 0:
            return data
        else:
            raise ValidationError("Customer Name (EN) is required.")

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
