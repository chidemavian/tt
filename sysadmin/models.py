from django.db import models


from staff.models import *


class Userprofile(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	staffrec=models.ForeignKey(tblSTAFF)
	email=models.EmailField()
	password=models.CharField(max_length=20)
	code=models.IntegerField()
	ceo=models.BooleanField()

	
	thrift1a=models.BooleanField() #the App itself
	thrift_officer = models.BooleanField() #merchant
	admin=models.BooleanField()    #admin
	cashier = models.BooleanField() #cashier  


	thrift1b=models.BooleanField() #investment banking
	thrift1b_officer = models.BooleanField()
	thrift1b_admin=models.BooleanField()
	thrift1b_cashier = models.BooleanField()


	loan1b=models.BooleanField() #investment banking loan
	loan1b_admin=models.BooleanField()
	loan1b_officer = models.BooleanField()	


	thrift3a=models.BooleanField() #Corporate C
	thrift3a_officer = models.BooleanField()
	thrift3a_admin=models.BooleanField()
	thrift3a_cashier = models.BooleanField()

	loan3a = models.BooleanField()
	loan3a_admin=models.BooleanField()
	loan3a_officer = models.BooleanField()


	thrift3b=models.BooleanField() #Cooprative
	thrift3b_officer = models.BooleanField()
	thrift3b_admin=models.BooleanField()
	thrift3b_cashier = models.BooleanField()

	loan3b = models.BooleanField()
	loan3b_admin=models.BooleanField()
	loan3b_officer = models.BooleanField()



	status=models.BooleanField()
	partner=models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.email,self.cashier,self.admin)



class tblthriftpackages(models.Model):
	package=models.CharField(max_length= 50)
	staff_count= models.IntegerField()
	customer_count=models.IntegerField()
	status =models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.package,self.staff_count,self.customer_count)

class tblsubscription(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	package=models.ForeignKey(tblthriftpackages)
	duration=models.IntegerField()
	start=models.DateField()
	end=models.DateField()
	status =models.BooleanField()
	receipt=models.CharField(max_length=320)

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.package,self.duration)




