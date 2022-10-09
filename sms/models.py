from django.db import models

from customer.models import *


class tblsmsappbusiness(models.Model):
	branch=models.ForeignKey(tblBRANCH)	
	App= models.CharField(max_length=40)
	status=models.CharField(max_length=40)
	balance=models.CharField(max_length=40)
	sender_ID=models.CharField(max_length=40)
	unit_price=models.CharField(max_length=40,default=3.50)


	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.App,self.balance) 


class tblcustomersms(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	customer=models.ForeignKey(tblCUSTOMER)
	App= models.CharField(max_length=40)
	status=models.BooleanField()
	balance=models.CharField(max_length=40)
	S = models.CharField(max_length=6)

	def __unicode__(self):
		return '%s %s %s'%(self.customer,self.App,self.balance)


class tblcustomersmsperiodicity_transaction(models.Model):
	schedule=models.ForeignKey(tblcustomersms)
	alert_type=models.CharField(max_length=40)

	def __unicode__(self):
		return '%s %s'%(self.schedule,self.alert_type)


class tblcustomersmsperiodicity_weekly(models.Model):

	schedule=models.ForeignKey(tblcustomersms)
	day_of_week =models.CharField(max_length=40)

	def __unicode__(self):
		return '%s %s'%(self.schedule,self.day_of_week)


class tblcustomersmsperiodicity_monthly(models.Model):
	schedule=models.ForeignKey(tblcustomersms)
	date_of_delivery=models.DateField(default='2021-05-08')
	nick =models.CharField(max_length=40)


	def __unicode__(self):
		return '%s %s'%(self.schedule,self.date_of_delivery)


class tblcustomersmspurchases(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	customer=models.ForeignKey(tblCUSTOMER)
	recdate = models.DateField()
	volume = models.IntegerField()
	merchant = models.IntegerField()
	cost = models.IntegerField()
	code=models.CharField(max_length=40)
	status = models.CharField(max_length=6)

	def __unicode__(self):
		return '%s %s %s'%(self.customer,self.recdate,self.code)




