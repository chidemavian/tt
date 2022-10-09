from __future__ import division

from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json



from num2words import num2words
from loans.forms import *
from IIIb.forms import *
from IIIb.models import *
from Ib.models import *

from sysadmin.models import *
from customer.models import *
from merchant.models import *
from savings.models import *

from IIIb.utils import *

import locale


from datetime import *
import calendar


#######import only merchant.models******
from calendar import monthrange

from django.core.serializers.json import json

from django.db.models import Max,Sum

import random


ddatt=date.today()




def welcome(request):
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

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if staff.thrift3b_admin==1:
			return render_to_response('IIIb/manager.html',{'company':mybranch, 'user':varuser})
		elif staff.thrift3b_cashier==1:
			return render_to_response('IIIb/manager_c.html',{'company':mybranch, 'user':varuser})
		elif staff.thrift3b_officer==1:
			return render_to_response('IIIb/manager_o.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/')



def adminwelcome(request):
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

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404loan.html',{'company':mybranch, 'user':varuser})

		return render_to_response('IIIb/dashboardIIIb.html',{'company':mybranch, 'user':varuser,'pincode':staff})

	else:
		return HttpResponseRedirect('/login/')

def changepass(request):
	if 'userid' in request.session:
		varuser = request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			return HttpResponseRedirect('/login/')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if request.method=='POST':
			oldpass= request.POST['oldpass']
			newpass1=request.POST['newpass1']
			newpass2=request.POST['newpass2']

			if oldpass== staff.password :
				if newpass2 == newpass1:
					msg= 'password change successfull'
					rr=Userprofile.objects.filter(email=varuser,status=1).update(password=newpass1)

					return render_to_response('IIIb/changepass_success.html',{'user':varuser,'company':mybranch,
						'menu':staff,'msg':msg})
				else:
					msg = 'the passwords do not match'
			else:
				msg='your old pass is not correct'
		else :
			msg=''
		return render_to_response('IIIb/changepass.html',{'user':varuser,'company':mybranch,
				'menu':staff,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')


def massReg(request):
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

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		msg = ''

		if request.method == 'POST':
			surname=request.POST['surname']

			try :


				acc_cus=tblCUSTOMER.objects.get(surname=surname,firstname=firstname,othername=othername,
					phone=phone,Address=address,wallet=wallet,code=68768,email=email,
					UX=0,branch=mybranch,merchant=memmerchant,status=1,
					online=0,sms=0,get_email=0)

				tblsavingsaccount(customer=acc_cus,branch=mybranch,UX=0,status=1,online=0,sms=0,get_email=0,withdr_status=1).save()

				return render_to_response('thrift/success.html',{'company':mybranch,'user':varuser,'wallet':wallet})

			except:
				msg = 'Incomplete phone number'

		return render_to_response('staff/massreg.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')




def newregistration(request):
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

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


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
				photo = 'staff_pix/user.png'


			try:
				phone1=int(phone)


				try:
					msg = 'Eimail already in use'
					countt=tblSTAFF.objects.get(email=email,phone=phone)

				except:
					k = random.randint(0,9)
					y = random.randint(0,9)
					x = random.randint(0,9)
					z = random.randint(0,9)
					a = random.randint(0,9)
					pin =  str(k) + str(y) + str(x) + str(z)+ str(a)

					tblSTAFF(code = pin, status=1, branch=mybranch,surname=surname,
						firstname=firstname,othername=othername,
						Address=address,types='Office', phone=phone,photo=photo, email=email).save()

					new_staff = tblSTAFF.objects.get(email=email)
					name = new_staff.surname + " " + new_staff.firstname + " " + new_staff.othername


					Userprofile(branch =mybranch, password='cooperative', staffrec=new_staff,code =pin, status=1, email=email,thrift3b=1,thrift3b_officer=1).save()

					email=[email]
					sendMailMembership(email)

				return render_to_response('IIIb/success.html',{'company':mybranch,'user':varuser,'name':name})

			except:
				msg = 'Incomplete phone number'
		else:
			msg=''

		return render_to_response('IIIb/registration.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def massReg(request):
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

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift3a_cashier==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('IIIb/adminwelcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/')



def stafflist(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.ceo==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		stafflist = tblSTAFF.objects.filter(branch=mybranch,status=1).exclude(email='njc@gmail.com')
		
		if staff.thrift3b==1:
			stafflist= tblIIIbcoop.objects.filter(branch=mybranch)
			return render_to_response('IIIb/listofstaff3b.html',{'company':mybranch, 'user':varuser,'list':stafflist})


		return render_to_response('IIIb/listofstaff.html',{'company':mybranch, 'user':varuser,'list':stafflist})

	else:
		return HttpResponseRedirect('/login/user/')



#*******************My Savings*******************************

def deposit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff, status=1)
		

		if request.method=='POST':
			form=mysavingsform(request.POST)
			if form.is_valid():
				month=form.cleaned_data['month']
				amount=request.POST['amount']

				if month == '---':
					msg = 'select month'
					return render_to_response('IIIb/selectloan.html',{'msg':msg})

				else:
					fig = num2words(int(amount))
					yyear=ddatt.year

					if staff.thrift3b_admin==1:
						return render_to_response('IIIb/deposit.html',{'company':mybranch, 'user':varuser,'msg':coop,'month':month,'fig':fig,'amount':amount,'year':yyear})
					if staff.thrift3b_cashier==1:
						return render_to_response('IIIb/deposit_c.html',{'company':mybranch, 'user':varuser,'msg':coop,'month':month,'fig':fig,'amount':amount,'year':yyear})
					if staff.thrift3b_officer==1:
						return render_to_response('IIIb/deposit_o.html',{'company':mybranch, 'user':varuser,'msg':coop,'month':month,'fig':fig,'amount':amount,'year':yyear})



		else:

			form = mysavingsform()
			if staff.thrift3b_admin==1:
				return render_to_response('IIIb/savings.html',{'company':mybranch, 'form':form,'user':varuser,'msg':coop})
			elif staff.thrift3b_cashier==1:
				return render_to_response('IIIb/savings_c.html',{'company':mybranch, 'form':form,'user':varuser,'msg':coop})
			elif staff.thrift3b_officer==1:
				return render_to_response('IIIb/savings_o.html',{'company':mybranch, 'form':form,'user':varuser,'msg':coop})

	else:
		return HttpResponseRedirect('/login/')



def checkdep(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,month=acccode.split(":")

        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		if month=='---':
        			msg='Select valid Month'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})

        		tdate= date.today()
        		year=tdate.year

        		account_type='Wallet'

        		
        		scsenario = tblIIIbfieldagent.objects.filter(branch=mybranch,
        			month=month,
        			staff=kfw,
        			year=year,
        			account_type=account_type)

        		if scsenario.count() > 0:
        			msg='you have an application already'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})

        	
        		yt= tblIIIbapprovals.objects.filter(branch=mybranch,
        			month=month,
        			year=year,
        			description=account_type)
        	
        		if yt.count() > 0:
        			msg='Applications are closed for this month'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})
     
        		else:

	        		return render_to_response('IIIb/sss.html')
        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/')




