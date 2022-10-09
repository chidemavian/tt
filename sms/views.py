from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json
from sms.models import *
from sysadmin.models import *
from sms.forms import*

from datetime import *
import calendar

from thrift.forms import *
from Ia.models import *

from Ib.models import *


from calendar import monthrange

from django.core.serializers.json import json

from django.db.models import Max,Sum

import random



def well(request):
    if  "userid" in request.session:
        varuser=request.session['userid']

        staff = Userprofile.objects.get(email=varuser,status=1)

        staffdet=staff.staffrec.id
        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)
        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

        all_cust = tblCUSTOMER.objects.filter(branch=mybranch)

        for k in all_cust:

	    	try:
	    		tblIaCUSTOMER.objects.get(customer=k)
	    		k.dc=1
	    		k.save()
	    	except:
	    		msg = 0

	        for k in all_cust:
	        	try:
	        		tblIbCUSTOMER.objects.get(customer=k)
	        		k.ivb=1
	        		k.save()
	        	except:
	        		msg = 0
	     
        msg= 'coming up next'
        return render_to_response('Ia/selectloan.html',{'varuser':varuser,'msg':msg})
    else:
        return HttpResponseRedirect('/login/')

def sms_customer(request):
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


		if staff.thrift_officer==0:
				return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
	
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
					form= smsform()
					return render_to_response('sms/sms_reg.html',{
						'company':mybranch,
						'form':form,
						'user':varuser,
					'customer':details,
					'wallet':mywallet})

				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('sms/sms.html',{
			'company':mybranch,
			'user':varuser,
			'form':form,
			'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/')


def sms_history(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		app,package,user,wallet=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffdet=staff.staffrec.id
    		branch=staff.branch.id
    		mycompany=staff.branch.company
    		company=mycompany.name
    		comp_code=mycompany.id
    		ourcompany=tblCOMPANY.objects.get(id=comp_code)
    		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
    		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

    		if app== '-----' : 
    			msg = 'Select Category'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
    		
    		if package == '-----' : 
    			msg = 'Select SMS Package'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})

    		customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)
    		tbt = tblcustomersms.objects.filter(branch=mybranch,customer=customer)
    		tbt__count = tbt.count()

    		if tbt__count > 0 : 
    			ms=5
    			all_sch = tblcustomersms.objects.get(branch=mybranch,customer=customer)
    			schh = all_sch.S  #periodicity-----trans,week,month

    			if schh=='trans': 
    				olschedule = tblcustomersmsperiodicity_transaction.objects.get(schedule=all_sch)
	    			olschedule= str(olschedule.alert_type)

	    		elif schh	== 'week' : 
	    			olschedule=tblcustomersmsperiodicity_weekly.objects.get(schedule=all_sch)
	    			olschedule=str(olschedule.day_of_week)
	    			olschedule='weekly',olschedule

	    		elif schh == 'month' :
	    			olschedule=tblcustomersmsperiodicity_monthly.objects.get(schedule=all_sch)
	    			olschedule=str(olschedule.date_of_delivery)
	    			olschedule='monthly', olschedule
	    	else : 
	    		ms = 1
	    		olschedule=''
	    
    		if app == 'Daily Contribution' :     			

    			if package == 'Transactional' : 
    				if ms == 5 : 
    					try : 
		    				my_schedule = tblcustomersmsperiodicity_transaction.objects.get(schedule=all_sch)
		    				schedule= str(my_schedule.alert_type)
		    				
		    				msg = 'your current preferrence is', schedule, ' Select other options to change'
		    				
		    				
		    				if  schedule=='Deposit': 
		    					
			    				return render_to_response('sms/transactional_rec.html',{
			    					'app':app,
			    					'wallet':wallet,
			    					'msg':msg,
			    					'schedule':schedule})

			    			elif schedule =='Withdraw':  			    				
			    				return render_to_response('sms/transactional_withdraw.html',{
			    					'app':app,
			    					'wallet':wallet,
			    					'msg':msg,
			    					'schedule':schedule})

			    			elif schedule =='Both' :   
			    				return render_to_response('sms/transactional_both.html',{
			    					'app':app,
			    					'wallet':wallet,
			    					'msg':msg,
			    					'schedule':schedule})	    				
	    				except: 
	    					if schh=='week': 
	    						hist ='weekly'
	    					elif schh=='month' :
	    						hist = 'monthly'

	    					msg ="Your current schedule is",  hist," Select from alert type to change"
	    			else : 
	    				msg = 'No schedules found, select alert type to begin'

	    			return render_to_response('sms/transactional.html',{
	    						'msg':msg,
	    						'app':app,
	    						'wallet':wallet})

    			if package == 'Weekly' : 
    				if ms == 5 : 
    					if schh =='trans' : 
    						mysch = tblcustomersmsperiodicity_transaction.objects.get(schedule=all_sch)
    						msg = str(mysch.alert_type)
    						msg ="Your current schedule is", msg ," Select day of week to change"
    					
    					elif schh== 'week' :
    						mysch=tblcustomersmsperiodicity_weekly.objects.get(schedule=all_sch)
    						msg= str(mysch.day_of_week)
    						msg ='Your current schedule is ', msg ,' Select day of week to change'
    					else : 
    						msg ='Your current schedule is monthly. Select day of week to change'
    				
    				else : 
    					msg = 'No schedules found. Select day of week to begin'

    				return render_to_response('sms/weekly.html',{
       					'user':user,
    					'app':app,
    					'msg':msg,
    					'wallet':wallet})

    			if package == 'Monthly' : 
    				
    				if ms == 5 : 
    					try : 
    						mysch = tblcustomersmsperiodicity_monthly.objects.get(schedule=all_sch)
    						schedule = str(mysch.date_of_delivery)
	    					
	    					if schedule== '2021-02-01' :
	    						msg ='Your current schedule is Firs of every month. Select your prefered delivery date to change'
	    						return render_to_response('sms/monthly_first.html',{
			    					'app':app,
			    					'wallet':wallet,
			    					'msg':msg,
			    					'schedule':schedule})	    						
	    				    					
	    					elif schedule == '2021-02-15': 
	    						msg ='Your current schedule is mid month. Select your prefered delivery date to change'
	    						return render_to_response('sms/monthly_mid.html',{
			    					'app':app,
			    					'wallet':wallet,
			    					'msg':msg,
			    					'schedule':schedule})

	    					elif schedule =='2021-07-29' : 
	    						msg ='Your current schedule is month end. Select your prefered delivery date to change'
	    						return render_to_response('sms/monthly_end.html',{
			    					'app':app,
			    					'wallet':wallet,
			    					'msg':msg,
			    					'schedule':schedule})

	    				except: 
	    					if schh == 'trans' : 
	    						histr = 'transactional'
	    					elif schh == 'week' :
	    						histr = 'weekly'
	    					msg ="Your current schedule is",  histr,", Select from alert type to change"

	    			else : 
						msg = 'No schedules found. Select date of delivery to begin'

				return render_to_response('sms/monthly_sms.html',{
		    					'user':user,
		    					'app':app,
		    					'msg':msg,
		    					'wallet':wallet
		    					})

    		else: 
    			msg = 'No schedules Available'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')


