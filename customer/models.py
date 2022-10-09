from django.db import models

from staff.models import *





class tblCUSTOMER(models.Model):
	branch=models.ForeignKey(tblBRANCH)

	surname=models.CharField(max_length=20)
	firstname=models.CharField(max_length=20)
	othername=models.CharField(max_length=20)
	wallet=models.IntegerField()
	phone=models.IntegerField()
	Address=models.CharField(max_length=200)
	photo=models.ImageField(upload_to='company_logo', null=True,blank=True,default='studentpix/user.png')
	email=models.EmailField()
	
	status=models.BooleanField()

	dc=models.BooleanField()  #daily contr
	ivb=models.BooleanField()  #investment Banking
	ts=models.BooleanField()   #target savings
	cc=models.BooleanField()  	#corperate C
	cs=models.BooleanField()   #cooperative society	
	code=models.IntegerField()
	def __unicode__(self):
		return '%s %s %s'%(self.surname,self.firstname,self.othername) 


