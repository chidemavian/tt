
from django import forms
from sysadmin.models import tblthriftpackages
class companyform(forms.Form):
	company = forms.IntegerField(label = 'Business Code')

class branchform(forms.Form):
	branch = forms.IntegerField(label = 'Branch Code')




class packageform(forms.Form):
	package = forms.ChoiceField(label='Package',choices = [(c.package, c.package) for c in tblthriftpackages.objects.all()])