def transactional(request):
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

		if staff.thrift_officer==0:
				return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST': 
			schedule = request.POST['schedule']
			wallet = request.POST['wallet']
			app = request.POST['app']
			
			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)
    		tbt = tblcustomersms.objects.filter(
    			branch=mybranch,
    			customer=customer)

    		tbt__count = tbt.count()

    		if tbt__count > 0 : 
    			ms=5
    			all_sch = tblcustomersms.objects.get(
    				branch=mybranch,
    				customer=customer)
    			schh = all_sch.S


	    	else : 
	    		ms =1

	    	if ms == 5 : 

	    		if schh == 'trans' : 

	    			ssch = tblcustomersmsperiodicity_transaction.objects.get(schedule=all_sch)
	    			old = ssch.alert_type
	    			ssch.alert_type =  schedule
	    			ssch.save()
	    			new = schedule

	    		elif schh== 'week' : 
	    			ssch = tblcustomersmsperiodicity_weekly.objects.get(schedule=all_sch).delete()
	    			ssch = tblcustomersmsperiodicity_transaction(schedule=all_sch,alert_type=schedule).save()
	    			all_sch.S = 'trans'
	    			all_sch.save()
	    			old= 'weekly'
	    		
	    		elif schh == 'month' : 
	    			ssch = tblcustomersmsperiodicity_monthly.objects.get(schedule=all_sch).delete()
	    			ssch = tblcustomersmsperiodicity_transaction(schedule=all_sch,alert_type=schedule).save()
	    			all_sch.S = 'trans'
	    			all_sch.save()
	    			old = 'monthly'

	    		if schh != 'trans' : 
	    			new = 'transactional'

	    		return render_to_response('sms/transactional_edit_success.html',{
					'company':mybranch,
					'user':varuser,
					'old':old,
					'new':new,
					'wallet':wallet})

	    	elif ms ==1 : 

				tblcustomersms(branch=mybranch,
					customer=customer,
					App =app,
					S = 'trans',
					balance = 0).save()

				tblcustomersms123 = tblcustomersms.objects.get(
					App=app,
					branch=mybranch,
					S = 'trans',
					customer=customer)

				tblcustomersmsperiodicity_transaction(
					schedule=tblcustomersms123,
					alert_type=schedule).save()
				
				return render_to_response('sms/sub_success.html',{'company':mybranch,'user':varuser,'wallet':wallet})
		
	else:
		return HttpResponseRedirect('/login/')