def save_deposit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		kfwf=tblIIIbcoop.objects.get(staff=memstaff,branch=mybranch,status=1)

		surname=kfwf.staff.surname
		firstname=kfwf.staff.firstname


		year=ddatt.year
		code = generate_trans_pin()

		amount=request.POST['amount']
		month =request.POST['month']
		
		tblIIIbfieldagent(staff =kfwf,
			branch = mybranch,
			month=month,
			year=year,
			amount=amount,
			status='Awaiting Execution',
			code=code,
			account_type='Wallet',
			scheme	='Wallet',
			transdate=ddatt).save()

		#***configure send email notification here

		try:
			deposit_email(varuser,surname,firstname,amount,month,year)
		except Exception, e:
			pass

		if staff.thrift3b_admin==1:
			return render_to_response('IIIb/saving_success.html',{'company':mybranch, 'user':varuser, 'amount':amount,'month':month,'year':year})

		elif staff.thrift3b_cashier==1:
			return render_to_response('IIIb/saving_success_c.html',{'company':mybranch, 'user':varuser, 'amount':amount,'month':month,'year':year})
						
		elif staff.thrift3b_officer==1:
			return render_to_response('IIIb/saving_success_o.html',{'company':mybranch, 'user':varuser, 'amount':amount,'month':month,'year':year})

	else:
		return HttpResponseRedirect('/login/')



def safepack(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,status=1)
		
		if request.method=='POST':
			form=saveapplyform(request.POST)
			if form.is_valid():
				package=form.cleaned_data['savepack']
				amount=request.POST['amount']

				fig = num2words(int(amount))
				c=tblstandardsavingIIIB.objects.get(description=package)

				if staff.thrift3b_admin==1:

					return render_to_response('IIIb/prosave.html',{'company':mybranch, 
						'user':varuser,
						'msg':coop,
						'package':package,
						'fig':fig,
						'amount':amount})

				elif staff.thrift3b_cashier==1:
					return render_to_response('IIIb/prosave_c.html',{'company':mybranch, 
						'user':varuser,
						'msg':coop,
						'package':package,
						'fig':fig,
						'amount':amount})

				elif staff.thrift3b_officer==1:
					return render_to_response('IIIb/prosave_o.html',{'company':mybranch, 
						'user':varuser,
						'msg':coop,
						'package':package,
						'fig':fig,
						'amount':amount})
		else:

			form = saveapplyform()
			if staff.thrift3b_admin==1:
				return render_to_response('IIIb/saving_apply.html',{'company':mybranch, 'form':form,'user':varuser,'msg':coop})
			elif staff.thrift3b_cashier==1:
				return render_to_response('IIIb/saving_apply_c.html',{'company':mybranch, 'form':form,'user':varuser,'msg':coop})
			elif staff.thrift3b_officer==1:
				return render_to_response('IIIb/saving_apply_o.html',{'company':mybranch, 'form':form,'user':varuser,'msg':coop})

	else:
		return HttpResponseRedirect('/login/')



def applydep(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,package=acccode.split(":")

        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)
        		mnm=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		tdate=datetime.today()
        		month=tdate.month #month_index
        		
        		year=tdate.year
        		
        		if package== '-----':
        			msg='select a savings scheme'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})
        		else:
        			gh = tblstandardsavingIIIB.objects.get(branch=mybranch,
        				description=package,)

        			starts = gh.from_month
        			starts = datetime.strptime(starts,"%B") #converts month_name to month_index
        			starts=starts.month

        			stopp = gh.to_month
        			stopp = datetime.strptime(stopp,"%B") #converts month_name to month_index
        			stopp=stopp.month


        			if month < starts:
        				msg = 'This scheme is not yet open'
        				return render_to_response('IIIb/selectloan.html',{'msg':msg})
        			
        			elif month > stopp:
        				msg = "This scheme is closed"
        				return render_to_response('IIIb/selectloan.html',{'msg':msg})

        			else:

	        			f = tblIIIIbstaffbsavings_pack.objects.filter(branch=mybranch,
	        				staff=mnm,description=package,year=year,status='Running').count()

	        			if f > 0:
	        				msg='you already submitted application for this savings scheme'
	        				return render_to_response('IIIb/selectloan.html',{'msg':msg})
	        			
	        			else:
	        				rt = tblIIIbapprovals.objects.filter(branch=mybranch,
								month = stopp, #if last month of the package is approved
								description='package',
								year=year).count()

	        				if rt ==1:
	        					msg='This scheme is already closed'
	        					return render_to_response('IIIb/selectloan.html',{'msg':msg})
	        				else:
	        					return render_to_response('IIIb/applypack.html')
        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/')




