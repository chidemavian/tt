


from django.db import models

from staff.models import *

from customer.models import *




class tblIaMERCHANT(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	staff=models.ForeignKey(tblSTAFF)
	status= models.BooleanField()
	code=models.IntegerField()
	thrift1a = models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.staff,self.status,self.code)

#customers who subscribe to 1a service
class tblIaCUSTOMER(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	merchant=models.ForeignKey(tblIaMERCHANT) #who registered me
	customer=models.ForeignKey(tblCUSTOMER)
	UX= models.BooleanField()
	status=models.BooleanField()
	online=models.BooleanField()
	code=models.IntegerField()
	sms=models.BooleanField()
	get_email=models.BooleanField()
	withdr_status=models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.status,self.code)




class tblIathrift(models.Model):
	customer=models.ForeignKey(tblIaCUSTOMER)
	branch=models.ForeignKey(tblBRANCH)
	month=models.CharField(max_length=20)
	thrift=models.IntegerField()
	code=models.IntegerField()
	year=models.CharField(max_length=20)
	account_type=models.CharField(max_length=20,default='Main account') #newly added


	def __unicode__(self):
		return '%s %s %s'%(self.account_type,self.month,self.code)


#C/Os accont for 1a where customers pay into
class tblIafieldagent(models.Model):
	status=models.CharField(max_length=30)
	branch=models.ForeignKey(tblBRANCH)
	merchant=models.ForeignKey(tblIaMERCHANT) #whose got the mone

	wallet_type=models.CharField(max_length=30)#main or referal

	amount=models.IntegerField() #amount recieved
	recdate=models.DateField() #date of recept
	customer=models.ForeignKey(tblIaCUSTOMER)
	number =models.IntegerField(max_length=40)
	
	code=models.CharField(max_length=30) #thrift related code
	account_type=models.CharField(max_length=20,default='Main account') #newly added
	transac_id=models.IntegerField(max_length=30) #transaction code

	def __unicode__(self):
		return '%s %s %s'%(self.recdate,self.amount,self.code)



#Cashiers accont for 1a where merchants  pay into ( for remittance)
class tblIaCashier(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	customer=models.ForeignKey(tblIaCUSTOMER)

	merchant=models.ForeignKey(tblIaMERCHANT) #whose got the money

	remdate=models.DateField() #date of recept
	amount=models.IntegerField() #amount recieved
	number =models.CharField(max_length=40)

	wallet_type=models.CharField(max_length=30)#main or referal
	status=models.CharField(max_length=30)

	code=models.CharField(max_length=30) #transaction code
	remitted_by=models.CharField(max_length=50) #cashier detail
	account_type=models.CharField(max_length=20,default='Main account') #newly added


	def __unicode__(self):
		return '%s %s %s'%(self.remdate,self.amount,self.code)



#admin account for 1a for holding sales and approvals
class tblIamerchantBank(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	# approved_date=models.DateField() #remittion date
	amount = models.IntegerField() #amount paid

	merchant=models.ForeignKey(tblIaMERCHANT) #if sales, admin. if approval, merchant

	customer=models.ForeignKey(tblIaCUSTOMER)
	recdate=models.DateField()  #date of record
	transdate=models.DateField()  #date of transaction


	number =models.CharField(max_length=40)
	code=models.IntegerField() #originates from thrift


	status= models.CharField(max_length=30)

	approved_by=models.CharField(max_length=50) #admin detail


	wallet_type=models.CharField(max_length=30,default='Main')
	account_type=models.CharField(max_length=20,default='Main account') #newly added


	transac_id = models.IntegerField() #transacttion id 



	def __unicode__(self):
		return '%s %s'%(self.recdate,self.amount)


#where all savings, withdrwals and service charges are kept
class tblIasavings_trans(models.Model):
	branch=models.ForeignKey(tblBRANCH)

	merchant=models.ForeignKey(tblIaMERCHANT) #who colected the money

	customer=models.ForeignKey(tblIaCUSTOMER) #whose money is it
	recdate=models.DateField() #recorddate
	transdate=models.DateField()  #date of transaction
	amount= models.IntegerField() #how much
	wallet_type=models.CharField(max_length=40,default='Main') #

	code=models.IntegerField(default=0) #originates from thrift

	number =models.CharField(max_length=40)
	description=models.CharField(max_length=40) #dr , cr
	status=models.CharField(max_length=40) #service charges, withdrawn,

	avalability=models.CharField(max_length=50) #use availability to manipulate withdrwal (if u got loan)

	account_type=models.CharField(max_length=20,default='Main account') #newly added

	transac_id = models.IntegerField() #transacttion id

	def __unicode__(self):
		return '%s %s %s'%(self.recdate,self.amount,self.wallet_type)



class tblIapayoutrequest(models.Model):
	customer=models.ForeignKey(tblIaCUSTOMER)
	merchant=models.ForeignKey(tblIaMERCHANT)
	branch=models.ForeignKey(tblBRANCH)
	account_type=models.CharField(max_length=40,default='Main')
	recdate=models.DateField() #cashin date from merchant
	status= models.CharField(max_length=20)
	amount=models.CharField(max_length=50)

	wallet_type=models.CharField(max_length=40,default='Main') #changed

	account_type=models.CharField(max_length=20,default='Main account') #newly added


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.wallet_type,self.customer)




class tblIapayoutrecord(models.Model):
	customer=models.ForeignKey(tblIaCUSTOMER)
	merchant=models.ForeignKey(tblIaMERCHANT)
	branch=models.ForeignKey(tblBRANCH)
	account_type=models.CharField(max_length=40,default='Main')
	recdate=models.DateField() #cashin date from merchant
	status= models.CharField(max_length=20)
	amount=models.CharField(max_length=50)
	wallet_type=models.CharField(max_length=40,default='Main') #changed

	account_type=models.CharField(max_length=20,default='Main account') #newly added


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.wallet_type,self.customer)