def weeklysms(request):
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

		if staff.thrift_officer==0:
				return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST': 
			dayofweek = request.POST['dayofweek']
			wallet = request.POST['wallet']
			app = request.POST['app']

			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)

			yhy = tblcustomersms.objects.filter(
				branch=mybranch,
				customer=customer,
				App =app)

			count_yhy = yhy.count()

			if count_yhy < 1 : 
				tblcustomersms(branch=mybranch,
					customer=customer,
					App =app,
					balance = 0).save()
				mywk = tblcustomersms.objects.get(branch=mybranch,
					customer=customer,
					App =app,
					balance = 0)
				tblcustomersmsperiodicity_weekly(
					schedule=mywk,
					day_of_week = dayofweek).save()
				mywk.S='week'
				mywk.save()

				return render_to_response('sms/sub_success.html',{
					'company':mybranch,
					'user':varuser,
					'wallet':wallet})

			else: 
				yhy = tblcustomersms.objects.get(
				branch=mybranch,
				customer=customer,
				App =app)
				sccch= yhy.S
							
				if sccch == 'trans' : 
					trans = tblcustomersmsperiodicity_transaction.objects.get(
						schedule=yhy)
					old='transactional'
					trans.delete()
					tblcustomersmsperiodicity_weekly(schedule=yhy,day_of_week=dayofweek).save()
					yhy.S='week'
					yhy.save()
					new='weekly'

				elif sccch == 'week' : 
					tgt=tblcustomersmsperiodicity_weekly.objects.get(schedule=yhy)
					old = tgt.day_of_week 
					tgt.day_of_week=dayofweek
					tgt.save()
					new = tgt.day_of_week

				elif sccch== 'month': 
					mmnt= tblcustomersmsperiodicity_monthly.objects.get(schedule=yhy).delete()
					old='monthly' 
					tblcustomersmsperiodicity_weekly(schedule=yhy,day_of_week=dayofweek).save()
					yhy.S='week'
					yhy.save()
					new ='weekly'

				return render_to_response('sms/transactional_edit_success.html',{
					'company':mybranch,
					'user':varuser,
					'old':old,
					'new':new,
					'wallet':wallet})
					

	else:
		return HttpResponseRedirect('/login/')


