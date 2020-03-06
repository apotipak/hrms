from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _


class CustomerCreateForm(forms.ModelForm):

    cus_no = forms.DecimalField(max_digits=10)

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
                'max_digits': _("ตัวเลขรหัสลูกค้าป้อนค่าได้ระหว่าง 1 - 9999999"),
            },
            'cus_brn': {
                'required': _("This field is required"),
                'max_digits': _("ตัวเลขรหัสสาขาป้อนค่าได้ระหว่าง 1 - 999"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(CustomerCreateForm, self).__init__(*args, **kwargs)
        self.fields['cus_id'].label = "Customer ID"
        self.fields['cus_id'].widget.attrs={'class': 'form-control', 'placeholder': _('Customer Code')}
        self.fields['cus_brn'].label = "Branch Code"
        self.fields['cus_brn'].widget.attrs={'class': 'form-control', 'placeholder': _('Branch Code')}
        self.fields['cus_name_th'].label = "Customer Name (TH)"
        
        self.initial['cus_brn'] = 0
        self.initial['cus_active'] = 1
        self.initial['upd_flag'] = 'A'
        self.initial['upd_by'] = 'Superadmin'

    def clean(self):
        cleaned_data = self.cleaned_data
        #cus_no = cleaned_data.get('cus_id') + cleaned_data.get('cus_brn')
        cus_no = 2094004
        matching_cus_no = Customer.objects.filter(cus_no=cus_no)

        try:
            customer = Customer.objects.get(cus_no=cus_no)
        except Customer.DoesNotExist:
            customer = None

        if customer:
            #msg = u"This value is exist."
            msg = "123"
            self._errors['cus_no'] = self.error_class([msg])
            return cleaned_data
        else:
            return self.cleaned_data


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