def save_pack(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		kfwf=tblIIIbcoop.objects.get(staff=memstaff,status=1)
		surname=kfwf.staff.surname
		firstname=kfwf.staff.firstname

		tdate= date.today()
		monthnam=calendar.month_name[tdate.month]
		year=tdate.year
		
		if request.method=='POST':
			amount=request.POST['amount']
			package =request.POST['package']

			bg = tblstandardsavingIIIB.objects.get(branch=mybranch,description=package)

			too =bg.to_month

			month=tdate.month #index of current month

			month4 = datetime.strptime(too,"%B") #converts month_name to month_index
			month4=month4.month


			tblIIIIbstaffbsavings_pack(branch=mybranch,
				staff=kfwf,
				description=package,
				status='Running',
				month=monthnam,
				year=year,
				amount=amount,
				transdate=tdate).save()


			rt = tblIIIbapprovals.objects.filter(branch=mybranch,
				month = monthnam,
				description='package',
				year=year).count()

			if rt ==1: #meaning that approvals have been done already

				if too == month:
					msg='This scheme is no longer open'
					return render_to_response('IIIb/selectloan.html',{'msg':msg})

				elif month < too:

					month=month+1

			bg = []
			for x in range(month,month4+1):
				monthname = calendar.month_name[x]
				bg.append(monthname)

				code = generate_trans_pin()

				tblIIIbfieldagent(staff =kfwf,
					branch = mybranch,
					month=monthname,
					amount=amount,
					year=year,
					status='Awaiting Execution',
					code=code,
					scheme=package,
					account_type='package',
					transdate=tdate).save()


				#**configure email sending***********

			try:
				savingscheme_email(varuser,surname,firstname,amount,year,package,bg[0],bg[-1])
			except :
				pass


			if staff.thrift3b_admin==1:
				return render_to_response('IIIb/package_success.html',{'company':mybranch, 'user':varuser, 'package':package})
			elif staff.thrift3b_cashier==1:
				return render_to_response('IIIb/package_success_c.html',{'company':mybranch, 'user':varuser, 'package':package})
			elif staff.thrift3b_officer==1:
				return render_to_response('IIIb/package_success_o.html',{'company':mybranch, 'user':varuser, 'package':package})

		else:
			return HttpResponseRedirect('/IIIb/threeb/savings/save_packages/')




def savelog(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,status=1)
		
		if staff.thrift3b_admin==1:
			return render_to_response('IIIb/savinglogs.html',{'company':mybranch, 'user':varuser,'msg':coop})
		elif staff.thrift3b_cashier==1:
			return render_to_response('IIIb/savinglogs_c.html',{'company':mybranch, 'user':varuser,'msg':coop})
		elif staff.thrift3b_officer==1:
			return render_to_response('IIIb/savinglogs_o.html',{'company':mybranch, 'user':varuser,'msg':coop})

	else:
		return HttpResponseRedirect('/login/')


def deplogs(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,account=acccode.split(":")

        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)
        		mnm=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		if account== '-----':
        			msg='select transaction type'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})
        		else:
        			if account=='dep':
        				account_type='Wallet'
        			else:
        				account_type='package'

        			req=tblIIIbfieldagent.objects.filter(branch=mybranch,staff=mnm,account_type=account_type)

        			return render_to_response('IIIb/logs.html',{'email':user,'req':req})
        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render_to_response('lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/')




####***********MY deductions********************************
def dedopts(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)



		form = approveform()
		if staff.thrift3b_admin==1:
			return render_to_response('IIIb/sosdeduct.html',{'company':mybranch, 'user':varuser,'form':form,'msg':coop})
		elif staff.thrift3b_cashier==1:
			return render_to_response('IIIb/sosdeduct_c.html',{'company':mybranch, 'user':varuser,'form':form,'msg':coop})
		elif staff.thrift3b_officer==1:
			return render_to_response('IIIb/sosdeduct_o.html',{'company':mybranch, 'user':varuser,'form':form,'msg':coop})


	else:
		return HttpResponseRedirect('/login/')


def ajaxded(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)


        		if month=='-':
        			msg='Select valid Month'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})


        		month=int(month)
        		monthnam = calendar.month_name[month]

        		tdate=date.today()
        		year=tdate.year

        		status='Executed'


        		scsenario = tblIIIbfieldagent.objects.filter(branch=mybranch,
        			month=monthnam,
        			year=year,
        			staff=kfw,
        			status=status)

        		tt=scsenario.aggregate(Sum('amount'))
        		total = tt['amount__sum']

				#*********loan deductions
				#**commodities deductions
						


        		return render_to_response('IIIb/dedajax.html',{'email':user,
        			'msg':scsenario,
        			'status':status, 
        			'month':monthnam,
        			'total':total,
        			'year':year})

        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/')





###############Pay outs*****************

def loan_payout(request):
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

		if staff.thrift3b_cashier==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		form=approveform()
		msg=''
		return render_to_response('IIIb/payout_loan.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def payout45(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		if month=='-':
        			msg='Select valid Month'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})


        		month=int(month)
        		monthnam = calendar.month_name[month]
        		tdate=date.today()
        		year=tdate.year

   

        		status='Awaiting Payment'

        		
        		scsenario = tblIIIbloandapplications.objects.filter(branch=mybranch,
        			date__month=month,
        			date__year=year,
        			status=status)

        		p=[]

        		for k in scsenario:
        			staff =k.staffrec.id
        			staff=tblIIIbcoop.objects.get(id =staff)

        			g=tblIIIb_bankdetail.objects.get(branch_code=mybranch,staff_rec=staff)
        			jk ={'staff':k,'bank':g}
        			p.append(jk)

        		tt=scsenario.aggregate(Sum('volume'))
        		total = tt['volume__sum']
		
        		return render_to_response('IIIb/payout_loan_ajax.html',{'email':user,
        			# 'msg':scsenario,
        			'msg':p,
        			'status':status, 
        			'month':monthnam,
        			'total':total})


        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/')









###############Aprovals*****************

def loan_approvals(request):
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

		if staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		form=approveform()
		msg=''
		return render_to_response('IIIb/approval_loan.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def loanscene45(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		if month=='-':
        			msg='Select valid Month'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})


        		month=int(month)
        		monthnam = calendar.month_name[month]
        		tdate=date.today()
        		year=tdate.year

   

        		status='Awaiting Approval'

        		
        		scsenario = tblIIIbloandapplications.objects.filter(branch=mybranch,
        			date__month=month,
        			date__year=year,
        			status=status)
        		tt=scsenario.aggregate(Sum('volume'))
        		total = tt['volume__sum']
		
        		return render_to_response('IIIb/approval_loan_ajax.html',{'email':user,
        			'msg':scsenario,
        			'status':status, 
        			'month':monthnam,
        			'total':total})

        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/')