def monthlysms(request):
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

		if staff.thrift_officer==0:
				return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST': 
			dateofdel = request.POST['dateofdel']
			wallet = request.POST['wallet']
			app = request.POST['app']


			if dateofdel == 'start' : 
				dateofdel=date(2021,2,1)
				nick='First'
			elif dateofdel=='mid' :
				dateofdel=date(2021,2,15)
				nick='Mid Month'
			elif dateofdel== 'end' :
				dateofdel=date(2021,7,29)
				nick='Month End'


			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)

			yhy = tblcustomersms.objects.filter(
				branch=mybranch,
				customer=customer,
				App =app)

			count_yhy = yhy.count()

			if count_yhy < 1 : 
				tblcustomersms(branch=mybranch,
					customer=customer,
					App =app,
					S= 'month',
					balance = 0).save()
				mywk = tblcustomersms.objects.get(branch=mybranch,
					customer=customer,
					App =app,
					S='month',
					balance = 0)
				tblcustomersmsperiodicity_monthly(
					schedule=mywk,
					nick = nick,
					date_of_delivery = dateofdel).save()


				return render_to_response('sms/sub_success.html',{
					'company':mybranch,
					'user':varuser,
					'wallet':wallet})

			else: #record exist 
				yhy = tblcustomersms.objects.get(
				branch=mybranch,
				customer=customer,
				App =app)
				sccch= yhy.S
				
				if sccch == 'trans' : 
					trans = tblcustomersmsperiodicity_transaction.objects.get(
						schedule=yhy)
					old='Transactional'
					trans.delete()
					tblcustomersmsperiodicity_monthly(schedule=yhy,
						date_of_delivery =dateofdel,
						nick=nick).save()
					yhy.S='month'
					yhy.save()
					new ="monthly"

				elif sccch == 'week' : 
					tgt=tblcustomersmsperiodicity_weekly.objects.get(schedule=yhy)
					old = 'weekly'
					tgt.delete()
					tblcustomersmsperiodicity_monthly(schedule=yhy,
						date_of_delivery=dateofdel,
						nick=nick).save()
					yhy.S='month'
					yhy.save()
					new ='monthly'

				elif sccch== 'month':

					mmnt= tblcustomersmsperiodicity_monthly.objects.get(schedule=yhy)
					old=mmnt.nick

					mmnt.date_of_delivery=dateofdel
					mmnt.nick=nick
					mmnt.save()

					mmnt= tblcustomersmsperiodicity_monthly.objects.get(schedule=yhy)
					new = mmnt.nick



				return render_to_response('sms/transactional_edit_success.html',{
					'company':mybranch,
					'user':varuser,
					'old':old,
					'new':new,
					'wallet':wallet})
					

	else:
		return HttpResponseRedirect('/login/')



def sms_purchase(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift_officer==0:
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
			return render_to_response('404cr.html',{
				'company':mybranch,
				'user':varuser})
							
		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				smslist=[]

				try:
					customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet,
						status=1)
					smsdetails = tblcustomersms.objects.get(branch=mybranch,
						customer=customer)	
				
					bus= tblsmsappbusiness.objects.filter(branch=mybranch,
						status=1,App='Daily Contribution')
					
					if bus.count() > 0: 
						myform = thriftform()
						bus= tblsmsappbusiness.objects.get(branch=mybranch,
						status=1,App='Daily Contribution')

						smsdic= {'balance':smsdetails.balance,
						'wallet':mywallet,
						'sender':bus.sender_ID,
						'surname':customer.surname,
						'firstname':customer.firstname,
						'othername':customer.othername}
						smslist.append(smsdic)

						return render_to_response('sms/pay_sms.html',{'company':mybranch,
							'user':varuser,
							'wallet':mywallet,	
							'smslist':smslist,
							})
					else:
						msg='hello, you have not subscribed for this service'
				except:
					msg='you havent subscribed for this service'
			else:
				msg='Incorrect entry'
		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('sms/buy_sms.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/')




def unit(request):  
	if request.is_ajax(): 
		if request.method == 'POST': 
			post = request.POST.copy()
			acccode = post['userid']
			unit,user,wallet,amount=acccode.split(':')
			
			if unit != '' : 
				unit= int(unit)

			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			sms_bal = tblsmsappbusiness.objects.get(status=1,branch=mybranch, App='Daily Contribution')
			balance=int(sms_bal.balance)
			
			if unit == '' : 
				msg = 'enter sms unit'
				return render_to_response('thrift/selectloan.html',{'msg':msg})

			if balance - unit < 0 : 
				msg = 'Sms Unit too large. Try reducing the unit of sms'
				return render_to_response('thrift/selectloan.html',{'msg':msg})

			else : 
				form=thriftform()
				return render_to_response('sms/funding.html',{'form':form,
					'unit':unit,
					'user':user,
					'amount':amount,
					})
		
		else: 
			return HttpResponseRedirect('/login/')
	
	else: 
		return HttpResponseRedirect('/login/')


