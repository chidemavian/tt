from django import forms
from staff.models import *
from IIIb.models import *



monthy = (('---','----'),('January','January'),('February','February'),('March','March'),('April', 'April'),
	('May','May'),('June','June'),('July','July'),('August', 'August'),('September','September'),
	('October','October'),('November', 'November'),('December','December'))


month = (('-','----'),(1,'January'),(2,'February'),(3,'March'),(4, 'April'),
	(5,'May'),(6,'June'),(7,'July'),(8, 'August'),(9,'September'),
	(10,'October'),(11, 'November'),(12,'December'))



loan_type = ( 

	('---', '--------'),
	('Standard','Standard'), 
	('Custom','Custom'), 

	)


class EmailForm(forms.Form):
    recipient = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    

class individualform(forms.Form):
	email = forms.IntegerField(label = 'E-mail Address')
	Type = forms.ChoiceField(label = 'Loan Type', choices=loan_type)



class savingsform(forms.Form):
	email = forms.EmailField(label = 'Staff E-mail')


class amountform(forms.Form):
	amount = forms.IntegerField(label = 'Amount')



class approveform(forms.Form):
	month = forms.ChoiceField(label = 'Month' , choices=month)


class loanreqform(forms.Form):
	amount = forms.IntegerField(label = 'Amount')
	loans = forms.ChoiceField(label = "Loan Parkage",choices = [(c.description, c.description) for c in tblstandardloanIIIB.objects.filter(status='ACTIVE')])


class mysavingsform(forms.Form):
	month = forms.ChoiceField(label = 'Month' , choices=monthy)



class savelogform(forms.Form):
	month = forms.ChoiceField(label = 'Month' , choices=monthy)
	savetypes = forms.ChoiceField(label = 'Month' , choices=[(a.description, a.description) for a in tblstandardsavingIIIB.objects.filter()])


class setsave(forms.Form):
	month_from = forms.ChoiceField(choices=monthy)
	month_to = forms.ChoiceField(choices=monthy)

class saveapplyform(forms.Form):
	savepack = forms.ChoiceField(label = 'Month' , choices=[(a.description, a.description) for a in tblstandardsavingIIIB.objects.filter(status='ACTIVE')])

