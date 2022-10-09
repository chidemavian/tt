from django.db import models


from business.models import *


class tblSTAFF(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	surname=models.CharField(max_length=20)
	firstname=models.CharField(max_length=20)
	othername=models.CharField(max_length=20)
	email=models.EmailField(max_length=20)
	phone=models.IntegerField()
	Address=models.CharField(max_length=200)
	photo=models.ImageField(upload_to='staff-pix', null=True,blank=True,default='staff-pix/user.png')
	code=models.IntegerField()
	types=models.CharField(max_length=20)
	status= models.BooleanField()
	
	def __unicode__(self):
		return '%s %s %s'%(self.surname,self.firstname,self.othername)


class tblMERCHANT(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	staff=models.ForeignKey(tblSTAFF)
	status= models.BooleanField()
	# status= models.CharField(max_length=20)
	code=models.IntegerField()

	thrift1a =models.BooleanField()
	thrift1b = models.BooleanField()
	thrift3b = models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.staff,self.status,self.code)


# # class capitalization(models.Model):
# # 	merchant= models.ForeignKey(tblSTAFF)
# # 	recdate= models.DateField()
# # 	branch=models.ForeignKey(tblBRANCH)
# # 	code=models.IntegerField()
# # 	capitalization=models.IntegerField()





