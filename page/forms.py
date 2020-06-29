from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from django.utils.translation import ugettext_lazy as _



class LanguageForm(ModelForm):
	language_options = (('en','English US'),('th','Thai'))
	language_code = forms.CharField(label=_('Set Display Language'), max_length=2, widget=forms.Select(choices=language_options), initial=0)	

	class Meta:
		model = UserProfile
		fields = ['language']

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(LanguageForm, self).__init__(*args, **kwargs)
		self.fields['language_code'].widget.attrs={'class': 'form-control'}

		if UserProfile.objects.filter(username=self.user.username).exists():
			default_language = UserProfile.objects.filter(username=self.user.username).values_list('language', flat=True).get()
			print("default lang = " + default_language)
		else:
			default_language = 'th'

		self.initial['language_code'] = default_language

	def clean(self):
		cleaned_data = super(LanguageForm, self).clean()
		language = self.cleaned_data.get('language_code')
		return cleaned_data
