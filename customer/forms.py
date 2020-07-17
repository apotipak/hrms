from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _


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

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cus_id', 'cus_name_th')
        widgets = {
            'cus_no': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['cus_id'].widget.attrs['readonly'] = True
        self.fields['cus_id'].label = "Customer ID"
        self.fields['cus_name_th'].label = "Customer Name (TH)"
        
    def clean_cus_no(self):
        if self.instance: 
            return self.instance.cus_no
        else: 
            return self.fields['cus_no']


class CustomerSearchForm(forms.ModelForm):
    cus_id = forms.CharField(label=_('Customer ID'), max_length=7, required=False, error_messages={'max_length': _('Customer ID is too long.')}, widget=forms.TextInput(attrs={'autocomplete':'off'}))
    cus_brn = forms.CharField(label=_('Customer Branch'), max_length=3, required=False, widget=forms.TextInput(attrs={'autocomplete':'off'}))
    
    class Meta:
        model = Customer
        fields = ['cus_id', 'cus_brn']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')      
        super(CustomerSearchForm, self).__init__(*args, **kwargs)
        self.fields['cus_id'].widget.attrs={'class': 'form-control form-control-sm'}
        self.fields['cus_id'].widget.attrs['placeholder'] = _("ID")
        self.fields['cus_brn'].widget.attrs={'class': 'form-control form-control-sm'}
        self.fields['cus_brn'].widget.attrs['placeholder'] = _("Branch")

    '''
    def clean_cus_id(self):
        data = self.cleaned_data['cus_id']        
        if len(data) > 7: 
            self._errors['cus_id'] = self.ValidationError('Minimum 5 characters required')

        return self.cleaned_data    
    '''

    def clean_cus_id(self):        
        cus_id = self.data.get('cus_id')
        if len(cus_id) > 7:
            raise forms.ValidationError('Maximum 7 characters required')

        data = self.cleaned_data['cus_id']        
        return data