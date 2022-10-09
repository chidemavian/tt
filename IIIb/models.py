from django.db import models


from staff.models import *



from customer.models import *



class tblIIIbcoop(models.Model): #cooperators' table
	branch=models.ForeignKey(tblBRANCH)
	staff=models.ForeignKey(tblSTAFF)
	status= models.BooleanField()
	code=models.IntegerField()
	thrift3b = models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.staff,self.status,self.code)



# # #where all savings packages applications go 
class tblIIIIbstaffbsavings_pack(models.Model):
	branch=models.ForeignKey(tblBRANCH)

	staff=models.ForeignKey(tblIIIbcoop) #who colected the money

	month= models.CharField(max_length=40)
	year= models.CharField(max_length=40)

	transdate=models.DateField()  #date of transaction
	amount= models.CharField(max_length=40) 

	description=models.CharField(max_length=40) #dr , cr
	status=models.CharField(max_length=40) 

	def __unicode__(self):
		return '%s %s %s'%(self.transdate,self.amount,self.status)



class tblIIIbclientsubscription(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	subscription=models.IntegerField() #who colected the money
	status=models.BooleanField(max_length=40) 

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.amount,self.status)


# #admin account for 1a for holding sales and approvals
# class tblIbMERCHANTbank(models.Model):
# 	branch=models.ForeignKey(tblBRANCH)
# 	amount = models.IntegerField() #amount paid

# 	merchant=models.ForeignKey(tblIIIbcoop) #if sales, admin. if approval, merchant

# 	customer=models.ForeignKey(tblIIIbCUSTOMER)
# 	recdate=models.DateField()  #date of record
# 	transdate=models.DateField()  #date of transaction

# 	code=models.IntegerField() #originates from thrift

# 	status= models.CharField(max_length=30)

# 	approved_by=models.CharField(max_length=50) #admin detail

# 	wallet_type=models.CharField(max_length=30,default='Main')
	


# 	def __unicode__(self):
# 		return '%s %s'%(self.recdate,self.amount)




# class tblIbpayoutrequest(models.Model):
# 	customer=models.ForeignKey(tblIIIbCUSTOMER)
# 	merchant=models.ForeignKey(tblIIIbcoop)
# 	branch=models.ForeignKey(tblBRANCH)
# 	account_type=models.CharField(max_length=40,default='Main')
# 	recdate=models.DateField() #cashin date from merchant
# 	status= models.CharField(max_length=20)
# 	amount=models.CharField(max_length=50)

# 	wallet_type=models.CharField(max_length=40,default='Main') #changed

# 	account_type=models.CharField(max_length=20,default='Main account') #newly added


# 	def __unicode__(self):
# 		return '%s %s %s'%(self.amount,self.wallet_type,self.customer)





#All c/os field activities here
class tblIIIbfieldagent(models.Model):
	status=models.CharField(max_length=30)
	branch=models.ForeignKey(tblBRANCH)
	staff=models.ForeignKey(tblIIIbcoop) #whose got the mone

	month=models.CharField(max_length=30)#main or referal
	year=models.CharField(max_length=30)
	amount=models.IntegerField() #amount recieved
	transdate=models.DateField() #date of recept
	
	code=models.CharField(max_length=30) #transaction code
	account_type=models.CharField(max_length=20) #wallet or package
	scheme=models.CharField(max_length=50,null =False)#main or referal

	def __unicode__(self):
		return '%s %s %s'%(self.transdate,self.amount,self.code)



class tblIIIbapprovals(models.Model):
	status=models.CharField(max_length=30)
	branch=models.ForeignKey(tblBRANCH)
	staff=models.ForeignKey(tblIIIbcoop) #whose got the mone
	month=models.CharField(max_length=30)#main or referal
	description=models.CharField(max_length=30)
	year=models.CharField(max_length=30)
	amount=models.IntegerField() #amount recieved
	transdate=models.DateField() #date of recept


	def __unicode__(self):
		return '%s %s %s'%(self.bank_name,self.account_number,self.branch)

# ###########Loans *************************************

# class tblIbstandardloan(models.Model):
# 	staffrec=models.ForeignKey(tblIIIbcoop)
# 	branch=models.ForeignKey(tblBRANCH, related_name='IB branch')
# 	duration=models.IntegerField(max_length=20)
# 	rate=models.CharField(max_length=20)
# 	description=models.CharField(max_length=20)
# 	status=models.BooleanField(max_length=20)

# 	def __unicode__(self):
# 		return '%s %s %s'%(self.rate,self.description,self.duration)

