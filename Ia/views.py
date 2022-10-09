from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json


from thriftplus.settings import EMAIL_HOST_USER

from django.core.mail import send_mail


from sysadmin.models import *
from customer.models import *
from merchant.models import *
from savings.models import *


from Ia.models import *
from Ia.utils import *
from Ia.forms import *

from num2words import num2words
from datetime import *
import calendar

#######import only merchant.models******
from calendar import monthrange


from django.db.models import Max,Sum

import random
import datetime




def welcome(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('Ia/welcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



def admindash(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.admin==0 and staff.cashier==0 and staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		else :
			# return render_to_response('Ia/adminwelcome.html',{'company':mybranch, 'user':varuser})
			return render_to_response('Ia/dashboardIa.html',{'company':mybranch, 'user':varuser,'pincode':staff})


	else:
		return HttpResponseRedirect('/login/user/')


def adminuserguide(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==1:
			return render_to_response('Ia/adminwelcome.html',{'company':mybranch, 'user':varuser})
		elif staff.cashier ==1:
			return render_to_response('Ia/cashwel.html',{'company':mybranch, 'user':varuser})
		elif staff.thrift_officer==1:
			return render_to_response('Ia/mercwell.html',{'company':mybranch, 'user':varuser})
		else:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')





def subscribe_cus(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})



		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,thrift1a=1, status=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)

		msg = ''

		if request.method == 'POST':
			acname=request.POST['acno']

			try:

				countt=tblCUSTOMER.objects.get(branch=mybranch, wallet=acname,status=1)

				try:
					cty = tblIaCUSTOMER.objects.get(customer=countt,branch=mybranch)
					msg = "This Customer already subscribed for this service"

					if staff.admin==1:
						return render_to_response('Ia/walletdetails.html',{'company':mybranch, 'user':varuser,'msg':msg,'details':cty})
					elif staff.cashier==1:
						return render_to_response('Ia/walletdetails_cash.html',{'company':mybranch, 'user':varuser,'msg':msg,'details':cty})
					elif staff.thrift_officer==1:
						return render_to_response('Ia/walletdetails_to.html',{'company':mybranch, 'user':varuser,'msg':msg,'details':cty})


				except Exception, e:


					if staff.admin==1:
						return render_to_response('Ia/subscribe_service.html',{'company':mybranch, 	'user':varuser,'details':countt})
					elif staff.cashier==1:
						return render_to_response('Ia/subscribe_service_cash.html',{'company':mybranch, 	'user':varuser,'details':countt})
					elif staff.thrift_officer==1:
						return render_to_response('Ia/subscribe_service_to.html',{'company':mybranch, 	'user':varuser,'details':countt})




			except:
				msg = 'Account number not found'


		else:
			if staff.admin==1:
				return render_to_response('Ia/subscribe.html',{'company':mybranch, 'user':varuser,'msg':msg})
			elif staff.cashier==1:
				return render_to_response('Ia/subscribe_cash.html',{'company':mybranch, 'user':varuser,'msg':msg})
			elif staff.thrift_officer==1:
				return render_to_response('Ia/subscribe_mer.html',{'company':mybranch, 'user':varuser,'msg':msg})



		return render_to_response('Ia/subscribe.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



def cus_list(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,thrift1a=1, status=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)


		if staff.admin:
			cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch)
		else:
			cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch,merchant=memmerchant)


		return render_to_response('Ia/custlist.html',{'company':mybranch, 'user':varuser,'client_list':cutlist})

	else:
		return HttpResponseRedirect('/login/user/')



def depositer(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		vid,user=acccode.split(':')

    		customer =tblIaCUSTOMER.objects.get(id=vid)
    		return render_to_response('Ia/selectloan.html',{'msg':msg})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def gensave(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,thrift1a=1, status=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)

		msg = ''

		if request.method == 'POST':
			customer=request.POST['customer']
			customer= tblCUSTOMER.objects.get(id=customer)
			email=customer.email
			acname=customer.wallet
			pin = customer. code


			try : #if he has been registered b4, not minding who did
				tblIaCUSTOMER.objects.get(
					branch=mybranch,
					customer=customer)
			except:

				tblIaCUSTOMER(code=pin,
					withdr_status=1,
					branch=mybranch,
					customer=customer,
					merchant=memmerchant,
					status=1,
					get_email=1).save()
				
				customer.dc=1
				customer.save()

				try:
					customer_activationIa(email)
				except:
					pass

				#configure email after activation forservice

				if staff.admin==1:
					return render_to_response('Ia/success.html',{'company':mybranch,'user':varuser,'wallet':acname })
				elif staff.cashier==1:
					return render_to_response('Ia/success_cash.html',{'company':mybranch,'user':varuser,'wallet':acname })
				elif staff.thrift_officer==1:
					return render_to_response('Ia/success_to.html',{'company':mybranch,'user':varuser,'wallet':acname })


		return HttpResponseRedirect('/fts/thrift/newsub/')

	else:
		return HttpResponseRedirect('/login/user/')





				### ****************************THRIFT AFFAIRS*************************


def addthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,status=1, thrift1a=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)


		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		monthname = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			

			if form.is_valid():
				mywallet=form.cleaned_data['wallet']

				try:
					details=tblCUSTOMER.objects.get(branch=mybranch,
						wallet=mywallet,
						status=1)

					if staff.admin==1: #anyone can add thrift to any client
						try:
							realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)
							myform = thriftform()
							return render_to_response('Ia/myadd.html',{'company':mybranch,	'user':varuser,'form':myform,'customer':details,'wallet':mywallet})

						except:
							msg = 'This customer hasnt subscribed yet for this  service'
					elif staff.cashier == 1: #anyone can add thrift to any client
						try:
							realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)
							myform = thriftform()
							return render_to_response('Ia/myadd_cash.html',{'company':mybranch,	'user':varuser,'form':myform,'customer':details,'wallet':mywallet})

						except:
							msg = 'This customer hasnt subscribed yet for this  service'

					elif staff.thrift_officer == 1: #anyone can add thrift to any client
						try:
							realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)
							myform = thriftform()
							return render_to_response('Ia/myadd_to.html',{'company':mybranch,	'user':varuser,'form':myform,'customer':details,'wallet':mywallet})

						except:
							msg = 'This customer hasnt subscribed yet for this  service'

				except:
					msg='INVALID WALLET ADDRESS'
			
			else:
				msg='Enter a valid Wallet Address'


			return render_to_response('Ia/selectloan.html',{'msg':msg})

		else:
			form=viewwalletform()
			msg = ''
			if staff.admin==1:
				return render_to_response('Ia/addthrift.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			elif staff.cashier==1:
				return render_to_response('Ia/addthrift_cash.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			elif staff.thrift_officer==1:
				return render_to_response('Ia/addthrift_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})



	else:
		return HttpResponseRedirect('/login/user/')


def account_type(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')

    		if month== '-' :
    			msg = 'Select a month'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		if acccode== '-----' :
    			msg = 'Select account type'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		else :
				try :
						www=int(month)

						monthname = calendar.month_name[www] #converts month_index to month_name

						staff = Userprofile.objects.get(email=user,status=1)
						staffid = staff.staffrec.id
						mybranch=staff.branch.id
						mybranch=tblBRANCH.objects.get(id=mybranch,status=1)

						memmerchant=tblIaMERCHANT.objects.get(thrift1a =1, staff= staffid ,status=1)


						details=tblCUSTOMER.objects.get(
							wallet=wallet,
							status=1)
						treu = tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)

						thriftrec=tblIathrift.objects.get(branch=mybranch, 
							account_type = acccode,
							month=monthname,
							customer=treu)

						return render_to_response('Ia/aaa.html',{'month':monthname,'wallet':wallet,
							'thriftrec':thriftrec,'acccode':acccode})

				except :


					myform = thriftform()
					return render_to_response('Ia/main_account.html',{'form':myform,
	    				'wallet':wallet,'account_type':acccode,'month':month})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')




def putthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,	staff=memstaff,status=1, thrift1a=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)


		yday = date.today().year

		if request.method == 'POST':
			form = thriftform(request.POST)
			if form.is_valid():
				number=request.POST['month']  #returns month number as directed in form
				mythrift=form.cleaned_data['thrift']
				wallet=request.POST['wallet']
				account_type=request.POST['account_type']

				monthname=calendar.month_name[int(number)] #converts month index to month name

				customer=tblCUSTOMER.objects.get(branch=mybranch,
					wallet=wallet,
					status=1)


				dc_customer=tblIaCUSTOMER.objects.filter(branch=mybranch,customer=customer,
					status=1).count()

				if dc_customer== 1:
					dc_customer=tblIaCUSTOMER.objects.get(branch=mybranch,status=1,customer=customer)

				generate_trans_pin()

				countt= tblIathrift.objects.filter(account_type = account_type,
					month=monthname,
					branch=mybranch,
					customer=dc_customer).count()

				if countt<1:
					tblIathrift(account_type = account_type,
						month=monthname,thrift=mythrift,branch=mybranch,customer=dc_customer,code=generate_trans_pin(),year=yday).save()

					if staff.admin==1:

						return render_to_response('Ia/addthriftsuccess.html',{'company':mybranch,
							'user':varuser,'wallet':wallet,'account':account_type,'year':yday,
							'thrift':mythrift,'month':monthname})

					elif staff.cashier==1:
						return render_to_response('Ia/addthriftsuccess_cash.html',{'company':mybranch,
							'user':varuser,'wallet':wallet,'account':account_type,'year':yday,
							'thrift':mythrift,'month':monthname})

					elif staff.thrift_officer==1:
						return render_to_response('Ia/addthriftsuccess_to.html',{'company':mybranch,
						'user':varuser,'wallet':wallet,'account':account_type,'year':yday,
						'thrift':mythrift,'month':monthname})
				


		else:
			return HttpResponseRedirect('/fts/thrift/addthrift/')
			
	else:
		return HttpResponseRedirect('/login/user/')



def addmythrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff=memstaff,status=1)

		tdate= date.today()
		mday=tdate.month
		month = calendar.month_name[mday]
		myform = kthriftform()


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			myform = kthriftform(request.POST)
			details=tblCUSTOMER.objects.get(
				# merchant=memmerchant,
				 wallet=mywallet,
				 status=1)
			return render_to_response('Ia/comeadd.html',{'company':mybranch,'user':varuser,'form':myform,
			'wallet':mywallet,'month':month})
		else:
			return HttpResponseRedirect('/login/user/')


def putinthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		if staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff=memstaff,status=1)

		if request.method == 'POST':
			form = kthriftform(request.POST)
			if form.is_valid():
				month=request.POST['month']  # month in words
				mythrift=form.cleaned_data['thrift']
				wallet=request.POST['wallet']

				today=date.today()
				yday=today.year

				month1 = datetime.strptime(month,"%B") #converts month_name to month_index
				month2=month1.month
				customer=tblCUSTOMER.objects.get(branch=mybranch,
					wallet=wallet,
					status=1)

				tblIathrift(account_type = 'Main account',month=month,year=yday,thrift=mythrift,branch=mybranch,
					# merchant= memmerchant,
					customer=customer,
					code=8797,number=month2).save()

				return render_to_response('Ia/addthriftsuccess.html',{'company':mybranch, 'user':varuser,'wallet':wallet,'thrift':mythrift,'month':month})
			else:
				msg = 'im me'
				return render_to_response('Ia/comeadd.html',{'msg':month})

		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')

def viewthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet,status=1)
					try:
						details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details)
						myform = thriftform()
						return render_to_response('Ia/myview.html',{'company':mybranch,'user':varuser,'form':myform,
							'customer':details,'wallet':mywallet})
					except:
						msg= 'Not subscribed for this service'
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		else:
			form=viewwalletform()
			msg = ''

			if staff.admin==1:
				return render_to_response('Ia/viewthrifthistory.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

			elif staff.cashier==1:
				return render_to_response('Ia/viewthrifthistory_cash.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			elif staff.thrift_officer==1:
				return render_to_response('Ia/viewthrifthistory_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')





		

def log(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


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
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		form=logform()
		if staff.admin==1:
			return render_to_response('Ia/activitlog.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		else:
			msg= 'error!!!'
		return render_to_response('Ia/selectloan.html',{'msg':msg})

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

    		data=tblIaMERCHANT.objects.filter(branch=mybranch, status=1)

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




def logapprove(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


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
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		form=viewtransform()
		if staff.admin==1:
			return render_to_response('Ia/activitlog_approve.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		else:
			msg= 'error!!!'
		return render_to_response('Ia/selectloan.html',{'msg':msg})

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

    		data=tblIaMERCHANT.objects.filter(branch=mybranch, status=1)

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
    		status,transdate,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffid = staff.staffrec.id
    		mybranch=staff.branch.id
    		mybranch=tblBRANCH.objects.get(id=mybranch,status=1)


    		if status=='-----':
    			msg= 'Select Status'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})


    		if transdate=='':
    			msg= 'select date'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

        	dday,mday,yday = transdate.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	

        	mydate=date(yday,mday,dday)



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



    		# 	return render_to_response('Ia/activitlog_merchant.html',{
    		# 		'company':mybranch,
    		# 		'dates':transdate,
    		# 		'merchant':merchant1,
    		# 		'total':ddt,
    		# 		'date':mydatwwwe,
    		# 		'ttt':thriftrec})

    		# else:
    		# 	msg= 'No transactons found'
    		# 	return render_to_response('Ia/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



###################################****************************************************





def account_view(request): #anybody can view anybodys thrift
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')
    		tdate= date.today()
    		year=tdate.year



    		if month== '-' :
    			msg = 'Select a month'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		if acccode== '-----' :
    			msg = 'Select account type'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		else :

				try :

						www=int(month)

						monthname = calendar.month_name[www]

						staff = Userprofile.objects.get(email=user,status=1)
						staffid = staff.staffrec.id

						memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff= staffid ,status=1)

						details=tblCUSTOMER.objects.get(
							wallet=wallet,
							status=1)

						details=tblIaCUSTOMER.objects.get(customer=details)

						thriftrec=tblIathrift.objects.get(account_type = acccode,
							month=monthname,
							year =year,
							customer=details)

						return render_to_response('Ia/vvv.html',{'month':monthname,'wallet':wallet,
							'thriftrec':thriftrec,'acccode':acccode})

				except :
					msg = 'No entries found'

	    			myform = thriftform()
	    			return render_to_response('Ia/selectloan.html',{'msg':msg,})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def changethrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to month_number to month_name

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet,status=1)
					try:
						details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details)
						myform = thriftform()
						if staff.admin==1:
							return render_to_response('Ia/mychange.html',{'company':mybranch,'user':varuser,'form':myform,
								'customer':details,'wallet':mywallet})
						if staff.cashier==1:
							return render_to_response('Ia/mychange_cash.html',{'company':mybranch,'user':varuser,'form':myform,
								'customer':details,'wallet':mywallet})
						if staff.thrift_officer==1:
							return render_to_response('Ia/mychange_to.html',{'company':mybranch,'user':varuser,'form':myform,
								'customer':details,'wallet':mywallet})

						return render_to_response('Ia/mychange.html',{'company':mybranch,'user':varuser,'form':myform,
							'customer':details,'wallet':mywallet})
					except:
						msg= 'Not subscribed for this service'
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		else:
			form=viewwalletform()
			msg = ''
			if staff.admin==1:
				return render_to_response('Ia/changethrift.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

			elif staff.cashier==1:
				return render_to_response('Ia/changethrift_cash.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			elif staff.thrift_officer==1:
				return render_to_response('Ia/changethrift_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})



	else:
		return HttpResponseRedirect('/login/user/')





def thriftrep(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})



		if staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form = thrifthistory(request.POST)
			if form.is_valid():

				month=form.cleaned_data['month'] #month in figures
				account_type=request.POST['account_type']

				if month == '-':
					msg ='Select Month'
					return render_to_response('Ia/selectloan.html',{'msg':msg})


				if account_type=='-----':
					msg ='Select Account Type'
					return render_to_response('Ia/selectloan.html',{'msg':msg})


				monthname = calendar.month_name[int(month)]


				dll=[]

				details=tblCUSTOMER.objects.filter(branch=mybranch)


				for  k in details:
					g = tblIaCUSTOMER.objects.filter(customer=k).count()
					
					if g > 0:
						p = tblIaCUSTOMER.objects.get(customer=k)

						if tblIathrift.objects.filter(branch=mybranch, 
							account_type = account_type,customer=p,month=monthname).count() > 0:


							thriftrec=tblIathrift.objects.get(
								branch=mybranch, 
								account_type = account_type,
								customer=p,
								month=monthname)


							thrift=thriftrec.thrift
							wallet=thriftrec.customer.customer.surname + "  " + thriftrec.customer.customer.firstname
							dl={'wallet':wallet,'thrift':thrift}
							dll.append(dl)



				return render_to_response('Ia/thriftrep.html',{'company':mybranch,
					'user':varuser,
					'thriftrec':dll,
					'account_type':account_type,
					'month':monthname})
			
		else:
			form=thrifthistory()
		return render_to_response('Ia/repthr.html',{'company':mybranch,'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')






def account_change(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffdet=staff.staffrec.id
    		branch=staff.branch.id
    		mycompany=staff.branch.company
    		company=mycompany.name
    		comp_code=mycompany.id
    		ourcompany=tblCOMPANY.objects.get(id=comp_code)
    		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
    		tdate=date.today()
    		year=tdate.year


    		if month== '-' :
    			msg = 'Select a month'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		if acccode== '-----' :
    			msg = 'Select account type'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		else :

				try :
					www=int(month)

					monthname = calendar.month_name[www]

					staff = Userprofile.objects.get(email=user,status=1)

					staffid = staff.staffrec.id

					details=tblCUSTOMER.objects.get(branch=mybranch,
						wallet=wallet,
						status=1)
					details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details)

					try:
						thriftrec=tblIathrift.objects.get(account_type = acccode,
							month=monthname,year=year,customer=details)
					except:
						msg = 'No record found'
						return render_to_response('Ia/selectloan.html',{'msg':msg})


					transactions=tblIasavings_trans.objects.filter(branch=mybranch,
						account_type=acccode,
						customer=details,
						transdate__month=www)

					if transactions.count() == 0 :
						transactions=0
						msg = 'Click the change link to begin'
					else:
						msg = ' you cannot change thrift value at this time'
						transactions=transactions.count()

					return render_to_response('Ia/ccc.html',{'count':transactions,
						'month':monthname,'wallet':wallet,'user':user,'acccode':acccode,
						'msg':msg,'thriftrec':thriftrec})

				except :
					msg = 'No entries found'
	    			return render_to_response('Ia/selectloan.html',{'msg':msg,})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def edit_thrift_popup(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		wallet,month,account_type,user=acccode.split(':')

    		fdate=date.today()
    		yer=fdate.year

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffdet=staff.staffrec.id
    		branch=staff.branch.id
    		mycompany=staff.branch.company
    		company=mycompany.name
    		comp_code=mycompany.id
    		ourcompany=tblCOMPANY.objects.get(id=comp_code)
    		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

    		customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
    		customer=tblIaCUSTOMER.objects.get(branch=mybranch, customer=customer)


    		mycom = tblIathrift.objects.get(
    			customer=customer,
    			month=month,
    			year=yer,
    			account_type=account_type)
    		thrift=mycom.thrift
	    	return render_to_response('Ia/thrif_edit.html',{'thrift':thrift,
	    		'income':mycom,'account_type':account_type,
	    		'month':month,
	    		'wallet':wallet,
	    		'year':yer})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def thriftedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		if staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		dattee= date.today().month


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			ttr=request.POST['thrift']
			dd=request.POST['date'] #month in fnumber
			dd = calendar.month_name[int(dd)] #converts to month name

			return render_to_response('Ia/prevchan.html',{'company':mybranch, 'user':varuser,'month':dd,'wallet':mywallet,'thrift':ttr})

	else:
		return HttpResponseRedirect('/login/user/')


def safethriftedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		if staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		dattee= date.today().month


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			ttr=request.POST['thrift']
			month=request.POST['month'] #month in words
			newthrift = request.POST['new thrift']
			year = request.POST['year']
			ttr =int(ttr)

			customer=tblCUSTOMER.objects.get(wallet=mywallet,status=1)
			customer=tblIaCUSTOMER.objects.get(customer=customer)

			firstthrift = tblIathrift.objects.get(
				account_type = 'Main account',
				month=month,
				year=year,
				customer=customer)

			# msg= newthrift
			# return render_to_response('Ia/selectloan.html',{'msg':msg})

			if firstthrift.thrift==ttr:
				firstthrift.thrift=newthrift
				firstthrift.save()
				return render_to_response('Ia/savethriftsuccess.html',{'company':mybranch,
					'user':varuser,
					'month':month,'year':year,
					'wallet':mywallet,'thrift':ttr,'newt':newthrift})

			else:
				msg='i no do again'
				return render_to_response('Ia/selectloan.html',{'msg':msg})
		else:

				return HttpResponseRedirect('/fts/thrift/changethrift/')
	else:
		return HttpResponseRedirect('/login/user/')


def rolloverthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		if staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		mydatee=date.today().month #month in figures
		current_date =int(mydatee)
		yday = date.today().year
		ddt= calendar.month_name[int(mydatee)] #month in words

		if mydatee == 12:
			nextmonth = 1
			yday=yday+1
		else:
			nextmonth=mydatee + 1

		nnm= calendar.month_name[int(nextmonth)]

		if request.method=='POST':
			details=tblCUSTOMER.objects.filter(branch=mybranch, status=1)

			# msg=details return render_to_response('Ia/selectloan.html',{'msg':msg})

			for  k in details:
				dj = tblIaCUSTOMER.objects.filter(customer=k,status=1).count()

				msg=dj
				return render_to_response('Ia/selectloan.html',{'msg':msg})


				if dj==1: #hes a member
					t1A = tblIaCUSTOMER.objects.get(customer=k,status=1)
					thriftrec=tblIathrift.objects.filter(branch=mybranch,
						customer= t1A,
						month=month,
						year = yday)

					for tt in thriftrec:
						td = tt.account_type
						thrift= t.thrift

						customer_thrift=tblIathrift.objects.filter(year=yday,
							month=nextmonth,
							customer=t1A,
							branch=mybranch,
							account_type=td).count()

						if customer_thrift==0:
							tblIathrift(year=yday,
								month=nextmonth,
								customer=t1A,
								thrift=thrift,
								branch=mybranch,
								account_type=td).save()

			return render_to_response('Ia/rollsuccess.html',{'company':mybranch,'user':varuser,'month':ddt,'nextmonth':nnm})


		else:
			return render_to_response('Ia/rolloverthrift.html',{'company':mybranch, 'user':ddt,'month':ddt,'nextmonth':nnm})

	else:
		return HttpResponseRedirect('/login/user/')




####  CAsh iN prOcedures************************

def payrequests(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		memmerchant=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(staff=memstaff, thrift1a=1, status=1)


		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, 
						wallet=mywallet,
						status=1)

					if staff.admin ==1 :
						dcty= tblIaCUSTOMER.objects.get(customer=details,status=1)

					else: #in the future, COs might get the right to deal any customer

						dcty= tblIaCUSTOMER.objects.get(customer=details,status=1)


					myform = thriftform()

					if staff.admin==1:
						return render_to_response('Ia/deposit.html',{'company':mybranch,'user':varuser,'form':myform,'customer':details,'wallet':mywallet})
					elif staff.cashier==1:
						return render_to_response('Ia/deposit_cash.html',{'company':mybranch,'user':varuser,'form':myform,'customer':details,'wallet':mywallet})
					elif staff.thrift_officer==1:
						return render_to_response('Ia/deposite_to.html',{'company':mybranch,'user':varuser,'form':myform,'customer':details,'wallet':mywallet})


				except:
					msg='EITHER YOU ARE NOT RESPONSIBLE TO THIS CUSTOMER OR THEIR WALLET ADDRESS IS INVALID'
					return render_to_response('Ia/selectloan.html',{'msg':msg})


		else:
			form=viewwalletform()
			if staff.admin==1:
				return render_to_response('Ia/all.html',{'company':mybranch, 'user':varuser,'form':form})
			elif staff.cashier==1:
				return render_to_response('Ia/all_cash.html',{'company':mybranch, 'user':varuser,'form':form})
			elif staff.thrift_officer==1:
				return render_to_response('Ia/all_to.html',{'company':mybranch, 'user':varuser,'form':form})


	else:
		return HttpResponseRedirect('/login/user/')



def account_dep(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		# acccode,wallet,month,user=acccode.split(':')
    		yeart=0
    		acccode,wallet,month,user=acccode.split(':')

    		if month== '-' :
    			msg = 'Select a month'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})


    		if acccode== '-----' :
    			msg = 'Select account type'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		else :

				staff = Userprofile.objects.get(email=user,status=1)
				staffid = staff.staffrec.id

	 			branch=staff.branch.id
				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)
				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


				memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff= staffid ,status=1)


				details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
			
				if staff.admin == 1:
					dcty= tblIaCUSTOMER.objects.get(customer=details)
				else:
					dcty= tblIaCUSTOMER.objects.get(customer=details)

				www=int(month)



				month = calendar.month_name[www] 


				thriftrec=tblIathrift.objects.filter(account_type = acccode,month=month,branch=mybranch,customer=dcty).count()
				
				if thriftrec>0:
					thriftrec=tblIathrift.objects.get(account_type = acccode,month=month,branch=mybranch,customer=dcty)
				else:
					msg = ' No thrift record found'
					return render_to_response('Ia/selectloan.html',{'msg':msg})

				thrift = thriftrec.thrift
				year=thriftrec.year
				yeart=year
				code = thriftrec.code




				CR= tblIasavings_trans.objects.filter(
					branch=mybranch,
					customer=dcty,
					code=code,
					description='CR',
					account_type = acccode)#.exclude(status='Account Maintenance')


				DR= tblIasavings_trans.objects.filter(
					branch=mybranch,
					customer=dcty,
					code=code,
					description='DR',
					account_type = acccode)


				if CR.count() > 0 :
					ncr=CR.aggregate(Sum('number'))
					ncr = ncr['number__sum']
				else:
					ncr =0

				if DR.count() > 0 :
					ndr=DR.aggregate(Sum('number'))
					ndr = ndr['number__sum']
				else:
					ndr = 0

				add = ncr

				if ncr == 31:

					msg = 'You reached the limit for this month'	
					return render_to_response('Ia/selectloan.html',{'msg':msg})

				else:

					return render_to_response('Ia/dep.html',{'month':month,
		            		'wallet':wallet,
		            		'thrift':thrift,
		            		'year':year, 
		            		'cccode':acccode,
		            		'user':user,
		            		'add':add})


    	else:
    		return HttpResponseRedirect('/fts/thrift/payrequest/')
    else:
    	return HttpResponseRedirect('/fts/thrift/payrequest/')




def source(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,thrift,month,account,user=acccode.split(':')
    		if acccode== '-----':
    			msg = 'Select funding source'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		elif acccode=='Cash':
    			myform = thriftamountform()
    			staff = Userprofile.objects.get(email=user,status=1)

    			if staff.admin==1:
    				return render_to_response('Ia/admin.html',{'form':myform,'wallet':wallet,'thrift':thrift,'month':month,'account_type':account})

    			elif staff.cashier==1:
    				return render_to_response('Ia/admin_cash.html',{'form':myform,'wallet':wallet,'thrift':thrift,'month':month,'account_type':account})

    			elif staff.thrift_officer==1:
    				return render_to_response('Ia/admin_to.html',{'form':myform,'wallet':wallet,'thrift':thrift,'month':month,'account_type':account})

    		elif acccode=='Transfer':
    			msg = 'This option is coming soon !!!'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})
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

	# varuser=request.session['userid']
	# staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

	# if staff.thrift==0:
	# 	return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

	# staffdet=staff.staffrec.id
	# branch=staff.branch.id

	# mycompany=staff.branch.company
	# company=mycompany.name
	# comp_code=mycompany.id
	# ourcompany=tblCOMPANY.objects.get(id=comp_code)

	# mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

	# memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)



    suggestions = []
    qset = tblIathrift.objects.get(account_type = 'Main account',code =8797)#[:10]
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


def history(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet, status=1)
					details= tblIaCUSTOMER.objects.get(customer=details,status=1)
					myform = thriftform()
					return render_to_response('Ia/conthistory.html',{'company':mybranch,'user':varuser,'form':myform,
					'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
			if staff.admin==1:
				return render_to_response('Ia/account_balance.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			elif staff.cashier==1:
				return render_to_response('Ia/account_balance_cash.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			elif staff.thrift_officer==1:
				return render_to_response('Ia/account_balance_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def statementtt(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet, status=1)
					details= tblIaCUSTOMER.objects.get(customer=details,status=1)
					myform = thriftform()
					return render_to_response('Ia/contstatement.html',{'company':mybranch,'user':varuser,'form':myform,
					'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
			if staff.admin==1:
				return render_to_response('Ia/account_statement.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			elif staff.cashier==1:
				return render_to_response('Ia/account_statement_cash.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			elif staff.thrift_officer==1:
				return render_to_response('Ia/account_statement_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')




def account_history(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffdet=staff.staffrec.id
    		branch=staff.branch.id
    		mycompany=staff.branch.company
    		company=mycompany.name
    		comp_code=mycompany.id
    		ourcompany=tblCOMPANY.objects.get(id=comp_code)
    		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


    		if month== '-' :
    			msg = 'Select a month'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		if acccode== '-----' :
    			msg = 'Select account type'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		else :


				try :
					www=int(month)

					monthname = calendar.month_name[www] #converts month_index to month_name

					staff = Userprofile.objects.get(email=user,status=1)
					staffid = staff.staffrec.id

					memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff= staffid ,status=1)

					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
					details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details,status=1)

					thrift=tblIathrift.objects.get(account_type = acccode, month=monthname,customer=details)
					code=thrift.code


					CR= tblIasavings_trans.objects.filter(
						branch=mybranch,
						customer=details,
						code=code,
						description='CR',
						account_type = acccode).exclude(status='Account Maintenance')


					DR= tblIasavings_trans.objects.filter(
						branch=mybranch,
						customer=details,
						code=code,
						description='DR',
						account_type = acccode)



					if CR.count() > 0 :
						cr=CR.aggregate(Sum('amount'))
						cr = cr['amount__sum']
					else:
						cr =0

					if DR.count() > 0 :
						dr=DR.aggregate(Sum('amount'))
						dr = dr['amount__sum']
					else:
						dr = 0


					# msg = cr - dr return render_to_response('Ia/selectloan.html',{'msg':msg})


					add = cr - dr
					comm =''
					uu=''

					if cr - dr == 0:
						if dr  > 0 :

							comm= dr
							uu= ' Cash Withdrawn by you' #catenation needed

						elif dr== 0:

							request_count= tblIapayoutrequest.objects.filter(account_type = acccode,
								wallet_type='Main',
								merchant=memmerchant,
								status='Unpaid',
								customer=details,
								recdate__month = www)

							rqt = request_count.count()

							if rqt  > 0 :
								add=request_count.aggregate(Sum('amount'))
								add = add['amount__sum']
								add= add , 'Requested'

					return render_to_response('Ia/bal.html',{
						# 'customer':details,
						'wallet':wallet,
						'comm':comm,
						'uu':uu,
						'bal':add})



				except :
					msg= 'No record found'
					msg=msg
					return render_to_response('Ia/selectloan.html',{'msg':msg})


    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')





def account_statement_history(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffdet=staff.staffrec.id
    		branch=staff.branch.id
    		mycompany=staff.branch.company
    		company=mycompany.name
    		comp_code=mycompany.id
    		ourcompany=tblCOMPANY.objects.get(id=comp_code)
    		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


    		if month== '-' :
    			msg = 'Select a month'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		if acccode== '-----' :
    			msg = 'Select account type'
    			return render_to_response('Ia/selectloan.html',{'msg':msg})

    		else :


				try :
					www=int(month)

					monthname = calendar.month_name[www] #converts month_index to month_name

					staff = Userprofile.objects.get(email=user,status=1)
					staffid = staff.staffrec.id

					memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff= staffid ,status=1)

					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
					details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details,status=1)

					thrift=tblIathrift.objects.get(account_type = acccode, month=monthname,customer=details)
					code=thrift.code



					thriftrec= tblIamerchantBank.objects.filter(
						branch=mybranch,
						customer=details,
						code=code,
						wallet_type='Main',
						account_type = acccode).order_by('recdate').reverse()


					CR= tblIasavings_trans.objects.filter(
						branch=mybranch,
						customer=details,
						code=code,
						description='CR',
						account_type = acccode).exclude(status='Account Maintenance')


					DR= tblIasavings_trans.objects.filter(
						branch=mybranch,
						customer=details,
						code=code,
						description='DR',
						account_type = acccode)



					if CR.count() > 0 :
						cr=CR.aggregate(Sum('amount'))
						cr = cr['amount__sum']
					else:
						cr =0

					if DR.count() > 0 :
						dr=DR.aggregate(Sum('amount'))
						dr = dr['amount__sum']
					else:
						dr = 0


					# msg = cr - dr return render_to_response('Ia/selectloan.html',{'msg':msg})


					add = cr - dr
					comm =''
					uu=''

					if cr - dr == 0:
						if dr  > 0 :

							comm= dr
							uu= ' Cash Withdrawn by you' #catenation needed

						elif dr== 0:

							request_count= tblIapayoutrequest.objects.filter(account_type = acccode,
								wallet_type='Main',
								merchant=memmerchant,
								status='Unpaid',
								customer=details,
								recdate__month = www)

							rqt = request_count.count()

							if rqt  > 0 :
								add=request_count.aggregate(Sum('amount'))
								add = add['amount__sum']
								add= add , 'Requested'

					return render_to_response('Ia/sta.html',{
						# 'customer':details,
						'wallet':wallet,
						'comm':comm,
						'thriftrec':thriftrec,
						'uu':uu,
						'bal':add})



				except :
					msg= 'No record found'
					msg=msg
					return render_to_response('Ia/selectloan.html',{'msg':msg})


    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def cashier_cashin(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.filter(staff=memstaff,thrift1a=1, status=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,thrift1a=1, status=1)


		if request.method == 'POST':
			form = thriftamountform(request.POST)
			if form.is_valid():
				amount=form.cleaned_data['amount']
				mythrift=request.POST['thrift']
				wallet=request.POST['wallet']
				account_type=request.POST['account_type']


				merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)
				merchant=tblIaMERCHANT.objects.get(staff=merchant,thrift1a=1)

				amount=int(amount)

				thrift=int(mythrift)

				fdate= date.today()
				transdate=fdate

				customer=tblCUSTOMER.objects.get(branch = mybranch, wallet=wallet)
				customer1=tblIaCUSTOMER.objects.get(customer=customer)
				monthname = calendar.month_name[fdate.month]

				th = tblIathrift.objects.get(branch=mybranch,
	            	account_type=account_type,
	            	customer=customer1,
	            	month=monthname,
	            	year =fdate.year)

				code = th.code

				ddt=[]
				lump,l=divmod(amount,thrift)

				p = (monthrange(transdate.year, transdate.month))[-1]
				number= int(amount / thrift)

				if l == 0 :	#how many have u saved so far?:

					mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch,

	                	customer=customer1, #who owns the mo
	                    recdate__month=fdate.month, #tranaction date
	                    description='CR',
	                    account_type = account_type,
	                    wallet_type='Main')

					if mont_contribution.count() == 0:
						add_count = 0
					else:
						add_count = mont_contribution.aggregate(Sum('number'))
						add_count = add_count['number__sum']

					if  add_count + lump <= p :

						if tblIafieldagent.objects.filter(branch=mybranch,merchant=merchant,code=code,customer=customer1,number=number,recdate=transdate,amount=amount,account_type = account_type,wallet_type='Main',status='Received').count() <1 :


							tblIafieldagent(branch=mybranch,merchant=merchant,code=code,customer=customer1,number=number,recdate=transdate,amount=amount,account_type = account_type,wallet_type='Main',status='Received').save()

							return render_to_response('Ia/cashinthriftsuccess_cash.html',{'account_type':account_type,
								'company':mybranch,
								'user':varuser,
								'wallet':wallet,
								'thrift':mythrift,
								'amount':amount,
								'count':number})

						else:
							msg = "you cant post same money twice same day"
							return render_to_response('Ia/selectloan.html',{'msg':msg})

					else:
						msg = 'amount too large'
						return render_to_response('Ia/selectloan.html',{'company':mybranch, 'user':varuser,'msg':msg})

				else:
					msg = 'amount not applicable'
					return render_to_response('Ia/selectloan.html',{'company':mybranch, 'user':varuser,'msg':msg})

	        else:
	        	msg = 'Error!!!'
	        	return render_to_response('Ia/selectloan.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


#### direct deposit
def admin_cashin(request): #customer - admin transaction
    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ia/selectloan.html',{'msg':msg})


        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.admin==0 :
    		return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
        	wallet =request.POST['wallet']
        	month =request.POST['month']

        	account_type =request.POST['account_type']
        	thrift =request.POST['thrift']
        	amount = request.POST['amount']

        	merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)
        	merchant=tblIaMERCHANT.objects.get(staff=merchant,thrift1a=1)

        	amount=int(amount)
        	thrift=int(thrift)

        	fdate= date.today()
        	transdate=fdate


        	customer=tblCUSTOMER.objects.get(branch = mybranch, wallet=wallet,status=1)
        	surname=customer.surname

        	email3=customer.email
        	customer1=tblIaCUSTOMER.objects.get(customer=customer,status=1)


        	th = tblIathrift.objects.get(branch=mybranch,
            	account_type=account_type,
            	customer=customer1,
            	month=month,
            	year =fdate.year)

        	code = th.code
        	ddt=[]

        	lump=0
        	l=0

        	lump,l=divmod(amount,thrift)

        	p=0

        	p = (monthrange(transdate.year, transdate.month))[-1] #in the future, we'll use settings to determin this 

        	p = 31
        	# p = int(p)

        	number= int(amount / thrift)

        	pl= number-1

        	new_amount = amount - thrift

        	if l == 0 :
        		generate_trans_pin()

        		mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch,

                	customer=customer1, #who owns the mo
                    code = code, #tranaction date
                    description='CR',
                    account_type = account_type,
                    wallet_type='Main')

        		add_count=0

        		if mont_contribution.count() == 0:
        			add_count = 0
        		else:
        			add_count=0
        			add_count = mont_contribution.aggregate(Sum('number'))
        			add_count = add_count['number__sum']


        		if  add_count + lump <= p :

        			if add_count == 0:
        				if number == 1:
        					if tblIamerchantBank.objects.filter(branch=mybranch,merchant=merchant,code=code,customer=customer1,number=1,recdate=transdate,transdate=fdate,amount=amount,account_type = account_type,wallet_type='Main',approved_by=varuser).count() < 1:
        						tblIamerchantBank(branch=mybranch,merchant=merchant,transac_id=generate_trans_pin(),code=code,customer=customer1,number=1,recdate=transdate,transdate=fdate,amount=amount,account_type = account_type,wallet_type='Main',approved_by=varuser,status='CR').save()

        					if tblIasavings_trans.objects.filter(branch=mybranch,merchant=merchant,code=code,customer=customer1,number=1,recdate=transdate,transdate=fdate,amount=amount,description='CR',account_type = account_type,wallet_type='Main',avalability='Not Available').count() <1 :
        						tblIasavings_trans(branch=mybranch,merchant=merchant,transac_id=generate_trans_pin(),code=code, customer=customer1,number=1,recdate=transdate, transdate=fdate,amount=amount,description='CR',account_type = account_type,wallet_type='Main',avalability='Not Available',status='Account Maintenance').save()

        				elif number > 1:
        					if tblIamerchantBank.objects.filter(branch=mybranch,merchant=merchant,code=code,customer=customer1,number=number,recdate=transdate,transdate=transdate,amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main').count() < 1:
        						tblIamerchantBank(branch=mybranch,merchant=merchant, transac_id=generate_trans_pin(),code=code,customer=customer1,number=number,recdate=transdate,transdate=transdate,amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main',status='CR').save()

        					if tblIasavings_trans.objects.filter(branch=mybranch,merchant=merchant,code=code,customer=customer1,number=1,recdate=transdate, transdate=transdate,amount=thrift,description='CR',account_type = account_type,wallet_type='Main').count() < 1:
        						tblIasavings_trans(branch=mybranch,merchant=merchant,transac_id=generate_trans_pin(),code=code, customer=customer1, number=1,recdate=transdate,transdate=transdate,amount=thrift,description='CR',account_type = account_type,wallet_type='Main',avalability='Not Available',status='Account Maintenance').save()

        					if tblIasavings_trans.objects.filter(branch=mybranch,merchant=merchant,code=code, customer=customer1, number=pl,recdate=transdate,transdate=transdate,amount=new_amount,description='CR',account_type = account_type,wallet_type='Main',avalability='Available').count() < 1:
        						tblIasavings_trans(branch=mybranch,merchant=merchant,transac_id=generate_trans_pin(),code=code,customer=customer1,number=pl,recdate=transdate,transdate=transdate,amount=new_amount,description='CR',account_type = account_type,wallet_type='Main',avalability='Available',status='Available').save()

        			elif add_count > 0 :
        				if tblIamerchantBank.objects.filter(branch=mybranch,merchant=merchant,code=code,customer=customer1,number=number,recdate=transdate,transdate=transdate,amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main').count() <1:
        					tblIamerchantBank(branch=mybranch,merchant=merchant,transac_id=generate_trans_pin(),code=code,customer=customer1,number=number,recdate=transdate,transdate=transdate,amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main', status='CR').save()

        					tblIasavings_trans(branch=mybranch,merchant=merchant,transac_id=generate_trans_pin(),code=code,customer=customer1, number=number,recdate=transdate, transdate=transdate,amount=amount,description='CR',account_type = account_type,wallet_type='Main',avalability='Available',status='Available').save()


        				else:
        					msg='you cant post same amount twice same day'
        					return render_to_response('Ia/selectloan.html',{'msg':msg})


        			# pl = [varuser,email3]
        			# for email31 in pl:
					try:
						Direct_creditingIa(email3,surname,thrift,amount,month)
					except:
						h=0

        			return render_to_response('Ia/apsuccess.html',{'company':mybranch,'customer':customer1,'amount':amount,'user':varuser})



        		else:
					msg = 'amount too large'
					return render_to_response('Ia/selectloan.html',{'msg':msg})
        	else:
        		msg = 'amount not applicable'
        		return render_to_response('Ia/selectloan.html',{'msg':msg})

        else:
        	return HttpResponseRedirect('/fts/thrift/payrequest/')
    else:
		return HttpResponseRedirect('/login/user/')





def agent_cashin(request): #customer - admin transaction
    if 'userid' in request.session:
        varuser=request.session['userid']
        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ia/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

        memmerchant=tblIaMERCHANT.objects.filter(staff=memstaff,thrift1a=1, status=1).count()

        if staff.thrift_officer==0  or memmerchant<1:
        	return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
        else:
        	memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,thrift1a=1, status=1)

        if request.method == 'POST':
            wallet =request.POST['wallet']
            month =request.POST['month']
            account_type =request.POST['account_type']
            thrift =request.POST['thrift']
            amount = request.POST['amount']


            merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)
            merchant=tblIaMERCHANT.objects.get(staff=merchant,thrift1a=1)

            amount=int(amount)
            thrift=int(thrift)

            fdate= date.today()
            yyr = fdate.year
            transdate=fdate

            customer=tblCUSTOMER.objects.get(branch = mybranch, wallet=wallet)
            customer1=tblIaCUSTOMER.objects.get(customer=customer)


            th = tblIathrift.objects.get(branch=mybranch,account_type=account_type,customer=customer1,month=month,year =transdate.year)

            code = th.code

            ddt=[]

            lump,l=divmod(amount,thrift)

            # p = (monthrange(transdate.year, transdate.month))[-1]
            #in the future, back offices can set this figure to just anything of choice
            p = 31

            number= int(amount / thrift)


            generate_trans_pin()

            if l == 0 :
 	#how many have u saved so far?
            	mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch,

                	customer=customer1, #who owns the mo
                    recdate__month=fdate.month, #tranaction date
                    description='CR',
                    account_type = account_type,
                    wallet_type='Main')

            	if mont_contribution.count() == 0:
            		add_count = 0
            	else:
            		add_count = mont_contribution.aggregate(Sum('number'))
            		add_count = add_count['number__sum']


            	if  add_count + lump <= p :

        			if tblIafieldagent.objects.filter(branch=mybranch,
        				merchant=merchant,
        				code=code,
        				customer=customer1,
        				number=number,
        				recdate=transdate,
        				amount=amount,
        				account_type = account_type,
        				wallet_type='Main',
        				status='Received').count() <1 :

        				tblIafieldagent(branch=mybranch,
            				merchant=merchant,
            				code=code,
            				customer=customer1,
            				number=number,
            				recdate=transdate,
            				transac_id=generate_trans_pin(),
            				amount=amount,
            				account_type = account_type,
            				wallet_type='Main',
            				status='Received').save()

        				return render_to_response('Ia/cashinthriftsuccess.html',{'account_type':account_type,
							'company':mybranch,
							'user':varuser,
							'wallet':customer1,
							'month':month,
							'year':yyr,
							'date':fdate,
							'thrift':thrift,
							'amount':amount,
							'count':number})


        			else:
						msg = "you cant post same money twice same day"
						return render_to_response('Ia/selectloan.html',{'msg':msg})

            	else:

					msg = 'amount too large'
					return render_to_response('Ia/selectloan.html',{'company':mybranch, 'user':varuser,'msg':msg})


            else:
        		msg = 'amount not applicable'
        		return render_to_response('Ia/selectloan.html',{'company':mybranch, 'user':varuser,'msg':msg})

        else:
        	msg = 'Error!!!, This is a get method'
        	return render_to_response('Ia/selectloan.html',{'company':mybranch, 'user':varuser,'msg':msg})


    else:
    	return HttpResponseRedirect('/login/user/')





def unremmitted(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		if staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form = depreportform(request.POST)
			if form.is_valid():
				mystatus=form.cleaned_data['status']
				tdate=form.cleaned_data['date']

				if mystatus =='-----':
					msg = 'select the appropriate status'
					return render_to_response('Ia/selectloan.html',{'msg':msg})

				dday,mday,yday = tdate.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				oydate=date(yday,mday,dday)
				oydate4= oydate.strftime('%A')

				thriftrec=[]


#########seperate this function into roles, admin, merchant, ccashier
				if mystatus=='Contribution':
					status='Sales'

					cont_list=tblIamerchantBank.objects.filter(branch=mybranch,
						recdate=oydate,
						merchant=memmerchant,
						status='CR')


					trec =[]

					if cont_list.count() > 0:
						for kp in cont_list:
							mtv = tblIathrift.objects.get(code=kp.code)
							thrift_month = mtv.month
							amount=kp.amount
							customer=kp.customer.customer.surname + '   ' + kp.customer.customer.firstname+ '   ' + kp.customer.customer.othername
							fr={'month':thrift_month,'customer':customer,'amount':amount}
							trec.append(fr)

					s =cont_list.aggregate(Sum('amount'))
					s=s['amount__sum']

					return render_to_response('Ia/merchantpayhistory_sales.html',{'company':mybranch, 
						'date':oydate4,
						'date2':oydate, 
						'user':varuser,
						's':s,
						'thriftrec':trec,
						'status':mystatus})



				elif mystatus=='Withdrawal':
					status='Withdrawn'

					cont_list=tblIasavings_trans.objects.filter(branch=mybranch,
						recdate=oydate,
						merchant=memmerchant,
						description='DR')



					trec =[]

					if cont_list.count() > 0:
						for kp in cont_list:
							mtv = tblIathrift.objects.get(code=kp.code)
							thrift_month = mtv.month
							amount=kp.amount
							customer=kp.customer.customer.surname + '   ' + kp.customer.customer.firstname+ '   ' + kp.customer.customer.othername
							fr={'month':thrift_month,'customer':customer,'amount':amount}
							trec.append(fr)

					w =cont_list.aggregate(Sum('amount'))
					w=w['amount__sum']


					return render_to_response('Ia/merchantpayhistory_withdraw.html',{'company':mybranch, 
						'date':oydate4,
						'date2':oydate, 
						'user':varuser,
						'w':w,
						'thriftrec':trec,
						'status':mystatus})


				elif mystatus == 'All':
					trec=[]

					withdrawals=tblIasavings_trans.objects.filter(branch=mybranch,
						recdate=oydate,
						merchant=memmerchant,
						description='DR')

					trec =[]

					if withdrawals.count() > 0:
						for kp in withdrawals:
							mtv = tblIathrift.objects.get(code=kp.code)
							thrift_month = mtv.month
							amount=kp.amount
							statusw=kp.status
							customer=kp.customer.customer.surname + '   ' + kp.customer.customer.firstname+ '   ' + kp.customer.customer.othername
							fr={'month':thrift_month,'customer':customer,'amount':amount,'status':statusw}
							trec.append(fr)
					


					sales=tblIamerchantBank.objects.filter(branch=mybranch,
						recdate=oydate,
						merchant=memmerchant,
						status='CR')


					if sales.count() > 0:
						for kp in sales:
							mtv = tblIathrift.objects.get(code=kp.code)
							thrift_month = mtv.month
							amount=kp.amount
							statusw=kp.status
							customer=kp.customer.customer.surname + '   ' + kp.customer.customer.firstname+ '   ' + kp.customer.customer.othername
							fr={'month':thrift_month,'customer':customer,'amount':amount,'status':statusw}
							trec.append(fr)




					w =withdrawals.aggregate(Sum('amount'))
					w=w['amount__sum']

					s =sales.aggregate(Sum('amount'))
					s=s['amount__sum']



				return render_to_response('Ia/merchantpayhistory.html',{'company':mybranch, 
					'date':oydate4,
					'date2':oydate, 
					'user':varuser,
					'w':w,
					's':s,
					'thriftrec':trec,
					'status':mystatus})

			
			else :
				msg = 'Fill up all boxes'
				return render_to_response('Ia/selectloan.html',{'msg':msg})


		else:
			
			if  staff.admin==1 :
				form=depreportform()
				return render_to_response('Ia/unremmitted.html',{'company':mybranch, 'user':varuser,'form':form})

			elif staff.cashier==1:
				form =viewtransform()
				return render_to_response('Ia/unremmitted_cash.html',{'company':mybranch, 'user':varuser,'form':form})

			elif staff.thrift_officer==1:
				form =viewtransform()
				return render_to_response('Ia/unremmitted_to.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def fa_unremmitted(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		if staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form = viewtransform(request.POST)
			if form.is_valid():
				mystatus=form.cleaned_data['status']
				tdate=form.cleaned_data['date']

				if mystatus =='-----':
					msg = 'select the appropriate status'
					return render_to_response('Ia/selectloan.html',{'msg':msg})

				dday,mday,yday = tdate.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				oydate=date(yday,mday,dday)
				oydate4= oydate.strftime('%A')

				thriftrec=[]


#########seperate this function into roles, admin, merchant, ccashier
				if mystatus=='DR':
					status='Sales'

					trec=tblIafieldagent.objects.filter(branch=mybranch,
						recdate=oydate,
						merchant=memmerchant)
					s =trec.aggregate(Sum('amount'))
					s=s['amount__sum']

					return render_to_response('Ia/merchant_sales.html',{'company':mybranch, 
						'date':oydate4,
						'date2':oydate, 
						'user':varuser,
						's':s,
						'thriftrec':trec,
						'status':status})


				elif mystatus=='WR':
					status='Withdrawn'

					trec=tblIapayoutrequest.objects.filter(branch=mybranch,
						recdate=oydate,
						merchant=memmerchant,
						status='DR')


					w =trec.aggregate(Sum('amount'))
					w=w['amount__sum']


					return render_to_response('Ia/merchant_widr.html',{'company':mybranch, 
						'date':oydate4,
						'date2':oydate, 
						'user':varuser,
						'w':w,
						'thriftrec':trec,
						'status':mystatus})


				elif mystatus == 'All':
					trec=[]


					withdrawals =tblIapayoutrequest.objects.filter(branch=mybranch,
						recdate=oydate,
						merchant=memmerchant,
						status='DR')

					
					for k in withdrawals:
						customer=k.customer
						amount=k.amount
						status=k.status
						j={'customer':customer,'amount':amount,'status':status}
						trec.append(j)
					


					sales=tblIafieldagent.objects.filter(branch=mybranch,
						recdate=oydate,
						merchant=memmerchant)

					for k in sales:
						customer=k.customer
						amount=k.amount
						status=k.status
						j={'customer':customer,'amount':amount,'status':status}
						trec.append(j)

					w =withdrawals.aggregate(Sum('amount'))
					w=w['amount__sum']

					s =sales.aggregate(Sum('amount'))
					s=s['amount__sum']



				return render_to_response('Ia/merchant_all.html',{'company':mybranch, 
					'date':oydate4,
					'date2':oydate, 
					'user':varuser,
					'w':w,
					's':s,
					'thriftrec':trec,
					'status':mystatus})

			
			else :
				msg = 'Fill up all boxes'
				return render_to_response('Ia/selectloan.html',{'msg':msg})


		else:
			
			if  staff.admin==1 :
				form=depreportform()
				return render_to_response('Ia/unremmitted.html',{'company':mybranch, 'user':varuser,'form':form})

			elif staff.cashier==1:
				form =viewtransform()
				return render_to_response('Ia/unremmitted_cash.html',{'company':mybranch, 'user':varuser,'form':form})

			elif staff.thrift_officer==1:
				form =viewtransform()
				return render_to_response('Ia/unremmitted_to.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')




def cashout(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']

				try:
					details=tblCUSTOMER.objects.get(branch=mybranch,wallet=mywallet,status=1)
					myform = thriftform()

					if staff.admin == 1:
						details=tblIaCUSTOMER.objects.get(customer=details,status=1)
						return render_to_response('Ia/reqcash.html',{'company':mybranch,
							'user':varuser,
							'form':myform,
							'customer':details,
							'wallet':mywallet})

					if staff.cashier == 1:
						try:

							details=tblIaCUSTOMER.objects.get(merchant=memmerchant, customer=details,status=1)
							return render_to_response('Ia/reqcash_cash.html',{'company':mybranch,
								'user':varuser,
								'form':myform,
								'customer':details,
								'wallet':mywallet})
						except:
							msg= 'Make sure you are RESPONSIBLE for this customer'
							return render_to_response('Ia/selectloan.html',{'msg':msg})

					if staff.thrift_officer == 1:
						try:

							details=tblIaCUSTOMER.objects.get(merchant=memmerchant, customer=details,status=1)
							return render_to_response('Ia/reqcash_to.html',{'company':mybranch,
								'user':varuser,
								'form':myform,
								'customer':details,
								'wallet':mywallet})
						except:
							msg= 'Make sure you are RESPONSIBLE for this customer'
							return render_to_response('Ia/selectloan.html',{'msg':msg})

				except:
					msg='INVALID WALLET ADDRESS'
					return render_to_response('Ia/selectloan.html',{'msg':msg})
			else:
				msg='Incorrect entry'
				return render_to_response('Ia/selectloan.html',{'msg':msg})

		else:
			form=viewwalletform()
			msg = ''
			if staff.admin==1:
				return render_to_response('Ia/cashout.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

			else:
				msg = 'direct all withdrawals through admin' 
				return render_to_response('Ia/selectloan.html',{'msg':msg})

			# elif staff.cashier==1:
			# 	return render_to_response('Ia/cashout_cash.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			# elif staff.thrift_officer== 1:
			# 	return render_to_response('Ia/cashout_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
	else:
		return HttpResponseRedirect('/login/user/')




def account_withdraw(request):
	if request.is_ajax():
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			acccode,wallet,month,user=acccode.split(':')
			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			if month== '-':
				msg = 'Select a month'
				return render_to_response('Ia/selectloan.html',{'msg':msg})

			if acccode== '-----' :
				msg = 'Select account type'
				return render_to_response('Ia/selectloan.html',{'msg':msg})

			try:
				www=int(month)
				monthname = calendar.month_name[www]
				acccode=str(acccode)

				memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,
					staff= staffdet ,status=1)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

				customer=tblIaCUSTOMER.objects.get(customer=customer,status=1)

				cus_thrift=tblIathrift.objects.get(
					account_type = acccode,
					branch=mybranch,
					customer=customer,
					month = monthname)

				mythrift=cus_thrift.thrift
				code = cus_thrift.code



				dll = []

				CR= tblIasavings_trans.objects.filter(
						branch=mybranch,
						customer=customer,
						code=code,
						description='CR',
						account_type = acccode).exclude(status='Account Maintenance')

				DR= tblIasavings_trans.objects.filter(
						branch=mybranch,
						customer=customer,
						code=code,
						description='DR',
						account_type = acccode)



				if CR.count() > 0 :
					cr=CR.aggregate(Sum('amount'))
					cr = cr['amount__sum']

					nc=CR.aggregate(Sum('number'))
					nc = nc['number__sum']
				else:
					cr =0
					nb=0

				if DR.count() > 0 :
					dr=DR.aggregate(Sum('amount'))
					dr = dr['amount__sum']
					nd=DR.aggregate(Sum('number'))
					nd= nd['number__sum']

				else:
					dr = 0
					nd=0

				add = cr - dr
				number =nc - nd



				jdjd= {'amount':add,'num':number,'thrift':mythrift}

				dll.append(jdjd)

				if staff.admin==1: #for direct withdrwal
					return render_to_response('Ia/withdrr.html',{'thriftrec':dll, 'wallet':wallet,'month':www,'monthname':monthname, 'account_type':acccode,'thrift':mythrift})
				if staff.cashier==1: #for indirect withdrwal
					return render_to_response('Ia/withdrr.html',{'thriftrec':dll, 'wallet':wallet,'month':www,'account_type':acccode,'thrift':mythrift})
				if staff.thrift_officer==1: #for indirect withdrwal
					return render_to_response('Ia/withdrr.html',{'thriftrec':dll, 'wallet':wallet,'month':www,'account_type':acccode,'thrift':mythrift})



			except :
				transit = tblpayoutrequest.objects.filter(
					status='Unpaid',
					branch=mybranch,
					account_type=acccode,
					customer=customer,
					wallet_type='Main',
					recdate__month=www)

				job_count = transit.count()

				if job_count > 0 :
					add=transit.aggregate(Sum('amount'))
					add = add['amount__sum']

					msg = add, 'requested'

				else :
					paid =tblIapayoutrecord.objects.filter(
						status='Paid',
						branch=mybranch,
						account_type=acccode,
						wallet_type='Main',
						recdate__month=www,
						customer=customer)
					paid_paid = paid.count()

					if paid_paid > 0 :

						add=paid.aggregate(Sum('amount'))
						add = add['amount__sum']

						msg	= add , 'Withdrawn by you'

					else:
						msg= 'No record found'

				msg=msg
				return render_to_response('Ia/selectloan.html',{'msg':msg})


		else:
			return HttpResponseRedirect('/dalogin/')

	else:
		return HttpResponseRedirect('/dalogin/')





def cashoutrequest(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'
			return render_to_response('Ia/selectloan.html',{'msg':msg})

		if staff.admin==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']
			month =request.POST['month'] #month_index
			account =request.POST['account'] #account_type
			withdrrr =request.POST['withdrr'] #account_type

			try:
				withdrrr = int(withdrrr)
			except:
				msg = 'Bad Entry'
				return render_to_response('Ia/selectloan.html',{'msg':msg})


			monthname = calendar.month_name[int(month)]

			myydate = date.today() #the date the merchant made the request
			year = myydate.year

			customer=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,status=1)

			email=customer.email
			customer=tblIaCUSTOMER.objects.get(branch=mybranch, customer=customer,status=1)

			thriftt= tblIathrift.objects.get(branch=mybranch,
				month=monthname,
				account_type=account,
				year=year,
				customer=customer)

			code=thriftt.code

			thrift=thriftt.thrift

			CR= tblIasavings_trans.objects.filter(
				branch=mybranch,
				customer=customer,
				code=code,
				description='CR',
				account_type = account).exclude(status='Account Maintenance')


			DR= tblIasavings_trans.objects.filter(
				branch=mybranch,
				customer=customer,
				code=code,
				description='DR',
				account_type = account)



			if CR.count() > 0 :
				cr=CR.aggregate(Sum('number'))
				cr = cr['number__sum']
			else:
				cr =0

			if DR.count() > 0 :
				dr=DR.aggregate(Sum('number'))
				dr = dr['number__sum']
			else:
				dr = 0

			number = cr - dr



			# msg = number - withdrrr
			# return render_to_response('Ia/selectloan.html',{'msg':msg})

			if number - withdrrr >= 0:
				ggg = thrift * withdrrr

				generate_trans_pin()

				tblIamerchantBank(branch=mybranch,
					merchant=memmerchant,
					customer=customer,
					account_type=account,
					recdate=myydate,
					transac_id=generate_trans_pin(),
					status='DR',
					amount=ggg,
					code=code,
					number=withdrrr,
					approved_by=varuser,
					transdate=myydate,
					wallet_type='Main').save()

				tblIasavings_trans(branch=mybranch,
					status='Withdrawn',
					transdate=myydate,
					account_type=account,
					description='DR',
					customer=customer,
					number=withdrrr,
					wallet_type = 'Main',
					amount=ggg,
					avalability='Not Available',
					merchant=memmerchant,
					transac_id=generate_trans_pin(),
					recdate=myydate,
					code =code).save()


				try:
					withdraw_email(email)
				except:
					iu=0

				return render_to_response('Ia/payoutsuccess.html',{'company':mybranch, 
					'customer':customer, 
					'tot':ggg,
					'user':varuser})
			else:
				msg = 'Number too large'
				return render_to_response('Ia/selectloan.html',{'msg':msg})

        


		else:
			return HttpResponseRedirect('/fts/thrift/cashout/')


	else:
		return HttpResponseRedirect('/login/user/')

def individual(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		if staff.cashier==0:
			return render_to_response('Ia/404.html',{'company':mybranch,'user':varuser})

		if request.method == 'POST':
			form = remittalform(request.POST)
			if form.is_valid():
				merchant =form.cleaned_data['merchant']
				mydate2=form.cleaned_data['date']  #JavaScript Date Object

				yday,mday,dday = mydate2.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday) #Python Date Object

        		try:
        		    memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant,status=1,branch=mybranch)
        		except:
        		    form=remittalform()
        		    msg = 'INVALID MERCHANT ID'
        		    return render_to_response('Ia/remittals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

        		ddt=[]
        		thriftrec= tblIasavings_trans.objects.filter(
        			branch=mybranch,
        			merchant=merchant,
					recdate=mydate,
					wallet_type='Main',
					remitted='Unremmitted',
					approved='Not Approved')

        		mycount= thriftrec.count()

        		if mycount >0:
        			add=thriftrec.aggregate(Sum('amount'))
        			add = add['amount__sum']
        			dl={'amount':add}
        			ddt.append(dl)

        			return render_to_response('Ia/remhistory.html',{'company':mybranch,'dates':mydate2,
        				'merchant':memmerchant,
        				'user':varuser,'thriftrec':ddt,
        				'date':mydate,'ttt':thriftrec})

        		else:
        			msg ='NO TRANSACTION FOUND'
		else:
			form=remittalform()
			msg=''
		return render_to_response('Ia/remittals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def reedit(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		merchant,trandate=acccode.split(':')

        	dday,mday,yday = trandate.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	mydatwwwe=date(yday,mday,dday)

        	merchant1=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant,status=1)
        	mybranch=merchant1.branch.id

    		ddt=[]

    		thriftrec= tblIafieldagent.objects.filter(
    			branch=mybranch,
    			merchant=merchant1,
				recdate=mydatwwwe,
				wallet_type='Main',
				status='Received')

    		mycount= thriftrec.count()

    		if mycount >0:
    			add=thriftrec.aggregate(Sum('amount'))
    			add = add['amount__sum']
    			dl={'amount':add}
    			ddt.append(dl)
    		# tot=

    			return render_to_response('Ia/app_all.html',{
    				'company':mybranch,
    				'dates':trandate,
    				'merchant':merchant1,
    				'thriftrec':ddt,
    				'tot':add,
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
    		state,trandate=acccode.split(':')

    		try:
	    		mycom = tblIafieldagent.objects.get(id=state, status='Received') #details of the trans on merchant tab

	    		return render_to_response('Ia/app_trans.html',{'income':mycom,'date1':trandate})

	    	except :
				msg='error !!!'
				return render_to_response('Ia/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def approveone(request):
    if 'userid' in request.session:
        varuser=request.session['userid']


        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ia/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.admin==0 :
    		return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
        	merchant2=request.POST['merchant']
        	transid = request.POST['trans']
        	cash =request.POST['cash'] #posted
        	amount =request.POST['mmm'] #carry come
        	mydate2=request.POST['date1'] #Javascript date object

        	amount=int(amount)
        	cash=int(cash)


        	dday,mday,yday = mydate2.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	mydate=date(yday,mday,dday) #python date object

        	fdate= date.today() #record date, the date you took record
        	remterr=date(fdate.year,fdate.month,fdate.day)
        	merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)

        	merchant=tblIaMERCHANT.objects.get(staff=merchant,thrift1a=1) #admin

        	merchant2=tblIaMERCHANT.objects.get(id=merchant2)

        	ttt =tblIafieldagent.objects.get(id=transid,status='Received')
        	code = ttt.code
        	thrift = int(ttt.amount / ttt.number)
        	transdate = ttt.recdate #date the original transaction happened
        	account_type=ttt.account_type
        	customer = ttt.customer.customer.id
        	number= ttt.number
        	transaction_id=ttt.transac_id

        	pl= number-1


        	customer=tblCUSTOMER.objects.get(branch=mybranch, id=customer)
        	customer=tblIaCUSTOMER.objects.get(customer=customer)
        	wallet=customer.customer.wallet

        	# monthname = calendar.month_name[fdate.month]
        	th = tblIathrift.objects.get(branch=mybranch,account_type=account_type,customer=customer,code=code,year =fdate.year)
        	code = th.code

        	ddt=[]

        	# p = (monthrange(fdate.year, fdate.month))[-1]
        	p=31


        	new_amount = amount - thrift

        	# msgk = p, number,pl,l # return render_to_response('Ia/selectloan.html',{'msg':msgk})

        	if amount == cash :
        		mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch, customer=customer, transdate=transdate, description='CR',  account_type = account_type, wallet_type='Main')

        		kdf= mont_contribution.count()

        		if kdf == 0 :
        			add_count = 0
        		else:
        			add_count = mont_contribution.aggregate(Sum('number'))
        			add_count = add_count['number__sum']

        		if add_count + number <= p:
        			# msgk = add_count , lump , p
        			# return render_to_response('Ia/selectloan.html',{'msg':msgk})

        			if add_count == 0:
        				if number == 1:
        					try:
        						tblIamerchantBank.objects.get(branch=mybranch,merchant=merchant2,code=code,customer=customer,number=1, transdate=transdate, amount=amount,account_type = account_type,wallet_type='Main',approved_by=varuser)

        					except:
								tblIamerchantBank(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id, customer=customer,number=1,recdate=fdate,transdate=transdate, amount=amount,account_type = account_type,wallet_type='Main',approved_by=varuser,status='CR').save()
								tblIasavings_trans(branch=mybranch, merchant=merchant2, code=code, transac_id= transaction_id,customer=customer, number=1,transdate=transdate, recdate=fdate,amount=amount, description='CR', account_type = account_type,  wallet_type='Main',  avalability='Not Available', status='Account Maintenance').save()
								ttt.status = 'Approved'
								ttt.save()
								return render_to_response('Ia/apsuccess.html',{'company':mybranch,'user':varuser,'customer':customer,'wallet':wallet,'amount':amount})

        				elif number > 1:
							try:
								tblIamerchantBank.objects.get(branch=mybranch,merchant=merchant2,code=code,customer=customer,number=number,transdate=transdate, amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main')
							except :
								tblIamerchantBank(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id,customer=customer,number=number,transdate=transdate ,recdate=fdate, amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main',status='CR').save()
								tblIasavings_trans(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id,customer=customer,number=1,transdate=transdate,recdate= fdate,amount=thrift,description='CR',account_type = account_type,wallet_type='Main',avalability='Not Available',status='Account Maintenance').save()
								tblIasavings_trans(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id,customer=customer,number=pl,transdate=transdate,recdate=fdate,amount=new_amount,description='CR',account_type = account_type,wallet_type='Main',avalability='Available',status='Available').save()
								ttt.status = 'Approved'
								ttt.save()
								return render_to_response('Ia/apsuccess.html',{'company':mybranch,'user':varuser,'customer':customer,'wallet':wallet,'amount':amount})

        			elif add_count > 0:
						try:
							tblIamerchantBank.objects.get(branch=mybranch,merchant=merchant2,code=code,customer=customer,number=number,transdate=transdate, account_type = account_type,approved_by=varuser,wallet_type='Main')
							msg = "you cant post same money twice same day"
						except:
							tblIamerchantBank(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id,customer=customer,number=number,transdate=transdate, recdate=fdate,amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main',status='CR').save()
							tblIasavings_trans(branch=mybranch,	merchant=merchant2, code=code, transac_id= transaction_id, customer=customer,number=number,transdate=transdate, recdate=fdate,amount=amount, description='CR',account_type = account_type, wallet_type='Main',avalability='Available', status='Available').save()
							ttt.status = 'Approved'			
							ttt.save()
							return render_to_response('Ia/apsuccess.html',{'company':mybranch,'user':varuser,'customer':customer,'wallet':wallet,'amount':amount})


        		else:
        			msg = "Amount too large"
        	else:
        		msg = 'amount not applicable'
        	return render_to_response('Ia/selectloan.html',{'msg':msg})

        else:
        	return HttpResponseRedirect('/fts/thrift/approvals/')


    else:
    	return HttpResponseRedirect('/login/user/')



def approveind(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		if staff.admin==0 :
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			merchant =request.POST['merchant']
			mydate2=request.POST['cdate']  #JavaScript Date Object
			cid = request.POST['cid']
			amount=request.POST['total']
			account_type=request.POST['account_type']
			transid=request.POST['transid']

			yday,mday,dday = mydate2.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #Python Date Object

			customer = tblCUSTOMER.objects.get(id =cid,status=1)
			customer1=customer.id
			mymerchant= tblIaMERCHANT.objects.get(thrift1a =1,id=merchant,status=1)

			myadmin = tblIamerchantBank.objects.get(id = transid)

			add =myadmin.amount
			remtotal=myadmin.amount

			return render_to_response('Ia/approvalindv.html',{'company':mybranch,
				'merchant':mymerchant,'customer':customer1,
				'user':varuser,'date':mydate,
				'thriftrec':myadmin, 'trannsid':transid,
				'cdate':mydate2,'total':add,'rem':remtotal})

	else:
		return HttpResponseRedirect('/logout/')


def approveindividualcash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ia/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.admin==0 :
    		return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
        	merchant =request.POST['merchant']
    		mydate=request.POST['date']
    		customer=request.POST['customer'] #already a database instance
    		amount=request.POST['rem']
    		transid=request.POST['transid']

    		yday,mday,dday = mydate.split('/')

    		yday=int(yday)
        	mday=int(mday)
    		dday=int(dday)

    		transdate=date(yday,mday,dday)
    		ddt=[]

    		merchant=tblIaMERCHANT.objects.get(thrift1a =1,status=1,id=merchant)

    		remit = tblIamerchantBank.objects.get( id = transid)

    		account_type=remit.account_type
    		code=remit.code

    		customer=tblCUSTOMER.objects.get(id=customer,status=1)

    		mythrift=tblIathrift.objects.get(account_type = account_type,branch=mybranch,
            	customer=customer,number=mday,year=yday)

    		customer_thrift = mythrift.thrift

    		number= remit.amount / customer_thrift

    		pl= number-1

    		new_amount = remit.amount - customer_thrift

    		mont_contribution = tblIathrift_trans.objects.filter(account_type =account_type ,wallet_type='Main', branch=mybranch,
    			merchant=merchant,
                customer=customer,recdate__month=mday).count()


        	if mont_contribution < 1:

        		if number == 1:
        			tblIathrift_trans(
        				account_type = account_type,
        				wallet_type='Main',
        				branch=mybranch,
                    	code=code,
                    	merchant=merchant,
                    	customer=customer,
                        number=1,
                        recdate=transdate,
                        amount=customer_thrift,
                        avalability='Not Available',
                        reason='Account Maintenance').save()

        		else :
        			tblIathrift_trans(
        				account_type = account_type,
        				wallet_type='Main',
        				branch=mybranch,
                    	code=code,
                    	merchant=merchant,
                    	customer=customer,
                        number=1,
                        recdate=transdate,
                        amount=customer_thrift,
                        avalability='Not Available',
                        reason='Account Maintenance').save()

        			tblIathrift_trans(
        				account_type = account_type,
        				wallet_type='Main',
        				branch=mybranch,
                    	code=code,
                    	merchant=merchant,
                    	customer=customer,
                        number=pl,
                        recdate=transdate,
                        amount=new_amount,
                        avalability='Available',
                        reason='Available').save()

    		else:
    			tblIathrift_trans(
    				account_type = account_type,
    				wallet_type='Main',
                	branch=mybranch,
                	merchant=merchant,
                	customer=customer,
                    number=number,
                    recdate=transdate,
                    amount=remit.amount,
                    code=code,
                    avalability='Available',
                    reason='Available').save()

    		remit.status='Approved'
    		remit.approved_by=varuser
    		remit.save()

        	return render_to_response('Ia/approve_success.html',{'company':mybranch,'tot':1,'user':varuser})

        else:
            form=remittalform()
        return render_to_response('Ia/remittals.html',{'company':mybranch, 'user':varuser,'form':form})

    else:
        return HttpResponseRedirect('/login/user/')



def approvebulkcash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']


        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ia/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.admin==0 :
    		return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

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

        	fdate= date.today() #record date, the date you took record
        	remterr=date(fdate.year,fdate.month,fdate.day)
        	merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)

        	merchant=tblIaMERCHANT.objects.get(staff=merchant,thrift1a=1)


        	merchant2=tblIaMERCHANT.objects.get(id =credit_officer)
        	# merchant2=tblIaMERCHANT.objects.get(id=credit_officer)

        	ttt =tblIafieldagent.objects.filter(branch=mybranch,recdate=mydate, status='Received', merchant=merchant2)


        	if amount1 == cash :


	        	for ttt in ttt :
	        		thrift = int(ttt.amount / ttt.number)

	        		transaction_id =0

	        		# generate_trans_pin()
	        		# transaction_id = ttt.transaction_id #ttt.transac_id
	        		transaction_id = ttt.transac_id
		        	transdate = ttt.recdate #date the original transaction happened
		        	account_type=ttt.account_type
		        	customer = ttt.customer.customer.id
		        	amount=ttt.amount
		        	customer=tblCUSTOMER.objects.get(branch=mybranch, id=customer)
		        	customer=tblIaCUSTOMER.objects.get(customer=customer)
		        	wallet=customer.customer.wallet

		        	code=ttt.code

		        	number= ttt.number
		        	pl= number-1
		    

		        	ddt=[]

		        
		        	p=31


		        	new_amount = amount - thrift

	        	# msgk = p, number,pl,l return render_to_response('Ia/selectloan.html',{'msg':msgk})

	        		mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch, customer=customer, transdate=transdate, description='CR',  account_type = account_type, wallet_type='Main')

	        		kdf= mont_contribution.count()

	        		if kdf == 0 :
	        			add_count = 0
	        		else:
	        			add_count = mont_contribution.aggregate(Sum('number'))
	        			add_count = add_count['number__sum']

	        		if add_count + number <= p:
	        			if add_count == 0:
	        				if number == 1:
	        					try:
	        						tblIamerchantBank.objects.get(branch=mybranch,merchant=merchant2,code=code,customer=customer,number=1, transdate=transdate, amount=amount,account_type = account_type,wallet_type='Main',approved_by=varuser)

	        					except:
									tblIamerchantBank(branch=mybranch,merchant=merchant2,code=code,transac_id=transaction_id, customer=customer,number=1,recdate=fdate,transdate=transdate, amount=amount,account_type = account_type,wallet_type='Main',approved_by=varuser,status='CR').save()
									tblIasavings_trans(branch=mybranch, merchant=merchant2, transac_id=transaction_id,code=code, customer=customer, number=1,transdate=transdate, recdate=fdate,amount=amount, description='CR', account_type = account_type,  wallet_type='Main',  avalability='Not Available', status='Account Maintenance').save()
									ttt.status='Approved'
									ttt.save()
									# return render_to_response('Ia/apsuccess.html',{'company':mybranch,'user':varuser,'wallet':wallet,'amount':amount})

	        				elif number > 1:
								try:
									tblIamerchantBank.objects.get(branch=mybranch,merchant=merchant2,code=code,customer=customer,number=number,transdate=transdate, amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main')
								except :
									tblIamerchantBank(branch=mybranch,merchant=merchant2,code=code,transac_id=transaction_id,customer=customer,number=number,transdate=transdate ,recdate=fdate, amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main',status='CR').save()
									tblIasavings_trans(branch=mybranch,merchant=merchant2,transac_id=transaction_id,code=code,customer=customer,number=1,transdate=transdate,recdate= fdate,amount=thrift,description='CR',account_type = account_type,wallet_type='Main',avalability='Not Available',status='Account Maintenance').save()
									tblIasavings_trans(branch=mybranch,merchant=merchant2,transac_id=transaction_id,code=code,customer=customer,number=pl,transdate=transdate,recdate=fdate,amount=new_amount,description='CR',account_type = account_type,wallet_type='Main',avalability='Available',status='Available').save()
									ttt.status='Approved'	
									ttt.save()
									# return render_to_response('Ia/apsuccess.html',{'company':mybranch,'user':varuser,'wallet':wallet,'amount':amount})

	        			elif add_count > 0:
							try:
								tblIamerchantBank.objects.get(branch=mybranch,merchant=merchant2,code=code,customer=customer,number=number,transdate=transdate, account_type = account_type,approved_by=varuser,wallet_type='Main')
								msg = "you cant post same money twice same day"
							except:
								tblIamerchantBank(branch=mybranch,merchant=merchant2,code=code,transac_id=transaction_id,customer=customer,number=number,transdate=transdate, recdate=fdate,amount=amount,account_type = account_type,approved_by=varuser,wallet_type='Main',status='CR').save()
								tblIasavings_trans(branch=mybranch,	merchant=merchant2, transac_id=transaction_id,code=code, customer=customer,number=number,transdate=transdate, recdate=fdate,amount=amount, description='CR',account_type = account_type, wallet_type='Main',avalability='Available', status='Available').save()
								ttt.status='Approved'	
								ttt.save()

	        		else:
	        			msg = "Amount too large"
	        			return render_to_response('Ia/selectloan.html',{'msg':msg})

	        	msg = " "
	        	return render_to_response('Ia/all_app_success.html',{'company':mybranch,'user':varuser,'amount':amount1})


        	else:
        		msg = 'amount not applicable'

		return render_to_response('Ia/selectloan.html',{'msg':msg})


    else:
    	return HttpResponseRedirect('/login/user/')



def all(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		if staff.cashier==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
			# return render_to_response('Ia/404.html')

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

		memmerchant=tblIaMERCHANT.objects.filter(staff=memstaff,thrift1a=1, status=1)

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
							thrifing= tblIasavings_trans.objects.filter(branch=mybranch,
								recdate=mydate,wallet_type='Main',remitted='Unremmitted',merchant=merchant)

							mycount= thrifing.count()

							if mycount >0:
								add=thrifing.aggregate(Sum('amount'))
								add = add['amount__sum']
								dl={'date':mydate,'amount':add,'merchant':merchant,'remitted':'Unremmitted'}
								ddt.append(dl)
							else:
								pass

				return render_to_response('Ia/allrem.html',{'company':mybranch, 'user':varuser,'thriftrec':ddt,'date':mydate})

		else:
			form=viewremallform()
		return render_to_response('Ia/all.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')


def report(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.cashier==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

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

				allmerchant = tblIaMERCHANT.objects.filter(branch=mybranch,status=1)
				remm=[]
				all_data=[]

				if 'checkbox' in request.POST:
					checkbox=request.POST['checkbox']
				else:
					checkbox=1

				if checkbox==1:
					if status == 'Remitted':
						for k in allmerchant:
							thriftrec= tblIamerchantBank.objects.filter(branch=mybranch,recdate=mydate,merchant=k)
							add=0
							add = thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']
							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)

					elif status == 'Unremmitted':
						for p in allmerchant:
							thriftrec= tblIasavings_trans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=mydate,merchant=p)
							add =0

							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':p,'amount':add}
								remm.append(gh)

					return render_to_response('Ia/remreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'status':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):
						realdate = date(yday,mday,n)
						k =0
						if status=='Remitted':
							for mn in allmerchant:
								thriftrec= tblIamerchantBank.objects.filter(branch=mybranch,recdate=realdate,merchant=mn)
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
								thriftrec= tblIasavings_trans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)
							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

					return render_to_response('Ia/histremreport.html',{'company':mybranch, 'user':varuser,
						'thriftrec':all_data,'month':month,'year':yday,'status':status})

		else:
			form=viewallremittedform()
		return render_to_response('Ia/report.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def approvalsmenu(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.admin ==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':

			merchant_id=request.POST['merchant']
			mydate=request.POST['date'] #js date object
			yday,mday,dday=mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			transdate=date(yday,mday,dday)

			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant_id, status=1)

			remit = tblIamerchantBank.objects.filter(
				branch=mybranch,
				recdate = transdate,
				merchant=memmerchant,
				status='Remitted')


			remamount = tblIamerchantBank.objects.filter(
				branch=mybranch,
				recdate=transdate,
				merchant=memmerchant,
				status='Remitted')

			ggt=[]

			for k in remit:
				name=k.customer.surname + "   "+k.customer.firstname
				customer=k.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)
				account_type=k.account_type

				cus_thrift = tblIathrift.objects.get(
					customer=customer,
					# merchant=memmerchant,
					number = mday,
					account_type=account_type,
					year=yday)
				cus_thrift=cus_thrift.thrift
				df={'thrift':cus_thrift,'amount':k.amount,'name':name,'status':'Not Approved'}
				ggt.append(df)

			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)


			remtotal=remamount.aggregate(Sum('amount'))
			remtotal = remtotal['amount__sum']
			remtotal = int(remtotal)

			return render_to_response('Ia/approvalhistory.html',{
				'company':mybranch,
				 'merchant':memmerchant,
				 'user':varuser,
				 'date':transdate,
				 'thriftrec':ggt,
				 'cdate':mydate,
				 'total':add,
				 'rem':remtotal})

	else:
		return HttpResponseRedirect('/login/user/')

def approvecash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
        	staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
        	msg = ' your account is not active for this service, kindly contact your boss'
        	return render_to_response('Ia/selectloan.html',{'msg':msg})

        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.admin==0:
    		return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
            merchant =request.POST['merchant']

            mydate=request.POST['date'] #JS date object
            dday,mday,yday = mydate.split('/')
            yday=int(yday)
            mday=int(mday)
            dday=int(dday)
            transdate=date(yday,mday,dday) #python date object

            ddt=[]
            merchant=tblIaMERCHANT.objects.get(thrift1a =1,status=1,id=merchant)

            remit = tblIamerchantBank.objects.filter(
            	branch=mybranch,
            	merchant=merchant,
            	recdate = transdate,
            	status='Remitted')

            msg='wahalla'

            count=remit.count()

            for k in remit:
            	code=k.code
            	amount=k.amount
            	customer=k.customer.id
            	account_type=k.account_type
            	customer=tblCUSTOMER.objects.get(id=customer,status=1)
            	mythrift=tblIathrift.objects.get(
		        	account_type = account_type,
		        	branch=mybranch,
		        	customer=customer,
		        	number = mday,
		        	year=yday)
            	customer_thrift = mythrift.thrift
            	number= int(amount / customer_thrift)

            	pl= number-1
            	new_amount = amount - customer_thrift

            	mont_contribution = tblIathrift_trans.objects.filter(
		        	account_type = account_type,
		        	wallet_type='Main',
		        	branch=mybranch,
		        	merchant=merchant,
		            customer=customer,
		            recdate__month=mday).count()

            	if mont_contribution < 1:

            		if number == 1:
            			msg = 'i am 1'
            			tblIathrift_trans(
		                	branch=mybranch,
		                	merchant=merchant,
		                	code=code,
		                	customer=customer,
		                    number=1,
		                    recdate=transdate,
		                    amount=customer_thrift,
		                    account_type = account_type,
		                    wallet_type='Main',
		                    avalability='Not Available',
		                    reason='Account Maintenance').save()

            		elif number > 1:
            			msg = ' i  am 2'
            			tblIathrift_trans(
		                	branch=mybranch,
		                	merchant=merchant,
		                	code=code,
		                	customer=customer,
		                	number=1,
		                	recdate=transdate,
		                	amount=customer_thrift,
		                	account_type = account_type,
		                	wallet_type='Main',
		                    avalability='Not Available',
		                    reason='Account Maintenance').save()

            			tblIathrift_trans(
		                	branch=mybranch,
		                	merchant=merchant,
		                	code=code,
		                	customer=customer,
		                    number=pl,
		                    recdate=transdate,
		                    amount=new_amount,
		                    account_type = account_type,
		                    wallet_type='Main',
		                    avalability='Available',
		                    reason='Available').save()

            	elif mont_contribution > 0 :
            		msg = 'i am 3'
            		tblIathrift_trans(
		            	account_type = account_type,
		            	wallet_type='Main',
		            	branch=mybranch,
		            	merchant=merchant,
		            	customer=customer,
		                code=code,
		                number=number,
		                recdate=transdate,
		                amount=k.amount,
		                avalability='Available',
		                reason='Available').save()

            	k.status='Approved'
            	k.approved_by=varuser
            	k.save()

            msg=msg
            # return render_to_response('Ia/selectloan.html',{'msg':msg})


            return render_to_response('Ia/apsuccess.html',{'company':mybranch,'tot':count,'user':varuser})

        else:
        	form=remittalform()
        return render_to_response('Ia/remittals.html',{'company':mybranch, 'user':varuser,'form':form})

    else:
    	return HttpResponseRedirect('/login/user/')


def approvals(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.admin==0 :
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewmerchantform(request.POST)
			if form.is_valid():
				merchant2=form.cleaned_data['merchant']
				mydate=form.cleaned_data['date']


				memmerchant=tblIaMERCHANT.objects.filter(staff=memstaff,thrift1a=1, status=1).count()

				if staff.admin==0  or memmerchant<1: #the admin
					return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
				else:
					memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,thrift1a=1, status=1)


				try:#the merchant
				 	merchanttrans=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,id=merchant2, status=1)
				except:
				 	msg = ' invalid merchant ID'
				 	return render_to_response('Ia/selectloan.html',{'msg':msg})


				dday,mday,yday=mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				monthname = calendar.month_name[int(mday)]

				transdate=date(yday,mday,dday)

				remit = tblIafieldagent.objects.filter(branch=mybranch,
					merchant=merchanttrans,
					recdate = transdate,
					status='Received')

				count=remit.count()
				# ggt=[]

				if count>0:
					kpp=[]

					for k in remit:
						thriftt= tblIathrift.objects.get(branch=mybranch, code=k.code)
						month=thriftt.month
						amount=k.amount
						customer=tblIaCUSTOMER.objects.get(branch=mybranch,id=k.customer.id)
						s={'month':month,'amount':amount,'customer':customer,'id':k.id}
						kpp.append(s)

					add=remit.aggregate(Sum('amount'))
					add = add['amount__sum']
					add = int(add)

					return render_to_response('Ia/ppp.html',{'company':mybranch,
						'account_type':account_type,
						'merchant':merchanttrans,
						'user':varuser,
						'thriftrec':kpp,# remit,
						'dates':transdate,
						'cdate':mydate,
						'total':add,
						})
				else:
					msg ="NO RECORDS FOUND"
					return render_to_response('Ia/selectloan.html',{'msg':msg})
			else:
				msg= 'Fill all boxes'
				return render_to_response('Ia/selectloan.html',{'msg':msg})
		else:
			form=viewmerchantform()
		return render_to_response('Ia/approvals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})




def approvalsmenuyes(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
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
	
	 	merchanttrans=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,id=merchant2, status=1)

		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)

		try:

			remit = tblIafieldagent.objects.get( id =trans_id,
				branch=mybranch,
				merchant=merchanttrans,
				wallet_type='Main',
				recdate = transdate,
				status='Received').delete()
		except:
			pass


			###add a delete notification


		remit = tblIafieldagent.objects.filter( branch=mybranch,
			merchant=merchanttrans,
			wallet_type='Main',
			recdate = transdate,
			status='Received')

		count=remit.count()
		# ggt=[]

		if count>0:

			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render_to_response('Ia/ppp.html',{'company':mybranch,
				'merchant':merchanttrans,
				'user':varuser,
				'thriftrec':remit,
				'dates':transdate,
				'cdate':mydate,
				'total':add,
				})
		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')

	else:
		return HttpResponseRedirect('/login/user/')


def allapproval(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		if staff.admin==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
			# return render_to_response('Ia/404.html')

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
			form=viewallremittedform()
		return render_to_response('Ia/all_to.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')



def approvereport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form  = form=viewallapprovedform(request.POST)
			status =request.POST['status']
			mydate=request.POST['date'] #javascript date object
			dday,mday,yday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object
			realmonth=calendar.month_name[mday]

			allmerchant = tblIaMERCHANT.objects.filter(branch=mybranch,status=1,thrift1a=1)


			if status =='Approvals':

				transaction_source = tblIafieldagent.objects.filter(branch=mybranch,
					status='Approved',wallet_type='Main',recdate=mydate)
				remm=[]
				all_data=[]

				for k in transaction_source:
					pl=k.merchant.id
					all_data.append(pl)

				msg=list(dict.fromkeys(all_data)) # remove duplicates from list

				for mm in msg:
					merchant = tblIaMERCHANT.objects.get(branch=mybranch,id=mm)
					transs = tblIafieldagent.objects.filter(branch=mybranch,
						status='Approved',merchant=mm, wallet_type='Main',recdate=mydate)
					total =transs.aggregate(Sum('amount'))
					total=total['amount__sum']
					mit = {'merchant':merchant,'trans':transs,'total':total}
					remm.append(mit)


				return render_to_response('Ia/appreport.html',{'company':mybranch, 'user':varuser,
						'thriftrec':remm,'date':mydate,'status':status})

			if status =='All':

				transaction_source = tblIafieldagent.objects.filter(branch=mybranch,
					status='Approved',wallet_type='Main',recdate=mydate)
				remm=[]
				all_data=[]
				tot=0

				for k in transaction_source:
					pl=k.merchant.id
					all_data.append(pl)

				msg=list(dict.fromkeys(all_data)) # remove duplicates from list

				for mm in msg:
					merchant = tblIaMERCHANT.objects.get(branch=mybranch,id=mm)
					transs = tblIafieldagent.objects.filter(branch=mybranch,
						status='Approved',merchant=mm, wallet_type='Main',recdate=mydate)
					total =transs.aggregate(Sum('amount'))
					total=total['amount__sum']
					tot = tot + total 
					mit = {'merchant':merchant,'total':total, 'status':'Approved'}
					remm.append(mit)


				return render_to_response('Ia/appreport_all.html',{'company':mybranch, 'user':varuser,
						'thriftrec':remm,'date':mydate,'status':status,'tot':tot})




			return render_to_response('Ia/monthrep.html',{'company':mybranch, 'user':varuser,
					'thriftrec':all_data,'status':status,'month':realmonth,'year':yday})


		else:
			form=viewallapprovedform()
		return render_to_response('Ia/approvalsreport.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')


def payout(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 :
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewmerchantform(request.POST)
			if form.is_valid():
				merchant=form.cleaned_data['merchant']

				datte=form.cleaned_data['date'] #JS date Object
				dday,mday,yday = datte.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				month=calendar.month_name[mday] #month_index to month_name

				mydate=date(yday,mday,dday)

				try:
					memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant,status=1,branch=mybranch)
				except:
					return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
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

				return render_to_response('Ia/adminpayout.html',
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
		return render_to_response('Ia/payout.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')





def withdrawoptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')
    		customer=tblCUSTOMER.objects.get(id=state)

    		return render_to_response('Ia/adminwithdrawfund.html',{
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
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 :
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

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
			merchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant)


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

					transactions = tblIathrift_trans.objects.filter(
						branch=mybranch,
						account_type = account_type[0],
						customer=customer,
						wallet_type='Main',
						avalability='Not Available',
						reason='requested',
						recdate=account_type[1],
						merchant=merchant).delete()


					bankk = tblIamerchantBank.objects.filter(
						status= 'Approved',
						branch=mybranch,
						account_type=	account_type[0],
						wallet_type='Main',
						merchant=merchant,
						recdate=account_type[1],
						customer=customer).delete()

				thrift = tblIathrift.objects.get(
					account_type = account_type[0],
					branch = mybranch,
					customer=customer,
					number=month,
					year=year)

				thrift_mi=int(thrift.thrift)

				transactions = tblIathrift_trans.objects.get(
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
				return render_to_response('Ia/reqestwithdrawsuccess.html',{
						'company':mybranch,
						'user':varuser,
						'amount':payable_sum,
						'customer':customer})
			else :
				msg = N,payable_sum, 'cash withdrawn'
				return render_to_response('Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/thrift/thrift/payouts/')
	else:
		return HttpResponseRedirect('/login/user/')





def canceloptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate,merchant=acccode.split(':')
    		customer=tblIafieldagent.objects.get(id=state, status='Received')

    		return render_to_response('Ia/delsales.html',{'date1':trandate,
    			'trans_id':state,'hhh':customer,'merchant':merchant})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def cancelreq(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 :
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

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
			merchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant)

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

					transactions = tblIathrift_trans.objects.get(
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
				return render_to_response('Ia/reqestcancel.html',{
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
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 :
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':

			merchant= request.POST['merchant']
			datte=request.POST['date'] #date the request was made

			merchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant,status=1)

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


			transactions = tblIathrift_trans.objects.filter(
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

			return render_to_response('Ia/adminpayoutsuccess.html',{'count':mycount,'company':mybranch,'merchant':merchant,'user':varuser})

		else:
			form=viewmerchantform()
		return render_to_response('Ia/payout.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def payoutreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		if staff.thrift_officer==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
			# return render_to_response('Ia/404.html')

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

				allmerchant = tblIaMERCHANT.objects.filter(branch=mybranch,status=1)
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

					return render_to_response('Ia/payoutdayreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'fund':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):
						realdate = date(yday,mday,n)
						k =0
						if status=='Remitted':
							for mn in allmerchant:
								thriftrec= tblIamerchantBank.objects.filter(branch=mybranch,recdate=realdate,merchant=mn)
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
								thriftrec= tblIasavings_trans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
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
		return render_to_response('Ia/payoutreport.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')




#######******** ceo reports *********************
def repome(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		return render_to_response('Ia/reporthome.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')




def merchantreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})
		if staff.ceo !=1:
			msg='error'
			return render_to_response('Ia/selectloan.html',{'msg':msg, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		form=performanceform()
		return render_to_response('Ia/reportmerchant.html',{'company':mybranch,'form':form, 'user':varuser})

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

                tuy = tblIasavings_trans.objects.filter(branch=bra,description='CR').exclude(status='Account Maintenance')

                guy = tblIasavings_trans.objects.filter(branch=bra,description='DR')

                
            	addw = tuy.aggregate(Sum('amount'))
            	add = addw['amount__sum']

            	ddd = guy.aggregate(Sum('amount'))
            	ddd = ddd['amount__sum']

            	if add < 1:
            		add = 0

            	if ddd < 1:
            		ddd = 0
            	sdd = add - ddd

                return render_to_response('Ia/dailyreport.html',{'total':sdd})

            else:
            	return HttpResponseRedirect('/fts/thrift/reports/sales/admn/')
        else:
        	return HttpResponseRedirect('/fts/thrift/reports/sales/admn/')
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

                return render_to_response('Ia/dailyreportdated.html',{
						'to':to,
						 'from' :frm,
						 'detli':selenco(bra,fd,td)})


   	return HttpResponseRedirect('/login/user/')



def cashierreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})
		if staff.ceo != 1:
			msg = 'error'
			return render_to_response('Ia/selectloan.html',{'msg':msg})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		
		allmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,status=1)

		# msg = allmerchant	return render_to_response('Ia/selectloan.html',{'msg':msg})

		tdate= date.today()

		if request.method=='POST':
			form= endofdayform(request.POST)
			if form.is_valid():
				td=form.cleaned_data['to_date']
				fd =form.cleaned_data['date']
				status=form.cleaned_data['status']

				if status == '-----':
					msg = "select a status"
					return render_to_response('Ia/selectloan.html',{'msg':msg})
	
				if status == 'All':
					msg = "Not Available"
					return render_to_response('Ia/selectloan.html',{'msg':msg})

				if fd =='':
					msg = "Select 'from' date "
					return render_to_response('Ia/selectloan.html',{'msg':msg})

				if td == '':
					msg = "Select 'to' date"
					return render_to_response('Ia/selectloan.html',{'msg':msg})



				dday,mday,yday = fd.split('/') #JSON Dates Object
				yday=int(yday)
				fmday=int(mday)
				fday=int(dday)
				fd=date(yday,fmday,fday)

				dday,mday,yday = td.split('/') #JSON Dates Object
				yday=int(yday)
				tmday=int(mday)
				tday=int(dday)
				td=date(yday,tmday,tday)

				if fmday <= tmday:
					a = range(fmday,tmday+1)
				else:
					a = range(tmday,fmday+1)

					fd=date(yday,tmday,tday)
					td=date(yday,fmday,fday)

				if fmday == tmday:
					if fday < tday:
						dddd=tday #to date
						tttt=fday #from date

					elif tday<fday:
						dddd=fday
						tttt=tday

					else:
						dddd =tttt=fday


				detli=[]
				toot=0

				if status == 'Contribution':
					status='CR'
				elif status=='Withdrawal':
					status='DR'

				if fd.year== td.year:
					for memmerchant in allmerchant:
						merchant_sales=0
						for k in a: # a is the months covered in the search
							if k == a[0]: #if month is the first month
								if k == a[-1]: #use the boundaries set by the dates
									fff=0
									fff= fff + tttt
									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIamerchantBank.objects.filter(
											branch=mybranch,
											status= status,
											merchant=memmerchant,
											wallet_type='Main',
											recdate=fd1)
										couunt = salees.count()
										if couunt> 0:
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											merchant_sales=add_cr
											toot = toot + add_cr
											df = {'sum':merchant_sales,'details':memmerchant,'status':status}
											detli.append(df)
										fff += 1 
									
								else: #boundaries = from_date to month end

									fff=0
									fff= fff+ fd.day
									dddd = (monthrange(fd.year, fd.month))[-1]

									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIamerchantBank.objects.filter(branch=mybranch,
											status= status,
											merchant=memmerchant,
											wallet_type='Main',
											recdate=fd1)
										couunt = salees.count()
										if couunt> 0:
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											merchant_sales=add_cr
											toot = toot + add_cr
											df = {'sum':merchant_sales,'details':memmerchant,'status':status}
											detli.append(df)
										fff += 1 

							else: 
								if k == a[-1]: #boundaries = 1st to to_date
									dddd = td.day
									
									fff=1
									fff += 1
									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIamerchantBank.objects.filter(
											branch=mybranch,
											status= status,
											merchant=memmerchant,
											wallet_type='Main',
											recdate=fd1)

										couunt = salees.count() 
										if couunt> 0:
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											merchant_sales=add_cr
											toot = toot + add_cr
											df = {'sum':merchant_sales,'details':memmerchant,'status':status}
											detli.append(df)
										fff += 1 

								else: # loop thru the whole month
						
									fff=0
									fff += 1
									dddd= (monthrange(td.year, k))[-1]
									
									while fff <= dddd : 
										fd1=date(yday,k,fff)
										salees = tblIamerchantBank.objects.filter(
											branch=mybranch,
											status=status,
											merchant=memmerchant,
											wallet_type='Main',
											recdate=fd1)

										couunt = salees.count() 
										if couunt> 0:
											add=salees.aggregate(Sum('amount'))
											add_cr = add['amount__sum']
											merchant_sales=add_cr
											toot = toot + add_cr
											df = {'sum':merchant_sales,'details':memmerchant,'status':status}
											detli.append(df)
										fff += 1 



					return render_to_response('Ia/report_performance.html',{
						'company':mybranch,
						'user':varuser,
						'form':form,
						'toot':toot,
						'to':td,
						'status':status,
						'from' :fd,
						'detli':detli})

				else:
					msg = 'Limit your search to same year'
					return render_to_response('Ia/selectloan.html',{'msg':msg})
			else:
				msg = 'fill up '
				return render_to_response('Ia/selectloan.html',{'msg':msg})
		
		else:
			form=endofdayform()
			msg = ''
			detli=0
			toot=0
			return render_to_response('Ia/report_performance_get.html',{'company':mybranch, 
				'msg':msg,'user':varuser,'form':form,'toot':toot,
				'detli':detli})


	else:
		return HttpResponseRedirect('/login/user/')













def adminreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})
		
		if staff.ceo !=1:
			msg='error'
			return render_to_response('Ia/selectloan.html',{'msg':msg, 'user':varuser})

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
				to_date=form.cleaned_data['to_date']
				datte =form.cleaned_data['date']

		
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
									tuy = tblIasavings_trans.objects.filter(branch=mybranch,
										status='Service Charge',
										description='DR',
										wallet_type='Main',
										avalability='Not Available',
										recdate=fd1)
								
									if tuy.count() < 1:
										add = 0
									else:
										addw = tuy.aggregate(Sum('amount'))
										add = addw['amount__sum']
										toot = toot + add_cr
										df = {'total':add_cr,'details':tuy}
										detli.append(df)

									fff += 1
								msg = ''




							else: #boundaries = from_date to month end 

								# msg = 'im first'
								# return render_to_response('Ia/selectloan.html',{'msg':msg})

								fff=0
								fff= fff+ fd.day

								dddd = (monthrange(fd.year, fd.month))[-1]


								while fff <= dddd : 
									fd1=date(yday,k,fff)
									tuy = tblIasavings_trans.objects.filter(branch=mybranch,
										status='Service Charge',
										description='DR',
										wallet_type='Main',
										avalability='Not Available',
										recdate=fd1)
								
									if tuy.count() < 1:
										add = 0
									else:
										addw = tuy.aggregate(Sum('amount'))
										add = addw['amount__sum']
										toot = toot + add_cr
										df = {'total':add_cr,'details':tuy}
										detli.append(df)

									fff += 1
								msg = ''
							
						else: 
							if k == a[-1]: #boundaries = 1st to to_date
								dddd = td.day
								
								fff=1
								fff += 1


								while fff <= dddd : 
									fd1=date(yday,k,fff)
									tuy = tblIasavings_trans.objects.filter(branch=mybranch,
										status='Service Charge',
										description='DR',
										wallet_type='Main',
										avalability='Not Available',
										recdate=fd1)
								
									if tuy.count() < 1:
										add = 0
									else:
										addw = tuy.aggregate(Sum('amount'))
										add = addw['amount__sum']
										toot = toot + add_cr
										df = {'total':add_cr,'details':tuy}
										detli.append(df)

									fff += 1
								msg = ''

							else: # loop thru the whole month
					
			
								fff=0
								fff += 1
								dddd= (monthrange(td.year, k))[-1]
								
								while fff <= dddd : 
									fd1=date(yday,k,fff)
									tuy = tblIasavings_trans.objects.filter(branch=mybranch,
										status='Service Charge',
										description='DR',
										wallet_type='Main',
										avalability='Not Available',
										recdate=fd1)
								
									if tuy.count() < 1:
										add = 0
									else:
										addw = tuy.aggregate(Sum('amount'))
										add = addw['amount__sum']
										toot = toot + add_cr
										df = {'total':add_cr,'details':tuy}
										detli.append(df)

									fff += 1
								msg = ''

					return render_to_response('Ia/report_performance.html',{'company':mybranch, 
							'msg':msg,'user':varuser,'form':form,'toot':toot,'merchant':merchant,
							'to':to_date, 'from' :datte,'name':memmerchant,
							'detli':detli})
				else:
					msg = 'Limit your search to same year'
					return render_to_response('Ia/selectloan.html',{'msg':msg})


		form = thrifthistory()
		
		return render_to_response('Ia/reportadmin.html',{'company':mybranch, 
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

                user,month = user.split(':')

                if month == '-':
                	msg =' select month'
                	return render_to_response('Ia/selectloan.html',{'msg':msg})

                month=int(month)

                monthname = calendar.month_name[month]
                today=date.today()
                yday=today.year


                chkstaff = tblSTAFF.objects.get(email=user,status=1)
                bra = chkstaff.branch.id
                bra= tblBRANCH.objects.get(id = bra)


                thriftp = tblIathrift.objects.filter(branch=bra, month = monthname,year=yday)
                tr=0

                if thriftp.count() > 0:
	                for k in thriftp:
	                	code =k.code
	                	tuy = tblIasavings_trans.objects.filter(branch=bra,
	                		status='Account Maintenance',
	                		description='CR',code=code)
	           	                
		            	if tuy.count() > 0:
		            		addw = tuy.aggregate(Sum('amount'))
		            		add = addw['amount__sum']
		            		tr = tr + add
		            	else:
		            		add = 0
		            	# tr=add 

                else:
                	msg = 'No records found'
                	return render_to_response('Ia/selectloan.html',{'msg':msg})


            	return render_to_response('Ia/mydailysales.html',{'total':tr,'monthname':monthname})

            else:
            	return HttpResponseRedirect('/fts/thrift/reports/sales/admn/')
        else:
        	return HttpResponseRedirect('/fts/thrift/reports/sales/admn/')
    else:
   		return HttpResponseRedirect('/login/user/')





def getmerchantname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]
    		data=tblIaMERCHANT.objects.get(thrift1a =1,id=acccode,status=1)
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










def getcashid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)

    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		allcashier = Userprofile.objects.filter(cashier=1,status=1,branch=branchcode)

    		for j in allcashier:
    			j = j.staffrec.id  #uses ID from tblSTAFF
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

def getcashname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]

    		data=tblSTAFF.objects.get(id=acccode)
    		j = data.surname
    		kk.append(j)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')
    	else:
    		gdata = ""
    		return render_to_response('index.html',{'gdata':gdata})
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

                if report == 'daily':
                	merc = tblIamerchantBank.objects.filter(remitted_by =relcashier,recdate=oydate)
                elif report == 'weekly':
                	merc= tblIamerchantBank.objects.filter(remitted_by=relcashier,weekno=weekday)

                elif report== 'monthly':
                	merc=tblIamerchantBank.objects.filter(remitted_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('Ia/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('Ia/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')






def getadminid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)

    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		alladmin = Userprofile.objects.filter(admin=1,status=1,branch=branchcode)

    		for j in alladmin:
    			j = j.staffrec.id
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

def getadminname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]
    		data=tblSTAFF.objects.get(id=acccode)
    		j = data.surname
    		kk.append(j)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')
    	else:
    		gdata = ""
    		return render_to_response('index.html',{'gdata':gdata})
    else:
    	return HttpResponseRedirect('/login/user/')

def getadminreportajax(request):
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

                if report == 'daily':
                	merc = tblIamerchantBank.objects.filter(remitted_by =relcashier,recdate=oydate)
                elif report == 'weekly':
                	merc= tblIamerchantBank.objects.filter(remitted_by=relcashier,weekno=weekday)

                elif report== 'monthly':
                	merc=tblIamerchantBank.objects.filter(remitted_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('Ia/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('Ia/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')


   		

def getadminreportajax(request):
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

                if report == 'daily':
                	merc = tblIamerchantBank.objects.filter(approved_by =relcashier,recdate=oydate)
                elif report == 'weekly':
                	merc= tblIamerchantBank.objects.filter(approved_by=relcashier,weekno=weekday)

                elif report== 'monthly':
                	merc=tblIamerchantBank.objects.filter(approved_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('Ia/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('Ia/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')



def customerslist(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.ceo==1 :
			client_list = tblCUSTOMER.objects.filter(branch=mybranch)
			return render_to_response('Ia/cust_list.html',{'company':mybranch,'user':varuser,'client_list':client_list})

		elif staff.thrift_officer== 1:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
			client_list = tblCUSTOMER.objects.filter(branch=mybranch)
			return render_to_response('Ia/cust_list_merc.html',{'company':mybranch,'user':varuser,'client_list':client_list})
		else:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')


def switches(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo==0:
				return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = switchesform(request.POST)
			if form.is_valid():
				mymerchant=form.cleaned_data['merchant']

				merch_count = tblIaMERCHANT.objects.filter(branch=mybranch,status=1).count()
				if merch_count> 1:

					try :
						msg = 'Coming soon'
						mmme= tblIaMERCHANT.objects.get(thrift1a =1,branch=mybranch,status=1,id=mymerchant)
						cus_list = tblCUSTOMER.objects.filter(branch=mybranch,status=1)
						if cus_list > 0 :
							form = newswitchform()
							return render_to_response('Ia/switchproc.html',{'company':mybranch,'user':varuser,
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
		return render_to_response('Ia/switch.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')

def getallstall(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		mrp = tblIaMERCHANT.objects.get(thrift1a =1,id=acccode)
    		branch=mrp.branch.id
    		branch=tblBRANCH.objects.get(id=branch)
    		merc = tblIaMERCHANT.objects.filter(branch=branch,status=1).exclude(id=acccode)
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
    			return render_to_response('Ia/selmerch.html')

    		else:
    			merchant=tblIaMERCHANT.objects.get(id=acccode)
    			return render_to_response('Ia/switchmerc.html',{'merchant':merchant})
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
	    		return render_to_response('Ia/selmerch.html',{'sd':a})

    		else:
    		# 	merchant=tblIaMERCHANT.objects.get(id=acccode)
    			return render_to_response('Ia/switchmerc.html')
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')










def regfieldagent(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.ceo==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		mystafflist = tblSTAFF.objects.filter(status=1, branch=mybranch).count()


		if request.method== 'POST':
			form = fieldofficerfform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']
				mystaff = tblSTAFF.objects.filter(email=email,status=1, branch=mybranch) #check status
				mycount=mystaff.count()

				if mycount == 1: #user is a staff
					querry_email = tblSTAFF.objects.get(email=email)

					try:
						ibco = tblIaMERCHANT.objects.get(branch = mybranch, thrift1a=1,staff=querry_email)
						if ibco.status == False:
							msg = 'credit officer is inactive'

						elif ibco.status == True:
							msg='ALREADY REGISTERED'

					except:
						diff = Userprofile.objects.get(email=email,status=1)
						diff.thrift_officer=1 #role
						diff.thrift1a=1 #app
						diff.save()
						form = fieldofficerfform()
						msg="SUCCESSFUL"

						try:
							register_field_officerIa(email)
							tblIaMERCHANT(status=1,branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()
						except:
							tblIaMERCHANT(status=1, branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()

				elif mycount == 0:
					msg = 'THIS EMAIL IS NOT REGISTERED'
			else:
				msg = 'INVALID ENTRY'
		else:
			form =fieldofficerfform()
			msg=''

		# meer = tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1)
		# mycolist = tblIaMERCHANT.objects.filter(status=1, thrift1a=1, branch=mybranch).count()
		# inactiveco = tblIaMERCHANT.objects.filter(status=0, thrift1a=1, branch=mybranch).count()

		return render_to_response('Ia/merch.html',{
			'company':mybranch,
			'msg':msg, 
			'user':varuser,
			'form':form,})

	else:
		return HttpResponseRedirect('/login/user/')




def mycos(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.cashier==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})


		msg = ''

		meer = tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1)
		inactiveco = tblIaMERCHANT.objects.filter(status=0, thrift1a=1, branch=mybranch).count()

		if staff.admin == 1:
			return render_to_response('Ia/merch_list.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})
		elif staff.cashier == 1:
			return render_to_response('Ia/merch_cash_list.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})

	else:
		return HttpResponseRedirect('/login/user/')