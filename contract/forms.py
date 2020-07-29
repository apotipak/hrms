from django import forms
from .models import CusContract
from customer.models import Customer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ContractForm(forms.ModelForm):
    '''
    cus_id = forms.DecimalField(label='Customer ID', required=True, max_value=9999999, initial=2600)
    cus_brn = forms.DecimalField(label='Branch', required=True, max_value=999, min_value=0, initial=0)
    cus_vol = forms.DecimalField(label='Volume', required=True, max_value=999, min_value=0, initial=1)
    '''

    cus_id = forms.DecimalField(label='Customer ID', required=False, max_value=9999999)
    cus_brn = forms.DecimalField(label='Branch', required=False, max_value=999, min_value=0)
    cus_vol = forms.DecimalField(label='Volume', required=False, max_value=999, min_value=0)

    class Meta:
        model = CusContract
        fields = ['cus_brn', 'cus_vol', 'cus_id'] 

    def __init__(self, *args, **kwargs):    	
        super(ContractForm, self).__init__(*args, **kwargs)

        self.fields['cus_id'].widget.attrs = {'class': 'form-control form-control-sm', 'placeholder': _('Customer ID')}        
        self.fields['cus_id'].error_messages = {'required': _('กรุณาป้อนข้อมูล'), 'max_value': _('รหัสสัญญาเกิน 7 หลัก')}

        self.fields['cus_brn'].widget.attrs={'class': 'form-control form-control-sm', 'placeholder': _('Branch')}
        self.fields['cus_brn'].error_messages = {'required': _('กรุณาป้อนข้อมูล'), 'max_value': _('รหัสสาขาเกิน 3 หลัก'), 'min_value': _('ป้อนข้อมูลน้อยกว่า 0')}

        self.fields['cus_vol'].widget.attrs={'class': 'form-control form-control-sm', 'placeholder': _('Volume')}
        self.fields['cus_vol'].error_messages = {'required': _('กรุณาป้อนข้อมูล'), 'max_value': _('รหัสลำดับสัญญาเกิน 3 หลัก'), 'min_value': _('ป้อนข้อมูลน้อยกว่า 0')}

    def clean_cus_id(self):
        if self.instance: 
            return self.instance.cus_id
        else: 
            return self.fields['cus_id']
        
    def clean_cus_brn(self):
        if self.instance: 
            return self.instance.cus_brn
        else: 
            return self.fields['cus_brn']

    def clean_cus_vol(self):
        if self.instance: 
            return self.instance.cus_vol
        else: 
            return self.fields['cus_vol']


    

class ContractUpdateForm(forms.ModelForm):    
    cnt_active = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput())
    
    cus_district_th_text = forms.CharField(required=False)
    cus_district_en_text = forms.CharField(required=False)
    cus_city_th_text = forms.CharField(required=False)
    cus_city_en_text = forms.CharField(required=False)
    cus_country_th_text = forms.CharField(required=False)
    cus_country_en_text = forms.CharField(required=False)

    class Meta:
        model = CusContract        
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContractUpdateForm, self).__init__(*args, **kwargs)        
        instance = getattr(self, 'instance', None)

        '''
        cus_district = forms.ModelChoiceField(queryset=None, required=False)
        cus_zone = forms.ModelChoiceField(queryset=None, required=False)
        cus_bill = forms.ModelChoiceField(queryset=None, required=False)

        cus_district_th_text = forms.CharField(required=False)
        self.initial['cus_district_th_text'] = instance.cus_district.dist_th
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

        return data
        '''