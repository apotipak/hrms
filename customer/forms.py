from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _


class CustomerCreateForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('cus_id', 'cus_brn', 'cus_name_th', 'cus_name_en')
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

        
        #self.initial['cus_brn'] = 0
        self.initial['cus_active'] = 1
        self.initial['upd_flag'] = 'A'
        self.initial['upd_by'] = 'Superadmin'

    def clean(self):
        cleaned_data = self.cleaned_data
        cus_no = str(cleaned_data.get('cus_id')) + str(cleaned_data.get('cus_brn'))
        
        #matching_cus_no = Customer.objects.filter(cus_no=float(cus_no))

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