def loanapprvopt(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		month=int(acccode)
    		monthnam = calendar.month_name[month]

    		return render_to_response('IIIb/apprlonakax.html',{
    			'month':monthnam,
    			'month_index':acccode})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')




def pwallapprove(request):
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
		year=f.year
		fdate=date(year,f.month,f.day)

		if staff.thrift3b_admin==0 :
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			month =request.POST['month121']


			month=int(month)
			monthnam = calendar.month_name[month]

			status='Awaiting Approval'

			scsenario = tblIIIbloandapplications.objects.filter(branch=mybranch,
    			date__month=month,
    			date__year=year,
    			status=status)
			scsenario.update(status='Running')

			for vp in scsenario:
				tenure= vp.package.tenure
				repay =vp.repay_month #30 0r 60
				if repay==30:
					month=month+1
				elif repay == 60:
					month=month+2

				# ddt = tenure + month

				for kl in tenure:
				 	tblIIIbloantransaction




			return render_to_response('IIIb/loanapproved.html',{'company':mybranch, 
				'user':varuser,
				'year':year,
				'month':monthnam})

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/')

###############Applications*****************

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

		if staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = individualform(request.POST)

			if form.is_valid():
				merchant =form.cleaned_data['merchant']
				mydate2=form.cleaned_data['date'] #JavaScript Date Object
			else:
				pass

		else:
			form=approveform()
			msg=''
		return render_to_response('IIIb/bookindividualloan.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

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
        		user,scene,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		if scene=='-----':
        			msg='Select savings type'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})

        		if month=='-':
        			msg='Select valid Month'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})


        		month=int(month)
        		monthnam = calendar.month_name[month]
        		tdate=date.today()
        		year=tdate.year

        		account_type=scene

        		status='Awaiting Execution'

        		
        		scsenario = tblIIIbfieldagent.objects.filter(branch=mybranch,
        			month=monthnam,
        			account_type=account_type,
        			status=status)
        		tt=scsenario.aggregate(Sum('amount'))
        		total = tt['amount__sum']

        		if scene == 'Wallet': 			
	        		return render_to_response('IIIb/scenario.html',{'email':user,
	        			'msg':scsenario,
	        			'status':status, 
	        			'month':monthnam,
	        			'total':total,
	        			'pack':scene})

	        	elif scene=='package':

	        		pkk= tblIIIIbstaffbsavings_pack.objects.filter(branch=mybranch,
	        			# staff=kfw,
	        			status="Running", 
	        			# transdate__month=month,
	        			# year=year
	        			)

	        		sds=[]

	        		if pkk.count() > 0:

		        		

		        		for jk in pkk:
		        			mstaff=tblIIIbcoop.objects.get(id=jk.staff.id,status=1)
		        			package=jk.description
		        			name = jk.staff.staff.surname+ "  "+jk.staff.staff.firstname+"  "+jk.staff.staff.othername

		        			try:

			        			fgf = tblIIIbfieldagent.objects.get(branch=mybranch,
			        				month=monthnam,
			        				year=year,
			        				staff=mstaff,
			        				scheme=jk.description,
			        				account_type=account_type,
			        				status=status)

			        			kl={'name':name,'package':package,
			        			     'amount':fgf.amount}
			        			sds.append(kl)
			        		except:
			        			pass
		        		


	        		return render_to_response('IIIb/scenario_p.html',{'email':user,
	        			'msg':scsenario,
	        			'status':status, 
	        			'month':monthnam,
	        			'total':total,
	        			'lk':sds,
	        			'year':year,
	        			'pack':scene})

        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/')




def declineoptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,month,package=acccode.split(':')#month in index form
    		customer=tblIIIbcoop.objects.get(id=state,status=1)

    		return render_to_response('IIIb/decline_opt.html',{
    			'state':state,'month':month,'package':package,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')


def yesdecline(request):
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
		mday=f.day
		mmonth =f.month
		myear=f.year
		fdate=date(myear,mmonth,mday)

		if staff.thrift3b_admin==0 :
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			month =request.POST['month123']
			pack =request.POST['pack123']
			state =request.POST['state123']

			status='Awaiting Execution'

			customer=tblIIIbfieldagent.objects.filter(id=state,status=status).update(status='Declined')

			month=int(month)
			monthnam = calendar.month_name[month]

			account_type=pack


			scsenario = tblIIIbfieldagent.objects.filter(branch=mybranch,
				month=monthnam,
				account_type=account_type,
				status=status)

			tt=scsenario.aggregate(Sum('amount'))
			total = tt['amount__sum']

			return render_to_response('IIIb/decredirect.html',{'company':mybranch,
				'user':varuser,
				'msg':scsenario,
				'status':status,
				'state':state,
				'total':total,
				'month':monthnam,
				'month_index':month,
				'pack':pack})
		
		else:
			return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/login/')







def approveoptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		month,pack=acccode.split(':')
    		month=int(month)
    		monthnam = calendar.month_name[month]

    		return render_to_response('IIIb/admiinpayoutoption.html',{
    			'month':monthnam,
    			'month_index':month, 'pack':pack})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')




def wallapprove(request):
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
		year=f.year
		fdate=date(year,f.month,f.day)

		if staff.thrift3b_admin==0 :
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			month =request.POST['month12']
			pack =request.POST['pack13']

			month=int(month)
			monthnam = calendar.month_name[month]

			account_type=pack
			status='Awaiting Execution'
		
			scsenario = tblIIIbfieldagent.objects.filter(branch=mybranch,
				month=monthnam,
				year=year,
				account_type=account_type,
				status=status)

			tt=scsenario.aggregate(Sum('amount'))
			total = tt['amount__sum']

			
			for k in scsenario:
				staff = k.staff.id
				staff=tblIIIbcoop.objects.get(id=staff,branch=mybranch,status=1)

				tblIIIbsavingsaccount(branch=mybranch,
				month=monthnam,
				staff=staff,
				year=k.year,
				account_type=k.scheme,
				code=k.code,
				amount=k.amount,
				status='CR').save()

			scsenario.update(status='Executed')


			tblIIIbapprovals(branch=mybranch,
				staff=staff,
				status='Executed',
				month=monthnam,
				description=pack,
				transdate=fdate,
				amount=total,
				year=year).save()

			if pack=='package':
				
				pl=tblIIIIbstaffbsavings_pack.objects.filter(branch=mybranch,
					status='Running',
					year=year)

				

				for j in pl:
					staff = k.staff.id
					staff=tblIIIbcoop.objects.get(id=staff,branch=mybranch,status=1)					
					
					gh=tblIIIbfieldagent.objects.filter(branch=mybranch,
						scheme=j.description,
						staff=staff,
						status=status, #status = 'awaiting execution'
						year=j.year)


					if gh.count() <1:
						j.status='Completed'
						j.save()


			return render_to_response('IIIb/walapprov.html',{'company':mybranch, 
				'user':varuser,
				'status':pack,
				'year':year,
				'month':monthnam})


		
		else:
			return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/login/')





def lr(request):
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

		if staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form =savingsform(request.POST)

			if form.is_valid():
				staff =form.cleaned_data['email']

				try:
					memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)
					kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)
				except Exception, e:
					raise e
			else:
				msg = 'enter valid email'
				return render_to_response('IIIb/selectloan.html',{'msg':msg})

		else:
			msg=''
		return render_to_response('IIIb/app_loan.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')

