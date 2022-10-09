# Create your views here.

from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json

from customer.forms import *
from customer.models import *



from Ia.models import *
from Ia.utils import *
from Ib.models import *
from Ib.utils import *
# from Ib.utils import *

from num2words import num2words

from sysadmin.models import *


# from merchant.models import *
# from Ib.models import *
# from savings.models import *


from datetime import *
import calendar

#######import only merchant.models******
from calendar import monthrange

from django.core.serializers.json import json

from django.db.models import Max,Sum

import random




def createwallet(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo == 0:
			return render_to_response('customer/404.html',{'company':mybranch, 'user':varuser})


		msg = ''

		if request.method == 'POST':
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']


			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])

			if 'photo' in request.FILES:
				photo=request.FILES['photo']
			else:
				photo = 'customerpix/user.png'

			try:
				phone1=int(phone)

				wallet=phone1


			except:
				msg = 'Incomplete phone number'
				return render_to_response('customer/selectloan.html',{'msg':msg})



			try:
				countt=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			except:

				k = random.randint(0,9)
				y = random.randint(0,9)
				x = random.randint(0,9)
				z = random.randint(0,9)
				a = random.randint(0,9)
				pin =  str(k) + str(y) + str(x) + str(z)+ str(a)


				tblCUSTOMER(surname=surname,
					firstname=firstname,
					othername=othername,
					phone=phone,
					Address=address,
					wallet=wallet,
					code=pin,
					email=email,
					branch=mybranch,
					status=1,
					photo=photo).save()



				try:
					wallet_registration(email)
				except:
					pass

			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)


			if staff.thrift1a == 1:
				memmerchant = tblIaMERCHANT.objects.get(branch=mybranch,staff=memstaff, thrift1a=1,status=1)
				tblIaCUSTOMER(branch=mybranch,merchant=memmerchant,customer=customer,
					status=1,code=pin,sms=0,get_email=1, withdr_status=1).save()
				try:
					customer_activationIa(email)
				except:
					pass


			if staff.thrift1b == 1:	
				memmerchant = tblIbco.objects.get(branch=mybranch,staff=memstaff, thrift1b=1,status=1)
				tblIbCUSTOMER(branch=mybranch,merchant=memmerchant,customer=customer,
					status=1,code=pin,sms=0,get_email=1, withdr_status=1).save()

				##email notification
				try:
					customer_activationIb(email)
				except:
					pass


			#add other services later
			#Corporate C
			#Target Savings
			#Cooperative

			return render_to_response('customer/success.html',{'company':mybranch,'user':varuser,'wallet':wallet})


		return render_to_response('customer/createwallet.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



def editwallet(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


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
			form= viewwalletform(request.POST)
			msg='Try again later'

			if form.is_valid():
				wallet=form.cleaned_data['wallet']
				try:
					customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
					msg=''
					return render_to_response('customer/myeditwallet.html',{'company':mybranch,
					'user':varuser,'wallet':wallet,'form':form,'customer':customer})

				except:
					msg='INVALID WALLET ADDRESS'
					return render_to_response('customer/selectloan.html',{'msg':msg})
		else:
			form = viewwalletform()
			msg=''

		return render_to_response('customer/editwallet.html',{'company':mybranch,'user':varuser,'msg':msg,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def doedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo == 0:
			return render_to_response('customer/404.html',{'company':mybranch, 'user':varuser})
		msg = ''

		if request.method == 'POST':
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']
			wallet= request.POST['wallet']

			if 'photo' in request.FILES:
				photo=request.FILES['photo']
			else:
				photo = 'customerpix/user.png'


				ccc = tblCUSTOMER.objects.filter(branch=mybranch,wallet=wallet, status=1).update(
					surname=surname,firstname= firstname, othername=othername,
					Address=address,email=email,photo=photo)


				try:
					wallet_edit(email)
				except:
					pass

				return render_to_response('customer/editwallet_successful.html',{'company':mybranch,'user':varuser,'wallet':wallet})


		# return render_to_response('customer/createwallet.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def viewwallet(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				wallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
					return render_to_response('customer/walletdetails.html',{'company':mybranch,'user':varuser,'details':details})
				except:
					msg = 'invalide wallet address'
					return render_to_response('customer/viewwallet.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			else:
				pass
		else:
			form=viewwalletform()
		return render_to_response('customer/viewwallet.html',{'company':mybranch,'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')





def customerslist(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

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
			client_list = tblCUSTOMER.objects.filter(branch=mybranch).order_by('surname')
			return render_to_response('customer/cust_list.html',{'company':mybranch,'user':varuser,'client_list':client_list})

		elif staff.thrift1b_officer== 1:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
			client_list = tblCUSTOMER.objects.filter(branch=mybranch,merchant=memmerchant)
			return render_to_response('customer/cust_list_merc.html',{'company':mybranch,'user':varuser,'client_list':client_list})
		else:
			return render_to_response('customer/404.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')




