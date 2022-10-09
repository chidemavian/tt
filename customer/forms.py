from django import forms

from staff.models import *



class staffform(forms.Form):
	email = forms.EmailField(label = 'Staff Email')



class createwalletform(forms.Form):
    surname = forms.CharField(label='Surname',max_length= 190)
    firstname = forms.CharField(label='Firstname',max_length= 190)
    othername = forms.CharField(label='Otherame',max_length= 190, required=False)
    phone = forms.IntegerField(label='Phone' ,required=False)
    address = forms.CharField(label='Address',max_length= 190)
    email = forms.EmailField(label='E-mail' ,required=False)
    photo = forms.ImageField(label='Passport' ,required=False)

    def __init__(self, *args, **kwargs):
        super(createwalletform, self).__init__(*args)
        self.fields['surname'].widget.attrs['class'] = 'loginTxtbox'


class viewwalletform(forms.Form):
	wallet = forms.IntegerField(label = 'Wallet Address')

	