def loanscene_old(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,funding=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		if funding=='-----':
        			msg='Select a source of fund for this transaction'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})
        		elif funding=='salary':
        			form=approveform()
        			return render_to_response('IIIb/salary.html',{'form':form,'user':user})

        		elif funding=='myself':
        			form=savingsform()
        			return render_to_response('IIIb/self.html',{'form':form,'user':user})

        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/')



def loandem(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		if month=='-':
        			msg='Select a month'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})



        		month=int(month)
        		monthnam = calendar.month_name[month]

    			scsenario = tblIIIbloandapplications.objects.filter(branch=mybranch,date__month=month,status=status)
    			return render_to_response('IIIb/app_decl.html',{'email':user,'msg':scsenario,'status':status, 'month':monthnam})


        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render_to_response('lesson/entersub.html',{'gdata':getdetails})
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


		loans = tblstandardloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			description=request.POST['package']
			rate= request.POST['rate']
			fromm= request.POST['fromm']
			pack_count=loans.count()

			if pack_count == 0 :
				tblstandardloanIIIB(rate = 0 ,description='-----', staffrec=user,branch=mybranch,status='ACTIVE',from_week=0).save()
				tblstandardloanIIIB(rate = rate ,status='ACTIVE', description=description, staffrec=user,branch=mybranch,from_week=fromm).save()
			else:
				tblstandardloanIIIB(rate = rate ,status='ACTIVE',description=description, staffrec=user,branch=mybranch,from_week=fromm).save()
			msg = "package added successfully"
			return render_to_response('IIIb/addpackage.html',{'company':mybranch, 'user':varuser,'msg':msg})

		return render_to_response('IIIb/set_uploan.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/')




def loan_limit(request):
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


		loans = tblmaxloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			rate=request.POST['rate']
			tblmaxloanIIIB(branch=mybranch,value=rate).save()

			return render_to_response('IIIb/limitsuccess.html',{'company':mybranch, 'user':varuser,'rate':rate})



		else:
			if loans.count() > 0:
				return render_to_response('IIIb/loanvalue.html',{'company':mybranch, 'user':varuser,'loans':loans})
			else:
				return render_to_response('IIIb/loanlimit.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/')

def opening(request):
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


		loans = tblstandardloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			email=request.POST['email']
			try:
				staff = tblSTAFF.objects.get(branch=mybranch, email=email)
			except:
				msg = 'Invalid Email'
				return render_to_response('IIIb/selectloan.html',{'msg':msg})

			staff2= tblIIIbcoop.objects.get(staff=staff)
			amt = tblIIIbsavingsaccount.objects.filter(branch=mybranch, staff=staff2, account_type='Wallet')
			amt =amt.aggregate(Sum('amount'))
			amt = amt['amount__sum']
			return render_to_response('IIIb/stafbal.html',{'company':mybranch, 'user':varuser,'staff':staff,'tot':amt})


		return render_to_response('IIIb/opening.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/')


def uppld(request):
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

		loans = tblstandardloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		llgg = LGA.objects.all().count()

		if staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':

			if request.FILES['input_excel']:

				if llgg < 1 :
					input_excel=request.FILES['input_excel']
					num = []
					rows = "testing"
					book = xlrd.open_workbook(file_contents=input_excel.read())
					sheet = book.sheet_by_index(0)
					for row_no in range(0, sheet.nrows):
						rows = sheet.row_values(row_no)
						num.append(rows)
					ncount = len(num)

					try:
						for k in num:
							j1 = k[0]
							j2 = k[1]
							savecon = LGA (state = j1,lga = j2)
							savecon.save()
						succ = "Record Uploaded !!!"
						return render_to_response('setup/upload.html',{'succ':succ})
					except:
						succ ="Uploading Error "
					return render_to_response('setup/upload.html',{'succ':succ})

		return render_to_response('IIIb/upload.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/')




def savings_setup(request):
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


		loans = tblstandardsavingIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)
		user=tblIIIbcoop.objects.get(branch=mybranch,staff=user)

		if staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = setsave(request.POST)
			if form.is_valid():
				description=request.POST['package']
				frommonth=form.cleaned_data['month_from']
				tomonth=form.cleaned_data['month_to']


				pack_count=loans.count()
				description=description.lower()

				if pack_count == 0 :
					tblstandardsavingIIIB(description='-----', staffrec=user,branch=mybranch,status='ACTIVE',from_month=0,to_month=0).save()
					tblstandardsavingIIIB(status='ACTIVE', description='Wallet', staffrec=user,branch=mybranch,from_month='January',to_month='December').save()
					tblstandardsavingIIIB(status='ACTIVE', description='subscription', staffrec=user,branch=mybranch,from_month='January',to_month='December').save()
					tblstandardsavingIIIB(status='ACTIVE', description=description, staffrec=user,branch=mybranch,from_month=frommonth,to_month=tomonth).save()
				else:
					df = tblstandardsavingIIIB.objects.filter(branch=mybranch, description=description)
					if df.count() > 0:
						pass
					else:
						tblstandardsavingIIIB(status='ACTIVE',description=description, staffrec=user,branch=mybranch,from_month=frommonth,to_month=tomonth).save()
				msg = "package added successfully"
				return render_to_response('IIIb/addsavee.html',{'company':mybranch, 'user':varuser,'msg':msg})

		else:
			form = setsave()
		return render_to_response('IIIb/set_upsavings.html',{'company':mybranch, 'user':varuser,'loans':loans,'form':form})
	else :
		return HttpResponseRedirect('/login/')



