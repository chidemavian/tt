

from django.db import models

from staff.models import *

from customer.models import *




class tblIbco(models.Model): #field_officers
	branch=models.ForeignKey(tblBRANCH)
	staff=models.ForeignKey(tblSTAFF)
	status= models.BooleanField()
	code=models.IntegerField()
	thrift1b = models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.staff,self.status,self.code)


#customers who subscribe to 1a service
class tblIbCUSTOMER(models.Model): #Ib Customers
	branch=models.ForeignKey(tblBRANCH)
	merchant=models.ForeignKey(tblIbco) #who registered me
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



# #where all savings, withdrwals and service charges are kept
class tblIbsavings_trans(models.Model): #firt leg savings
	branch=models.ForeignKey(tblBRANCH)

	merchant=models.ForeignKey(tblIbco) #who colected the money

	customer=models.ForeignKey(tblIbCUSTOMER) #whose money is it
	
	recdate=models.DateField() #recorddate
	transdate=models.DateField()  #date of transaction
	amount= models.CharField(max_length=40) #how much
	wallet_type=models.CharField(max_length=40,default='Main') #

	code=models.IntegerField(default=0) #originates from thrift

	description=models.CharField(max_length=40) #dr , cr
	status=models.CharField(max_length=40) #service charges, withdrawn,

	avalability=models.CharField(max_length=50) #use availability to manipulate withdrwal (if u got loan)
	channel=models.CharField(max_length=50, default='deposit')

	def __unicode__(self):
		return '%s %s %s'%(self.recdate,self.amount,self.wallet_type)




#admin account for 1a for holding sales and approvals
class tblIbMERCHANTbank(models.Model): #second leg savings
	branch=models.ForeignKey(tblBRANCH)
	amount = models.IntegerField() #amount paid

	merchant=models.ForeignKey(tblIbco) #if sales, admin. if approval, merchant

	customer=models.ForeignKey(tblIbCUSTOMER)
	recdate=models.DateField()  #date of record
	transdate=models.DateField()  #date of transaction

	code=models.IntegerField() #originates from thrift

	status= models.CharField(max_length=30)

	approved_by=models.CharField(max_length=50) #admin detail

	wallet_type=models.CharField(max_length=30,default='Main')
	


	def __unicode__(self):
		return '%s %s'%(self.recdate,self.amount)





class tblIbfieldagent(models.Model):
	status=models.CharField(max_length=30)
	branch=models.ForeignKey(tblBRANCH)
	merchant=models.ForeignKey(tblIbco) #whose got the mone

	wallet_type=models.CharField(max_length=30)#main or referal

	amount=models.IntegerField() #amount recieved
	transdate=models.DateField() #date of recept
	customer=models.ForeignKey(tblIbCUSTOMER)

	
	code=models.CharField(max_length=30) #transaction code


	def __unicode__(self):
		return '%s %s %s'%(self.transdate,self.amount,self.code)




class tblIbpayoutrequest(models.Model):
	customer=models.ForeignKey(tblIbCUSTOMER)
	merchant=models.ForeignKey(tblIbco)
	branch=models.ForeignKey(tblBRANCH)
	account_type=models.CharField(max_length=40,default='Main')
	recdate=models.DateField() #cashin date from merchant
	status= models.CharField(max_length=20)
	amount=models.CharField(max_length=50)

	wallet_type=models.CharField(max_length=40,default='Main') #changed

	account_type=models.CharField(max_length=20,default='Main account') #newly added


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.wallet_type,self.customer)






class tblIbCashier(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	customer=models.ForeignKey(tblIbCUSTOMER)

	merchant=models.ForeignKey(tblIbco) #whose got the money

	transdate=models.DateField() #date of recept
	remitdate=models.DateField()
	amount=models.IntegerField() #amount recieved
	
	wallet_type=models.CharField(max_length=30)#main or referal
	status=models.CharField(max_length=30)

	code=models.CharField(max_length=30) #transaction code
	remitted_by=models.CharField(max_length=50) #cashier detail
	# account_type=models.CharField(max_length=20,default='Main account') #newly added


	def __unicode__(self):
		return '%s %s %s'%(self.transdate,self.amount,self.code)




####**************Interests*******************
class tblIbinterest(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	duration=models.IntegerField()

	interest =models.CharField(max_length=5) 

	status=models.BooleanField()
	code =models.IntegerField()

	def __unicode__(self):
		return '%s %s %s'%(self.duration,self.interest,self.code)





###########Loans *************************************

class tblIbstandardloan(models.Model):
	staffrec=models.ForeignKey(tblSTAFF)
	branch=models.ForeignKey(tblBRANCH, related_name='IB branch')
	duration=models.IntegerField(max_length=20)
	rate=models.CharField(max_length=20)
	description=models.CharField(max_length=20)
	status=models.BooleanField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.rate,self.description,self.duration)

class tblIbbankdetail(models.Model):
	customer=models.ForeignKey(tblIbCUSTOMER)
	branch_code=models.ForeignKey(tblBRANCH)
	bank_name=models.CharField(max_length=20)
	account_number=models.CharField(max_length=20)
	def __unicode__(self):
		return '%s %s %s'%(self.bank_name,self.account_number,self.branch)
	

class tblIbloanrequests(models.Model):
	branch=models.ForeignKey(tblBRANCH, related_name='allbranches')
	date =models.CharField(max_length=20)
	repay =models.CharField(max_length=50)
	customer=models.ForeignKey(tblIbCUSTOMER, related_name='allcustomer')
	package=models.ForeignKey(tblIbstandardloan)
	status=models.CharField(max_length=20)
	volume=models.CharField(max_length=20)
	thrift=models.CharField(max_length=20)
	output=models.CharField(max_length=20)
	loancode=models.CharField(max_length=30)

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.volume,self.package)



class tblIbloanrepaymentplan(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	description=models.CharField(max_length=20)
	status=models.BooleanField(max_length=20)

	def __unicode__(self):
		return '%s %s'%(self.description,self.branch)

class tblIbloantransaction(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	transaction_source=models.ForeignKey(tblIbloanrequests)
	start_date=models.DateField(max_length=20)
	status=models.CharField(max_length=20)
	thrift=models.CharField(max_length=20)
	loancode=models.CharField(max_length=30)

	

	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.start_date,self.status)


class tblIbgrace(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	plan=models.CharField(max_length=20)
	grace=models.IntegerField(max_length=20)
	status=models.BooleanField(max_length=20)

	def __unicode__(self):
		return '%s %s'%(self.plan,self.branch)