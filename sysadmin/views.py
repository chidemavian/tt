from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse

from sysadmin.models import *
from customer.models import *
# from partner.models import *






def index(request):
	if request.method=='POST':
		email=request.POST['email']
		password=request.POST['password']
		
		try:			
			user=Userprofile.objects.get(email=email,password=password,status=1)
			request.session['userid'] = user.email
			varuser = request.session['userid']
			return  HttpResponseRedirect('/dashboard/')
		except: #customer login
			pass

		try:
			tblCUSTOMER.objects.get(wallet=email,status=1,surname=password)
			request.session['userid'] = email
			varuser = request.session['userid']
			return  HttpResponseRedirect('/home/')
		except:
			pass

		msg = 'Invalid Login Credentials, Contact Administrator'
		try:
			Userprofile.objects.get(email=email,password=password,status=0)
			msg =' your trial period has elapsed.'
			# return render_to_response('Ia/selectloan.html',{'msg':msg})
		except:
			pass

		
		return render_to_response('login.html',{'varerr':msg})


	else:
		return render_to_response('index.html')


def login(request):

	return render_to_response('login.html')



def inldex(request):
	if request.method=='POST':
		email=request.POST['email']
		password=request.POST['password']
		
		try:			
			user=Userprofile.objects.get(email=email,password=password,status=1)
			request.session['userid'] = user.email
			varuser = request.session['userid']
			return  HttpResponseRedirect('/dashboard/')
		except: #customer login
			if tblCUSTOMER.objects.filter(wallet=email,status=1,surname=password).count()==1:
				request.session['userid'] = email
				varuser = request.session['userid']
				return  HttpResponseRedirect('/home/')

			if Userprofile.objects.filter(email=email,password=password,status=0).count() ==1:
				msg =' your trial period has elapsed.'
				return render_to_response('Ia/selectloan.html',{'msg':msg})
			else:
				return HttpResponseRedirect('/login/user/')

	else:
		return render_to_response('index.html')



def dashboard(request):
	if 'userid' in request.session:
		varuser = request.session['userid']
		
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
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.ceo:

			if staff.thrift3b ==1:
				return render_to_response('c_dashboard.html',{'user':varuser,'company':mybranch,
					'pincode':staff})

			else:

				return render_to_response('dashboard.html',{'user':varuser,'company':mybranch,
					'pincode':staff})
		else:

			if staff.thrift3b ==1:
				return render_to_response('c_dashboard.html',{'user':varuser,'company':mybranch,
					'pincode':staff})

			else:

				return render_to_response('dashboard.html',{'user':varuser,'company':mybranch,
					'pincode':staff})


	else:
		return HttpResponseRedirect('/login/user/')



def dashboard_client(request):
	if 'userid' in request.session:
		varuser = request.session['userid']
		
		try:
			staff = tblCUSTOMER.objects.get(wallet=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact the organization'

			return render_to_response('Ia/selectloan.html',{'msg':msg})

		# staffdet=staff.staffrec.id
		
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		customer=tblCUSTOMER.objects.get(wallet=varuser,status=1)

		return render_to_response('dashboard_clients.html',{'user':varuser,'company':mybranch,
			'pincode':customer})

	else:
		return HttpResponseRedirect('/login/user/')


def indexr(request):

	pk=[8,10,11]
	for t in pk:
		mybranch=tblBRANCH.objects.get(id=t)
		user=Userprofile.objects.get(branch= mybranch)
		user.status=0
		user.save()








# Wrapper to make a view handle both normal and api request
def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap

def namesearch(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                post = request.POST.copy()
                acccode = post['userid']
                if acccode=='':
                  return render_to_response("namesearch.html")

                else: 


					data = tblCUSTOMER.objects.filter(branch=3, status=1, surname__contains=acccode)
					# tblIbCUSTOMER.objects.get(customer=countt,branch=mybranch)

					# data = Student.objects.filter(admitted_session = currse,surname__contains = acccode,gone = False)
					

					return render_to_response('serch.html',{'data':data})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('serch.html',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def cusdetailS(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		# state,trandate=acccode.split(':')
    		customer=tblCUSTOMER.objects.get(wallet=acccode)

    		return render_to_response('walletdetails.html',{'details':customer})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')







def logoutuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/user/')

def switchuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/user/')

def changepass(request):
	if 'userid' in request.session:
		varuser = request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			return HttpResponseRedirect('/login/user/')
		
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
					return render_to_response('success.html',{'user':varuser,'company':mybranch,
						'menu':staff,'msg':msg})
				else:
					msg = 'the passwords do not match'
			else: 
				msg='your old pass is not correct'


		else : 
			msg=''


		
		return render_to_response('changepass.html',{'user':varuser,'company':mybranch,
				'menu':staff,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



def tutorial(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/user/')


def tutorial(request):
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
		# partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.ceo==0:
			return render_to_response('Ia/404.html',{'company':mybranch, 'user':varuser})
	
		sub_history = tblsubscription.objects.filter(branch=mybranch)
			

		return render_to_response('Ia/subscription_detail.html',{'company':mybranch,
			'user':varuser,
			'comp':mybranch,
			'history':sub_history})


		# else:
		# 	form = companyform()
		# 	msg=''

		# 	return render_to_response('partner/subscription.html',{'company':mybranch,'user':varuser,'msg':msg,'form':form})

	else:
		return HttpResponseRedirect('/login/')