def manage_setup(request):
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


		loans = tblstandardsavingIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = setsave(request.POST)
			if form.is_valid():
				description=request.POST['package']
				frommonth=form.cleaned_data['month_from']
				tomonth=form.cleaned_data['month_to']


				pack_count=loans.count()

				if pack_count == 0 :
					tblstandardsavingIIIB(description='-----', staffrec=user,branch=mybranch,status='ACTIVE',from_month=0,to_month=0).save()
					tblstandardsavingIIIB(status='ACTIVE', description=description, staffrec=user,branch=mybranch,from_month=frommonth,to_month=tomonth).save()
				else:
					tblstandardsavingIIIB(status='ACTIVE',description=description, staffrec=user,branch=mybranch,from_month=frommonth,to_month=tomonth).save()
				msg = "package added successfully"
				return render_to_response('IIIb/addsavee.html',{'company':mybranch, 'user':varuser,'msg':msg})

		else:
			form = setsave()
		return render_to_response('IIIb/managesetup.html',{'company':mybranch, 'user':varuser,'loans':loans,'form':form})
	else :
		return HttpResponseRedirect('/login/')




def staffwelcome(request):
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
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('IIIb/welcome.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/')









#**********************My LOANs**************************************
def reqloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)
		surname=coop.staff.surname
		firstname=coop.staff.firstname
		cop_man = Userprofile.objects.get(branch=mybranch,thrift3b_admin=1)
		cop_man = cop_man.staffrec.surname + cop_man.staffrec.firstname 


#***********************####  ACCOUNT BALANCE************************
		sav=tblIIIbsavingsaccount.objects.filter(branch=mybranch,
			status='CR',
			staff=coop)

		if sav.count()>0:

			add=sav.aggregate(Sum('amount'))
			add_cr = add['amount__sum']
		else:
			add_cr = 0

		sav_dr=tblIIIbsavingsaccount.objects.filter(branch=mybranch,
			status='DR',
			staff=coop) 

		if sav_dr.count()>0 :
			add=sav_dr.aggregate(Sum('amount'))
			add_dr = add['amount__sum']
		else:
			add_dr =0

		amount=add_cr - add_dr

##**************###MAX LOAN***********************

		mmx =tblmaxloanIIIB.objects.get(branch=mybranch)
		mx_loan = mmx.value
		mx_loan=int(mx_loan)
		mx_loan=mx_loan * amount / 100
		mx_loan=  locale.format("%.2f",mx_loan,grouping=True)


		pending = tblIIIbloandapplications.objects.filter(branch=mybranch,
			staffrec=coop,status='Awaiting Approval')


		running = tblIIIbloandapplications.objects.filter(branch=mybranch,
			staffrec=coop,status='Running')

		approved = tblIIIbloandapplications.objects.filter(branch=mybranch,
			staffrec=coop,status='Approved')






		if request.method == 'POST':
			form = loanreqform(request.POST)
			if form.is_valid():

				thrift=request.POST['thrift']
				amount= request.POST['amount']
				package=request.POST['package']
				repay=request.POST['repay']

				if repay=='-----':
					msg = 'Select the month you would like to commence repayment'
					return render_to_response('IIIb/selectloan.html',{'msg':msg})

				fdate= datetime.today()
				todayy=date(fdate.year,fdate.month,fdate.day)

				loan_package = tblstandardloanIIIB.objects.get(description=package, branch=mybranch)



				tblIIIbloandapplications(branch=mybranch,staffrec=coop,package=loan_package,
					volume=amount,status='Awaiting Approval', repay_month= repay, date= todayy,thrift=thrift).save()



				##********Sending email notifications*************
				try:
					loanbook_email(varuser,surname,firstname,amount,cop_man)
				except:
					pass
				# sendMailapplyloan(email)

				if staff.thrift3b_admin==1:
					return render_to_response('IIIb/booking.html',{'company':mybranch, 'user':varuser,'customer':0})
				elif staff.thrift3b_cashier==1:
					return render_to_response('IIIb/booking_cashier.html',{'company':mybranch, 'user':varuser,'customer':0})
				elif staff.thrift3b_officer==1:
					return render_to_response('IIIb/booking_officer_success.html',{'company':mybranch, 'user':varuser,'customer':0})




		else:
			form = loanreqform()

			if staff.thrift3b_admin==1:

				if pending.count() > 0 :
					msg='Your previous application is still awaiting approval. Contact the manager or Select log to view'
					return render_to_response('IIIb/req_cash_admin1.html',{'company':mybranch,'name':find_staff,'user':varuser,'msg':msg})


				elif running.count() > 0 :
					msg='You have a running loan, fresh loans are not applicable at this moment'
					return render_to_response('IIIb/req_cash_admin1.html',{'company':mybranch,'name':find_staff,'user':varuser,'msg':msg})

				else:
					return render_to_response('IIIb/req_cash_admin.html',{'company':mybranch,'name':find_staff,'user':varuser,'form':form,'amount':amount,'max':mx_loan})



			elif staff.thrift3b_cashier==1:

				if pending.count() > 0 :
					msg='Your previous application is still awaiting approval. Contact the manager or Select log to view'
					return render_to_response('IIIb/req_cash_c1.html',{'company':mybranch,'name':find_staff,'user':varuser,'msg':msg})

				elif running.count() > 0 :
					msg='You have a running loan, fresh loans are not applicable at this moment'
					return render_to_response('IIIb/req_cash_c1.html',{'company':mybranch,'name':find_staff,'user':varuser,'msg':msg})
				else:
					return render_to_response('IIIb/req_cash_c.html',{'company':mybranch, 'name':find_staff,'user':varuser,'form':form,'amount':amount,'max':mx_loan})
			


			elif staff.thrift3b_officer==1:

				if pending.count() > 0 :
					msg='Your previous application is still awaiting approval. Contact the manager or Select log to view'
					return render_to_response('IIIb/req_cash_o1.html',{'company':mybranch,'name':find_staff,'user':varuser,'msg':msg})

				elif running.count() > 0 :
					msg='You have a running loan, fresh loans are not applicable at this moment'
					return render_to_response('IIIb/req_cash_o1.html',{'company':mybranch,'name':find_staff,'user':varuser,'msg':msg})
				else:
					return render_to_response('IIIb/req_cash_o.html',{'company':mybranch, 'name':find_staff,'user':varuser,'form':form,'amount':amount,'max':mx_loan})


	else:
		return HttpResponseRedirect('/login/')



