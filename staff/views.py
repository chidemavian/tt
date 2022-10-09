from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from staff.forms import *
from sysadmin.models import *
from staff.models import *
from datetime import date
import calendar

from staff.utils import *
from IIIb.models import *


from django.db.models import Max,Sum
today=date.today()





def welcome(request):
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

		if staff.ceo==0 :
			return render_to_response('staff/404.html',{'company':mybranch, 'user':varuser})
		if staff.thrift3b==1:
			return render_to_response('staff/3bwelcome.html',{'company':mybranch, 'user':varuser})
		else:
			return render_to_response('staff/welcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def newst(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.ceo==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if request.method == 'POST':
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']


			if 'photo' in request.FILES:
				photo=request.FILES['photo']
			else:
				photo = 'staff-pix/user.png'

			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])
			try:
				phone=int(phone)
			except:
				return render_to_response('staff/staffdet.html',{'company':mybranch, 'user':varuser})

			wallet=phone

			try:
				countt=tblSTAFF.objects.get(email=email,branch=mybranch) #whether active or not
				msg = "EMAIL ALREADY EXIST"
				return render_to_response('staff/staffdet.html',{'company':mybranch,
					'user':varuser,'msg':msg})

			except:

				pin = generate_staff_pin()

				password = generate_password()


				tblSTAFF(surname=surname,firstname=firstname,othername=othername, status=1,phone=phone,Address=address,photo=photo,code=pin,email=email,branch=mybranch,types='Field').save()

				myuser =tblSTAFF.objects.get(email=email,branch=mybranch)  #whether active or not

				Userprofile(status=1,
					branch=mybranch,
					code=pin,
					staffrec=myuser,
					password=password,
					email=email).save()

				try:
					staff_registration(email,surname,password)
				except:
					pass

				if staff.thrift3b==1:

					tblIIIbcoop(branch=mybranch,staff=myuser,code=pin,status=1,thrift3b=1 ).save()
					fr= Userprofile.objects.filter(email=email).update(thrift3b=1, thrift3b_officer=1)
					return render_to_response('staff/success3b.html',{'company':mybranch,'user':varuser,'email':email})
				
				else:
					return render_to_response('staff/success.html',{'company':mybranch,'user':varuser,'email':email})

		else:

			if staff.thrift3b==1:
				return render_to_response('staff/membership.html',{'company':mybranch, 'user':varuser})
			
			sub = tblsubscription.objects.filter(branch=mybranch)
			return render_to_response('staff/staffdet.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



def massReg(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)


		if staff.ceo == 0:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})


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
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		msg = ''

		if request.method == 'POST':
			excel =request.FILES['excel']

			# try :
			# 	sds =7

			# 	return render_to_response('staff/success.html',{'company':mybranch,'user':varuser,'wallet':wallet})

			# except:
			# 	msg = 'Incomplete phone number'

		if staff.thrift3b==1:
			return render_to_response('staff/massregthreeb.html',{'company':mybranch, 'user':varuser,'msg':msg})
		else:
			return render_to_response('staff/massreg.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')