def pay4sms(request): 
	if request.is_ajax(): 
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']

			funding,month,account_type,user,amount,unit,wallet = acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)
			
		
			if funding== '-----':	
				msg = 'Select a funding source'
				return render_to_response('thrift/selectloan.html',{'msg':msg})

			if month== '-':	
				msg = 'Select a month'
				return render_to_response('thrift/selectloan.html',{'msg':msg})

			if account_type== '-----' : 
				msg = 'Select account type'
				return render_to_response('thrift/selectloan.html',{'msg':msg})
				

			if funding == 'Daily Contribution': 
				money = tblthrift_trans.objects.filter(branch=mybranch,
					account_type=account_type,
					customer=customer,
					avalability='Available',
					reason='Available',
					recdate__month=month)

				if money.count() > 0 :  
					add=money.aggregate(Sum('amount'))
					add = add['amount__sum']

					if int(add) - int(amount) > 0: 

						return render_to_response('sms/submit.html',{'funding':funding,
							'month':month,
							'account':account_type,
							'user':user,
							'unit':unit,
							'amount':amount,
							'wallet':wallet})

					else : 
						amount=int(amount)
						msg = 'you have', add , 'but needs ', amount , ' for this transaction'
						return render_to_response('thrift/selectloan.html',{'msg':msg})
			
	
				else : 
					msg = 'No record found. Try selecting another month / account type'
					return render_to_response('thrift/selectloan.html',{'msg':msg})
			
						
			else : 
				msg='Cash funding not allowed'
				return render_to_response('thrift/selectloan.html',{'msg':msg})
		
		else: 
			return HttpResponseRedirect('/login/')

	else: 
		return HttpResponseRedirect('/dalogin/')



def buysms(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		if staff.thrift_officer==0: 
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
		
		# msg=memmerchant.id
		# return render_to_response('thrift/selectloan.html',{'msg':msg})	
	
		if request.method == 'POST':
			amount=request.POST['amount']
			unit=request.POST['unit']
			wallet=request.POST['wallet']

			month=request.POST['month']
			account=request.POST['account']
			user=request.POST['user']
			funding=request.POST['funding']

			unit=int(unit)

			fdate= datetime.today()

			month=fdate.month #in figures
			year=fdate.year
			dayy = fdate.day
			oydate=date(year,month,dayy)

			customer= tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1,
				merchant=memmerchant)

			bus_sms = tblsmsappbusiness.objects.get(branch=mybranch,
				status=1)

			sms_balance = int(bus_sms.balance) 

			sms_bal= sms_balance - unit

			bus_sms.balance = sms_bal

			bus_sms.save()

			cus_sms =tblcustomersms.objects.get(branch=mybranch,
				customer=customer,
				App=funding)

			old_bal = int(cus_sms.balance)
			new_bal = old_bal + unit
			cus_sms.balance = new_bal

			cus_sms.save()

			merchant=memmerchant.id

			tblcustomersmspurchases(branch=mybranch,
				customer=customer,
				recdate = oydate,
				merchant=merchant,
				volume = unit,
				status='Unpaid',
				cost = amount).save()

			nn=unit+old_bal




			return render_to_response('sms/sms_purchase_successful.html',{
				'account_type':account, 
				'company':mybranch, 
				'user':varuser,
				'wallet':wallet,
				'thrift':unit,
				 'nn':nn,
				'amount':amount})

		else : 
			# return HttpResponseRedirect('/sms/daily_contribution/requests/buysms/')
			return HttpResponseRedirect('/sms/daily_contribution/balance/')
				
	else:
		return HttpResponseRedirect('/login/')
