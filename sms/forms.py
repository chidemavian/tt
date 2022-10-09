from django import forms
# from staff.models import *




month = (('-','----'),(1,'January'),(2,'February'),(3,'March'),(4, 'April'),
	(5,'May'),(6,'June'),(7,'July'),(8, 'August'),(9,'September'),
	(10,'October'),(11, 'November'),(12,'December'))




apps = ( 
	('-----','-----'),

	('Daily Contribution', 'Daily Contribution'),
	('Loans','Loans'),
	)

week = (('-','----'),(1,'Sunday'),(2,'Monday'),(3,'Tuesday'),(4, 'Wednesday'),
	(5,'Thursday'),(6,'Friday'),(7,'Saturday'))





class smsform(forms.Form):
	app = forms.ChoiceField(label = "App Category",choices = apps )


class smsweeklyform(forms.Form):
	dow = forms.ChoiceField(label = "Day Of Week",choices = week )