def regmerchant2(request): #from daily contr service
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
						ibco = tblMERCHANT.objects.get(branch = mybranch, thrift1a=1,staff=querry_email)
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
							sendMailCO_ON(email)
							tblMERCHANT(status=1,branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()
						except:
							tblMERCHANT(status=1, branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()

				elif mycount == 0:
					msg = 'THIS EMAIL IS NOT REGISTERED'
			else:
				msg = 'INVALID ENTRY'
		else:
			form =fieldofficerfform()
			msg=''

		meer = tblMERCHANT.objects.filter(branch=mybranch,thrift1a=1)
		mycolist = tblMERCHANT.objects.filter(status=1, thrift1a=1, branch=mybranch).count()
		inactiveco = tblMERCHANT.objects.filter(status=0, thrift1a=1, branch=mybranch).count()

		return render_to_response('Ia/merch.html',{'staffcount':mystafflist, 'ggg': mycolist,'company':mybranch,'msg':msg, 'user':varuser,'form':form,'merchant':meer})

	else:
		return HttpResponseRedirect('/login/user/')






def deactivate(request):
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
			return render_to_response('staff/404.html',{'company':mybranch, 'user':varuser})

		if request.method== 'POST':
			email= request.POST['email']

			mystaff = tblSTAFF.objects.filter(branch=mybranch, email=email,status=1) #check status
			mycount=mystaff.count()

			if mycount == 1:
				querry_email = tblSTAFF.objects.get(email=email)

				try:
					ibco=Userprofile.objects.get(staffrec=querry_email,status=1)
				except:
					msg = 'this account is already inactive'
					# ibco=Userprofile.objects.get(staffrec=querry_email,status=0)

					# return render_to_response('stafffdetails.html',{'detail':ibco,
					# 	'company':mybranch,
					# 	'msg':msg, 'user':varuser})

					return render_to_response('staff/selectloan.html',{'msg':msg})

				if ibco.ceo ==0 :
					if ibco.status == 1:
						ibco.status=0
						msg='Account Deactivated successfully!!!'
						ibco.save()

						try:
							sendMailCO_ON(email)

						except:
							m=9


				else:
					msg = 'Cant deactivate the account'
			else:
				msg = 'Invalid email'
		else:
			msg=''

		return render_to_response('staff/merch.html',{'company':mybranch,'msg':msg, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')



def activate(request):
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
			return render_to_response('staff/404.html',{'company':mybranch, 'user':varuser})

		if request.method== 'POST':
			email= request.POST['email']

			mystaff = tblSTAFF.objects.filter(branch=mybranch, email=email,status=1) #check status
			mycount=mystaff.count()

			if mycount == 1:
				querry_email = tblSTAFF.objects.get(email=email)

				try:
					ibco=Userprofile.objects.get(staffrec=querry_email,status=1)
				except:
					# msg = 'this account is already inactive'
					ibco=Userprofile.objects.get(staffrec=querry_email,status=0)

					# # return render_to_response('stafffdetails.html',{'detail':ibco,
					# # 	'company':mybranch,
					# # 	'msg':msg, 'user':varuser})

					# return render_to_response('staff/selectloan.html',{'msg':msg})

					if ibco.ceo ==0 :
						if ibco.status == 0:
							ibco.status=1
							msg='Account Activated successfully!!!'
							ibco.save()

							try:
								sendMailCO_ON(email)

							except:
								m=9
						else :
							msg ='This account is already activate'

					else:
						msg = 'Cant deactivate the account'

					msg ='User already  active!!!'



			else:
				msg = 'Invalid email'
		else:
			msg=''

		return render_to_response('staff/activate.html',{'company':mybranch,'msg':msg, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')


def delete(request):
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
			return render_to_response('staff/404.html',{'company':mybranch, 'user':varuser})

		if request.method== 'POST':
			form = staffform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']
				mystaff = tblSTAFF.objects.filter(branch=mybranch, email=email,status=1) #check status
				mycount=mystaff.count()

				if mycount == 1:
					querry_email = tblSTAFF.objects.get(email=email)
					pin = querry_email.code

					try:
						ibco = tblMERCHANT.objects.get(branch = mybranch, staff=querry_email)
						if ibco.thrift1b == 0:
							msg = 'nor efr'

						elif ibco.thrift1b == 1:
							msg='ALREADY REGISTERED'

					except:
						diff = Userprofile.objects.get(email=email,status=1)
						diff.thrift_officer=1
						diff.save()
						tblMERCHANT(branch = mybranch,code=pin, staff=querry_email,thrift1a=1).save()
						form = staffform()
						msg="SUCCESSFUL"
						try:
							sendMailCO_ON(email)
							tblMERCHANT(status=1,branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()
						except:
							tblMERCHANT(status=1, branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()

				else:
					msg = 'THIS EMAIL IS NOT REGISTERED OR STAFF IS INACTIVE'
			else:
				msg = 'INVALID ENTRY'
		else:
			form = staffform()
			msg=''

		return render_to_response('staff/delete.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')


def reset(request):
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
			return render_to_response('staff/404.html',{'company':mybranch, 'user':varuser})

		if request.method== 'POST':
			form = staffform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']
				mystaff = tblSTAFF.objects.filter(branch=mybranch, email=email,status=1) #check status
				mycount=mystaff.count()

				if mycount == 1:
					querry_email = tblSTAFF.objects.get(email=email)
					pin = querry_email.code

					try:
						ibco = tblMERCHANT.objects.get(branch = mybranch, staff=querry_email)
						if ibco.thrift1b == 0:
							msg = 'nor efr'

						elif ibco.thrift1b == 1:
							msg='ALREADY REGISTERED'

					except:
						diff = Userprofile.objects.get(email=email,status=1)
						diff.thrift_officer=1
						diff.save()
						tblMERCHANT(branch = mybranch,code=pin, staff=querry_email,thrift1a=1).save()
						form = staffform()
						msg="SUCCESSFUL"
						try:
							sendMailCO_ON(email)
							tblMERCHANT(status=1,branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()
						except:
							tblMERCHANT(status=1, branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()

				else:
					msg = 'THIS EMAIL IS NOT REGISTERED OR STAFF IS INACTIVE'
			else:
				msg = 'INVALID ENTRY'
		else:
			form = staffform()
			msg=''

		return render_to_response('staff/reset.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')




def tutorial(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		if staff.ceo==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)


## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.ceo==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('staff/adminwelcome.html',{'company':mybranch, 'user':varuser})
		# pass
	else:
		return HttpResponseRedirect('/login/user/')


def roles(request):
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
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		stafflist = Userprofile.objects.filter(branch=mybranch,status=1).exclude(email='njc@gmail.com')
		mystafflist=[]
		for  k in stafflist:
			name=k.staffrec.surname + "  " + k.staffrec.firstname +"  "+ k.staffrec.othername
			ID = k.staffrec.id
			s= {'name':name,'id':ID}
			mystafflist.append(s)

		if staff.thrift3b==1:

			return render_to_response('staff/stafflist3b.html',{
				'company':mybranch, 
				'user':varuser,
				'list':mystafflist})
		else:

			return render_to_response('staff/stafflist.html',{
				'company':mybranch, 
				'user':varuser,
				'list':mystafflist})

	else:
		return HttpResponseRedirect('/login/user/')




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
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})



		stafflist = tblSTAFF.objects.filter(branch=mybranch,status=1).exclude(email='njc@gmail.com')
		# stafflist = Userprofile.objects.filter(branch=mybranch,status=1).exclude(email='njc@gmail.com')
		# mystafflist=[]
		# for  k in stafflist:
		# 	name=k.staffrec.surname + "  " + k.staffrec.firstname +"  "+ k.staffrec.othername
		# 	ID = k.staffrec.id
		# 	s= {'name':name,'id':ID}
		# 	mystafflist.append(s)

		return render_to_response('staff/listofstaff.html',{'company':mybranch, 'user':varuser,'list':stafflist})

	else:
		return HttpResponseRedirect('/login/user/')

def setroles(request):
	if  "userid" in request.session:
		if request.is_ajax():
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				stafflist = tblSTAFF.objects.get(id = acccode)
				userlist = Userprofile.objects.get(staffrec=stafflist,status=1)
				branch_code = stafflist.branch.id
				appplist = tblapp.objects.get(branch=branch_code)

				myy=[]
				name = stafflist.surname.upper() + " " + stafflist.firstname.upper() + " " + stafflist.othername.upper()


#######thrifts IA********************
				if userlist.cashier is True:
					cashier= 'checked'
				else:
					cashier='unchecked'

				if userlist.admin is True:
					admin='checked'
				else:
					admin='unchecked'


#######thrifts IB********************
				if userlist.thrift1b_cashier is True:
					thrift1bcashier= 'checked'
				else:
					thrift1bcashier='unchecked'

				if userlist.thrift1b_admin is True:
					thrift1badmin='checked'
				else:
					thrift1badmin='unchecked'

#############loan IB*******************
				if userlist.loan1b_officer is True:
					loan1b_officer= 'checked'
				else:
					loan1b_officer='unchecked'

				if userlist.loan1b_admin is True:
					loan1b_admin='checked'
				else:
					loan1b_admin='unchecked'

##########thrift IIIA *********************
				if userlist.thrift3a_admin is True:
					thrift3a_admin= 'checked'
				else:
					thrift3a_admin='unchecked'

				if userlist.thrift3a_cashier is True:
					thrift3a_officer='checked'
				else:
					thrift3a_officer='unchecked'

##########thrift IIIB *********************
				if userlist.thrift3b_admin is True:
					thrift3b_admin= 'checked'
				else:
					thrift3b_admin='unchecked'

				if userlist.thrift3b_cashier is True:
					thrift3b_officer='checked'
				else:
					thrift3b_officer='unchecked'


#############loan IIIB*******************
				if userlist.loan3b_officer is True:
					loan3b_officer= 'checked'
				else:
					loan3b_officer='unchecked'

				if userlist.loan3b_admin is True:
					loan3b_admin='checked'
				else:
					loan3b_admin='unchecked'

####coop*****************

				s= {'name':name ,
				'cash':cashier,'adm':admin,
				'thr1bc':thrift1bcashier,'thr1bad':thrift1badmin,
				'loan1bo':loan1b_officer,'loan1ba':loan1b_admin,
				'thr3aad':thrift3a_admin,'thr3ao':thrift3a_officer,
				'thr3bad':thrift3b_admin,'thr3bo':thrift3b_officer,
				'loan3ba':loan3b_admin , 'loan3bo':loan3b_officer,
				'app':appplist}



				myy.append(s)
				return render_to_response('staff/staffroles.html',{'list':myy,'ID':acccode})
			else:
				gdata = ""
				return render_to_response('index.html',{'gdata':gdata})
		else:
			gdata = ""
			return render_to_response('getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')

def updaterole(request,vid):
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
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		thestaff = tblSTAFF.objects.get(id=vid)

 #Thrift IA*********************
		if 'mycashier' in request.POST:
			cashier=request.POST['mycashier']
			Userprofile.objects.filter(staffrec= thestaff).update(cashier=cashier)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(cashier=0)


		if 'myadmin' in request.POST:
			admin=request.POST['myadmin']
			Userprofile.objects.filter(staffrec= thestaff).update(admin=1)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(admin=0)


#thrift IB************************

		if 'thr1bc' in request.POST:
			ao=request.POST['thr1bc']
			
		else:
			ao =0

		Userprofile.objects.filter(staffrec= thestaff).update(thrift1b_cashier=ao)

		if 'thr1bad' in request.POST:
			sa=request.POST['thr1bad']
			
		else:
			sa =0
		
		Userprofile.objects.filter(staffrec= thestaff).update(thrift1b_admin=sa)


###loan IB**************************
		if 'loan1bcashier' in request.POST:
			lc=request.POST['loancashier']
			Userprofile.objects.filter(staffrec= thestaff).update(loan1b_officer=lc)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(loan1b_officer=0)

		if 'loan1badmin' in request.POST:
			la=request.POST['loanadmin']
			Userprofile.objects.filter(staffrec= thestaff).update(loan1b_admin=la)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(loan1b_admin=0)

### thrift IIIA**************************

		if 'thr3ac' in request.POST:
			co=request.POST['thr3ac']
			Userprofile.objects.filter(staffrec= thestaff).update(thrift3a_cashier=co)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(thrift3a_cashier=0)

		if 'thr3aad' in request.POST:
			ca=request.POST['thr3aad']
			Userprofile.objects.filter(staffrec= thestaff).update(thrift3a_admin=ca)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(thrift3a_admin=0)


### thrift IIIB**************************

		if 'thr3bc' in request.POST:
			co=request.POST['thr3bc']
			Userprofile.objects.filter(staffrec= thestaff).update(thrift3b_cashier=co)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(thrift3b_cashier=0)

		if 'thr3bad' in request.POST:
			ca=request.POST['thr3bad']
			Userprofile.objects.filter(staffrec= thestaff).update(thrift3b_admin=ca)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(thrift3b_admin=0)


### Loan IIIB**************************

		if 'loan3ao' in request.POST:
			co=request.POST['loan3ao']
			Userprofile.objects.filter(staffrec= thestaff).update(loan3b_officer=co)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(loan3b_officer=0)

		if 'loan3bad' in request.POST:
			ca=request.POST['thr3aad']
			Userprofile.objects.filter(staffrec= thestaff).update(loan3b_admin=ca)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(loan3b_admin=0)


		return HttpResponseRedirect('/staff/staff/roleplay/')

	else:
		return HttpResponseRedirect('/login/user/')

def viewdetail(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		if staff.ceo==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		if request.method=='POST':
			form = staffform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']

				mystaff = tblSTAFF.objects.filter(branch=mybranch, email=email,status=1) #check status
				mycount=mystaff.count()

				if mycount == 1:
					msg= ''
					querry_email = tblSTAFF.objects.get(email=email)

					return render_to_response('staff/myprofile.html',{'company':mybranch,
						'details':querry_email, 
						'user':varuser,'form':form})

				else:
					msg = 'THIS EMAIL IS NOT REGISTERED'
			else:
				msg = 'INVALID ENTRY'
		else:
			form = staffform()
			msg=''
		if staff.thrift3b==1:
			return render_to_response('staff/profdetail3b.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})
		else:
			return render_to_response('staff/profdetail.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')