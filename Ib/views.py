from __future__ import division

from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json

from Ib.forms import *
from Ib.utils import *

from num2words import num2words

from sysadmin.models import *
from customer.models import *
from merchant.models import *
from Ib.models import *
from savings.models import *


from datetime import *
import calendar

#######import only merchant.models******
from calendar import monthrange

from django.core.serializers.json import json

from django.db.models import Max,Sum

import random

import locale


def welcome(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1,thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if staff.thrift1b_cashier==1 or staff.thrift1b_admin==1:
			return render_to_response('Ib/adminwelcome.html',{'company':mybranch, 'user':varuser})

		elif staff.thrift1b_officer==1:
			return render_to_response('Ib/welcome.html',{'company':mybranch, 'user':varuser})


	else:
		return HttpResponseRedirect('/login/user/')




def adminuserguide(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift1b_admin ==1:
			return render_to_response('Ib/adminwelcome.html',{'company':mybranch, 'user':varuser})
		elif staff.thrift1b_cashier ==1:
			return render_to_response('Ib/cashierwelcome.html',{'company':mybranch, 'user':varuser})
		elif staff.thrift1b_officer ==1:
			return render_to_response('Ib/welcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



def adminwelcome(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1,thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'
			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)



		if staff.thrift1b_admin==1: 
			return render_to_response('Ib/dashboardIb.html',{'company':mybranch, 'user':varuser,'pincode':staff})
		elif staff.thrift1b_cashier==1:
			return render_to_response('Ib/dashboardIb_cash.html',{'company':mybranch, 'user':varuser,'pincode':staff})
		elif staff.thrift1b_officer==1:
			return render_to_response('Ib/dashboardIb_co.html',{'company':mybranch, 'user':varuser,'pincode':staff})
			


	else:
		return HttpResponseRedirect('/login/user/')






def adminwelcome_p(request): #code tonormaliz database for victor
	if 'userid' in request.session:
		k1=[1,2,3,4]

		for m in k1:

			fdate=date('2022',m,1)

			p = (monthrange(fdate.year, fdate.month))[-1]

			k = 1 
			while k <= p:
				kdate=date('2022',m,k)

				tblIbsavings_trans.objects.objects.get()
			try:

				savings = tblIbsavings_trans.objects.get(branch=mybranch,
					# merchant=memmerchant,
					# customer=Ib,
					# recdate=myydate,
					# amount=amount,
					wallet_type='Main',
					description='DR',
					status='Available',
					avalability='Available')

			except:

				tblIbsavings_trans(branch=mybranch,
					merchant=memmerchant,
					customer=Ib,
					recdate=myydate,
					amount=amount,
					wallet_type='Main',
					description='DR',
					status='Withdrawn',
					avalability='Not Available').save()

				tblIbMERCHANTbank(branch=mybranch,
					merchant=memmerchant,
					wallet_type='Main',
					remitted_by=varuser,
					approved_by=varuser,
					recdate=mydate,
					rem_date=mydate,
					customer=Ib,
					amount=amount,
					status='Withdrawn').save()

				tblIbsavings_trans(branch=mybranch,
					merchant=memmerchant,
					customer=Ib,
					recdate=myydate,
					amount=charge,
					wallet_type='Main',
					description='DR',
					status='Service Charge',
					avalability='Not Available').save()
				tblIbMERCHANTbank(branch=mybranch,
					merchant=memmerchant,
					wallet_type='Main',
					remitted_by=varuser,
					approved_by=varuser,
					recdate=mydate,
					rem_date=mydate,
					customer=Ib,
					amount=charge,
					status='Service Charge').save()





		return render_to_response('Ib/dashboardIb.html',{'company':mybranch, 'user':varuser,'pincode':staff})

	else:
		return HttpResponseRedirect('/login/user/')


# This function gives credit officer privilege to a staff




#**************************CREDIT OFFICERS*************************

def regcreditofficer(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.thrift1b_cashier==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		# mystafflist = tblSTAFF.objects.filter(status=1, branch=mybranch).count()


		if request.method== 'POST':
			form = staffform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']
				mystaff = tblSTAFF.objects.filter(email=email,status=1, branch=mybranch) #check status
				mycount=mystaff.count()

				if mycount == 1: #user is a staff
					querry_email = tblSTAFF.objects.get(email=email)

					try:
						ibco = tblIbco.objects.get(branch = mybranch, thrift1b=1,staff=querry_email)
						if ibco.status == False:
							msg = 'credit officer is inactive'

						elif ibco.status == True:
							msg='ALREADY REGISTERED'

					except:
						diff = Userprofile.objects.get(email=email,status=1)
						diff.thrift1b_officer=1
						diff.thrift1b=1
						diff.save()						
						form = staffform()
						msg="SUCCESSFUL"

						try:
							register_field_officerIb(email)
						except:
							pass

						tblIbco(status=1, branch=mybranch,thrift1b=1, staff=querry_email,code=querry_email.code).save()

				elif mycount == 0:
					msg = 'THIS EMAIL IS NOT REGISTERED'
			else:
				msg = 'INVALID ENTRY'
		else:
			form = staffform()
			msg=''

		meer = tblIbco.objects.filter(branch=mybranch,thrift1b=1)
		inactiveco = tblIbco.objects.filter(status=0, thrift1b=1, branch=mybranch).count()

		if staff.thrift1b_admin == 1:
			return render_to_response('Ib/merch.html',{
				# 'staffcount':mystafflist, 'ggg': mycolist,
				'company':mybranch,'msg':msg, 'user':varuser,'form':form,'merchant':meer})
		elif staff.thrift1b_cashier == 1:
			return render_to_response('Ib/merch_cash.html',{
				# 'staffcount':mystafflist, 'ggg': mycolist,
				'company':mybranch,'msg':msg, 'user':varuser,'form':form,'merchant':meer})

	else:
		return HttpResponseRedirect('/login/user/')







def mycos(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.thrift1b_cashier==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		msg = ''

		meer = tblIbco.objects.filter(branch=mybranch,thrift1b=1)
		inactiveco = tblIbco.objects.filter(status=0, thrift1b=1, branch=mybranch).count()

		if staff.thrift1b_admin == 1:
			return render_to_response('Ib/merch_list.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})
		elif staff.thrift1b_cashier == 1:
			return render_to_response('Ib/merch_cash_list.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})

	else:
		return HttpResponseRedirect('/login/user/')



def managecos(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.thrift1b_cashier==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		msg = ''

		meer = tblIbco.objects.filter(branch=mybranch,thrift1b=1)


		if staff.ceo == 1:
			return render_to_response('Ib/manageco.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})
		elif staff.thrift1b_admin == 1:
			return render_to_response('Ib/manageco_admin.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})

	else:
		return HttpResponseRedirect('/login/user/')


def editstaf(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)

    		try:
    			memmerchant=tblIbco.objects.get( id= state)
    			my_staff_id = memmerchant.staff.id
    			my_staff_id2= tblSTAFF.objects.get(branch=mybranch,id=my_staff_id)
    			status=Userprofile.objects.get(branch=mybranch,staffrec=my_staff_id2)
    			status=status.status

    			return render_to_response('Ib/stafffedit.html',{'income':memmerchant,'status':status})

    		except:
    			msg='error !!!'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def changestatus(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		if 'status' in request.POST:
			co = request.POST['status']
		else:
			co=0

		merchant=request.POST['CO']

		memmerchant=tblIbco.objects.get(branch=mybranch, id= merchant)
		my_staff_id = memmerchant.staff.id
		my_staff_id2= tblSTAFF.objects.get(branch=mybranch,id=my_staff_id)
		status=Userprofile.objects.filter(branch=mybranch,staffrec=my_staff_id2).update(status=co)
		

		memmerchant.status=co
		memmerchant.save()


		my_staff_id2.status=co
		my_staff_id2.save()


		return HttpResponseRedirect('/vts/staff/merchant/manage/')

	else:
		return HttpResponseRedirect('/login/user/')



def priviledges(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.thrift1b_cashier==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		msg = ''

		meer = tblIbco.objects.filter(branch=mybranch,thrift1b=1)


		if staff.ceo == 1:
			return render_to_response('Ib/priviledge.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})
		elif staff.thrift1b_admin == 1:
			return render_to_response('Ib/priviledge.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})

	else:
		return HttpResponseRedirect('/login/user/')
		

def editstaf(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)

    		try:
    			memmerchant=tblIbco.objects.get( id= state)
    			my_staff_id = memmerchant.staff.id
    			my_staff_id2= tblSTAFF.objects.get(branch=mybranch,id=my_staff_id)
    			status=Userprofile.objects.get(branch=mybranch,staffrec=my_staff_id2)
    			status=status.status

    			return render_to_response('Ib/stafffedit.html',{'income':memmerchant,'status':status})

    		except:
    			msg='error !!!'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def changestatus(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		if 'status' in request.POST:
			co = request.POST['status']
		else:
			co=0

		merchant=request.POST['CO']

		memmerchant=tblIbco.objects.get(branch=mybranch, id= merchant)
		my_staff_id = memmerchant.staff.id
		my_staff_id2= tblSTAFF.objects.get(branch=mybranch,id=my_staff_id)
		status=Userprofile.objects.filter(branch=mybranch,staffrec=my_staff_id2).update(status=co)
		

		memmerchant.status=co
		memmerchant.save()


		my_staff_id2.status=co
		my_staff_id2.save()


		return HttpResponseRedirect('/vts/staff/merchant/manage/')

	else:
		return HttpResponseRedirect('/login/user/')


def subscribe(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		msg = ''

		if request.method == 'POST':
			acname=request.POST['acno']

			try:
				countt=tblCUSTOMER.objects.get(branch=mybranch, wallet=acname,status=1)

				try:
					cty = tblIbCUSTOMER.objects.get(customer=countt,branch=mybranch, status=1)
					msg = "This Customer already subscribed for this service"
					if staff.thrift1b_admin:
						return render_to_response('Ib/walletdetails.html',{'company':mybranch, 'user':varuser,'msg':msg,'details':cty})

					if staff.thrift1b_cashier:
							return render_to_response('Ib/walletdetails_cash.html',{'company':mybranch, 'user':varuser,'msg':msg,'details':cty})

					if staff.thrift1b_officer:
							return render_to_response('Ib/walletdetails_co.html',{'company':mybranch, 'user':varuser,'msg':msg,'details':cty})

				except Exception, e:
					if staff.thrift1b_admin:
						return render_to_response('Ib/subscribe_service.html',{'company':mybranch, 'user':varuser,'details':countt})

					if staff.thrift1b_cashier:
						return render_to_response('Ib/subscribe_service_cash.html',{'company':mybranch, 'user':varuser,'details':countt})

					if staff.thrift1b_officer:
						return render_to_response('Ib/subscribe_service_co.html',{'company':mybranch, 'user':varuser,'details':countt})
			

			except:
				msg = 'Account number not found'

		if staff.thrift1b_admin:
			return render_to_response('Ib/subscribe.html',{'company':mybranch, 'user':varuser,'msg':msg})
		elif staff.thrift1b_cashier:
			return render_to_response('Ib/subscribe_cash.html',{'company':mybranch, 'user':varuser,'msg':msg})
		elif staff.thrift1b_officer:
			return render_to_response('Ib/subscribe_co.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')




def mylist(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIbco.objects.filter(branch=mybranch, 
			staff=memstaff,
			thrift1b=1, 
			status=1).count()
		
		if staff.thrift1b_officer==0  or memmerchant<1:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIbco.objects.get(branch=mybranch, staff=memstaff,thrift1b=1, status=1)


		if staff.thrift1b_admin:
			cutlist= tblIbCUSTOMER.objects.filter(branch=mybranch)
			return render_to_response('Ib/custlist.html',{'company':mybranch, 
				'user':varuser,'client_list':cutlist})
		
		elif staff.thrift1b_cashier:
			cutlist = tblIbCUSTOMER.objects.filter(branch=mybranch,merchant=memmerchant)
			return render_to_response('Ib/custlist_cash.html',{'company':mybranch, 'user':varuser,'client_list':cutlist})
		
		elif staff.thrift1b_officer:
			cutlist = tblIbCUSTOMER.objects.filter(branch=mybranch,merchant=memmerchant)
			return render_to_response('Ib/custlist_co.html',{'company':mybranch, 'user':varuser,'client_list':cutlist})

	else:
		return HttpResponseRedirect('/login/user/')



def gensave(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		msg = ''

		if request.method == 'POST':
			customer=request.POST['customer']
			customer= tblCUSTOMER.objects.get(id=customer,branch=mybranch)
			pin=customer.code
			email=customer.email
			acname=customer.wallet

			try :
				cty = tblIbCUSTOMER.objects.get(withdr_status=1,branch=mybranch,customer=customer,status=1,get_email=1)
				
				msg = "This Customer already subscribed for this service"
				if staff.thrift1b_admin:
					return render_to_response('Ib/walletdetails.html',{'company':mybranch, 'user':varuser,'msg':msg,'details':cty})

				if staff.thrift1b_cashier:
						return render_to_response('Ib/walletdetails_cash.html',{'company':mybranch, 'user':varuser,'msg':msg,'details':cty})

				if staff.thrift1b_officer:
						return render_to_response('Ib/walletdetails_co.html',{'company':mybranch, 'user':varuser,'msg':msg,'details':cty})

			except:

				tblIbCUSTOMER(code=pin,withdr_status=1,branch=mybranch, customer=customer,merchant=memmerchant,status=1,get_email=1).save()
				customer.cs=1
				customer.save()

				try:
					customer_activationIb(email)
				except:
					pass

				if staff.thrift1b_admin:
					return render_to_response('Ib/success.html',{'company':mybranch,'user':varuser,'wallet':acname })
				if staff.thrift1b_cashier:
					return render_to_response('Ib/success_cash.html',{'company':mybranch,'user':varuser,'wallet':acname })
				if staff.thrift1b_officer:
					return render_to_response('Ib/success_co.html',{'company':mybranch,'user':varuser,'wallet':acname })

	else:
		return HttpResponseRedirect('/login/user/')




def asserteditwallet(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html')

		if request.method == 'POST':
			wallet=request.POST['wallet']
			surname=request.POST['surname']
			othername=request.POST['othername']
			firstname=request.POST['firstname']
			address=request.POST['address']
			email=request.POST['email']

			customer=tblCUSTOMER.objects.get(branch=mybranch, merchant=memmerchant, wallet=wallet,status=1)

			customer.surname=surname
			customer.firstname=firstname
			customer.othername=othername
			customer.address=address
			customer.email=email

			if 'photo' in request.FILES:
				photo = request.FILES['photo']
				customer.photo=photo

			customer.save()

			msg='Customer information edited successfully'

			return render_to_response('Ib/editsucc.html',{'company':mybranch,'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')

def addmythrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)

		tdate= date.today()
		mday=tdate.month
		month = calendar.month_name[mday]
		myform = kthriftform()


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			myform = kthriftform(request.POST)
			details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)
			return render_to_response('Ib/comeadd.html',{'company':mybranch,'user':varuser,'form':myform,
			'wallet':mywallet,'month':month})
		else:
			return HttpResponseRedirect('/login/user/')




####  CAsh iN prOcedures {FIELD}************************

def payrequests(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		fdate=date.today()

		try:
			memmerchant=tblIbco.objects.get(branch=mybranch, staff=memstaff,status=1,thrift1b=1)

		except:

			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			amount=request.POST['amount']


			try:
				details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet,status=1)
				fig = num2words(int(amount))
				# fig = num2words(amount, lang='enk', to='ordinal', separator=' and', cents=False, currency='USD')


				if staff.thrift1b_admin:
					detailIb=tblIbCUSTOMER.objects.get(branch=mybranch, customer=details)
					return render_to_response('Ib/deposit.html',{'company':mybranch,'user':varuser,
						'customer':detailIb,'branch':branch, 'wallet':mywallet,'wrd':fig,'amount':amount})

				if staff.thrift1b_cashier:
					try:
						detailIb=tblIbCUSTOMER.objects.get(branch=mybranch, customer=details, 
							# merchant=memmerchant
							)

						agcount = tblIbfieldagent.objects.filter(
							branch=mybranch,
							status='Received',
							wallet_type='Main',
							amount=amount,
							transdate=fdate,					
							merchant=memmerchant,
							customer=detailIb).count()
						
						if agcount==1:
							msg='you cant post same amount twice'
							return render_to_response('Ib/selectloan.html',{'msg':msg})
						return render_to_response('Ib/deposit_cash.html',{'company':mybranch,'user':varuser,
							'customer':detailIb,'branch':branch, 'wallet':mywallet,'wrd':fig,'amount':amount})
					except:
						msg ='Invalid Account number'
						return render_to_response('Ib/selectloan.html',{'msg':msg})

				


				if staff.thrift1b_officer:
					try:
						detailIb=tblIbCUSTOMER.objects.get(branch=mybranch, customer=details,
							# merchant=memmerchant
							)
						agcount = tblIbfieldagent.objects.filter(
							branch=mybranch,
							status='Received',
							wallet_type='Main',
							amount=amount,
							transdate=fdate,					
							merchant=memmerchant,
							customer=detailIb).count()
						
						if agcount==1:
							msg='you cant post same amount twice'
							return render_to_response('Ib/selectloan.html',{'msg':msg})
						

						return render_to_response('Ib/deposit_co.html',{'company':mybranch,'user':varuser,
							'customer':detailIb,'branch':branch, 'wallet':mywallet,'wrd':fig,'amount':amount})

					except:
						msg ='Invalid Account number'
						return render_to_response('Ib/selectloan.html',{'msg':msg})


			except:
				msg='Invalid Account number'
				return render_to_response('Ib/selectloan.html',{'company':mybranch,'msg':msg})
		else:
			msg=''

			if staff.thrift1b_admin==1 :
				return render_to_response('Ib/all.html',{'company':mybranch, 'user':varuser,'msg':msg})
			elif staff.thrift1b_cashier==1:
				return render_to_response('Ib/all_cash.html',{'company':mybranch, 'user':varuser,'msg':msg})
			elif staff.thrift1b_officer==1:
				return render_to_response('Ib/all_co.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



def cashin(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		if staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		fdate= datetime.today()

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']
			customer=request.POST['customer']
			branch=request.POST['branch']
			amount=request.POST['amount']

			customer1 =tblCUSTOMER.objects.get(branch=mybranch,wallet=wallet,status=1)
			code=customer1.code
			email=customer1.email


			customer=tblIbCUSTOMER.objects.get(branch=mybranch,customer=customer1)


			if staff.thrift1b_admin==1 : ##instant crediting if you are the admin


				adcount = tblIbMERCHANTbank.objects.filter(
					branch=mybranch,
					status='Approved',
					transdate=fdate,
					wallet_type='Main',
					amount=amount,
					approved_by=varuser,
					merchant=memmerchant,
					recdate=fdate,
					customer=customer).count()

				if adcount<1:


					tblIbMERCHANTbank(
						branch=mybranch,
						status='Approved',
						transdate=fdate,
						wallet_type='Main',
						amount=amount,
						code =code,
						approved_by=varuser,
						merchant=memmerchant,
						recdate=fdate,
						customer=customer).save()


				savecount = tblIbsavings_trans.objects.filter(
					branch=mybranch,
					status='Available',
					transdate=fdate,
					description='CR',
					wallet_type='Main',
					amount=amount,
					avalability='Available',
					customer=customer,
					recdate=fdate,
					merchant=memmerchant).count()

				if savecount <1 :


					tblIbsavings_trans(
					branch=mybranch,
					status='Available',
					transdate=fdate,
					description='CR',
					wallet_type='Main',
					amount=amount,
					avalability='Available',
					customer=customer,
					code=code,
					recdate=fdate,
					merchant=memmerchant).save()


						##configure email and sms notifications


				try:
					direct_depositIb(email)
				except:
					pass


				return render_to_response('Ib/cashin_success.html',{'company':mybranch,
						'user':varuser,
						'wallet':wallet,
						'amount':amount})

			else:
				return HttpResponseRedirect('/vts/thrift/payrequest/')


	else:
		return HttpResponseRedirect('/login/user/')



def cashin_cash(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		if staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		fdate= datetime.today()
		fdate=date(fdate.year,fdate.month,fdate.day)

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']

			customer=request.POST['customer']
			branch=request.POST['branch']
			amount=request.POST['amount']

			customer1 =tblCUSTOMER.objects.get(branch=mybranch,wallet=wallet,status=1)
			code=customer1.code

			if staff.thrift1b_cashier==1 : ##instant crediting if you are the admin
				
				try:
					customer=tblIbCUSTOMER.objects.get(branch=mybranch,
						# merchant=memmerchant, 
						customer=customer1)
				except:
					msg='error'
					return render_to_response('Ib/selectloan.html',{'msg':msg})

				agcount = tblIbfieldagent.objects.filter(
					branch=mybranch,
					status='Received',
					wallet_type='Main',
					amount=amount,
					transdate=fdate,					
					merchant=memmerchant,
					customer=customer).count()
				
				if agcount<1:

					tblIbfieldagent(
						branch=mybranch,
						status='Received',
						wallet_type='Main',
						amount=amount,
						transdate=fdate,
						code=code,				
						merchant=memmerchant,
						customer=customer).save()

					return render_to_response('Ib/cashin_success_cash.html',{'company':mybranch,
						'user':varuser,
						'wallet':wallet,
						'amount':amount})

		else:
			return HttpResponseRedirect('/vts/thrift/payrequest/')

	else:
		return HttpResponseRedirect('/login/user/')




def cashin_agent(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		if staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		fdate= datetime.today()
		fdate=date(fdate.year,fdate.month,fdate.day)

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']
			customer=request.POST['customer']

			branch=request.POST['branch']
			amount=request.POST['amount']

			customer1 =tblCUSTOMER.objects.get(branch=mybranch,wallet=wallet,status=1)
			code=customer1.code


			if staff.thrift1b_officer==1 : ##instant crediting if you are the admin
				
				try:
					customer=tblIbCUSTOMER.objects.get(branch=mybranch,
						# merchant=memmerchant, 
						customer=customer1)
				except:
					msg='error'
					return render_to_response('Ib/selectloan.html',{'msg':msg})

				agcount = tblIbfieldagent.objects.filter(
					branch=mybranch,
					status='Received',
					wallet_type='Main',
					amount=amount,
					transdate=fdate,					
					merchant=memmerchant,
					customer=customer).count()
				
				# msg=agcount			
				# return render_to_response('Ib/selectloan.html',{'msg':msg})


				if agcount<1:

					tblIbfieldagent(
						branch=mybranch,
						status='Received',
						wallet_type='Main',
						amount=amount,
						transdate=fdate,
						code=code,				
						merchant=memmerchant,
						customer=customer).save()

					return render_to_response('Ib/cashin_success_co.html',{'company':mybranch,
						'user':varuser,
						'wallet':wallet,
						'amount':amount})

		else:
			return HttpResponseRedirect('/vts/thrift/payrequest/')


	else:
		return HttpResponseRedirect('/login/user/')



def source(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,thrift,month,account=acccode.split(':')
    		if acccode== '-----':
    			msg = 'Select funding source'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})
    		elif acccode=='Cash':
    			myform = thriftamountform()
    			return render_to_response('Ib/cash.html',{'form':myform,
    				'wallet':wallet,'thrift':thrift,'month':month,'account_type':account})
    		elif acccode=='Transfer':
    			msg = 'This option is coming soon !!!'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')




def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap

@json_view
def autocomplete(request):
    term = request.GET.get('term')
    suggestions = []
    qset = tblthrift.objects.get(account_type = 'Main account',code =8797)#[:10]
    thrift  = 1000
    thrr = 2000
    suggestions.append(thrr)

    # for x in range(1,6):
    # 	thrr = x * thrift
    # 	suggestions.append({'label': '%s :%s :%s :%s ' % (x, thrr), 'number': x,'amount':thrr})
    # 	# suggestions.append({'amount':thrr})
    return suggestions

    # for i in qset:
    #     suggestions.append({'label': '%s :%s :%s :%s ' % (i.admissionno, i.fullname,i.admitted_class,i.admitted_arm), 'admno': i.admissionno,'name':i.fullname,'klass':i.admitted_class,'arm':i.admitted_arm})
    # return suggestions

def statement(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift1b_officer==0:
				return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			mywallet=request.POST['wallet']

			try:
				details=tblCUSTOMER.objects.get(wallet=mywallet,
					branch=mybranch,
					status=1)
				cus=tblIbCUSTOMER.objects.get(customer=details)

				sav1=tblIbsavings_trans.objects.filter(branch=mybranch, customer=cus,wallet_type='Main').exclude(status='Service Charge')



				sav=tblIbsavings_trans.objects.filter(customer=cus,description='CR')
				

				total = account_balance(cus.id)


				if staff.thrift1b_admin==1:

					return render_to_response('Ib/statement_admin_hist.html',{'company':mybranch,
						'user':varuser,
						'amount':sav1,
						'total':total,
					'customer':details,
					'wallet':mywallet})
				
				elif staff.thrift1b_cashier==1:

					return render_to_response('Ib/statement_cash_hist.html',{'company':mybranch,
						'user':varuser,
						'amount':sav1,
						'total':total,
					'customer':details,
					'wallet':mywallet})
					
				
				elif staff.thrift1b_officer==1:
					return render_to_response('Ib/statement_co_hist.html',{'company':mybranch,
						'user':varuser,
						'amount':sav1,
						'total':total,
					'customer':details,
					'wallet':mywallet})

			except:
				msg='INVALID ACCOUNT NUMBER'
				return render_to_response('Ib/selectloan.html',{'msg':msg})

		else:
			msg = ''
			if staff.thrift1b_admin==1:
				return render_to_response('Ib/statement.html',{'company':mybranch,'user':varuser,'msg':msg})
			elif staff.thrift1b_cashier==1:
				return render_to_response('Ib/statement_cash.html',{'company':mybranch,'user':varuser,'msg':msg})
			elif staff.thrift1b_officer==1:
				return render_to_response('Ib/statement_co.html',{'company':mybranch,'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')

def history(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift1b_officer==0:
				return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			mywallet=request.POST['wallet']
			try:
				details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet,
					status=1)

				cus=tblIbCUSTOMER.objects.get(branch=mybranch,customer=details,status=1)

				sav=tblIbsavings_trans.objects.filter(branch=mybranch,
					customer=cus,
					wallet_type='Main',
					status='Available',
					avalability='Available',
					description='CR')


				amount = account_balance(cus.id)


				if staff.thrift1b_admin==1:

					return render_to_response('Ib/adm_ac_bal.html',{'company':mybranch,
						'user':varuser,
						'amount':amount,
					'customer':details,'wallet':mywallet})
				
				elif staff.thrift1b_cashier==1:

					return render_to_response('Ib/acbal_cash.html',{'company':mybranch,
						'user':varuser,
						'amount':amount,
					'customer':details,'wallet':mywallet})
					
				
				elif staff.thrift1b_officer==1:
					return render_to_response('Ib/conthistory.html',{'company':mybranch,
						'user':varuser,
						'amount':amount,
					'customer':details,'wallet':mywallet})
			except:
				msg='INVALID ACCOUNT NUMBER'

		else:
			msg = ''
			if staff.thrift1b_admin==1:
				return render_to_response('Ib/acc_bal_admin.html',{'company':mybranch,'user':varuser,'msg':msg})
			elif staff.thrift1b_cashier==1:
				return render_to_response('Ib/acc_bal_cash.html',{'company':mybranch,'user':varuser,'msg':msg})
			elif staff.thrift1b_officer==1:
				return render_to_response('Ib/acc_bal_co.html',{'company':mybranch,'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')





##########AACTIVITY LOG*******************************************************


def log(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.ceo==0 :
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})
		form=logform()
		if staff.thrift1b_admin==1:
			return render_to_response('Ib/activitlog.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		else:
			msg= 'error!!!'
		return render_to_response('Ib/selectloan.html',{'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



def fillmerchant(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		merchant,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)

    		data=tblIbco.objects.filter(branch=mybranch, status=1)

    		sdic={}
    		kk=[]
    		kk.append('----')
    		for j in data:
    			j = j.id
    			s = {j:j}
    			sdic.update(s)
    			klist = sdic.values()
    		for p in klist:
    			kk.append(p)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')





def fillmerchantb(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		status,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)

    		if status=='-----':
    			msg= 'select status'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

        	mydate = date.today()


        	if status == 'DR':
	        	transaction_source = tblIafieldagent.objects.filter(branch=mybranch,
					status='Received',wallet_type='Main',recdate=mydate)
	        	remm=[]
	        	all_data=[]

	        	for k in transaction_source:
	        		pl=k.merchant.id
	        		all_data.append(pl)

	        	msg=list(dict.fromkeys(all_data)) # remove duplicates from list

	        	for mm in msg:
	        		merchant = tblIaMERCHANT.objects.get(branch=mybranch,id=mm)
	        		transs = tblIafieldagent.objects.filter(branch=mybranch,
						status='Received',merchant=mm, wallet_type='Main',recdate=mydate)
	        		total =transs.aggregate(Sum('amount'))
	        		total=total['amount__sum']
	        		mit = {'merchant':merchant,'trans':transs,'total':total}
	        		remm.append(mit)

	        	return render_to_response('Ia/activitlog_merchant.html',{'company':mybranch,
					'thriftrec':remm,'date':mydate,'status':status})

	        if status == 'WR':
	        	msg = 'not Available'
	      		return render_to_response('Ia/selectloan.html',{'msg':msg})


    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def fillmerchantb(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		status,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)


    		# msg= status return render_to_response('Ia/selectloan.html',{'msg':msg})

    		if status=='-----':
    			msg= 'select status'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})

        	if status == 'DR':
	        	transaction_source = tblIbfieldagent.objects.filter(
	        		branch=mybranch,
					status='Received',wallet_type='Main')
	        	remm=[]
	        	all_data=[]

	        	for k in transaction_source:
	        		pl=k.merchant.id
	        		all_data.append(pl)

	        	msg=list(dict.fromkeys(all_data)) # remove duplicates from list

	        	for mm in msg:
	        		merchant = tblIaMERCHANT.objects.get(branch=mybranch,id=mm)
	        		transs = tblIafieldagent.objects.filter(branch=mybranch,
						status='Received',merchant=mm, wallet_type='Main',recdate=mydate)
	        		total =transs.aggregate(Sum('amount'))
	        		total=total['amount__sum']
	        		mit = {'merchant':merchant,'trans':transs,'total':total}
	        		remm.append(mit)

    			return render_to_response('Ib/activitlog_merchant.html',{
    				'company':mybranch,
    				# 'dates':transdate,
    				# 'merchant':merchant1,
    				# 'total':total,
    				# 'date':mydatwwwe,
    				'ttt':transaction_source})
    		else:
    			msg= 'No transactons found'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')







































def logapprove(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.ceo==0 :
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		form=viewtransform()
		if staff.thrift1b_admin==1:
			return render_to_response('Ib/activitlog_approve.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		else:
			msg= 'error!!!'
		return render_to_response('Ib/selectloan.html',{'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



def fillmerchantappr(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		merchant,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)

    		data=tblIbco.objects.filter(branch=mybranch, status=1)

    		sdic={}
    		kk=[]
    		kk.append('----')
    		for j in data:
    			j = j.id
    			s = {j:j}
    			sdic.update(s)
    			klist = sdic.values()
    		for p in klist:
    			kk.append(p)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def showtrans(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		merchant,transdate,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)


    		if merchant=='----':
    			msg= 'merchant ID'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})


    		if transdate=='':
    			msg= 'select date'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})

        	dday,mday,yday = transdate.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	mydatwwwe=date(yday,mday,dday)

        	merchant1=tblIbco.objects.get(branch=mybranch,id=merchant)
        	mybranch=merchant1.branch.id
        	mybranch=tblBRANCH.objects.get(id=mybranch)
        

    		ddt=[]

    		thriftrec= tblIbMERCHANTbank.objects.filter(
    			branch=mybranch,
    			merchant=merchant1,
				transdate=mydatwwwe,
				wallet_type='Main',
				status='Approved')

    		mycount= thriftrec.count()

    		if mycount >0:
    			add=thriftrec.aggregate(Sum('amount'))
    			add = add['amount__sum']
    			dl={'amount':add}
    			ddt.append(dl['amount'])
    			ddt=ddt[0]

    			return render_to_response('Ib/activitlog_merchant.html',{
    				'company':mybranch,
    				'dates':transdate,
    				'merchant':merchant1,
    				'total':ddt,
    				'date':mydatwwwe,
    				'ttt':thriftrec})

    		else:
    			msg= 'No transactons found'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



###################################****************************************************



##########AACTIVITY LOG*******************************************************





def interestrate(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo==0 :
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		ventry= tblIbinterest.objects.get(branch=mybranch)

		if request.method=='POST':
			form = setinterestform(request.POST)
			if form.is_valid():
				interest=form.cleaned_data['interest']
				duration = form.cleaned_data['duration']

				try:
					old_set = tblIbinterest.objects.get(branch=mybranch)
					msg = 'We found a value already, use the edit menu to change'					
				except:

					k = random.randint(0,9)
					y = random.randint(0,9)
					x = random.randint(0,9)
					z = random.randint(0,9)
					a = random.randint(0,9)
					pin =  str(k) + str(y) + str(x) + str(z)+ str(a)


					tblIbinterest(branch=mybranch,code=pin,interest=interest,duration=duration,status=1).save()
					msg = 'entry saved successfully'
					
				form = setinterestform()

				# return render_to_response('Ib/setinterest.html',{'company':mybranch, 
				# 	'user':varuser,
				# 	'form':form,
				# 	'interest':ventry,
				# 	'msg':msg})


			else:
				msg	= 'Fill up all boxes'
				return render_to_response('Ib/selectloan.html',{'msg':msg})
		else:

			form=setinterestform()

		return render_to_response('Ib/setinterest.html',{'company':mybranch, 
			'user':varuser,
			'form':form,
			'interest':ventry,
			'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def editinterestrate(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo==0 :
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		ventry= tblIbinterest.objects.get(branch=mybranch)
		msg='Click on status to edit values'



		return render_to_response('Ib/editinterest.html',{'company':mybranch, 
			'user':varuser,
			'interest':ventry,
			'msg':msg})


	else:
		return HttpResponseRedirect('/login/user/')





def popedit(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		user = post['userid']
    		

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)


    		ftrec= tblIbinterest.objects.get(
    			branch=mybranch)


    		return render_to_response('Ib/editinterest_pop.html',{'ttt':ftrec})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def changepopedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		if 'status' in request.POST:
			co = request.POST['status']
		else:
			co=0

		interest=request.POST['interest']
		duration=request.POST['duration']

		recc = tblIbinterest.objects.get(branch=mybranch)
		recc.interest=interest
		recc.duration=duration
		recc.save()



		return HttpResponseRedirect('/vts/thrift/interest/edit/')

	else:
		return HttpResponseRedirect('/login/user/')








##**************************************************************************************************8


def unremmitted(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		if staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		form=withdrawform()

		if request.method == 'POST':
			form = withdrawform(request.POST)
			if form.is_valid():
				mystatus=form.cleaned_data['status']
				tdate=form.cleaned_data['date']

				dday,mday,yday = tdate.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				oydate=date(yday,mday,dday)

				# thismonth= calendar.month_name[mday]

				
				approved_c=[]
				notapproved_c=[]
				unap_list=[]

				# thismonth= calendar.month_name[mday]
				# month_name = calendar.month_abbr[2]
				# month_number = list(calendar.month_abbr).index('Feb')


				if mystatus=='Deposit':


##**********************Approved**********************************
					d = tblIbMERCHANTbank.objects.filter(
						branch=mybranch,
						recdate=oydate,
						merchant=memmerchant,
						wallet_type='Main',						
						status='Approved')

					countt=d.count()

					if countt>0:
						add=d.aggregate(Sum('amount'))
						add = add['amount__sum']
						dl={'total':add}
						approved_c.append(dl)

##**********************pending*********************************

					d1 = tblIbfieldagent.objects.filter(
							branch=mybranch,
							wallet_type='Main',
							transdate=oydate,
							status='Received')

					
					countt=d1.count()

					if countt>0:

						for kl in d1:
							stdic = {'customer':kl.customer.customer.surname,
										'amount':kl.amount,
										'status':kl.status}

							unap_list.append(stdic)

						add1=d1.aggregate(Sum('amount'))
						add1 = add1['amount__sum']

					else:
						add1 = 0

######################Cashier*************************************************8
					d2 = tblIbCashier.objects.filter(
							branch=mybranch,
							wallet_type="Main",
							status='',
							remitdate=oydate)

					countr=d2.count()

					if countr>0:

						for ll in d2:
							stdic = {'customer':ll.customer.customer.surname,
										'amount':ll.amount,
										'status':'Not Approved'}

							unap_list.append(stdic)

						add2=d2.aggregate(Sum('amount'))
						add2 = add2['amount__sum']
					else:
						add2 = 0

					add1  = int(add1) + int(add2)

					billdic = {'totalbill': add1 }
					notapproved_c.append(billdic)


					return render_to_response('Ib/merchantpayhistory_others.html',{'company':mybranch, 
						'user':varuser,
						'approved':d,
						'status':'Approved',
						'total':approved_c,
						'form':form,

						'notapproved':unap_list,
						'status2':'Not Approved',
						'total_una':notapproved_c,
						'date':oydate})


				elif mystatus=='withdrawal':
					hk = tblIbsavings_trans.objects.filter(branch=mybranch,
						description='DR',
						wallet_type='Main',
						status='Withdrawn',
						recdate=oydate,
						merchant=memmerchant)

					cout=hk.count()
					withdrwalp=[]

					if cout>0:
						add=hk.aggregate(Sum('amount'))
						add = add['amount__sum']
						yl={'total':add}
						withdrwalp.append(yl)


					return render_to_response('Ib/merchantpayhistory.html',{'company':mybranch, 
						'user':varuser,
						'form':form,
						'thriftrec':hk,
						'status':mystatus})

				elif mystatus== 'All':
				

##**********************Approved**********************************
					d = tblIbMERCHANTbank.objects.filter(
						branch=mybranch,
						recdate=oydate,
						merchant=memmerchant,
						wallet_type='Main',						
						status='Approved')

					countt=d.count()

					if countt>0:
						add=d.aggregate(Sum('amount'))
						add = add['amount__sum']
						dl={'total':add}
						approved_c.append(dl)

##**********************pending*********************************

					d1 = tblIbfieldagent.objects.filter(
							branch=mybranch,
							wallet_type='Main',
							transdate=oydate,
							status='Received')

					
					countt=d1.count()

					if countt>0:

						for kl in d1:
							stdic = {'customer':kl.customer.customer.surname,
										'amount':kl.amount,
										'status':kl.status}

							unap_list.append(stdic)

						add1=d1.aggregate(Sum('amount'))
						add1 = add1['amount__sum']

					else:
						add1 = 0

######################Cashier*************************************************8
					d2 = tblIbCashier.objects.filter(
							branch=mybranch,
							wallet_type="Main",
							status='',
							remitdate=oydate)

					countr=d2.count()

					if countr>0:

						for ll in d2:
							stdic = {'customer':ll.customer.customer.surname,
										'amount':ll.amount,
										'status':'Not Approved'}

							unap_list.append(stdic)

						add2=d2.aggregate(Sum('amount'))
						add2 = add2['amount__sum']
					else:
						add2 = 0

					add1  = int(add1) + int(add2)

					billdic = {'totalbill': add1 }
					notapproved_c.append(billdic)



################total withdrawal *************************
					hk = tblIbsavings_trans.objects.filter(branch=mybranch,
						description='DR',
						wallet_type='Main',
						status='Withdrawn',
						recdate=oydate,
						merchant=memmerchant)

					cout=hk.count()
					withdrwalp=[]

					if cout>0:
						add=hk.aggregate(Sum('amount'))
						add = add['amount__sum']
						yl={'total':add}
						withdrwalp.append(yl)


					return render_to_response('Ib/merchantpayhistory_all.html',{'company':mybranch, 
						'user':varuser,
						'approved':d,
						'status':'Approved',
						'total':approved_c,
						'form':form,

						'notapproved':unap_list,
						'status2':'Not Approved',
						'total_una':notapproved_c,
						'date':oydate,

						'thriftrec':hk,
						'status3':mystatus})


			else :
				msg = 'Fill up all boxes'
				return render_to_response('Ia/selectloan.html',{'msg':msg})


		else:
			 

			if staff.thrift1b_admin==1 :
				return render_to_response('Ib/unremmitted_admin.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def userreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		if staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		form=withdrawform2()

		if request.method == 'POST':
			form = withdrawform2(request.POST)
			if form.is_valid():
				mystatus=form.cleaned_data['status']
				tdate=form.cleaned_data['date']

				dday,mday,yday = tdate.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				oydate=date(yday,mday,dday)

				
				totalbill=[]

				unap_list=[]


				if mystatus == '---' or tdate == '---':
					return HttpResponseRedirect('/thrift/thrift/unremmitted/')

				elif mystatus=='Deposit Requests':

##**********************pending*********************************

					d1 = tblIbfieldagent.objects.filter(
							branch=mybranch,
							wallet_type='Main',
							transdate=oydate,
							merchant=memmerchant,
							status='Received')

					
					countt=d1.count()

					if countt>0:
						status='Not Approved'

						add1=d1.aggregate(Sum('amount'))
						totalbill = add1['amount__sum']


					else:

						status='Approved'

						d1 = tblIbMERCHANTbank.objects.filter(
								branch=mybranch,
								merchant=memmerchant,
								status='Approved',
								wallet_type='Main',
								transdate=oydate)

						countt=d1.count()

						if countt>0:
							status='Approved'

							add1=d1.aggregate(Sum('amount'))
							totalbill = add1['amount__sum']


				elif mystatus=='withdrawal Requests':

					d1 = tblIbpayoutrequest.objects.filter(branch=mybranch,
						wallet_type='Main',
						status='requested',
						recdate=oydate,
						merchant=memmerchant)


					
					countt=d1.count()

					if countt>0:
						status='Not Approved'

						add1=d1.aggregate(Sum('amount'))
						totalbill = add1['amount__sum']


					else:

						status='Approved'

						d1 = tblIbMERCHANTbank.objects.filter(
								branch=mybranch,
								merchant=memmerchant,
								status='Withdrawn',
								wallet_type='Main',
								transdate=oydate)

						countt=d1.count()

						if countt>0:
							status='Approved'

							add1=d1.aggregate(Sum('amount'))
							totalbill = add1['amount__sum']


				if staff.thrift1b_cashier:
					return render_to_response('Ib/depositrequest_cash.html',{'company':mybranch, 
							'user':varuser,
							'status':status,
							'form':form,
							'list':d1,
							'total':totalbill,
							'date':oydate})

				elif staff.thrift1b_officer:

					return render_to_response('Ib/depositrequest_co.html',{'company':mybranch, 
							'user':varuser,
							'status':status,
							'form':form,
							'list':d1,
							'total':totalbill,
							'date':oydate})

				
		else:
			 
			if staff.thrift1b_cashier==1:
				return render_to_response('Ib/unremmitted.html',{'company':mybranch, 'user':varuser,'form':form})

			elif staff.thrift1b_officer==1:
				return render_to_response('Ib/unremmitted_co.html',{'company':mybranch, 'user':varuser,'form':form})
		

	else:
		return HttpResponseRedirect('/login/user/')


def cashout(request): #step 1 walk in customers
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift1b_officer==0:
				return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			withdrw=request.POST['amount']
			charge=request.POST['charge']

			try:
				details=tblCUSTOMER.objects.get(branch=mybranch,wallet=mywallet,
					status=1)
				detailIb=tblIbCUSTOMER.objects.get(customer=details)
				fig = num2words(int(withdrw))
				chg = num2words(int(charge))

				www=detailIb.id 
				bal= account_balance(www)

				leftover = int(bal) - int(withdrw) - int(charge)
				


				if leftover >= 0 :

					if detailIb.withdr_status == 1:							

						return render_to_response('Ib/reqcash.html',{'company':mybranch,
							'user':varuser,
						'customer':detailIb,
						'amount':withdrw,
						'charge':charge,
						'wrd':fig,
						'chg':chg,
						'bal':bal,
						'left':leftover,
						'wallet':mywallet})
					
					else:
						return render_to_response('Ib/reqc_with.html',{'company':mybranch,
								'user':varuser,
							'customer':detailIb,
							'amount':withdrw,
							'charge':charge,
							'wrd':fig,
							'chg':chg,
							'bal':bal,
							'left':leftover,
							'wallet':mywallet})

				else:
					return render_to_response('Ib/no_withdraw.html',{'company':mybranch,
							'user':varuser,
						'customer':detailIb,
						'amount':withdrw,
						'charge':charge,
						'wrd':fig,
						'chg':chg,
						'bal':bal,
						'left':leftover,
						'wallet':mywallet})


			except:
				msg='INVALID ACCOUNT NUMBER'

		else:
			msg = ''

		if staff.thrift1b_admin==1:

			return render_to_response('Ib/cashout.html',{'company':mybranch,
				'user':varuser,
				'msg':msg})

		elif staff.thrift1b_cashier==1:

			msg='Direct all withdrawals to the admin'
			return render_to_response('Ib/selectloan.html',{'msg':msg})
			return render_to_response('Ib/cashout_cashier.html',{'company':mybranch,
				'user':varuser,
				'msg':msg})

		elif staff.thrift1b_officer==1:

			msg='Direct all withdrawals to the admin'
			return render_to_response('Ib/selectloan.html',{'msg':msg})

			return render_to_response('Ib/cashout_officer.html',{'company':mybranch,
				'user':varuser,
				'msg':msg})


	else:
		return HttpResponseRedirect('/login/user/')


def cashoutrequest(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIbco.objects.get(staff=memstaff,status=1,thrift1b=1)
		except:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']
			amount =request.POST['amount']
			charge =request.POST['charge']

			myydate = date.today() #the date the merchant made the request
			myydate=date(myydate.year,myydate.month,myydate.day)


			customer=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,status=1)
			code=customer.code

			Ib = tblIbCUSTOMER.objects.get(customer=customer,status=1)


			if staff.thrift1b_admin==1:

				try:
					savings = tblIbsavings_trans.objects.get(branch=mybranch,
						merchant=memmerchant,
						customer=Ib,
						recdate=myydate,
						amount=amount,
						wallet_type='Main',
						description='DR',
						status='Available',
						avalability='Available')

				except:


					t1= tblIbsavings_trans.objects.filter(branch=mybranch,
						merchant=memmerchant,
						customer=Ib,
						recdate=myydate,
						transdate=myydate,
						amount=amount,
						wallet_type='Main',
						description='DR',
						status='Withdrawn',
						avalability='Not Available')
					
					if t1.count() == 0:
						tblIbsavings_trans(branch=mybranch,
							merchant=memmerchant,
							customer=Ib,
							recdate=myydate,
							transdate=myydate,
							code=code,
							amount=amount,
							wallet_type='Main',
							description='DR',
							status='Withdrawn',
							avalability='Not Available').save()


					t2 = tblIbMERCHANTbank.objects.filter(branch=mybranch,
						status='Withdrawn',
						merchant=memmerchant,
						transdate=myydate,
						wallet_type='Main',
						amount=amount,
						recdate=myydate,
						customer=Ib)

					if t2.count()==0:
						tblIbMERCHANTbank(branch=mybranch,
							status='Withdrawn',
							transdate=myydate,
							merchant=memmerchant,
							code=code,							
							wallet_type='Main',
							amount=amount,
							approved_by=varuser,
							recdate=myydate,
							customer=Ib).save()

					t3= tblIbsavings_trans.objects.filter(branch=mybranch,
						merchant=memmerchant,
						customer=Ib,
						recdate=myydate,
						transdate=myydate,
						amount=charge,
						wallet_type='Main',
						description='DR',
						status='Service Charge',
						avalability='Not Available')

					if t3.count()==0:

						tblIbsavings_trans(branch=mybranch,
							merchant=memmerchant,
							customer=Ib,
							recdate=myydate,
							transdate=myydate,
							amount=charge,
							code=code,
							wallet_type='Main',
							description='DR',
							status='Service Charge',
							avalability='Not Available').save()

					t4 = tblIbMERCHANTbank.objects.filter(branch=mybranch,
							status='Service Charge',
							merchant=memmerchant,
							transdate=myydate,
							wallet_type='Main',
							amount=charge,
							code=code,
							approved_by=varuser,
							recdate=myydate,
							customer=Ib)

					if t4.count()==0:

						tblIbMERCHANTbank(branch=mybranch,
							merchant=memmerchant,
							wallet_type='Main',
							approved_by=varuser,
							transdate=myydate,
							recdate=myydate,
							code=code,
							customer=Ib,
							amount=charge,
							status='Service Charge').save()

				return render_to_response('Ib/payoutsuccess.html',{'company':mybranch, 'user':varuser,'tot':amount,'customer':Ib})#'tot':total})

			elif staff.thrift1b_cashier==1 or staff.thrift1b_officer==1:

				try:
					tblIbpayoutrequest.objects.get(customer=Ib,
						merchant=memmerchant,
						branch=mybranch,
						recdate=myydate,
						amount=amount,
						wallet_type='Main',
						status='Sent')

				except Exception, e:

					tblIbpayoutrequest(customer=Ib,
						merchant=memmerchant,
						branch=mybranch,
						recdate=myydate,
						amount=amount,
						wallet_type='Main',
						status='Sent').save()

			
			if staff.thrift1b_cashier==1:
				return render_to_response('Ib/payoutrequest.html',{'company':mybranch, 'user':varuser,'tot':amount})

			elif  staff.thrift1b_officer==1:
				return render_to_response('Ib/payoutrequestco.html',{'company':mybranch, 'user':varuser,'tot':amount})
	

	else:
		return HttpResponseRedirect('/login/user/')


def individual(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		if staff.thrift1b_cashier==0:
			return render_to_response('Ib/404.html',{'company':mybranch,'user':varuser})

		if request.method == 'POST':
			merchant =request.POST['mercode']
			trandate = request.POST['date']  #Jquery

			try:
				memmerchant=tblIbco.objects.get(id=merchant,
					thrift1b=1,
					status=1,
					branch=mybranch)

			except:

				msg = 'INVALID MERCHANT CODE'
				return render_to_response('Ib/remittals.html',{'company':mybranch, 'user':varuser,'msg':msg})



			if staff.thrift1b_cashier == 1: #if you are a cashier perforing remittals

				ddt=[]
				thriftrec= tblIbcoTrans.objects.filter(
	    			branch=mybranch,
	    			merchant=merchant,
					recdate=trandate)
				mycount= thriftrec.count()


				if mycount >0: ###checks if C/O is a credit officer
					add=thriftrec.aggregate(Sum('amount'))
					add = add['amount__sum']
					dl={'amount':add}
					ddt.append(dl)

					return render_to_response('Ib/remhistory.html',{'company':mybranch,
						'dates':trandate,
	    				'merchant':memmerchant,
	    				'user':varuser,
	    				'thriftrec':ddt,
	    				'date':trandate,
	    				'ttt':thriftrec})

				else:
					msg ='NO TRANSACTION FOUND'

		else:
			msg=''
		return render_to_response('Ib/remittals.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')




def appppprooovennn(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		merchant,trandate=acccode.split(':')

        	merchant1=tblIbco.objects.get(id=merchant,thrift1b=1,status=1)
        	staff_mail=merchant1.staff.email

        	mybranch=merchant1.branch.id

    		ddt=[]

    		sales = tblIbMERCHANTbank.objects.filter(
				branch=mybranch,
				remitted_by=staff_mail,
				recdate = trandate,
				merchant=merchant1,
				status='Remitted')

    		salescount=sales.count()

    		# msg=salescount
    		# return render_to_response('Ib/selectloan.html',{'msg':msg})

    		if salescount >0:

    			add= sales.aggregate(Sum('amount'))
    			add = add['amount__sum']
    			# dl={'amount':add}
    			total=add
    			# ddt.append(dl)

    			return render_to_response('Ib/appall.html',{
    				'company':mybranch,
    				'dates':trandate,
    				'merchant':merchant1,
    				'thriftrec':total,
    				'date':trandate,
    				'ttt':sales})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')




def aproveCO(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		merchant,trandate=acccode.split(':')

        	merchant1=tblIbco.objects.get(id=merchant,thrift1b=1,status=1)
        	staff_mail=merchant1.staff.email

        	mybranch=merchant1.branch.id

    		ddt=[]

    		sales = tblIbcoTrans.objects.filter(
				branch=mybranch,
				merchant=merchant1,
				wallet_type='Main',
				recdate = trandate)

    		salescount=sales.count()

    		# msg=salescount
    		# return render_to_response('Ib/selectloan.html',{'msg':msg})

    		if salescount >0:

    			add= sales.aggregate(Sum('amount'))
    			add = add['amount__sum']
    			# dl={'amount':add}
    			total=add
    			# ddt.append(dl)

    			return render_to_response('Ib/appco.html',{
    				'company':mybranch,
    				'dates':trandate,
    				'merchant':merchant1,
    				'thriftrec':total,
    				'date':trandate,
    				'ttt':sales})
    		else:
    			return HttpResponseRedirect('/vts/thrift/approvalsmenu/')

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')





def approvalsmenu(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.ceo==0 :
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewmerchantform(request.POST)
			if form.is_valid():
				merchant2=form.cleaned_data['merchant']
				mydate=form.cleaned_data['date']


				memmerchant=tblIbco.objects.filter(branch=mybranch, 
					staff=memstaff,
					thrift1b=1, 
					status=1).count() #admin

				if staff.thrift1b_admin==0  or memmerchant<1: #the admin
					return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})
				else:
					memmerchant=tblIbco.objects.get(branch=mybranch, 
						staff=memstaff,
						thrift1b=1, 
						status=1) #field worker


				try:#the merchant
				 	merchanttrans=tblIbco.objects.get(branch=mybranch, thrift1b =1,id=merchant2, status=1)
				except:
				 	msg = ' invalid merchant ID'
				 	return render_to_response('Ib/selectloan.html',{'msg':msg})


				dday,mday,yday=mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				# monthname = calendar.month_name[int(mday)]

				transdate=date(yday,mday,dday)

				remit = tblIbfieldagent.objects.filter(
					branch=mybranch,
					merchant=merchanttrans,
					wallet_type='Main',
					transdate = transdate,
					status='Received')

				count=remit.count()
				# ggt=[]

				if count>0:

					add=remit.aggregate(Sum('amount'))
					add = add['amount__sum']
					add = int(add)

					return render_to_response('Ib/ppp.html',{'company':mybranch,
						'merchant':merchanttrans,
						'user':varuser,
						'thriftrec':remit,
						'dates':transdate,
						'cdate':mydate,
						'total':add,
						})
				else:
					msg ="NO RECORDS FOUND"
					# return render_to_response('Ib/selectloan.html',{'msg':msg})
			else:
				msg ="FILL UP ALL BOXES"
				# return render_to_response('Ib/selectloan.html',{'msg':msg})

		else:
			form=viewmerchantform()
			if staff.thrift1b_admin==1:
				return render_to_response('Ib/approvals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
			else:
				msg= 'error!!!'
		return render_to_response('Ib/selectloan.html',{'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')




def reedit(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		merchant,trandate,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)
    		memmerchant=tblIbco.objects.get(thrift1b =1, staff= staffid ,status=1)

        	dday,mday,yday = trandate.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	mydatwwwe=date(yday,mday,dday)

        	merchant1=tblIbco.objects.get(thrift1b =1,id=merchant,status=1)
        	mybranch=merchant1.branch.id

    		ddt=[]

    		thriftrec= tblIbfieldagent.objects.filter(
    			branch=mybranch,
    			merchant=merchant1,
				transdate=mydatwwwe,
				wallet_type='Main',
				status='Received')

    		mycount= thriftrec.count()

    		if mycount >0:
    			add=thriftrec.aggregate(Sum('amount'))
    			add = add['amount__sum']
    			dl={'amount':add}
    			ddt.append(dl)
    			return render_to_response('Ib/app_all.html',{
    				'company':mybranch,
    				'dates':trandate,
    				'merchant':merchant1,
    				'thriftrec':ddt,
    				'date':mydatwwwe,
    				'ttt':thriftrec})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def seedit(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate,user=acccode.split(':')


        	dday,mday,yday = trandate.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	transdate2=date(yday,mday,dday)


    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)
    		memmerchant=tblIbco.objects.get(thrift1b =1, staff= staffid ,status=1)

    		try:
    			mycom = tblIbfieldagent.objects.get(branch=mybranch, id=state) #details of the trans on merchant tab
    			return render_to_response('Ib/app_trans.html',{'income':mycom,
    				'date1':transdate2,
    				'date':trandate})
    		except :
    			msg='error !!!'
    			return render_to_response('Ib/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def canceloptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate,merchant=acccode.split(':')
    		customer=tblIbfieldagent.objects.get(id=state)

    		return render_to_response('Ib/delsales.html',{'date1':trandate,
    			'trans_id':state,'hhh':customer,'merchant':merchant})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def approvalsmenuyes(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo==0 :
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		merchant2=request.POST['merchant']
		mydate=request.POST['date1']
		trans_id = request.POST['trans_id']
	
	 	merchanttrans=tblIbco.objects.get(branch=mybranch, thrift1b =1,id=merchant2, status=1)

		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)

		try:

			remit = tblIbfieldagent.objects.get( id =trans_id,
				branch=mybranch,
				merchant=merchanttrans,
				wallet_type='Main',
				transdate = transdate,
				status='Received').delete()
		except:
			pass


			###add a delete notification


		remit = tblIbfieldagent.objects.filter( branch=mybranch,
			merchant=merchanttrans,
			wallet_type='Main',
			transdate = transdate,
			status='Received')

		count=remit.count()
		# ggt=[]

		if count>0:

			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render_to_response('Ib/ppp.html',{'company':mybranch,
				'merchant':merchanttrans,
				'user':varuser,
				'thriftrec':remit,
				'dates':transdate,
				'cdate':mydate,
				'total':add,
				})
		else:
			return HttpResponseRedirect('/vts/thrift/approvalsmenu/')

	else:
		return HttpResponseRedirect('/login/user/')



def approveone(request):
    if 'userid' in request.session:
        varuser=request.session['userid']


        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ib/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

        if request.method == 'POST':
        	merchant2=request.POST['merchant']
        	transid = request.POST['trans']
        	cash =request.POST['cash'] #posted
        	amount =request.POST['mmm'] #carry come
        	mydate2=request.POST['date'] #transdate Javascript date object

        	amount=int(amount)
        	cash=int(cash)

        	dday,mday,yday = mydate2.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	mydate=date(yday,mday,dday) #python date object


        	fdate= datetime.today() #record date, the date you took record



        	merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)

        	merchant=tblIbco.objects.get(branch=mybranch,
        		status=1,
        		staff=merchant,
        		thrift1b=1) #admin

        	merchant2=tblIbco.objects.get(branch=mybranch,
        		status=1,
        		id=merchant2) #field agent
 

        	ttt =tblIbfieldagent.objects.get(branch=mybranch, 
        		status='Received',
        		wallet_type="Main",
        		transdate=mydate,
        		merchant=merchant2,
        		id=transid)

        	customer=ttt.customer.id
        	code = ttt.customer.code
        	email=ttt.customer.customer.email



        	customer=tblIbCUSTOMER.objects.get(branch=mybranch, id=customer, status=1)

        
        	wallet=customer.customer.wallet



        	if amount == cash :
        		
        		mont_contribution = tblIbsavings_trans.objects.filter(
        			branch=mybranch,
        			status='Available',
        			customer=customer,
        			amount=amount,
        			avalability='Available',
        			transdate=mydate,  #python date object
        			description='CR',  
        			wallet_type='Main')

        		kdf= mont_contribution.count()

        		if kdf == 0 :
        			tblIbsavings_trans(
        			branch=mybranch,
        			amount=amount,
        			customer=customer, 
        			transdate=mydate,  #python date object
        			description='CR',
        			status='Available',
        			avalability='Available',
        			code=code, 
        			recdate=fdate,
        			merchant=merchant2,
        			wallet_type='Main').save()


        			try:
        				direct_depositIb(email)
        			except:
        				pass

        		ft = tblIbMERCHANTbank.objects.filter(
	        			branch=mybranch,
	        			merchant=merchant2,
	        			customer=customer,
	        			transdate=mydate, 
	        			amount=amount,
	        			wallet_type='Main',
	        			status='Approved')

        		ft = ft.count()

        		if ft == 0:

        			tblIbMERCHANTbank(
	        			branch=mybranch,
	        			merchant=merchant2,
	        			customer=customer,
	        			transdate=mydate, 
	        			amount=amount,
	        			code=code,
	        			recdate=fdate,
	        			approved_by=varuser,
	        			wallet_type='Main',
	        			status='Approved').save()

        		ttt.delete()

        		remit = tblIbfieldagent.objects.filter( branch=mybranch,
					merchant=merchant2,
					wallet_type='Main',
					transdate = mydate,
					status='Received')

        		count=remit.count()


        		if count>0:
        			add=remit.aggregate(Sum('amount'))
        			add = add['amount__sum']
        			add = int(add)

        			return render_to_response('Ib/ppp.html',{'company':mybranch,
						'merchant':merchant2,
						'user':varuser,
						'thriftrec':remit,
						'dates':mydate,
						'cdate':mydate,
						'total':add,
						})

        		else:
					return HttpResponseRedirect('/vts/thrift/approvalsmenu/')

        	else:
				msg = 'amount not applicable'
				return render_to_response('Ib/selectloan.html',{'msg':msg})

        else:
        	return HttpResponseRedirect('/vts/thrift/approvalsmenu/')


    else:
    	return HttpResponseRedirect('/login/user/')



def approvebulkcash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']


        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ib/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.thrift1b_admin==0 :
    		return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
        	amount1 =request.POST['amount'] #carry come
        	mydate2=request.POST['dates'] #Javascript date object
        	credit_officer=request.POST['merchant']
        	mydate22 = request.POST['date']
        	cash =request.POST['cash'] #posted



        	amount1=int(amount1)
        	cash=int(cash)


        	dday,mday,yday = mydate2.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	mydate=date(yday,mday,dday) #python date object

        	fdate= datetime.today() #record date, the date you took record
        	fdate=date(fdate.year,fdate.month,fdate.day)
        	merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)

        	merchant=tblIbco.objects.get(branch=mybranch, staff=merchant,thrift1b=1)


        	merchant2=tblIbco.objects.get(branch=mybranch, id =credit_officer)
      

        	ttt =tblIbfieldagent.objects.filter(branch=mybranch, 
        		status='Received',
        		wallet_type="Main",
        		transdate=mydate,
        		merchant=merchant2)


        	if amount1 == cash :

        		for kp in ttt:
        			customer=kp.customer.id
        			code = kp.customer.code
        			customer=tblIbCUSTOMER.objects.get(branch=mybranch,id=customer,status=1)
        			wallet=customer.customer.wallet
        			amount=kp.amount
        			email= kp.customer.customer.email



	        		mont_contribution = tblIbsavings_trans.objects.filter(
	        			branch=mybranch,
	        			status='Available',
	        			customer=customer,
	        			amount=amount,
	        			avalability='Available',
	        			transdate=mydate,  #python date object
	        			description='CR',  
	        			wallet_type='Main')

	        		kdf= mont_contribution.count()

	        		if kdf == 0 :

	        			tblIbsavings_trans(
	        			branch=mybranch,
	        			amount=amount,
	        			status='Available',
	        			code=code,
	        			avalability='Available',
	        			customer=customer, 
	        			transdate=mydate,  #python date object
	        			description='CR',  
	        			recdate=fdate,
	        			merchant=merchant2,
	        			wallet_type='Main').save()

	        			try:
	        				direct_depositIb(email)
	        			except:
	        				pass


	        		ft = tblIbMERCHANTbank.objects.filter(
		        			branch=mybranch,
		        			merchant=merchant2,
		        			customer=customer,
		        			transdate=mydate, 
		        			amount=amount,
		        			wallet_type='Main',
		        			status='Approved')

	        		ft = ft.count()

	        		if ft == 0 :

	        			tblIbMERCHANTbank(
		        			branch=mybranch,
		        			merchant=merchant2,
		        			customer=customer,
		        			transdate=mydate, 
		        			amount=amount,
		        			code=code,
		        			recdate=fdate,
		        			approved_by=varuser,
		        			wallet_type='Main',
		        			status='Approved').save()

	        		kp.status='Approved'
	        		kp.save()

	        	return render_to_response('Ib/all_app_success.html',{'company':mybranch,'user':varuser,'amount':amount1})


        	else:
        		msg = 'amount not applicable'
        		return render_to_response('Ib/selectloan.html',{'msg':msg})

        else:
        	return HttpResponseRedirect('/vts/thrift/approvalsmenu/')

    else:
    	return HttpResponseRedirect('/login/user/')


def indremitcash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ib/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id

        branch=staff.branch.id

        mycompany=staff.branch.company

        company=mycompany.name
        comp_code=mycompany.id

        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

        if staff.thrift1b_cashier==0:
        	return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


        if request.method == 'POST':
        	merchant=request.POST['merchant'] #Ib merchant id
        	transid = request.POST['trans'] #transaction id
        	cash =request.POST['cash'] #typed in
        	mmm =request.POST['mmm'] #carry come cash
        	mydate2=request.POST['date1'] #Javascript date object
        	uuuser=request.POST['user'] #Javascript date object
        	userr=Userprofile.object.get(email=uuuser,status=1)


        	fdate= datetime.today()
        	remterr=date(fdate.year,fdate.month,fdate.day)

        	ddt5=[]

        	merchanttt=tblIbco.objects.get(id=merchant,status=1,thrift1b=1)

        	if mmm == cash:


        		if userr.thrift1b_admin==1:


	        		try: #assuming that c/o is a merchant
			    		mymy = tblIbcoTrans.objects.get(id=transid)
			    		cid =mymy.customer.id
			    		jjf= tblIbCUSTOMER.objects.get(id=cid,status=1)

		        		mycom = tblIbcoTrans.objects.get(
		        			customer=jjf,
		        			recdate=mydate2,
		        			id=transid)

		        		try:
			    			tblIbMERCHANTbank.objects.get(
			    				branch=mybranch,
			    				recdate=mydate2,
			    				amount=cash,
			    				status='Remitted',
			    				customer = jjf,
			    				wallet_type ='Main',
			    				merchant=merchanttt)
		        		except:

			    			tblIbMERCHANTbank(
			    				branch=mybranch,
			    				recdate=mydate2,
			    				amount=cash,
			    				status='Remitted',
			    				customer = jjf,
			    				wallet_type ='Main',
			    				merchant=merchanttt,
			    				remitted_by = varuser,
			    				rem_date=remterr).save()

			    			mycom.delete()

			    			mymerchant = tblIbMERCHANTbank.objects.get(
			    				branch=mybranch,
			    				recdate=mydate2,
			    				amount=cash,
			    				status='Remitted',
			    				remitted_by = varuser,
			    				customer = jjf,
			    				merchant=merchanttt,
			    				rem_date=remterr,
			    				wallet_type ='Main')

			    			trans_id=mymerchant.id


			    			thriftrec= tblIbcoTrans.objects.filter(
			    				branch=mybranch,
			    				merchant=merchanttt,
			    				recdate=mydate2,
			    				wallet_type='Main')

			    			mycount= thriftrec.count()

			        		if mycount >0:
			        			add=thriftrec.aggregate(Sum('amount'))
			        			add = add['amount__sum']
			        			dl={'amount':add}
			        			ddt5.append(dl)

			        			return render_to_response('Ib/remhistory.html',{'company':mybranch,
			        				'dates':mydate2,'date':mydate2,
			        				'merchant':merchanttt,'user':varuser,
			        				'thriftrec':ddt5,'ttt':thriftrec})


				        	else:
				        		if staff.thrift1b_admin==1:

					        		return render_to_response('Ib/remsuccess_indiv.html',{'company':mybranch,
					        				'cdate':mydate2,
					        				'merchant':merchant,
					        				'transid':trans_id,
					        				'cid':cid,
					        				'user':varuser,
					        				'total':cash})

					        	elif staff.thrift1b_cashier==1:
					        		return render_to_response('Ib/remsuccess_indiv_cashier.html',{'company':mybranch,
					        				'cdate':mydate2,
					        				'merchant':merchant,
					        				'transid':trans_id,
					        				'cid':cid,
					        				'user':varuser,
					        				'total':cash})


	        		except:
	        			return HttpResponseRedirect('/vts/thrift/remittals/')


      		else:
        		return HttpResponseRedirect("/vts/thrift/remittals/")
        else:
        	return HttpResponseRedirect("/vts/thrift/remittals/")


    else:
       	return HttpResponseRedirect('/login/user/')



def remitcash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ib/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

        if staff.thrift1b_cashier==0:
        	return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
            merchant1 =request.POST['merchant']
            cashe1=request.POST['cash']
            amount= request.POST['amount']

            mydate1=request.POST['dates'] #JS date object


            fdate= datetime.today()
            remdate=date(fdate.year,fdate.month,fdate.day)


            merchant=tblIbco.objects.get(id=merchant1,status=1,thrift1b=1)

            
            if cashe1 == amount:
            	thriftrec= tblIbcoTrans.objects.filter(
            		branch=mybranch,
            		merchant=merchant,
            		recdate=mydate1,
            		wallet_type='Main')

            	for k in thriftrec:
            		amount = k.amount
            		customer=k.customer.id
            		customer=tblIbCUSTOMER.objects.get(
            			id=customer,
            			status=1)


            		try:
            			tblIbMERCHANTbank.objects.get(
            				branch=mybranch,
            				recdate=mydate1,
            				amount=amount,
            				customer = customer,
            				status='Remitted',
            				merchant=merchant)

            		except:

            			tblIbMERCHANTbank(
            				branch=mybranch,
            				recdate=mydate1,
            				amount=amount,
            				status='Remitted',
            				remitted_by = varuser,
            				rem_date=remdate,
            				customer = customer,
            				merchant=merchant).save()

            			k.delete()

            	return render_to_response('Ib/remsuccess.html',{
            		'company':mybranch,
            		'merchant':merchant.id,
            		'cdate':mydate1, #js date object
            		'user':varuser,
            		'total':cashe1})

            else:
            	msg = 'The amount you entered is not the correct value'
            	return render_to_response('Ib/remittals.html',{'company':mybranch, 'user':varuser,'msg':msg})
 

        else:
        	return HttpResponseRedirect('/vts/thrift/remittals/')

    else:
        return HttpResponseRedirect('/login/user/')





def approveind(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		if staff.thrift1b_admin==0 and staff.thrift1b_cashier==0 and staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			merchant =request.POST['merchant']
			mydate2=request.POST['cdate']  #JavaScript Date Object
			cid = request.POST['cid']
			amount=request.POST['total']
			transid=request.POST['transid']


			customer = tblIbCUSTOMER.objects.get(id =cid,status=1)
			customer1=customer.id
			mymerchant= tblIbco.objects.get(id=merchant,status=1,thrift1b=1)

			myadmin = tblIbMERCHANTbank.objects.get(id = transid)

			add =myadmin.amount
			remtotal=myadmin.amount

			return render_to_response('Ib/approvalindv.html',{'company':mybranch,
				'merchant':mymerchant,'customer':customer1,
				'user':varuser,'date':mydate2,
				'thriftrec':myadmin, 'trannsid':transid,
				'cdate':mydate2,'total':add,'rem':remtotal})

	else:
		return HttpResponseRedirect('/logout/')


def approveindividualcash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']


        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ib/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.thrift1b_admin==0 and staff.thrift1b_cashier==0 and staff.thrift1b_officer==0:
    		return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
        	merchant =request.POST['merchant'] #the one collecting the money
    		mydate=request.POST['date']
    		customer=request.POST['customer'] #already a database instance
    		amount=request.POST['rem'] #amount remitted
    		transid=request.POST['transid'] #transaction ID


    		merchant=tblIbco.objects.get(status=1,id=merchant,thrift1b=1)

    		remit = tblIbMERCHANTbank.objects.get( id = transid)

    		code=remit.code

    		customer=tblIbCUSTOMER.objects.get(id=customer,status=1)


    		remit.status='Approved'
    		remit.approved_by=varuser
    		remit.save()

    		tblIbsavings_trans(branch=mybranch,
    			customer=customer,
    			description="CR",
    			wallet_type='Main',
    			amount=amount,
    			recdate=mydate,
    			avalability="Available",
    			merchant=merchant).save()

        	return render_to_response('Ib/approve_success.html',{'company':mybranch,'tot':1,'user':varuser})

        else:
            form=remittalform()
        return render_to_response('Ib/remittals.html',{'company':mybranch, 'user':varuser,'form':form})

    else:
        return HttpResponseRedirect('/login/user/')







def all(request):
	if 'userid' in request.session:
		varuser=request.session['userid']



		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		if staff.thrift1b_cashier==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIbco.objects.filter(staff=memstaff,status=1,thrift1b=1)

		if request.method == 'POST':
			form = viewremallform(request.POST)
			if form.is_valid():
				# checkbox =request.POST['checkbox']
				mydate=form.cleaned_data['date']
				yday,mday,dday = mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				ddt=[]

				ddd= dday+1

				for d in xrange(ddd):
					if d == 0:
						pass
					else:
						mydate= date(yday,mday,d)

						for merchant in memmerchant:
							thrifing= tblIbcoTrans.objects.filter(branch=mybranch,
								recdate=mydate,wallet_type='Main',remitted='Unremmitted',merchant=merchant)

							mycount= thrifing.count()

							if mycount >0:
								add=thrifing.aggregate(Sum('amount'))
								add = add['amount__sum']
								dl={'date':mydate,'amount':add,'merchant':merchant,'remitted':'Unremmitted'}
								ddt.append(dl)
							else:
								pass

				return render_to_response('Ib/allrem.html',{'company':mybranch, 'user':varuser,'thriftrec':ddt,'date':mydate})

		else:
			form=viewremallform()
		return render_to_response('Ib/all.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')


def report(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.thrift1b_cashier==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			if form.is_valid():
				status=form.cleaned_data['status']
				date1=form.cleaned_data['date']
				yday,mday,dday = date1.split('/')

				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday)
				month = calendar.month_name[mday]

				allmerchant = tblIbco.objects.filter(branch=mybranch,status=1,thrift1b=1)
				remm=[]
				all_data=[]

				if 'checkbox' in request.POST:
					checkbox=request.POST['checkbox']
				else:
					checkbox=1

				if checkbox==1:
					if status == 'Remitted':
						for k in allmerchant:
							thriftrec= tblIbMERCHANTbank.objects.filter(branch=mybranch,recdate=mydate,merchant=k)
							add=0
							add = thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']
							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)

					elif status == 'Unremmitted':
						for p in allmerchant:
							thriftrec= tblIbcoTrans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=mydate,merchant=p)
							add =0

							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':p,'amount':add}
								remm.append(gh)

					return render_to_response('Ib/remreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'status':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):
						realdate = date(yday,mday,n)
						k =0
						if status=='Remittance':
							for mn in allmerchant:
								thriftrec= tblIbMERCHANTbank.objects.filter(branch=mybranch,
									recdate=realdate,
									merchant=mn)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':mn,'amount':add,'month':realdate}
									remm.append(gh)

							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

						elif status == 'Sales':
							for kl in allmerchant:
								thriftrec= tblIbMERCHANTbank.objects.filter(status='Remitted',
									branch=mybranch,
									merchant=kl,
									wallet_type='Main',									
									recdate=realdate)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)

							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

						elif status == 'All':
							for kl in allmerchant:
								thriftrec= tblIbcoTrans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)
							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

					return render_to_response('Ib/histremreport.html',{'company':mybranch, 'user':varuser,
						'thriftrec':all_data,'month':month,'year':yday,'status':status})

		else:
			form=viewallremittedform()
		return render_to_response('Ib/report.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')







def approvals(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch,'user':varuser})

		if request.method == 'POST':
			form=viewmerchantform(request.POST)
			if form.is_valid():

				merchant_id=form.cleaned_data['merchant']
				mydate=form.cleaned_data['date']

				# merchant_id=request.POST['merchant']
				# mydate=request.POST['date'] #js date object

				try:
					memmerchant=tblIbco.objects.get(id=merchant_id,	thrift1b=1,status=1,branch=mybranch)
					staff_mail = memmerchant.staff.email #take note
					staff_roles=Userprofile.objects.get(email=staff_mail,branch=mybranch,status=1)

				except:
					msg = 'INVALID MERCHANT CODE'
					form=viewmerchantform()
					return render_to_response('Ib/approvals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})


				if staff_roles.thrift1b_cashier==1: #if CO is cashier

					sales = tblIbMERCHANTbank.objects.filter(
						branch=mybranch,
						remitted_by=staff_mail,
						recdate = mydate,
						merchant=memmerchant,
						status='Remitted')

					salescount=sales.count()

					# msg=salescount
					# return render_to_response('Ib/selectloan.html',{'msg':msg})
				

					if salescount >0:

						all_sales=[]

						for k in sales:
							name=k.customer.customer.surname + "   "+k.customer.customer.firstname
							c1=k.customer.id #id on tblibcustomer
							customer=tblIbCUSTOMER.objects.get(id=c1,status=1)

							df={'amount':k.amount,
							'name':name,
							'id': c1}
							all_sales.append(df)

						add=sales.aggregate(Sum('amount'))
						add = add['amount__sum']
						add = int(add)

						totalsales=sales.aggregate(Sum('amount'))
						totalsales = totalsales['amount__sum']
						totalsales = int(totalsales)

					else:
						add = 0
						remtotal = 0
						all_sales=[]
						totalsales=0


					remit = tblIbMERCHANTbank.objects.filter(branch=mybranch,remitted_by=staff_mail,	recdate = mydate,status='Remitted').exclude(merchant=memmerchant)


					remittcount=remit.count()				

					if remittcount > 0:

						allremit=[]

						for k in remit:
							name=k.merchant.staff.surname + "   "+k.merchant.staff.firstname
							merchant=k.merchant.id
							merchant=tblIbco.objects.get(id= merchant,status=1)

							rm={'amount':k.amount,
							'name':name}
							allremit.append(rm)

						add=remit.aggregate(Sum('amount'))
						add = add['amount__sum']
						add = int(add)

						totalrem=remit.aggregate(Sum('amount'))
						totalrem= totalrem['amount__sum']
						totalrem = int(totalrem)
					else:
						add=0
						remtotal=0
						allremit=[]
						totalrem=0

					return render_to_response('Ib/approvalhistory.html',{
						'company':mybranch,
						 'merchant':memmerchant,
						 'user':varuser,
						 'date':mydate,
						 'sales':all_sales,
						 'remit':allremit,
						 'cdate':mydate,
						 'total':add,
						 'rem':totalrem,
						 'totsalr':totalsales})

				

				elif staff_roles.thrift1b_officer==1: #if CO is a C/O

					sales= tblIbcoTrans.objects.filter(
						branch=mybranch,
						merchant=memmerchant,
						wallet_type='Main',
						recdate = mydate)


					kunt = sales.count()



					if kunt > 0 :


						ggt=[]

						for k in sales:
							name=k.customer.customer.surname + "   "+k.customer.customer.firstname
							customer=k.customer.id
							customer=tblIbCUSTOMER.objects.get(id=customer,status=1)



							df={'amount':k.amount,
							'name':name}
							ggt.append(df)

						add=sales.aggregate(Sum('amount'))
						add = add['amount__sum']
						add = int(add)

						return render_to_response('Ib/approvall.html',{	'company':mybranch, 'merchant':memmerchant, 'user':varuser,'date':mydate, 'sales':ggt,'cdate':mydate, 'total':add})
					
					else:
						msg = 'jii'



		else:
			form=viewmerchantform()

		return render_to_response('Ib/approvals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})


	else:
		return HttpResponseRedirect('/login/user/')


def approvecash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ib/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.thrift1b_admin==0:
    		return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
            merchant =request.POST['merchant']

            mydate=request.POST['date'] #JS date object

            amount =request.POST['amount']

            cash=request.POST['cash'] #JS date object


            ddt=[]
            merchant=tblIbco.objects.get(status=1,id=merchant,thrift1b=1)
            
            staff_mail = merchant.staff.email #take note
            staff_roles=Userprofile.objects.get(email=staff_mail,branch=mybranch,status=1)



            if cash==amount:
            	
            	sales = tblIbMERCHANTbank.objects.filter(
	            	branch=mybranch,
	            	status='Remitted',
	            	merchant=merchant,
	            	wallet_type='Main',
	            	remitted_by= staff_mail,
	            	recdate = mydate,
	            	rem_date=mydate)


            	count=sales.count()

            	if count > 0 :

            		for k in sales:
            			amount=k.amount
            			customer=k.customer.id
            			customer=tblIbCUSTOMER.objects.get(id=customer,status=1)

            			try : 
            				tblIbsavings_trans.objects.get(	branch=mybranch,amount=amount,merchant=merchant,customer=customer,recdate=mydate,description='CR',status= 'Available',wallet_type='Main')
            			except :
            				tblIbsavings_trans(branch=mybranch,amount=amount,merchant=merchant,customer=customer,recdate=mydate,	description='CR',status= 'Available',avalability= 'Available',wallet_type='Main').save()

            			k.status='Approved'
            			k.approved_by=varuser
            			k.save()
            		return render_to_response('Ib/apsuccess.html',{'company':mybranch,'tot':count,'user':varuser})

            	else:
           			msg='lo'

            else:
            	
            	msg = 'The amount you entered is not the correct value'
            	form=viewmerchantform()
            	return render_to_response('Ib/approvals.html',{'company':mybranch, 'user':varuser,'msg':msg,'form':form})
            	
				# msg ='lo'
            	# return render_to_response('Ib/selectloan.html',{'msg':msg})

        else:
        	return HttpResponseRedirect("/vts/thrift/remittals/")

    else:
    	return HttpResponseRedirect('/login/user/')


def approveallco(request):
    if 'userid' in request.session:
        varuser=request.session['userid']


        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ib/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.thrift1b_admin==0 and staff.thrift1b_cashier==0 and staff.thrift1b_officer==0:
    		return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
            merchant =request.POST['merchant']

            mydate=request.POST['date'] #JS date object

            amount =request.POST['amount']

            cash=request.POST['cash'] #JS date object


            ddt=[]
            merchant=tblIbco.objects.get(status=1,id=merchant,thrift1b=1)
            
            staff_mail = merchant.staff.email #take note
            staff_roles=Userprofile.objects.get(email=staff_mail,branch=mybranch,status=1)
            
            fdate= datetime.today()
            fdate=date(fdate.year,fdate.month,fdate.day)

            # msg =amount
            # return render_to_response('Ib/selectloan.html',{'msg':msg})


            if cash==amount:
            	
            	sales = tblIbcoTrans.objects.filter(
	            	branch=mybranch,
	            	merchant=merchant,
	            	wallet_type='Main',
	            	recdate = mydate)


            	count=sales.count()

            	if count > 0 :

            		for k in sales:
            			amount=k.amount
            			customer=k.customer.customer.id
            			customer=tblIbCUSTOMER.objects.get(id=customer,status=1)

            			try:
            				ds=tblIbMERCHANTbank.objects.get(status='Approved',branch=mybranch,merchant=merchant,wallet_type='Main',recdate=mydate,customer=customer)
            				
            			except :
            				tblIbMERCHANTbank(status='Approved',branch=mybranch,merchant=merchant,wallet_type='Main',remitted_by=varuser,amount=amount,approved_by=varuser, recdate=mydate,customer=customer,rem_date=fdate).save()

            			try : 
            				tblIbsavings_trans.objects.get(	branch=mybranch,amount=amount,merchant=merchant,customer=customer,recdate=mydate,description='CR',status= 'Available',wallet_type='Main')
            			except :
            				tblIbsavings_trans(branch=mybranch,amount=amount,merchant=merchant,customer=customer,recdate=mydate,	description='CR',status= 'Available',avalability= 'Available',wallet_type='Main').save()


            			k.delete()

            		return render_to_response('Ib/apsuccess.html',{'company':mybranch,'tot':count,'user':varuser})

            	else:
           			msg='lo'
		        	# return HttpResponseRedirect()




            else:
            	
            	msg = 'The amount you entered is not the correct value'
            	form=viewmerchantform()
            	return render_to_response('Ib/approvals.html',{'company':mybranch, 'user':varuser,'msg':msg,'form':form})
            	
				# msg ='lo'
    #         	return render_to_response('Ib/selectloan.html',{'msg':msg})

        else:
        	return HttpResponseRedirect("/vts/thrift/remittals/")

    else:
    	return HttpResponseRedirect('/login/user/')




def allapproval(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		if staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			merchant =request.POST['merchant']
			mydate=request.POST['date']
			yday,mday,dday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			transdate=date(yday,mday,dday)
		else:
			form=viewallremittedform() #allapproval.html changed to all_co
		return render_to_response('Ib/allapproval.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')




#this function is related with the salesss fuction
def approvereport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		admin_staff = tblIbco.objects.get(staff=memstaff,thrift1b=1,status=1)


		if request.method == 'POST':
			form  = form=viewallapprovedform(request.POST)

			
			if form.is_valid():

				status1 =form.cleaned_data['status']
				mydate=form.cleaned_data['date'] #javascript date object


				dday,mday,yday = mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday) #python date object
				realmonth=calendar.month_name[mday]

				allmerchant = tblIbco.objects.filter(branch=mybranch,status=1,thrift1b=1)
				remm=[]
				salessss=[]
				all_data=[]
				notapproved_cg=[]


				if status1=="Approvals":
					tott=0

					status='Approved'
					for k in allmerchant:

		
						thriftrec= tblIbMERCHANTbank.objects.filter(status=status, 
							approved_by=varuser, 
							branch=mybranch,
							recdate=mydate,
							merchant=k)

						add=thriftrec.aggregate(Sum('amount'))
						add = add['amount__sum']
						

						if add > 0:
							tott = add + tott
							gh={'my_merchant':k,'amount':add,'status':'Approved'}
							remm.append(gh)


					return render_to_response('Ib/appreport.html',{'company':mybranch, 'user':varuser,
					'thriftrec':remm,'date':mydate,'status':status,'total':tott})


				elif status1=="Unapprovals":


					tott=0

					status='Unapproved'


					for k in allmerchant:
						email=k.staff.email
		
						cash_rec= tblIbMERCHANTbank.objects.filter(branch=mybranch,
							recdate=mydate,
							status='Remitted',
							remitted_by=email,
							merchant=k.id)

						all_add=cash_rec.aggregate(Sum('amount'))
						all_add= all_add['amount__sum']



						if all_add> 0:

							tott = all_add + tott
							status1= {'stat':'Sales'}
							status1=status1['stat']
							gh={'my_merchant':k,'amount':all_add,'status':status1}
							remm.append(gh)

								

						casho= tblIbMERCHANTbank.objects.filter(branch=mybranch,
							recdate=mydate,
							status='Remitted',
							remitted_by=email).exclude(merchant=k.id)
						

						add3=casho.aggregate(Sum('amount'))
						add3 = add3['amount__sum']


						if add3 > 0 :
							tott = add3 + tott
							status1= {'stat':'Remittance'}
							status1=status1['stat']
							gh={'my_merchant':k,'amount':add3,'status':status1}
							remm.append(gh)


						d2 = tblIbcoTrans.objects.filter(branch=mybranch,
								wallet_type="Main", 
								merchant=k, 
								recdate=mydate)


						add2=d2.aggregate(Sum('amount'))
						add2 = add2['amount__sum']
						

						if add2 > 0:
							tott = add2 + tott
							status2= {'stat':'Sales'}
							status2=status2['stat']
							gh={'my_merchant':k,'amount':add2,'status':status2}
							remm.append(gh)


					return render_to_response('Ib/appreport.html',{'company':mybranch, 'user':varuser,
					'thriftrec':remm,'date':mydate,'status':status,'total':tott})
			
			else :
				msg = 'Fill up all boxes'
				return render_to_response('Ia/selectloan.html',{'msg':msg})


		else:
			form=viewallapprovedform()
			if staff.thrift1b_admin==1:
				return render_to_response('Ib/approvalsreport.html',{'company':mybranch, 'user':varuser,'form':form})
			else:
				msg = 'error!!!'
				return render_to_response('Ib/selectloan.html',{'msg':msg})
	else:
		return HttpResponseRedirect('/login/user/')






def saless_1(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,froom,toto,status= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()

                # dday,mday,yday = dates.split('/') #JSON Dates Object
                # yday=int(yday)
                # mday=int(mday)
                # dday=int(dday)
                # oydate=date(yday,mday,dday)
                # weekday=int(date(yday,mday,dday).isocalendar()[1])
                relmerchant = tblIbco.objects.get(id=ID,status=1)

                if status == 'daily':
                	merc = tblIbMERCHANTbank.objects.filter(merchant=relmerchant,recdate=oydate)
                elif status == 'weekly':
                	merc= tblIbMERCHANTbank.objects.filter(merchant=relmerchant,weekno=weekday)
              
                elif status== 'monthly':
                	merc=tblIbMERCHANTbank.objects.filter(merchant=relmerchant,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('thrift/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')



def daily(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		admin_staff = tblIbco.objects.get(staff=memstaff,thrift1b=1,status=1)


		if request.method == 'POST':
			form=viewallsalesform(request.POST)
			status1 =request.POST['status']
			mydate=request.POST['date'] #javascript date object


			yday,mday,dday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object
			realmonth=calendar.month_name[mday]

			allmerchant = tblIbco.objects.filter(branch=mybranch,status=1,thrift1b=1)
			remm=[]
			all_data=[]

			if 'checkbox'  in request.POST:
				checkbox=request.POST['checkbox']
			else:
				checkbox=1

			if checkbox==1:
				if status1=="Approvals":
					status='Approved'
					for k in allmerchant:

						try:
							thriftrec= tblIbMERCHANTbank.objects.filter(status=status, branch=mybranch,recdate=mydate,merchant=k)
							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)
							else:

								gh={'my_merchant':k,'amount':0}
								remm.append(gh)

						except:
							pass

					return render_to_response('Ib/appreport.html',{'company':mybranch, 'user':varuser,
					'thriftrec':remm,'date':mydate,'status':status})


				elif status1=="Sales":
					status='Approved'

					rer = tblIbMERCHANTbank.objects.filter(merchant=admin_staff,status='Approved',branch=mybranch,wallet_type='Main',approved_by=varuser,recdate=mydate)

					return render_to_response('Ib/appsales.html',{'company':mybranch, 'user':varuser,
						'thriftrec':rer,'date':mydate,'status':status1})


				elif status1=="Unapprovals":
					status='Remitted'

					codet= []
					sumsum=0

					coo = []


					co = tblIbcoTrans.objects.filter(branch=mybranch,
						wallet_type='Main',
						recdate=mydate) #for cos

					jk = co.count()

					if jk >0:


						all_co=[]
						uniq_co= []

						for k in co:
							mm =k.merchant.id
							all_co.append(mm)

							
						[uniq_co.append(x) for x in all_co if x not in uniq_co] #remove dup items



						codkesh=[]
						
						sumsum2=0

						for kk in uniq_co:
							merchant=tblIbco.objects.get(thrift1b=1,
								branch=mybranch,
								status=1,
								id=kk)

	#wehn co is co
							co2 = tblIbcoTrans.objects.filter(branch=mybranch,
								wallet_type='Main',
								recdate=mydate,
								merchant=merchant)

							totco = co2.aggregate(Sum('amount'))
							totco = totco['amount__sum']
							gh={'merchant':merchant,'amount':totco,'date':mydate}
							codet.append(gh)
							sumsum= sumsum + totco

					else:
						codet= []
						codkesh=[]
						sumsum=0
						sumsum2=0

#for cashiers
					
					kkesh = tblIbMERCHANTbank.objects.filter(branch=mybranch,
						wallet_type='Main',
						status=status,
						recdate=mydate) #for cos

					jkg = kkesh.count()

					if jkg >0:


						all_co1=[]
						uniq_co1= []

						for k in kkesh:
							mm =k.merchant.id
							all_co1.append(mm)

							
						[uniq_co1.append(x) for x in all_co1 if x not in uniq_co1] #remove dup items


						codkesh1=[]
						sumsum1=0
						sumsum3=0

						for kk in uniq_co1: #unique cashiers
							merchant=tblIbco.objects.get(thrift1b=1,
								branch=mybranch,
								status=1,
								id=kk)

	#wehn co is co
							cassh = tblIbMERCHANTbank.objects.filter(branch=mybranch,
								wallet_type='Main',
								status=status,
								recdate=mydate,
								merchant=merchant)

							totco1 = cassh.aggregate(Sum('amount'))
							totco1 = totco1['amount__sum']
							gh2={'merchant':merchant,'amount':totco1,'date':mydate}
							codet.append(gh2)
							sumsum= sumsum + totco1

							# msg=codet
							# return render_to_response('Ib/selectloan.html',{'msg':msg})



					else:
						sumsum2=0




					return render_to_response('Ib/unapproved.html',{'company':mybranch,
						'user':varuser,
						'date':mydate,
						'status':status1,
						'co':codet,
						'sum':sumsum,
						})





			else:
				P = (monthrange(yday, mday))[-1]
				for n in range (P,0,-1):
					realdate = date(yday,mday,n)
					k =0
					if status=="Not Approved":
						for kp in allmerchant:
							thriftrec= tblIbMERCHANTbank.objects.filter(status='Remitted', branch=mybranch,recdate=realdate,merchant=kp)
							if thriftrec.count() > 0:
								k = 'fff'
								add=thriftrec.aggregate(Sum('amount'))
								add = add['amount__sum']
								gh={'my_merchant':kp,'amount':add,'date':realdate}
								remm.append(gh)
						if k =='fff':
							datasdict={'remm':remm,'udate':realdate}
							all_data.append(datasdict)

					elif status=="Approved":
						for kpo in allmerchant:
							thriftrec= tblIbMERCHANTbank.objects.filter(status=status, branch=mybranch,recdate=realdate,merchant=kpo)
							if thriftrec.count() > 0:
								k = 'fff'
								add=thriftrec.aggregate(Sum('amount'))
								add = add['amount__sum']
								gh={'my_merchant':kpo,'amount':add,'date':realdate}
								remm.append(gh)
						if k =='fff':
							datasdict={'remm':remm,'udate':realdate}
							all_data.append(datasdict)

				return render_to_response('Ib/monthrep.html',{'company':mybranch, 'user':varuser,
					'thriftrec':all_data,'status':status,'month':realmonth,'year':yday})


		else:
			form=daysalesform()
		return render_to_response('Ib/dailysalesreport.html',{'company':mybranch,
			'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')






def saless(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		admin_staff = tblIbco.objects.get(staff=memstaff,thrift1b=1,status=1)


		if request.method == 'POST':
			form=viewallsalesform(request.POST)
			status1 =request.POST['status']
			mydate=request.POST['date'] #javascript date object


			yday,mday,dday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object
			realmonth=calendar.month_name[mday]

			allmerchant = tblIbco.objects.filter(branch=mybranch,status=1,thrift1b=1)
			remm=[]
			all_data=[]

			if 'checkbox'  in request.POST:
				checkbox=request.POST['checkbox']
			else:
				checkbox=1

			if checkbox==1:
				if status1=="Approvals":
					status='Approved'
					for k in allmerchant:

						try:
							thriftrec= tblIbMERCHANTbank.objects.filter(status=status, branch=mybranch,recdate=mydate,merchant=k)
							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)
							else:

								gh={'my_merchant':k,'amount':0}
								remm.append(gh)

						except:
							pass

					return render_to_response('Ib/appreport.html',{'company':mybranch, 'user':varuser,
					'thriftrec':remm,'date':mydate,'status':status})


				elif status1=="Sales":
					status='Approved'

					rer = tblIbMERCHANTbank.objects.filter(merchant=admin_staff,status='Approved',branch=mybranch,wallet_type='Main',approved_by=varuser,recdate=mydate)

					return render_to_response('Ib/appsales.html',{'company':mybranch, 'user':varuser,
						'thriftrec':rer,'date':mydate,'status':status1})


				elif status1=="Unapprovals":
					status='Remitted'

					codet= []
					sumsum=0

					coo = []


					co = tblIbcoTrans.objects.filter(branch=mybranch,
						wallet_type='Main',
						recdate=mydate) #for cos

					jk = co.count()

					if jk >0:


						all_co=[]
						uniq_co= []

						for k in co:
							mm =k.merchant.id
							all_co.append(mm)

							
						[uniq_co.append(x) for x in all_co if x not in uniq_co] #remove dup items



						codkesh=[]
						
						sumsum2=0

						for kk in uniq_co:
							merchant=tblIbco.objects.get(thrift1b=1,
								branch=mybranch,
								status=1,
								id=kk)

	#wehn co is co
							co2 = tblIbcoTrans.objects.filter(branch=mybranch,
								wallet_type='Main',
								recdate=mydate,
								merchant=merchant)

							totco = co2.aggregate(Sum('amount'))
							totco = totco['amount__sum']
							gh={'merchant':merchant,'amount':totco,'date':mydate}
							codet.append(gh)
							sumsum= sumsum + totco

					else:
						codet= []
						codkesh=[]
						sumsum=0
						sumsum2=0

#for cashiers
					
					kkesh = tblIbMERCHANTbank.objects.filter(branch=mybranch,
						wallet_type='Main',
						status=status,
						recdate=mydate) #for cos

					jkg = kkesh.count()

					if jkg >0:


						all_co1=[]
						uniq_co1= []

						for k in kkesh:
							mm =k.merchant.id
							all_co1.append(mm)

							
						[uniq_co1.append(x) for x in all_co1 if x not in uniq_co1] #remove dup items


						codkesh1=[]
						sumsum1=0
						sumsum3=0

						for kk in uniq_co1: #unique cashiers
							merchant=tblIbco.objects.get(thrift1b=1,
								branch=mybranch,
								status=1,
								id=kk)

	#wehn co is co
							cassh = tblIbMERCHANTbank.objects.filter(branch=mybranch,
								wallet_type='Main',
								status=status,
								recdate=mydate,
								merchant=merchant)

							totco1 = cassh.aggregate(Sum('amount'))
							totco1 = totco1['amount__sum']
							gh2={'merchant':merchant,'amount':totco1,'date':mydate}
							codet.append(gh2)
							sumsum= sumsum + totco1

							# msg=codet
							# return render_to_response('Ib/selectloan.html',{'msg':msg})



					else:
						sumsum2=0




					return render_to_response('Ib/unapproved.html',{'company':mybranch,
						'user':varuser,
						'date':mydate,
						'status':status1,
						'co':codet,
						'sum':sumsum,
						})





			else:
				P = (monthrange(yday, mday))[-1]
				for n in range (P,0,-1):
					realdate = date(yday,mday,n)
					k =0
					if status=="Not Approved":
						for kp in allmerchant:
							thriftrec= tblIbMERCHANTbank.objects.filter(status='Remitted', branch=mybranch,recdate=realdate,merchant=kp)
							if thriftrec.count() > 0:
								k = 'fff'
								add=thriftrec.aggregate(Sum('amount'))
								add = add['amount__sum']
								gh={'my_merchant':kp,'amount':add,'date':realdate}
								remm.append(gh)
						if k =='fff':
							datasdict={'remm':remm,'udate':realdate}
							all_data.append(datasdict)

					elif status=="Approved":
						for kpo in allmerchant:
							thriftrec= tblIbMERCHANTbank.objects.filter(status=status, branch=mybranch,recdate=realdate,merchant=kpo)
							if thriftrec.count() > 0:
								k = 'fff'
								add=thriftrec.aggregate(Sum('amount'))
								add = add['amount__sum']
								gh={'my_merchant':kpo,'amount':add,'date':realdate}
								remm.append(gh)
						if k =='fff':
							datasdict={'remm':remm,'udate':realdate}
							all_data.append(datasdict)

				return render_to_response('Ib/monthrep.html',{'company':mybranch, 'user':varuser,
					'thriftrec':all_data,'status':status,'month':realmonth,'year':yday})


		else:
			form=viewallsalesform()
		return render_to_response('Ib/salesreport.html',{'company':mybranch,
			'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')





def getid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)
    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		allmerchants = tblIbco.objects.filter(branch=branchcode, thrift1b=1, status=1)
    		
    		kk.append('----')
    		for j in allmerchants:
    			j = j.id
    			kk.append(j)
    		
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

		# else:
		# 	gdata = ""
		# 	return render_to_response('index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')





def getstudent(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                h,j = acccode.split(':')
                stlist = []
                
                if term == 'Third':
                    stuk= Student.objects.filter(admitted_session = session,third_term=True,
                        admitted_class = klass,
                        admitted_arm = arm,
                        gone = False)

                    tday = datetime.date.today()
                    if tday.year < 2212:
                        if tblpin.objects.filter(ydate__year = tday.year):
                           gdate = tblpin.objects.get(ydate__year = tday.year)
                           if tday < gdate.ydate:
                              pass
                           else:
                              gpin = gdate.pin
                              gused = gdate.used
                              k = decrypt1(str(gused))
                              uu = encrypt(k)
                              if str(gpin) == str(uu):
                                 pass
                              else:
                                 return HttpResponseRedirect('/sysadmin/page-expire/%s/'%int(tday.year))
                    else:
                         return HttpResponseRedirect('/sysadmin/page-expire/%s/'%int(tday.year))

                if term == 'First':
                    stuk= Student.objects.filter(admitted_session = session,first_term=True,
                        admitted_class = klass,
                        admitted_arm = arm,
                        gone = False)
                
                elif term=='Second':
                    stuk= Student.objects.filter(admitted_session = session,second_term=True,
                        admitted_class = klass,
                        admitted_arm = arm,
                        gone = False)


                data2 = subjectteacher.objects.filter(teachername=varuser,
                    status = 'ACTIVE',
                    klass=klass,
                    arm=arm,
                    term=term,
                    subject=subject,
                    session = session).count()

                # return render_to_response('assessment/selectloan.html',{'msg':data2})

                if data2 > 0: 

                    try:
                        Arm.objects.get(arm=arm)                       

                        for j in stuk:

                            fd=StudentAcademicRecord.objects.filter(student = j,
                                session = session,
                                klass=j.admitted_class,
                                term = term).count()

                            
                            if fd == 1:

                                st = StudentAcademicRecord.objects.get(student = j,
                                    session = session,
                                    term = term)

                                fnh = SubjectScore.objects.filter(academic_rec = st,
                                    klass = klass,
                                    subject = subject,
                                    session = session,
                                    arm=arm,
                                    term =term).count()

                                if fnh==1:

                                    gs = SubjectScore.objects.get(academic_rec = st,
                                        klass = klass,
                                        subject = subject,
                                        session = session,
                                        arm=arm,term =term)
                                    
                                    
                                    kk = {'id':gs.id,
                                    'admissionno':j.admissionno,
                                    'fullname':j.fullname,
                                    'sex':j.sex,
                                    'subject':gs.subject,
                                    'term':str(term),
                                    'first_ca':gs.first_ca,
                                    'second_ca':gs.second_ca,
                                    'third_ca':gs.third_ca,
                                    'fourth_ca':gs.fourth_ca,
                                    'fifth_ca':gs.fifth_ca,
                                    'sixth_ca':gs.sixth_ca,
                                    'klass':gs.klass,                                    
                                    'arm':gs.arm,
                                    'exam_score':gs.end_term_score}
                                    stlist.append(kk)


                                # else:
                                #     msg="I am tired"
                                    # return render_to_response('assessment/selectloan.html',{'msg':msg})
                            # else:
                            #     msg ="No such record"
                                # return render_to_response('assessment/selectloan.html',{'msg':msg})

                    except:
                        for j in stuk:

                            fd=StudentAcademicRecord.objects.filter(student = j,
                                session = session,
                                term = term).count()

                            fnh = SubjectScore.objects.filter(academic_rec = st,
                                klass = klass,
                                subject = subject,
                                session = session,
                                subject_group =arm,
                                term =term).count()

                            
                            if fd == 1:

                                st = StudentAcademicRecord.objects.get(student = j,
                                    session = session,
                                    term = term)


                                if fnh==1:

                                    gs = SubjectScore.objects.get(academic_rec = st,
                                        klass = klass,
                                        subject = subject,
                                        session = session,
                                        subject_group=arm,
                                        term =term)
                                    

                                    kk = {'id':gs.id,
                                    'admissionno':j.admissionno,
                                    'fullname':j.fullname,
                                    'sex':j.sex,
                                    'subject':gs.subject,
                                    'term':str(term),
                                    'first_ca':gs.first_ca,
                                    'second_ca':gs.second_ca,
                                    'third_ca':gs.third_ca,
                                    'fourth_ca':gs.fourth_ca,
                                    'fifth_ca':gs.fifth_ca,
                                    'sixth_ca':gs.sixth_ca,
                                    'klass':gs.klass,
                                    'arm':gs.arm,
                                    'exam_score':gs.end_term_score}
                                    stlist.append(kk)
                                else:
                                    pass
                    if reporttype=='Mid term':
                        # if klass=='JS 1' or klass== 'SS 1':
                        return render_to_response('assessment/mid.html',{'data':stlist,'subject':subject,'term':term,'klass':klass,'arm':arm,'report':reporttype})
                        # else:
                        #     return render_to_response('assessment/ca_first.html',{'data':stlist})
                    elif reporttype=='End term':
                        # if klass=='JS 1' or klass== 'SS 1':
                        return render_to_response('assessment/endterm.html',{'data':stlist,'subject':subject,'term':term,'klass':klass,'arm':arm,'report':reporttype})
                        # else:
                        #     return render_to_response('assessment/ca_first.html',{'data':stlist})

                else:
                    varerr='User not asigned for the term'
                    return render_to_response('assessment/notallowed.html',{'varerr':varerr})

            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')







def payout(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift1b_admin==0 and staff.thrift1b_cashier==0 and staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewmerchantform(request.POST)
			if form.is_valid():
				merchant=form.cleaned_data['merchant']

				datte=form.cleaned_data['date'] #JS date Object
				yday,mday,dday = datte.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				month=calendar.month_name[mday] #month_index to month_name

				mydate=date(yday,mday,dday)

				try:
					memmerchant=tblIbco.objects.get(id=merchant,status=1,branch=mybranch,thrift1b=1)
				except:
					return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})
				ddt=[]
				frf=[]
				allunpaid= tblpayoutrequest.objects.filter(
					merchant=memmerchant,
					branch=mybranch,
					request_date =mydate,
					wallet_type='Main',
					status='Unpaid')

				mycost=[]
				myc=[int(q.customer.id) for q in allunpaid]
				[mycost.append(x) for x in myc if x not in mycost] #removes duplicates in lost

				for kid in mycost:
					customer=tblCUSTOMER.objects.get(id = kid,status=1)

					rtpp = tblpayoutrequest.objects.filter(
						customer=customer,
						request_date=mydate,
						status='Unpaid',
						wallet_type='Main')

					custo=rtpp.aggregate(Sum('amount'))
					custo = custo['amount__sum']

					fd ={'sum':custo,'customer':customer}
					frf.append(fd)

				add = allunpaid.aggregate(Sum('amount'))
				add = add['amount__sum']
				dl={'total':add}
				ddt.append(dl)

				return render_to_response('Ib/adminpayout.html',
					{'total':ddt,
					'company':mybranch,
					'merchant':memmerchant,
					'user':varuser,
					'mydate':mydate,
					'date':datte,
					'thriftrec':frf})
			else:
				msg ='Fill up all boxes'

		else:
			form=viewmerchantform()
			msg=''
			if staff.thrift1b_admin==1:
				return render_to_response('Ib/payout.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
			else:
				msg = 'error!!!'
				return render_to_response('Ib/selectloan.html',{'msg':msg})
	else:
		return HttpResponseRedirect('/login/user/')





def withdrawoptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')
    		customer=tblCUSTOMER.objects.get(id=state)

    		return render_to_response('Ib/adminwithdrawfund.html',{
    			'date1':trandate,
    			'customer':state,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def withdrawfunds(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift1b_admin==0 :
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer_id=request.POST['customer']

			datte=request.POST['date1'] #JS date Object
			yday,mday,dday = datte.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #only useful fo me to know request date

			customer=tblCUSTOMER.objects.get(id=customer_id)
			merchant=customer.merchant.id
			merchant=tblIbco.objects.get(id=merchant,thrift1b=1)


			allreq = tblpayoutrequest.objects.filter(
				status='Unpaid',
				branch=mybranch,
				request_date=mydate,
				customer = customer)

			mycount=allreq.count()

			add=allreq.aggregate(Sum('amount'))
			payable_sum = add['amount__sum']

			account_type_list=[]
			myc=[(str(q.account_type),q.recdate) for q in allreq]
			[account_type_list.append(x) for x in myc if x not in account_type_list] #removes duplicates in lost
			yyu= len(account_type_list)
			t_date= date.today()

			if yyu > 0 :

				for account_type in account_type_list :

					month = str(account_type[1]).split('-')[-2] #month_index
					year = str(account_type[1]).split('-')[0]

					request_item = tblpayoutrequest.objects.filter(
						status='Unpaid',
						branch=mybranch,
						account_type = account_type[0],
						customer = customer,
						wallet_type='Main',
						recdate=account_type[1]).delete()

					transactions = tblthrift_trans.objects.filter(
						branch=mybranch,
						account_type = account_type[0],
						customer=customer,
						wallet_type='Main',
						avalability='Not Available',
						reason='requested',
						recdate=account_type[1],
						merchant=merchant).delete()


					bankk = tblIbMERCHANTbank.objects.filter(
						status= 'Approved',
						branch=mybranch,
						account_type=	account_type[0],
						wallet_type='Main',
						merchant=merchant,
						recdate=account_type[1],
						customer=customer).delete()

				thrift = tblthrift.objects.get(
					account_type = account_type[0],
					branch = mybranch,
					customer=customer,
					number=month,
					year=year)

				thrift_mi=int(thrift.thrift)

				transactions = tblthrift_trans.objects.get(
					account_type = account_type[0],
					wallet_type='Main',
					branch=mybranch,
					recdate__month=month,
					avalability='Not Available',
					reason='Account Maintenance',
					customer=customer,
					merchant=merchant).delete()

				thrift.delete()

				try :
					tblpayoutrecord.objects.get(
						status='Paid',
						branch=mybranch,
						customer=customer,
						account_type=account_type[0],
						paid_by=varuser,
						wallet_type='Main',
						amount=payable_sum,
						recdate= mydate,
						merchant=merchant,
						thrift=thrift_mi)
				except :
					tblpayoutrecord(
						status='Paid',
						branch=mybranch,
						customer=customer,

						account_type=account_type[0],
						paid_by=varuser,
						wallet_type='Main',
						amount=payable_sum,
						paid_date=t_date,
						recdate=mydate,
						merchant=merchant,
						thrift=thrift_mi).save()


				customer=customer.surname +" " + customer.firstname + " " + customer.othername
				return render_to_response('Ib/reqestwithdrawsuccess.html',{
						'company':mybranch,
						'user':varuser,
						'amount':payable_sum,
						'customer':customer})
			else :
				msg = N,payable_sum, 'cash withdrawn'
				return render_to_response('Ib/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/thrift/thrift/payouts/')
	else:
		return HttpResponseRedirect('/login/user/')





def cancelreq(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift1b_admin==0 and staff.thrift1b_cashier==0 and staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer_id=request.POST['customer']
			# account_type=request.POST['account_type']

			datte=request.POST['date1'] #JS date Object
			yday,mday,dday = datte.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object
			month=calendar.month_name[mday]



			customer=tblCUSTOMER.objects.get(id=customer_id)
			merchant=customer.merchant.id
			merchant=tblIbco.objects.get(id=merchant,thrift1b=1)

			allreq = tblpayoutrequest.objects.filter(
				status='Unpaid',
				branch=mybranch,
				request_date=mydate,
				customer = customer)

			add=allreq.aggregate(Sum('amount'))
			payable_sum = add['amount__sum']


			account_type_list=[]
			myc=[(str(q.account_type),q.recdate) for q in allreq]
			[account_type_list.append(x) for x in myc if x not in account_type_list] #removes duplicates in lost
			yyu= len(account_type_list)


			if yyu > 0 :

				for account_type in account_type_list :

					month = str(account_type[1]).split('-')[-2] #month_index
					year = str(account_type[1]).split('-')[0]

					request_item = tblpayoutrequest.objects.filter(
						status='Unpaid',
						branch=mybranch,
						account_type = account_type[0],
						customer = customer,
						wallet_type='Main',
						recdate=account_type[1]).delete()

					transactions = tblthrift_trans.objects.get(
						branch=mybranch,
						account_type = account_type[0],
						customer=customer,
						wallet_type='Main',
						avalability='Not Available',
						reason='requested',
						recdate=account_type[1],
						merchant=merchant)

					transactions.avalability='Available'
					transactions.reason='Available'
					transactions.save()


				customer=customer.surname +" " + customer.firstname + " " + customer.othername
				return render_to_response('Ib/reqestcancel.html',{
						'company':mybranch,
						'user':varuser,
						'amount':payable_sum,
						'customer':customer})
			else:
				return HttpResponseRedirect('/thrift/thrift/payouts/')

	else:
		return HttpResponseRedirect('/login/user/')





def adminpayfund(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift1b_admin==0 and staff.thrift1b_cashier==0 and staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':

			merchant= request.POST['merchant']
			datte=request.POST['date'] #date the request was made

			merchant=tblIbco.objects.get(id=merchant,status=1,thrift1b=1)

			yday,mday,dday = datte.split('/')

			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			mydate=date(yday,mday,dday)

			month=calendar.month_name[mday]

			ddt=[]

			allunpaid= tblpayoutrequest.objects.filter(merchant=merchant,branch=mybranch,recdate=mydate,
				month=month,status='Unpaid') #request by all customers thru the merchant

			mycost=[]
			myc=[int(q.customer.id) for q in allunpaid]
			[mycost.append(x) for x in myc if x not in mycost] #Unique list of customers who request cash

			mycount= len(mycost)


			transactions = tblthrift_trans.objects.filter(
				account_type = 'Main account',
				wallet_type='Main',
				merchant=memmerchant,
				branch=mybranch,
				reason='requested',
				avalability='Available',
				recdate__month=mday)

			code=[]
			for k in allunpaid: #Allunpaid = gross number of requests
				customer=k.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)

				try:
					tblpayoutrecord.objects.get(branch=mybranch,merchant=merchant,customer=customer,recdate=mydate,
						amount=k.amount,status='Paid')
				except:
					tblpayoutrecord(branch=mybranch,merchant=merchant,customer=customer,amount=k.amount,status='Paid',
						recdate=mydate).save()
					code.append(int(k.code))

					k.delete()


			for j in transactions:
				dc=j.code
				customer=j.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)

			 	for k in code:
			 		trans_code = int(k.code)
			 		code.append(trans_code)
			 		if dc==k:
			 			k.reason='Withdrawn'
			 			k.save()
			 			j.delete()

			return render_to_response('Ib/adminpayoutsuccess.html',{'count':mycount,'company':mybranch,'merchant':merchant,'user':varuser})

		else:
			form=viewmerchantform()
		return render_to_response('Ib/payout.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def payoutreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		if staff.thrift1b_officer==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if request.method == 'POST':
			form = payoutform(request.POST)
			if form.is_valid():
				status=form.cleaned_data['status']
				date1=form.cleaned_data['date']
				yday,mday,dday = date1.split('/')

				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday)
				month = calendar.month_name[mday]

				allmerchant = tblIbco.objects.filter(branch=mybranch,status=1,thrift1b=1)
				remm=[]
				all_data=[]

				if 'checkbox' in request.POST:
					checkbox=request.POST['checkbox']
				else:
					checkbox=1

				if checkbox==1:
					if status == 'Paid':
						for k in allmerchant:
							thriftrec= tblpayoutrecord.objects.filter(branch=mybranch,recdate=mydate,merchant=k)
							add=0
							add = thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']
							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)

					elif status == 'Pending':
						for p in allmerchant:
							thriftrec= tblpayoutrequest.objects.filter(month=month,status='Unpaid', branch=mybranch,recdate=mydate,merchant=p)
							add =0

							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':p,'amount':add}
								remm.append(gh)

					return render_to_response('Ib/payoutdayreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'fund':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):
						realdate = date(yday,mday,n)
						k =0
						if status=='Remitted':
							for mn in allmerchant:
								thriftrec= tblIbMERCHANTbank.objects.filter(branch=mybranch,recdate=realdate,merchant=mn)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':mn,'amount':add,'month':realdate}
									remm.append(gh)

							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

						elif status == 'Unremmitted':
							for kl in allmerchant:
								thriftrec= tblIbcoTrans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)
							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)


		else:
			form=payoutform()
		return render_to_response('Ib/payoutreport.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')

#######******** ceo reports *********************
def repome(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		return render_to_response('Ib/reporthome.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')



def merchantreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		if staff.ceo !=1:
			msg='error'
			return render_to_response('Ib/selectloan.html',{'msg':msg, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		form=performanceform()
		return render_to_response('Ib/reportmerchant.html',{'company':mybranch,'form':form, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



def getmereportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                user = post['userid']

                chkstaff = tblSTAFF.objects.get(email=user,status=1)
                bra = chkstaff.branch.id
                bra= tblBRANCH.objects.get(id = bra)

                tuy = tblIbMERCHANTbank.objects.filter(branch=bra,status='Approved')

                
            	addw = tuy.aggregate(Sum('amount'))
            	add = addw['amount__sum']
            	if add < 1:
            		add = 0

                return render_to_response('Ib/dailyreport.html',{'total':add})

            else:
            	return HttpResponseRedirect('vts/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('Ib/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')



def getmereportajaxdate(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                user = post['userid']
                user,fd,td = user.split(':')
                chkstaff = tblSTAFF.objects.get(email=user,status=1)
                bra = chkstaff.branch.id

                to = td
                frm =fd

                if fd =='':
                	fd=date.today()
                if td =='':
                	td=date.today()

                if fd < td:
                	to = fd
                	frm=td

                return render_to_response('Ib/dailyreportdated.html',{
						'to':to,
						 'from' :frm,
						 'detli':selenco(bra,fd,td)})


   	return HttpResponseRedirect('/login/user/')


def cashierreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		if staff.ceo != 1:
			msg = 'error'
			return render_to_response('Ib/selectloan.html',{'msg':msg})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		
		allmerchant=tblIbco.objects.filter(branch=mybranch,thrift1b=1,status=1)


		tdate= date.today()

		if request.method=='POST':
			form = performanceform(request.POST)
			if form.is_valid():
				td=form.cleaned_data['to_date']
				fd =form.cleaned_data['date']

				dday,mday,yday = fd.split('/') #JSON Dates Object
				yday=int(yday)
				fmday=int(mday)
				dday=int(dday)
				fd=date(yday,fmday,dday)
				
				dday,mday,yday = td.split('/') #JSON Dates Object
				yday=int(yday)
				tmday=int(mday)
				dday=int(dday)
				td=date(yday,tmday,dday)


				if fmday <= tmday:
					a = range(fmday,tmday+1)
				else:
					a = range(tmday,fmday+1)


				detli=[]
				toot=0
				
				
				if fd.year== td.year:
					for memmerchant in allmerchant:
						merchant_sales=0
						for k in a: # a is the months covered in the search
							if k == a[0]: #if month is the first month
								if k == a[-1]: #use the boundaries set by the dates
									dddd = td.day								
									tttt = fd.day
									fff=0
									fff= fff + tttt
									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIbMERCHANTbank.objects.filter(branch=mybranch,status='Approved',merchant=memmerchant,wallet_type='Main',recdate=fd1)
										couunt = salees.count()
										if couunt> 0:
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											merchant_sales=add_cr
											toot = toot + add_cr
											df = {'sum':merchant_sales,'details':memmerchant}
											detli.append(df)
										fff += 1 
									
								else: #boundaries = from_date to month end

									fff=0
									fff= fff+ fd.day
									dddd = (monthrange(fd.year, fd.month))[-1]

									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIbMERCHANTbank.objects.filter(branch=mybranch,status='Approved',merchant=memmerchant,wallet_type='Main',recdate=fd1)
										couunt = salees.count()
										if couunt> 0:
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											merchant_sales=add_cr
											toot = toot + add_cr
											df = {'sum':merchant_sales,'details':memmerchant}
											detli.append(df)
										fff += 1 

							else: 
								if k == a[-1]: #boundaries = 1st to to_date
									dddd = td.day
									
									fff=1
									fff += 1
									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIbMERCHANTbank.objects.filter(branch=mybranch,
											status='Approved',
											merchant=memmerchant,wallet_type='Main',
											recdate=fd1)

										couunt = salees.count() 
										if couunt> 0:
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											merchant_sales=add_cr
											toot = toot + add_cr
											df = {'sum':merchant_sales,'details':memmerchant}
											detli.append(df)
										fff += 1 

								else: # loop thru the whole month
						
									fff=0
									fff += 1
									dddd= (monthrange(td.year, k))[-1]
									
									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIbMERCHANTbank.objects.filter(branch=mybranch,
											status='Approved',
											merchant=memmerchant,wallet_type='Main',
											recdate=fd1)

										couunt = salees.count() 
										if couunt> 0:
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											merchant_sales=add_cr
											toot = toot + add_cr
											df = {'sum':merchant_sales,'details':memmerchant}
											detli.append(df)
										fff += 1 



					return render_to_response('Ib/report_performance.html',{'company':mybranch, 
							'user':varuser,'form':form,'toot':toot,
							'to':td, 'from' :fd,'detli':detli})

				else:
					msg = 'Limit your search to same year'
					return render_to_response('Ib/selectloan.html',{'msg':msg})
			else:
				msg = 'fill up '
		
		else:
			form=performanceform()
			msg = ''
			detli=0
			toot=0
		return render_to_response('Ib/report_performance_get.html',{'company':mybranch, 
			'msg':msg,'user':varuser,'form':form,'toot':toot,
			'detli':detli})


	else:
		return HttpResponseRedirect('/login/user/')



def adminreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		
		if staff.ceo !=1:
			msg='error'
			return render_to_response('Ib/selectloan.html',{'msg':msg, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		form = trackform()
		
		return render_to_response('Ib/reportadmin.html',{'company':mybranch, 
			'form':form,
			'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')




def getprofit(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                user = post['userid']

                chkstaff = tblSTAFF.objects.get(email=user,status=1)

                bra = chkstaff.branch.id
                bra= tblBRANCH.objects.get(id = bra)

                tuy = tblIbsavings_trans.objects.filter(branch=bra,
                	status='Service Charge',
                	description='DR',
                	wallet_type='Main',
                	avalability='Not Available')
                	

            	if tuy.count() < 1:
            		add = 0
            	else:
	            	addw = tuy.aggregate(Sum('amount'))
	            	add = addw['amount__sum']

                return render_to_response('Ib/mydailysales.html',{'total':add})

            else:
            	return HttpResponseRedirect('/vts/thrift/reports/sales/admn/')
        else:
        	return render_to_response('Ib/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')


  


def getdateprofit(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                user = post['userid']
                	
                user,fd,td = user.split(':')
                chkstaff = tblSTAFF.objects.get(email=user,status=1)
                bra = chkstaff.branch.id

                to = td
                frm =fd

                if fd =='':
                	fd=date.today()
                if td =='':
                	td=date.today()

                if fd > td:
                	to = fd
                	frm=td

                return render_to_response('Ib/mydailysales_dated.html',{
						'to':to,
						 'from' :frm,
						 'detli':dateprofit(bra,fd,td)})


   	return HttpResponseRedirect('/login/user/')



def unapprovals(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		if staff.ceo != 1:
			msg = 'error'
			return render_to_response('Ib/selectloan.html',{'msg':msg})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		
		allmerchant=tblIbco.objects.filter(branch=mybranch,thrift1b=1,status=1)


		tdate= date.today()

		if request.method=='POST':
			form = trackform(request.POST)
			if form.is_valid():
				td=form.cleaned_data['to_date']
				fd =form.cleaned_data['from_date']

				dday,mday,yday = fd.split('/') #JSON Dates Object
				yday=int(yday)
				fmday=int(mday)
				dday=int(dday)
				fd=date(yday,fmday,dday)
				
				dday,mday,yday = td.split('/') #JSON Dates Object
				yday=int(yday)
				tmday=int(mday)
				dday=int(dday)
				td=date(yday,tmday,dday)


				if fmday <= tmday:
					a = range(fmday,tmday+1)
				else:
					a = range(tmday,fmday+1)


				detli=[]
				toot=0
				
				
				if fd.year== td.year:
					for memmerchant in allmerchant:
						merchant_sales=0
						for k in a: # a is the months covered in the search
							if k == a[0]: #if month is the first month
								if k == a[-1]: #use the boundaries set by the dates
									dddd = td.day								
									tttt = fd.day
									fff=0
									fff= fff + tttt
									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIbfieldagent.objects.filter(branch=mybranch,status='Received',merchant=memmerchant,wallet_type='Main', transdate=fd1)
										couunt = salees.count()
										if couunt> 0: 
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											toot = toot + add_cr
											merchant_sales=merchant_sales + add_cr
										else:
											add_cr = 0
											toot = toot + add_cr
											merchant_sales=merchant_sales + add_cr
										fff += 1								
									msg=''

									df = {'sum':merchant_sales,'details':memmerchant}
									detli.append(df)
									
								else: #boundaries = from_date to month end

									fff=0
									fff= fff+ fd.day
									dddd = (monthrange(fd.year, fd.month))[-1]

									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIbfieldagent.objects.filter(branch=mybranch,status='Received',merchant=memmerchant,wallet_type='Main', transdate=fd1)
										couunt = salees.count()
										if couunt> 0: 
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											toot = toot + add_cr
											merchant_sales=merchant_sales + add_cr
										else:
											add_cr = 0
											toot = toot + add_cr
											merchant_sales=merchant_sales + add_cr
										fff += 1								
									msg=''

									df = {'sum':merchant_sales,'details':memmerchant}
									detli.append(df)

							else: 
								if k == a[-1]: #boundaries = 1st to to_date
									dddd = td.day
									
									fff=1
									fff += 1
									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIbfieldagent.objects.filter(branch=mybranch,status='Received',merchant=memmerchant,wallet_type='Main', transdate=fd1)
										couunt = salees.count() 
										if couunt> 0: 
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											toot = toot + add_cr
											merchant_sales=merchant_sales + add_cr
										else:
											add_cr = 0
											toot = toot + add_cr
											merchant_sales=merchant_sales + add_cr
										fff += 1								
									msg=''

									df = {'sum':merchant_sales,'details':memmerchant}
									detli.append(df)

								else: # loop thru the whole month
						
									fff=0
									fff += 1
									dddd= (monthrange(td.year, k))[-1]
									
									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIbfieldagent.objects.filter(branch=mybranch,status='Received',merchant=memmerchant,wallet_type='Main', transdate=fd1)
										couunt = salees.count() 
										if couunt> 0: 
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											toot = toot + add_cr
											merchant_sales=merchant_sales + add_cr
										else:
											add_cr = 0
											toot = toot + add_cr
											merchant_sales=merchant_sales + add_cr
										fff += 1								
									msg=''

									df = {'sum':merchant_sales,'details':memmerchant}
									detli.append(df)
									


					return render_to_response('Ib/unapprov_red.html',{'company':mybranch, 
							'msg':msg,'user':varuser,'form':form,'toot':toot,
							'to':td, 'from' :fd,'detli':detli})

				else:
					msg = 'Limit your search to same year'
					return render_to_response('Ib/selectloan.html',{'msg':msg})
			else:
				msg = 'fill up '
		
		else:
			form=trackform()
			msg = ''
			detli=0
			toot=0

		return render_to_response('Ib/unapprov_red.html',{'company':mybranch, 
			'msg':msg,'user':varuser,'form':form,'toot':toot,
			'detli':detli})


	else:
		return HttpResponseRedirect('/login/user/')




def clientwithdraw(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		if staff.ceo !=1:
			msg='error'
			return render_to_response('Ib/selectloan.html',{'msg':msg, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		tdate= date.today()

		if request.method=='POST':
			form = performanceform(request.POST)
			if form.is_valid():
				merchant=form.cleaned_data['merchant']
				to_date=form.cleaned_data['to_date']
				datte =form.cleaned_data['date']

				try:
					memmerchant=tblIbco.objects.get(id = merchant, branch =mybranch, status=1,thrift1b=1)
				except:
					return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

				if datte == '':
					fd = tdate
				else:
					fd = form.cleaned_data['date']

					dday,mday,yday = fd.split('/') #JSON Dates Object
					yday=int(yday)
					fmday=int(mday)
					dday=int(dday)
					fd=date(yday,fmday,dday)
					
				if to_date  == '':
					td = tdate
				else:
					td =  form.cleaned_data['to_date']

					dday,mday,yday = td.split('/') #JSON Dates Object
					yday=int(yday)
					tmday=int(mday)
					dday=int(dday)
					td=date(yday,tmday,dday)


				if fmday <= tmday:
					a = range(fmday,tmday+1)
				else:
					a = range(tmday,fmday+1)

				detli=[]
				toot=0
				
				if fd.year== td.year:

					for k in a: 
						if k == a[0]: #if month is the first month

							if k == a[-1]: #use the boundaries set by the dates

								dddd = td.day
								
								tttt = fd.day

								fff=0
								fff= fff + tttt


								while fff <= dddd : 
									fd1=date(yday,k,fff)
									salees = tblIbMERCHANTbank.objects.filter(branch=mybranch,
										status='Approved',
										merchant=memmerchant,
										wallet_type='Main',
										recdate=fd1)

									couunt = salees.count() 
									if couunt> 0: 
										add=salees.aggregate(Sum('amount'))
										add_cr = add['amount__sum']

										toot = toot + add_cr

										df = {'total':add_cr,'details':salees}
										detli.append(df)

									fff += 1
							
								msg=''

							else: #boundaries = from_date to month end 

								# msg = 'im first'
								# return render_to_response('Ib/selectloan.html',{'msg':msg})

								fff=0
								fff= fff+ fd.day

								dddd = (monthrange(fd.year, fd.month))[-1]


								while fff <= dddd : 
									fd1=date(yday,k,fff)
									salees = tblIbMERCHANTbank.objects.filter(branch=mybranch,
										status='Approved',
										merchant=memmerchant,wallet_type='Main',
										recdate=fd1)

									couunt = salees.count() 
									if couunt> 0: 
										add=salees.aggregate(Sum('amount'))
										add_cr = add['amount__sum']

										toot = toot + add_cr

										df = {'total':add_cr,'details':salees}
										detli.append(df)

									fff += 1
							
								msg=''
							
						else: 
							if k == a[-1]: #boundaries = 1st to to_date
								dddd = td.day
								
								fff=1
								fff += 1


								while fff <= dddd : 
									fd1=date(yday,k,fff)
									salees = tblIbMERCHANTbank.objects.filter(branch=mybranch,
										status='Approved',
										merchant=memmerchant,wallet_type='Main',
										recdate=fd1)

									couunt = salees.count() 
									if couunt> 0: 
										add=salees.aggregate(Sum('amount'))
										add_cr = add['amount__sum']

										toot = toot + add_cr

										df = {'total':add_cr,'details':salees}
										detli.append(df)

									fff += 1
							
									msg=''

							else: # loop thru the whole month
					
			
								fff=0
								fff += 1
								dddd= (monthrange(td.year, k))[-1]
								
								while fff <= dddd : 
									fd1=date(yday,k,fff)
									salees = tblIbMERCHANTbank.objects.filter(branch=mybranch,
										status='Approved',
										merchant=memmerchant,wallet_type='Main',
										recdate=fd1)

									couunt = salees.count() 
									if couunt> 0: 
										add=salees.aggregate(Sum('amount'))
										add_cr = add['amount__sum']

										toot = toot + add_cr

										df = {'total':add_cr,'details':salees}
										detli.append(df)

									fff += 1
							
								msg=''

					return render_to_response('Ib/report_performance.html',{'company':mybranch, 
							'msg':msg,'user':varuser,'form':form,'toot':toot,'merchant':merchant,
							'to':to_date, 'from' :datte,'name':memmerchant,
							'detli':detli})
				else:
					msg = 'Limit your search to same year'
					return render_to_response('Ib/selectloan.html',{'msg':msg})



		form = trackform()
		return render_to_response('Ib/withdrw_rep.html',{'company':mybranch, 
			'form':form,
			'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')






def getmerchantid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)
    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		allmerchants = tblIbco.objects.filter(branch=branchcode, status=1,thrift1b=1)

    		for j in allmerchants:
    			j = j.id
    			s = {j:j}
    			sdic.update(s)
    		klist = sdic.values()
    		for p in klist:
    			kk.append(p)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

		# else:
		# 	gdata = ""
		# 	return render_to_response('index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')



def getmerchantname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]
    		data=tblIbco.objects.get(id=acccode,status=1,thrift1b=1)
    		data =data.staff.id
    		data = tblSTAFF.objects.get(id =data)
    		j = data.surname #+ " " + data.firstname+ " " + data.othername
    		kk.append(j)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')
    	else:
    		gdata = ""
    		return render_to_response('index.html',{'gdata':gdata})
    else:
    	return HttpResponseRedirect('/login/user/')



def getmydate113(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,report= acccode.split(':')
                stlist = []

                # relmerchant = tblIbco.objects.get(id=ID,status=1,thrift1b=1)

                if report == '---':
                	msg = 'Choose a report type'
                	return render_to_response('Ib/selectloan.html',{'msg':msg})
                	merc = tblIbMERCHANTbank.objects.filter(merchant=relmerchant,recdate=oydate)
                elif report == 'daily':
                	msg = 'Select date'
                	return render_to_response('Ib/mercdate.html',{'msg':msg})


                elif report== 'weekly' or report== 'monthly':
                	msg = 'Select date'
                	return render_to_response('Ib/monthdate.html',{'msg':msg})


                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('Ib/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('Ib/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')






def getcashreportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,name,dates,report= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()
                # else:
                # 	dates = request.POST['date']

                dday,mday,yday = dates.split('/') #JSON Dates Object
                yday=int(yday)
                mday=int(mday)
                dday=int(dday)
                oydate=date(yday,mday,dday)
                weekday=int(date(yday,mday,dday).isocalendar()[1])

                relcashier = tblSTAFF.objects.get(id=ID)
                relcashier=relcashier.email

                if report == 'Sales':
                	merc = tblIbMERCHANTbank.objects.filter(remitted_by =relcashier,recdate=oydate)
                elif report == 'Approvals':
                	merc= tblIbMERCHANTbank.objects.filter(remitted_by=relcashier,weekno=weekday)

                elif report== 'Unapprovals':
                	merc=tblIbMERCHANTbank.objects.filter(remitted_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('Ib/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('Ib/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')







def clientwithdraw(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		if staff.ceo !=1:
			msg='error'
			return render_to_response('Ib/selectloan.html',{'msg':msg, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		form = trackform()
		return render_to_response('Ib/withdrw_rep.html',{'company':mybranch, 
			'form':form,
			'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')

def getwithdraw(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                user = post['userid']

                chkstaff = tblSTAFF.objects.get(email=user,status=1)
                bra = chkstaff.branch.id
                bra= tblBRANCH.objects.get(id = bra)

                tuy = tblIbsavings_trans.objects.filter(branch=bra,
                	status='Withdrawn',
                	description='DR',
                	wallet_type='Main',
                	avalability='Not Available'
                	)

                
            	addw = tuy.aggregate(Sum('amount'))
            	add = addw['amount__sum']
            	if add < 1:
            		add = 0

                return render_to_response('Ib/withdajax.html',{'total':add})

            else:
            	return HttpResponseRedirect('/vts/thrift/reports/sales/admn/')
        else:
        	return render_to_response('Ib/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')





def getdatewithdraw(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                user = post['userid']

                user,fd,td = user.split(':')
                chkstaff = tblSTAFF.objects.get(email=user,status=1)
                bra = chkstaff.branch.id

                to = td
                frm =fd

                if fd =='':
                	fd=date.today()
                if td =='':
                	td=date.today()

                if fd > td:
                	to = fd
                	frm=td

                return render_to_response('Ib/withdajax_date.html',{
						'to':to,
						 'from' :frm,
						 'detli':datewithdraw(bra,fd,td)})
   		return HttpResponseRedirect('/login/user/')








def switches(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1b=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ib/selectloan.html',{'msg':msg})
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo==0:
				return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = switchesform(request.POST)
			if form.is_valid():
				mymerchant=form.cleaned_data['merchant']

				merch_count = tblIbco.objects.filter(branch=mybranch,status=1,thrift1b=1).count()
				if merch_count> 1:

					try :
						msg = 'Coming soon'
						mmme= tblIbco.objects.get(branch=mybranch,status=1,id=mymerchant,thrift1b=1)
						cus_list = tblCUSTOMER.objects.filter(branch=mybranch,merchant=mmme,status=1)
						if cus_list > 0 :
							form = newswitchform()
							return render_to_response('Ib/switchproc.html',{'company':mybranch,'user':varuser,
								'merchant':mmme,'customer':cus_list,'form':form})
						else :
							msg = 'No customers found'
					except:
						msg = 'Invalid ID'
				else:
					msg='YOU MUST HAVE A MINIMUM OF 2 FIELD WORKERS'
		else:
			form=switchesform()
			msg = ''
		return render_to_response('Ib/switch.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')

def getallstall(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		mrp = tblIbco.objects.get(id=acccode,thrift1b=1)
    		branch=mrp.branch.id
    		branch=tblBRANCH.objects.get(id=branch)
    		merc = tblIbco.objects.filter(branch=branch,status=1,thrift1b=1).exclude(id=acccode)
    		kk=[]
    		kk.append('-----')
    		for jj in merc :
    			gh =  jj.id
    			kk.append(gh)

    		return HttpResponse(json.dumps(kk), mimetype='application/json')

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')

def getbutton(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		if acccode== '-----':
    			return render_to_response('Ib/selmerch.html')

    		else:
    			merchant=tblIbco.objects.get(id=acccode,thrift1b=1)
    			return render_to_response('Ib/switchmerc.html',{'merchant':merchant})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def openoption(request):
    if request.is_ajax():
    	if request.method == 'POST':

    		if 'ggg' in request.POST :
    			a= request.POST['ggg']

	    		# post = request.POST.copy()

	    		# acccode = post['userid']
	    		# if acccode== '-----':
	    		return render_to_response('Ib/selmerch.html',{'sd':a})

    		else:
    			return render_to_response('Ib/switchmerc.html')
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')
















#####LOAN AFFairs*********************




def loanwelcome(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


		return render_to_response('Ib/manager.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/')




def loan_setup(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		loans = tblIbstandardloan.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift1b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			description=request.POST['package']
			rate= request.POST['rate']
			duration=request.POST['duration']

			pack_count=loans.count()

			if pack_count == 0 :
				tblIbstandardloan(rate = 0 ,description='-----', staffrec=user,branch=mybranch,status=1,duration=0).save()
				tblIbstandardloan(rate = rate ,description=description, staffrec=user,branch=mybranch,status=1,duration=duration).save()
			else:
				tblIbstandardloan(rate = rate ,description=description, staffrec=user,branch=mybranch,status=1,duration=duration).save()
			msg = "package added successfully"
			return render_to_response('Ib/addpackage.html',{'company':mybranch, 'user':varuser,'msg':msg})

		return render_to_response('Ib/set_uploan.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/')





def setgrace(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		return render_to_response('Ib/setgrace.html',{'company':mybranch, 'user':varuser})
	else :
		return HttpResponseRedirect('/login/')


def ajaxsetgrace(request):
	if  "userid" in request.session:
		if request.is_ajax():
			if request.method == 'POST':
				post = request.POST.copy()
				acccode = post['userid']

				email,plan = acccode.split(':')
		
				staff = Userprofile.objects.get(email=email,status=1)
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompay=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


				if plan == '-----':
					msg='Select repayment plan'
					return render_to_response('Ib/selectloan.html',{'msg':msg})

				# msg=plan 
				# return render_to_response('Ib/selectloan.html',{'msg':msg})

				if plan == 'day(s)':
					rplan = 'daily'

				elif plan == 'week(s)':
					rplan= 'weekly'

				try:
					grace = tblIbgrace.objects.get(branch=mybranch,plan = rplan)
					return render_to_response('Ib/getgrace.html',{'msg':grace})
				except:
					return render_to_response('Ib/plan.html',{'user':email,'plan':plan})

	else:
		return HttpResponseRedirect('/login/')


def addgrace(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST':
			plan = request.POST['plan']
			grace = request.POST['grace']


			if plan == 'day(s)':
				rplan = 'daily'

			elif plan == 'week(s)':
				rplan= 'weekly'


			try:
				tblIbgrace.objects.get(branch=mybranch,plan=rplan,grace=grace)
			except:
				tblIbgrace(branch=mybranch,plan=rplan,grace=grace,status=1).save()

			return render_to_response('Ib/graceset_success.html',{'company':mybranch, 
				'user':varuser,
				'rplan':rplan,
				'dur':grace,'plan':plan})



		return render_to_response('Ib/setgrace.html',{'company':mybranch, 'user':varuser})
	else :
		return HttpResponseRedirect('/login/')



		

def loan_packages(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		loans = tblIbstandardloan.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		return render_to_response('Ib/loanpackages.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/')

def reqloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		form = loanreqform()
		return render_to_response('Ib/req_cash.html',{'company':mybranch,
				'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/')




def getloanpacks(request):
	if  "userid" in request.session:
		if request.is_ajax():
			if request.method == 'POST':
				post = request.POST.copy()
				acccode = post['userid']

				staff = Userprofile.objects.get(email=acccode,status=1)
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompay=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
				t1= tblIbstandardloan.objects.filter(branch=mybranch,status=1)
				sdic={}
				kk=[]
				klist=[]

				for j in t1:
					j = j.description
					s = {j:j}
					sdic.update(s)
					klist = sdic.values()

				for p in klist:
					kk.append(p)
				kk.sort()
			else :
				kk.append('NO LOAN PACKAGES FOUND')
			return HttpResponse(json.dumps(kk), mimetype='application/json')
		else:
			gdata = ""
			return render_to_response('index.html',{'gdata':gdata})



def getrepaypacks(request):
	if  "userid" in request.session:
		if request.is_ajax():
			if request.method == 'POST':
				post = request.POST.copy()
				acccode = post['userid']

				staff = Userprofile.objects.get(email=acccode,status=1)
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompay=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
				t1= tblIbloanrepaymentplan.objects.filter(branch=mybranch,status=1)
				sdic={}
				kk=[]
				klist=[]

				for j in t1:
					j = j.description
					s = {j:j}
					sdic.update(s)
					klist = sdic.values()
				for p in klist:
					kk.append(p)
				kk.sort()
			else :
				kk.append('NO LOAN PACKAGES FOUND')
			return HttpResponse(json.dumps(kk), mimetype='application/json')
		else:
			gdata = ""
			return render_to_response('index.html',{'gdata':gdata})







def loandetails(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,loan,amount,repay,customer=acccode.split(":")

        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

        		

        		if customer== '':
        			msg='enter account number'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})
        		elif amount== '':
        			msg='enter amount'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})
        		elif loan == '-----':
        			msg='select a loan package'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})

        		elif repay == '-----':
        			msg='select a repayment plan'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})
        		

        		else :
        			try:

	        			customer=tblCUSTOMER.objects.get(wallet=customer,branch=mybranch,status=1)
	        			customer=tblIbCUSTOMER.objects.get(customer=customer,status=1)
	        			pending = tblIbloanrequests.objects.filter(branch=mybranch,customer=customer,status='Awaiting Approval')
	        			running = tblIbloanrequests.objects.filter(branch=mybranch,customer=customer,status='Running')
	        		except:
	        			msg = 'invalid account number'
	        			return render_to_response('Ib/selectloan.html',{'msg':msg})

        			wallet=customer.id
        			if pending.count() > 0 :
        				msg='you have a pending loan request, Select history to view'
        				return render_to_response('Ib/selectloan.html',{'msg':msg})

        			if running.count() > 0 :
        				msg='you have a running loan, fresh loans are not applicable at this moment'
        				return render_to_response('Ib/selectloan.html',{'msg':msg})


        			grc = tblIbgrace.objects.filter(branch=mybranch,plan=repay)
        			g_count= grc.count()

    				# msg=g_count
    				# return render_to_response('Ib/selectloan.html',{'msg':msg})


        			if g_count < 1:
        				msg='You havent set up grace period for '+ repay  +'  repayment plan'
        				return render_to_response('Ib/ggg.html',{'msg':msg})


        			det = tblIbstandardloan.objects.get(description=loan, branch=mybranch,status=1)
        			loan_rate = int(det.rate)
        			amount=int(amount)
        			thrift = 0
        			duration = det.duration
        			thrift  = (100 + loan_rate )
        			thrift = thrift / 100
        			thrifty = thrift * amount

        			if repay== 'daily':
        				duration=duration*7
        			
    				thrift=  thrifty / duration

    				bal = account_balance(wallet)
    			


    				thrift=  locale.format("%.2f",thrift,grouping=True)
	    			return render_to_response('Ib/staffbookloan.html',{'email':user,
	    				'repay':repay, 
	    				'amount':amount,
	    				'loan':loan,
	    				'customer':customer,
	    				'repay':repay,
	    				'output':thrifty,
	    				'balance':bal,
	    				'interest':loan_rate,
	    				'duration':duration,
	    				'thrift':thrift})
        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render_to_response('Ib/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/')




def apply(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.thrift1b_admin == 0: # or staff.thrift3b_cashier==0  or staff.thrift3b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		# find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

		if request.method == 'POST':
			thrift=request.POST['thrift']
			amount= request.POST['amount']
			package=request.POST['package']
			customer=request.POST['customer']
			repaying =request.POST['repay']
			output =request.POST['output']

			fdate= datetime.today()
			todayy=date(fdate.year,fdate.month,fdate.day)


			try:
				customer= tblIbCUSTOMER.objects.get(id=customer,branch=mybranch)
			except:
				msg = repaying
				return render_to_response('Ib/selectloan.html',{'msg':msg})

			
			loan_package = tblIbstandardloan.objects.get(description=package, branch=mybranch)

			code = generate_loancode()


			tblIbloanrequests(branch=mybranch,repay=repaying, output=output, customer=customer,package=loan_package,
				volume=amount,status='Awaiting Approval', loancode=code, date= todayy,thrift=thrift).save()


			#********disable withdraw ability***************
			customer.withdr_status=0
			customer.save()


			email = [varuser]

			try:
				sendMailapplyloan(email)
			except:
				pass

			if staff.thrift1b_admin==1:
				return render_to_response('Ib/booking_cashier.html',{'company':mybranch, 'user':varuser,'customer':0})


	else:
		return HttpResponseRedirect('/login/')




def bookloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.thrift1b_admin== 0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = individualform(request.POST)

			if form.is_valid():
				merchant =form.cleaned_data['merchant']
				mydate2=form.cleaned_data['date'] #JavaScript Date Object

		else:
			form=approveform()
			msg=''
		return render_to_response('Ib/bookindividualloan.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def bookloanlog(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.thrift1b_admin== 0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = individualform(request.POST)

			if form.is_valid():
				merchant =form.cleaned_data['merchant']
				mydate2=form.cleaned_data['date'] #JavaScript Date Object

		else:
			form=approveform()
			msg=''
		return render_to_response('Ib/bookloanlog.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')

def withdrawoptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		# state,trandate=acccode.split(':')
    		customer=tblIbCUSTOMER.objects.get(id=acccode)

    		return render_to_response('Ib/approve_opt.html',{
    			# 'date1':trandate,
    			'customer':acccode,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')


def yesapprovaloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		
		f= datetime.today()
		dd= date(f.year,f.month,f.day)

		newmonth =f.month

		p = (monthrange(f.year, newmonth))[-1] #no of dys in the month
		




		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer2 =request.POST['staff']

			customer=tblIbCUSTOMER.objects.get(id=customer2)

		 	details = tblIbloanrequests.objects.get(customer=customer,status='Awaiting Approval',branch=mybranch)
		 	loancode=details.loancode

		 	email=details.customer.customer.email
		 	email=[email]

		 	thrift=details.thrift
		 	duration= int(details.package.duration)
		 	output=float(details.output)

			my_stat= tblIbgrace.objects.get(branch=mybranch,plan=details.repay)

			grace=my_stat.grace

			step=0



			duration=(duration * 7)  + grace +f.day

		 	if details.repay =='daily':

		 		start = f.day + grace

		 		step += 1	

		 	elif details.repay=='weekly':

		 		start = f.day + (grace * 7)
		 		
		 		step += 7		


		 	volume=details.volume
	

		 	trans = tblIbloantransaction.objects.filter(transaction_source=details, loancode =loancode, status='DR',thrift=output)
		 	trans_count= trans.count()

		 	if trans_count== 0 :

		 		for k in range(start,duration,step):
		 			p = (monthrange(f.year, newmonth))[-1]
		 			if start <= p:
		 				datte=  date(f.year,newmonth,start)
		 			else:
		 				start = start - p
		 				newmonth += 1
		 				datte =  date(f.year,newmonth,start)

		 			start = start + step

		 			tblIbloantransaction(branch=mybranch, loancode=loancode, transaction_source=details,start_date=datte, status='DR', thrift=thrift).save()

				 
				details = tblIbloanrequests.objects.filter(customer=customer).update(status='Running')
				
				
			 	try:
			 		sendMailapproveloan(email)
			 	except:
			 		pass

			# details2 = tblIbloanrequests.objects.filter(branch=mybranch,date__month=month,status='Not Approved')
			# ccc = details2.count()
			
			# if ccc>0:
			# 	return HttpResponseRedirect('/vts/threeb/loans/approve/')
			# else:

			return render_to_response('Ib/approve_success.html',{'company':mybranch, 'user':varuser,'sum':volume,'customer':customer})
		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/')


def decoptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		# state,trandate=acccode.split(':')
    		customer=tblIbCUSTOMER.objects.get(id=acccode)

    		return render_to_response('Ib/decline.html',{
    			# 'date1':trandate,
    			'customer':acccode,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')



def yesdeclineloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		f= datetime.today()



		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer =request.POST['staff']
			customer=tblIbCUSTOMER.objects.get(id=customer)

			try:

			 	details = tblIbloanrequests.objects.get(customer=customer,
			 		status='Awaiting Approval',
			 		branch=mybranch)

			 	details.status='Declined'
			 	details.save()
			 	customer.withdr_status=1
			 	customer.save()
			 	
			 	email=details.customer.customer.email
			 	email=[email]

			 	try:
			 		sendMaildeclineloan(email)
			 	except:
			 		pass


		 	except:
		 		p=0


			return render_to_response('Ib/dec_success.html',{'company':mybranch, 'user':varuser,'customer':customer})
		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/')


def loanscene(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,status,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		if status=='-----':
        			msg='Select loan Status'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})

        		if month=='-':
        			msg='Select valid Month'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})



        		month=int(month)
        		monthnam = calendar.month_name[month]

        		if status=='Pending' :
        			status='Awaiting Approval'
        			scsenario = tblIbloanrequests.objects.filter(branch=mybranch,date__month=month,status=status)
        			return render_to_response('Ib/scenario.html',{'email':user,'msg':scsenario,'status':status, 'month':monthnam})
        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render_to_response('lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/')




def apploanlog(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,status,mdate=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		if status=='-----':
        			msg='Select loan Status'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})

        		if mdate=='':
        			msg='Select date'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})



        		d,m,y = mdate.split('/')

        		d=int(d)
        		m=int(m)
        		y=int(y)


        		md = date(y,m,d)


        		if status=='application' :
        			status='Awaiting Approval'

        		if status=='Approval' :
        			status='Running'

        		if status=='decline' :
        			status='Declined'

    			scsenario = tblIbloanrequests.objects.filter(branch=mybranch,date=md,status=status)
    			return render_to_response('Ib/apploanlog.html',{'email':user,'msg':scsenario,'status':status,'date':md})
    	

        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render_to_response('lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/')




def loanscenelog(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,status,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		if status=='-----':
        			msg='Select loan Status'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})

        		if month=='-':
        			msg='Select valid Month'
        			return render_to_response('Ib/selectloan.html',{'msg':msg})



        		month=int(month)
        		monthnam = calendar.month_name[month]

        		if status=='All' :
        			scsenario = tblIbloanrequests.objects.filter(branch=mybranch,date__month=month)
        			return render_to_response('Ib/application.html',{'email':user,'msg':scsenario,'status':status, 'month':monthnam})

        		elif status=='Approved':
        			status='Repaid'
        			scsenario = tblIbloanrequests.objects.filter(branch=mybranch,date__month=month,status=status)
        			return render_to_response('Ib/app_decl.html',{'email':user,'msg':scsenario,'status':status, 'month':monthnam})


        		else :
        			status='Awaiting Approval'
        			scsenario = tblIbloanrequests.objects.filter(branch=mybranch,date__month=month,status=status)
        			return render_to_response('Ib/scenariolog.html',{'email':user,'msg':scsenario,'status':status, 'month':monthnam})
        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render_to_response('Ib/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/')






def repay(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


		if staff.thrift1b_admin ==0:
				return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			wallet=request.POST['wallet']
			p=[]

			try :
				memstaff = tblCUSTOMER.objects.get(branch=mybranch,wallet =wallet, status=1)
				memstaff = tblIbCUSTOMER.objects.get(branch=mybranch,customer=memstaff, status=1)

				lln=tblIbloanrequests.objects.get(customer=memstaff,branch=mybranch,
					status='Running')

				thrift=lln.thrift
				total = lln.output

				ltrans = tblIbloantransaction.objects.filter(transaction_source=lln, status='CR')

				summ = ltrans.aggregate(Sum('thrift'))
				repaid = summ['thrift__sum']

				if ltrans.count()< 1:
					balance= float(total)
					repaid=0.00
				else:
					balance= float(total) - repaid

				return render_to_response('Ib/repay_hist.html',{'name':memstaff,
					'wallet':wallet,
					'company':mybranch,
					'user':varuser,
					'total':total,
					'repaid':repaid,
					'balance':balance,
					'thrift':thrift})

			except:

				msg='no records found'

				return render_to_response('Ib/selectloan.html',{'msg':msg})

		else:
			msg = ''
			return render_to_response('Ib/repay1.html',{'company':mybranch,'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')




def yesrepayloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		f= datetime.today().date()

		staffy=tblSTAFF.objects.get(email=varuser,branch=mybranch)

		merchant=tblIbco.objects.get(staff=staffy)


		if staff.thrift1b_admin==0:
			return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet  = request.POST['customer']
			amount = request.POST['amount']
			# balance = request.POST['balance']			

			memstaff = tblCUSTOMER.objects.get(branch=mybranch,wallet =wallet, status=1)
			memstaff = tblIbCUSTOMER.objects.get(branch=mybranch,customer=memstaff, status=1)

			myloan=tblIbloanrequests.objects.get(branch=mybranch,customer=memstaff,status='Running')


			loancode=myloan.loancode
			thrift= myloan.thrift
			thrift=float(thrift)
			amount=int(amount)
			balance2=float(myloan.output)


			done=0

			if amount  < thrift:
				msg = 'This amount is unapplicable'
				return render_to_response('Ib/selectloan.html',{'msg':msg})

			my_balance= tblIbloantransaction.objects.filter(branch=mybranch, transaction_source=myloan,status='CR')#.exclude(status='DR')
			bal_count = my_balance.count()


			if bal_count>0:
				repaid=my_balance.aggregate(Sum('thrift'))
				repaid=float(repaid['thrift__sum'])
			else:
				repaid=0.0

			original_balance = balance2 - repaid


			vlump=0
			pkm=0



			if amount == original_balance:
				vlump=balance2
				pkm = 0.00
				done = 2
				# msg = 'loan completely repaid'
			
			elif amount < original_balance:
				vlump,pkm=divmod(amount,thrift)
				vlump=vlump*thrift
				done = 1
				msg=''

			elif amount > original_balance:
				vlump,pkm=divmod(amount,thrift)
				vlump=vlump*thrift
				done = 2
				# msg=''


			tblIbloantransaction(branch=mybranch, status="CR", loancode= loancode,transaction_source=myloan,start_date=f,thrift=vlump).save()

			if done == 2:
				msg = 'loan completely repaid'

				ght = tblIbloanrequests.objects.filter(branch=mybranch,customer=memstaff ,status='Running').update(status='Repaid')
				
				memstaff.withdr_status=1
				memstaff.save()

			if pkm > 0.0:

				tblIbsavings_trans(branch=mybranch,
					transdate=f, 
					description='CR', 
					wallet_type='Main', 
					amount=pkm, 
					recdate=f,
					channel='LRE',
					avalability='Available',
					code =990,
					merchant=merchant,
					customer=memstaff,
					status='Available').save()

			# done = balance2,amount


			return render_to_response('Ib/repay_success.html',{'company':mybranch,
				'user':varuser,
				'done':msg,
				'savings':pkm,
				'loan':vlump})


###Email Notifications **********************************
			 # sendMailrepayloan(email,mmonth,y)


		else:
			return HttpResponseRedirect('/vts/threeb/staff/repay_loan/')

	else:
		return HttpResponseRedirect('/login/')



def loanperformance(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


		if staff.thrift1b_admin ==0:
				return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST':
			customer=request.POST['wallet']

			try:
				customer=tblCUSTOMER.objects.get(wallet=customer,branch=mybranch)
				customer=tblIbCUSTOMER.objects.get(customer=customer,status=1)
			
			except:
				msg = 'check the account number'
				return render_to_response('Ib/selectloan.html',{'msg':msg})
				

			try:

				transactions= tblIbloanrequests.objects.get(branch=mybranch,status='Running',customer=customer)


				loan_list = tblIbloantransaction.objects.filter(branch=mybranch,transaction_source=transactions).exclude(status='DR')
				

				total =transactions.output


				if loan_list.count()> 0:
					repaid = loan_list.aggregate(Sum('thrift'))
					repaid=float(repaid['thrift__sum'])
				else:
					repaid=0.0

				balance= float(total) - repaid

				return render_to_response('Ib/loanperf.html',{'company':mybranch,
						'user':varuser,
						'total':total,
						'repaid':repaid,
						'balance':balance,
						'list':loan_list})

			except:
				msg = 'check the account number'
				return render_to_response('Ib/selectloan.html',{'msg':msg})



		else:
			msg = ''
			return render_to_response('Ib/loanperf_admin.html',{'company':mybranch,'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')






def loanhistory(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


		if staff.thrift1b_admin ==0:
				return render_to_response('Ib/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST':
			customer=request.POST['wallet']

			try:
				customer=tblCUSTOMER.objects.get(wallet=customer,branch=mybranch)
				customer=tblIbCUSTOMER.objects.get(customer=customer,status=1)
				loan_list = tblIbloanrequests.objects.filter(branch=mybranch,customer=customer)
			
				return render_to_response('Ib/loandetails.html',{'company':mybranch,
						'user':varuser,'list':loan_list})


			except:
				msg = 'check the account number'
				return render_to_response('Ib/selectloan.html',{'msg':msg})



		else:
			msg = ''
			form =viewremallform()
			return render_to_response('Ib/loanhist.html',{'company':mybranch,'user':varuser,'msg':msg,'form':form})

	else:
		return HttpResponseRedirect('/login/')


	






