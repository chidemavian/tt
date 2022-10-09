from django.db import models



from customer.models import *


class tblmerchantBank(models.Model):
	branch=models.ForeignKey(tblBRANCH)	
	merchant=models.ForeignKey(tblMERCHANT)

	customer=models.ForeignKey(tblCUSTOMER)
	recdate=models.DateField()

	weekno=models.IntegerField() #of recdate
	amount = models.IntegerField()
	code=models.IntegerField()

	rem_date=models.DateField()
	remitted_by=models.CharField(max_length=50)
	status= models.CharField(max_length=30)
	approved_by=models.CharField(max_length=50)

	account_type=models.CharField(max_length=20,default='Main account')
	thrift=models.IntegerField()
	wallet_type=models.CharField(max_length=30,default='Main')
	
	# remit_time=models.TimeField()
	# approve_time=models.TimeField()

	def __unicode__(self):
		return '%s %s'%(self.recdate,self.amount)




class tblMerchantTrans(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	customer=models.ForeignKey(tblCUSTOMER)
	merchant=models.ForeignKey(tblMERCHANT)
	recdate=models.DateField()
	weekno=models.IntegerField()
	amount=models.IntegerField()
	wallet_type=models.CharField(max_length=30)
	remitted=models.CharField(max_length=30)
	approved=models.CharField(max_length=30)
	code=models.CharField(max_length=30)
	account_type=models.CharField(max_length=20,default='Main account')
	# time_in=models.TimeField()


	def __unicode__(self):
		return '%s %s %s'%(self.recdate,self.amount,self.code)



class tblpayoutrecord(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	customer=models.ForeignKey(tblCUSTOMER)
	merchant=models.ForeignKey(tblMERCHANT)
	recdate=models.DateField(default='2021-6-12')
	amount=models.CharField(max_length=50)

 	status= models.CharField(max_length=20)
	
	account_type=models.CharField(max_length=20,default= 'Main account') #newly added
	wallet_type=models.CharField(max_length=40,default='Main') #changed
	paid_date=models.DateField(default='2021-6-12')

	thrift=models.CharField(max_length=50)
	paid_by=models.CharField(max_length=90)
	# month=models.CharField(max_length=20)


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.date,self.customer) 

class tblpayoutrequest(models.Model):
	customer=models.ForeignKey(tblCUSTOMER)
	merchant=models.ForeignKey(tblMERCHANT)
	branch=models.ForeignKey(tblBRANCH)
	recdate=models.DateField() #cashin date from merchant
	status= models.CharField(max_length=20)	
	amount=models.CharField(max_length=50)

	code=models.IntegerField()
	account_type=models.CharField(max_length=20,default= 'Main account') #newly added
	wallet_type=models.CharField(max_length=40,default='Main') #changed
	request_date=models.DateField(default='2021-6-12') #date request was made


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.account_type,self.customer)