# class tblIbbankdetail(models.Model):
# 	customer=models.ForeignKey(tblIbCUSTOMER)
# 	branch_code=models.ForeignKey(tblBRANCH)
# 	bank_name=models.CharField(max_length=20)
# 	account_number=models.CharField(max_length=20)
# 	def __unicode__(self):
# 		return '%s %s %s'%(self.bank_name,self.account_number,self.branch)
	

# class tblIbloanrequests(models.Model):
# 	branch=models.ForeignKey(tblBRANCH, related_name='allbranches')
# 	date =models.CharField(max_length=20)
# 	repay =models.CharField(max_length=50)
# 	customer=models.ForeignKey(tblIbCUSTOMER, related_name='allcustomer')
# 	package=models.ForeignKey(tblIbstandardloan)
# 	status=models.CharField(max_length=20)
# 	volume=models.CharField(max_length=20)
# 	thrift=models.CharField(max_length=20)
# 	output=models.CharField(max_length=20)

# 	def __unicode__(self):
# 		return '%s %s %s'%(self.branch,self.volume,self.package)



# class tblIbloanrepaymentplan(models.Model):
# 	branch=models.ForeignKey(tblBRANCH)
# 	description=models.CharField(max_length=20)
# 	status=models.BooleanField(max_length=20)

# 	def __unicode__(self):
# 		return '%s %s'%(self.description,self.branch)

# class tblIbloantransaction(models.Model):
# 	branch=models.ForeignKey(tblBRANCH)
# 	transaction_source=models.ForeignKey(tblIbloanrequests)
# 	start_date=models.CharField(max_length=20)
# 	status=models.CharField(max_length=20)
# 	thrift=models.CharField(max_length=20)
	

# 	def __unicode__(self):
# 		return '%s %s %s'%(self.amount,self.start_date,self.status)









class tblstandardloanIIIB(models.Model):
	staffrec=models.ForeignKey(tblIIIbcoop)
	branch=models.ForeignKey(tblBRANCH)
	tenure=models.IntegerField()
	rate=models.CharField(max_length=20)
	description=models.CharField(max_length=20)
	status=models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.rate,self.description,self.tenure)


class tblstandardsavingIIIB(models.Model): #for savings packaages
	staffrec=models.ForeignKey(tblIIIbcoop)
	branch=models.ForeignKey(tblBRANCH)
	from_month=models.CharField(max_length=20)
	to_month=models.CharField(max_length=20)
	description=models.CharField(max_length=20)
	status=models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.rate,self.description,self.from_week)

class tblIIIb_bankdetail(models.Model):
	staff_rec=models.ForeignKey(tblIIIbcoop)
	branch_code=models.ForeignKey(tblBRANCH)
	bank_name=models.CharField(max_length=20)
	account_number=models.CharField(max_length=20)


	def __unicode__(self):
		return '%s %s %s'%(self.bank_name,self.account_number,self.branch)
	

class tblIIIbloandapplications(models.Model):
	branch=models.ForeignKey(tblBRANCH, related_name='allbranch')
	date =models.CharField(max_length=20)
	staffrec=models.ForeignKey(tblIIIbcoop)
	package=models.ForeignKey(tblstandardloanIIIB)
	status=models.CharField(max_length=20)
	volume=models.CharField(max_length=20)
	thrift=models.CharField(max_length=20)
	repay_month=models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.volume,self.package)



class tblmaxloanIIIB(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	value=models.CharField(max_length=20)


	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.value)


class tblIIIbloantransaction(models.Model):
	transaction_source=models.ForeignKey(tblIIIbloandapplications)
	# start_date=models.CharField(max_length=20)
	status=models.CharField(max_length=20)
	amount=models.CharField(max_length=20)
	

	month=models.CharField(max_length=30)#main or referal
	year=models.CharField(max_length=30)


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.self.month,self.status)


class tblIIIbsavingsaccount(models.Model): #actual wallet
	branch=models.ForeignKey(tblBRANCH)
	status=models.CharField(max_length=30)
	staff=models.ForeignKey(tblIIIbcoop) #whose got the mone
	month=models.CharField(max_length=30)#main or referal
	amount=models.IntegerField() #amount recieved
	transdate=models.DateField(default= '2020-02-04') #date of recept	
	code=models.CharField(max_length=30) #transaction code
	account_type=models.CharField(max_length=20) #wallet or package
	year=models.CharField(max_length=30)


	def __unicode__(self):
		return '%s %s %s'%(self.staff_rec,self.amount,self.saving_date)

