from django import forms
from .models import TAprove

class CompanyApprovePriorityForm(forms.ModelForm):
    class Meta:
        model = TAprove
        fields = ('apr_id', 'apr_name_th', 'apr_pos_th', 'apr_piority', )