def loandetails(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,loan,amount=acccode.split(":")

        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)
        		memstaff = tblIIIbcoop.objects.get(staff=memstaff,branch=mybranch,status=1)

        		if amount== '':
        			msg='enter amount'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})
        			
        		elif loan == '-----':
        			msg='select a loan package'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})


    			det = tblstandardloanIIIB.objects.get(description=loan, branch=mybranch)
    			loan_rate = int(det.rate)
    			amount=int(amount)
    			duration = int(det.tenure)
    			thrift  = (100 + loan_rate )
    			thrift = thrift / 100
    			thrift = thrift * amount
    			thrift=  thrift / duration
    			thrift=  locale.format("%.2f",thrift,grouping=True)

    			return render_to_response('IIIb/staffbookloan.html',{'email':user,
    				'amount':amount,
    				'loan':loan,
    				'duration':duration,
    				'thrift':thrift})

        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render_to_response('lesson/entersub.html',{'gdata':getdetails})
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

		if staff.thrift3b_officer==0: 
			return render_to_response('IIIb/404loan.html',{'company':mybranch, 'user':varuser})


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

		if request.method == 'POST':
			thrift=request.POST['thrift']
			amount= request.POST['amount']
			package=request.POST['package']
			repay=request.POST['repay']

			if repay=='-----':
				msg = 'Select appropriate repayment month'
				return render_to_response('IIIb/selectloan.html',{'msg':msg})

			fdate= datetime.today()
			todayy=date(fdate.year,fdate.month,fdate.day)

			loan_package = tblstandardloanIIIB.objects.get(description=package, branch=mybranch)

			try:
				etwtwer
			except:

				tblIIIbloandapplications(branch=mybranch,staffrec=find_staff,package=loan_package,
					volume=amount,status='Not Approved', date= todayy,thrift=thrift).save()

				email = [varuser]
				# sendMailapplyloan(email)

				if staff.thrift3b_cashier==1:
					return render_to_response('IIIb/booking_cashier.html',{'company':mybranch, 'user':varuser,'customer':0})
				else:
					return render_to_response('IIIb/booking_officer_success.html',{'company':mybranch, 'user':varuser,'customer':0})


	else:
		return HttpResponseRedirect('/login/')





def loanhistory(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		find_staff = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)
		loan_list = tblIIIbloandapplications.objects.filter(branch=mybranch,staffrec=find_staff)

		if staff.thrift3b_admin==1:
				return render_to_response('IIIb/loanhist_admin.html',{'company':mybranch,
					'name':find_staff,'user':varuser,'list':loan_list})
		
		elif staff.thrift3b_cashier==1:
			return render_to_response('IIIb/loanhist_c.html',{'company':mybranch,
					'name':find_staff,'user':varuser,'list':loan_list})
		
		elif staff.thrift3b_officer==1:
			return render_to_response('IIIb/loanhist.html',{'company':mybranch,
					'name':find_staff,'user':varuser,'list':loan_list})

	else:
		return HttpResponseRedirect('/login/')



