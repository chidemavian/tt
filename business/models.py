from django.db import models

from partner.models import *
# from staff.models import *


class tblCOMPANY(models.Model):
	partner = models.ForeignKey(tblPARTNER)
	name =models.CharField(max_length=500)
	code = models.CharField(max_length=15)
	web = models.CharField(max_length=200)
	ig=models.CharField(max_length=50)
	twitter = models.CharField(max_length=40)
	fb= models.CharField(max_length=50)
	youtube=models.CharField(max_length=50)
	engine=models.CharField(max_length=50)
	size=models.IntegerField()
	ux= models.BooleanField()
	status= models.BooleanField()
	logo = models.ImageField(upload_to='company_logo', null=True,
		blank=True,default='company_logo/thrift.png')
	

	def __unicode__(self):
		return '%s %s %s'%(self.name,self.web,self.size)



class tblBRANCH(models.Model):
	company=models.ForeignKey(tblCOMPANY)
	code=models.IntegerField()
	Address = models.CharField(max_length=300)
	phone= models.IntegerField()
	types=models.CharField(max_length=50)
	status = models.BooleanField(max_length=300)
	currency_code = models.CharField(max_length=300)
	currency_description= models.CharField(max_length=300)

	def __unicode__(self):
		return '%s %s %s'%(self.company,self.Address,self.types)

class tblmanager(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	name=models.CharField(max_length=200)
	phone=models.IntegerField()
	photo=models.ImageField(upload_to='staff-pix', null=True,
		blank=True,default='staff-pix/thrift.png')
	code=models.IntegerField()

	def __unicode__(self):
		return '%s %s %s'%(self.name,self.code,self.phone)


class tblaccountDetails(models.Model):
	company=models.ForeignKey(tblCOMPANY) #use tblbranch instaed
	account=models.IntegerField()
	bank = models.CharField(max_length=10)
	code= models.IntegerField()

	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.date,self.customer)


		
class tblapp(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	partner = models.ForeignKey(tblPARTNER)

	thrift1a=models.BooleanField() #daily contrinution
	
	thrift1b=models.BooleanField() #investment banking
	loan1b=models.BooleanField()

	thrift3a=models.BooleanField() #cooperatives


	thrift3b=models.BooleanField() #corporat C


	def __unicode__(self):
		return '%s %s %s'%(self.partner,self.thrift1a,self.branch)



class tblvas(models.Model):
	company=models.ForeignKey(tblCOMPANY) #use tblbranch instaed
	partner = models.ForeignKey(tblPARTNER)
	ux= models.BooleanField()
	otp= models.BooleanField()
	sms= models.BooleanField()
	email= models.BooleanField()
	

	def __unicode__(self):
		return '%s %s %s'%(self.email,self.otp,self.partner)