def loanperformance(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		find_staff = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)

		p=[]

		# try:
		loan_detail =  tblIIIbloandapplications.objects.filter(status='Running', branch=mybranch,	staffrec=find_staff)
		

		# y,m,d =loan_detail.date.split("-")
		# month = calendar.month_name[int(m)]

			# if staff.thrift3b_cashier==0:
			# 	return render_to_response('IIIb/not_approved.html',{'company':mybranch,
			# 		'k':loan_detail,
			# 		'month':month,
			# 		'year': y,
			# 		'user':varuser})

			# elif staff.thrift3b_cashier == 1 :
			# 	return render_to_response('IIIb/notappadmin.html',{'company':mybranch,
			# 		'k':loan_detail,
			# 		'month':month,
			# 		'year': y,
			# 		'user':varuser})

		# except :

		# 	try:
		# 		loan_detail =  tblIIIbloandapplications.objects.get(status='Awaiting Payment', branch=mybranch,
		# 			staffrec=memstaff)

		# 		loan_pack = loan_detail.package

		# 		trans = tblIIIbloantransaction.objects.filter(transaction_source=loan_detail)



		# 		for k in trans:
		# 			month= k.start_date
		# 			year,month,day=month.split('-')
		# 			year=str(year)
		# 			month =str(month)
		# 			month =int(month)
		# 			monthnam = calendar.month_name[month]
		# 			det = {'month':monthnam, 'year':year,'amount':k.amount,'status':k.status}
		# 			p.append(det)


			# except :
			# 	msg = ''

		if staff.thrift3b_admin==1:
			return render_to_response('IIIb/loanperf.html',{'p':loan_detail,'company':mybranch,'name':find_staff,'user':varuser})

		elif staff.thrift3b_cashier == 1 :
			return render_to_response('IIIb/loanperf_c.html',{'p':loan_detail,'company':mybranch,'name':find_staff,'user':varuser})
		
		elif staff.thrift3b_officer == 1 :
			return render_to_response('IIIb/loanperf_o.html',{'p':loan_detail,'company':mybranch,'name':find_staff,'user':varuser})



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
				t1= tblstandardloanIIIB.objects.filter(branch=mybranch)
				sdic={}
				kk=[]

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


		if staff.thrift3b_cashier==0:
				return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			email=request.POST['email']
			p=[]

			try :
				memstaff = tblSTAFF.objects.get(branch=mybranch,email=email)
				lln=tblIIIbloandapplications.objects.get(staffrec=memstaff,branch=mybranch,
					status='Running')

				ltrans = tblIIIbloantransaction.objects.filter(transaction_source=lln)

				for k in ltrans:
					month= k.start_date
					year,month,day=month.split('-')
					year=str(year)
					month =str(month)
					month =int(month)
					monthnam = calendar.month_name[month]
					det = {'month':monthnam, 'year':year,'amount':k.amount,'status':k.status,'id':k.id}
					p.append(det)

				return render_to_response('IIIb/repay_hist.html',{'name':memstaff,'email':email,'company':mybranch,'user':varuser,'p':p})

			except:

				msg='no loan to repay'

				return render_to_response('IIIb/repay1.html',{'company':mybranch,'user':varuser,'msg':msg})

		else:
			msg = ''
			return render_to_response('IIIb/repay1.html',{'company':mybranch,'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def optionx(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,email=acccode.split(':')
    		myloan=tblIIIbloantransaction.objects.get(id=acccode)
    		mydate = int(myloan.start_date.split('-')[1])
    		monthnam = calendar.month_name[mydate]

    		return render_to_response('IIIb/repayopt.html',{'code':acccode,'hhh':myloan,'date':monthnam,'email':email})
    	else:
    		return HttpResponseRedirect('/login/')
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
		f= datetime.today()
		mday=f.day
		mmonth = f.month
		myear=f.year
		fdate=date(myear,mmonth,mday)

		if staff.thrift3b_cashier==0 or staff.thrift3b_admin==0 or staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			email =request.POST['email']
			loan_code=request.POST['myid']
			myloan=tblIIIbloantransaction.objects.get(id= loan_code)
			myloan.status="CR"
			myloan.save()
			y,m,d =myloan.start_date.split("-")
			month = calendar.month_name[int(m)]
			email=[email]

			sendMailrepayloan(email,mmonth,y)

			soou = myloan.transaction_source.id
			loandet = tblIIIbloandapplications.objects.get(id=soou)

			myloancount=tblIIIbloantransaction.objects.filter(transaction_source=loandet, status="DR")

			if myloancount.count() < 1:
				tblIIIbloandapplications.objects.filter(status='Running').update(status= 'Fully Paid')
				sendMailfullypaid(email)
			return HttpResponseRedirect('/dashboard/')

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/')



def history(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)
		

		sav=tblIIIbsavingsaccount.objects.filter(branch=mybranch,
			status='CR',
			staff=coop)

		if sav.count()>0:

			add=sav.aggregate(Sum('amount'))
			add_cr = add['amount__sum']
		else:
			add_cr = 0

		sav_dr=tblIIIbsavingsaccount.objects.filter(branch=mybranch,
			status='DR',
			staff=coop) 

		if sav_dr.count()>0 :
			add=sav_dr.aggregate(Sum('amount'))
			add_dr = add['amount__sum']
		else:
			add_dr =0

		amount=add_cr - add_dr

		if staff.thrift3b_admin==1:
			return render_to_response('IIIb/adm_ac_bal.html',{'company':mybranch,
				'user':varuser,
				'msg':coop,
				'amount':amount})

		elif staff.thrift3b_cashier==1:
			return render_to_response('IIIb/adm_ac.html',{'company':mybranch,
				'user':varuser,
				'msg':coop,
				'amount':amount})

		elif staff.thrift3b_officer==1:
			return render_to_response('IIIb/adm_o.html',{'company':mybranch,
				'user':varuser,
				'msg':coop,
				'amount':amount})

	else:
		return HttpResponseRedirect('/login/')


def statement(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)
		
		statement=tblIIIbsavingsaccount.objects.filter(branch=mybranch,staff=coop)

		sav=tblIIIbsavingsaccount.objects.filter(branch=mybranch,
			status='CR',
			staff=coop)

		if sav.count()>0:

			add=sav.aggregate(Sum('amount'))
			add_cr = add['amount__sum']
		else:
			add_cr = 0

		sav_dr=tblIIIbsavingsaccount.objects.filter(branch=mybranch,
			status='DR',
			staff=coop) 

		if sav_dr.count()>0 :
			add=sav_dr.aggregate(Sum('amount'))
			add_dr = add['amount__sum']
		else:
			add_dr =0

		amount=add_cr - add_dr

		if staff.thrift3b_admin==1:
			return render_to_response('IIIb/statement.html',{'company':mybranch,
				'user':varuser,
				'msg':coop,
				'statement':statement,
				'amount':amount})

		elif staff.thrift3b_cashier==1:
			return render_to_response('IIIb/statement_c.html',{'company':mybranch,
				'user':varuser,
				'msg':coop,
				'statement':statement,
				'amount':amount})

		elif staff.thrift3b_officer==1:
			return render_to_response('IIIb/statement_o.html',{'company':mybranch,
				'user':varuser,
				'statement':statement,
				'msg':coop,
				'amount':amount})

	else:
		return HttpResponseRedirect('/login/')


##############################H-R********************************
def hr(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_cashier==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)



		form = mysavingsform()
		if staff.thrift3b_cashier==1:
			return render_to_response('IIIb/hr_income.html',{'company':mybranch,
				'user':varuser,
				'form':form,
				'msg':coop})

	else:
		return HttpResponseRedirect('/login/')


def deductions(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_cashier==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)


		form = approveform()
		if staff.thrift3b_cashier==1:
			return render_to_response('IIIb/hr_deduct.html',{'company':mybranch,
				'user':varuser,
				'form':form,
				'msg':coop})

	else:
		return HttpResponseRedirect('/login/')



def deajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.filter(branch=mybranch,status=1)

	

        		if month=='-':
        			msg='Select valid Month'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})


        		month=int(month)
        		monthnam = calendar.month_name[month]
        		tdate=date.today()
        		year=tdate.year

        		status='CR'

        		allmoney =0
        		yup=[]

        		for t in kfw:

        				##deductions from savings*******************

	        		scsenario = tblIIIbsavingsaccount.objects.filter(branch=mybranch,
	        			month=monthnam,
	        			staff=t,
	        			status=status)

	        		if scsenario.count() ==0:
	        			total=0
	        		else:
		        		tt=scsenario.aggregate(Sum('amount'))
		        		total = tt['amount__sum']

		        		allmoney=allmoney+total

			        	tg={'staff':t,'total':total}
			        	yup.append(tg)

		##dections from loan repayment
		##deductions from commodities


		
        		return render_to_response('IIIb/hr_deduct_ajax.html',{
        			'msg':yup,
        			'status':status, 
        			'month':monthnam,
        			'year':year,
        			'total':total,
        			'pack':allmoney})


        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/')