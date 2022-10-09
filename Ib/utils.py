


from django.conf import settings
from django.shortcuts import render_to_response
from django.core.mail import send_mail
import smtplib, ssl

from staff.models import *
from Ib.models import *
from datetime import *
from django.db.models import Max,Sum
from calendar import monthrange


import random

def generate_loancode():
    krt = random.randint(0,9)
    pyb = random.randint(0,9)
    qtv = random.randint(0,9)
    bb = random.randint(0,9)
    vb = random.randint(0,9)
    hz = random.randint(0,9)
    ywq = random.randint(0,9)
    xfg = random.randint(0,9)
    zvv = random.randint(0,9)
    a = random.randint(0,9)
    hzp = random.randint(0,9)
    yq = random.randint(0,9)
    xj = random.randint(0,9)
    zp = random.randint(0,9)
    au = random.randint(0,9)
    pin =  str(krt) + str(pyb) + str(qtv) + str(bb)+ str(vb) + str(hz) + str(ywq) + str(xfg) + str(zvv)+ str(a) + str(hzp) + str(yq) + str(xj) + str(zp)+ str(au)

    return pin


def register_field_officerIb(receiver_email):
    messageSent = False
    subject = "Field officer activation"
    message = "YOU HAVE SUCCESFULLY BEEN ACTIVATED AS A CREDIT OFFICER"
    send_mail(subject,
    	message,
    	settings.EMAIL_HOST_USER,
    	[receiver_email],
    	fail_silently=False)
    messageSent = True


def customer_activationIb(receiver_email):
    messageSent = False
    subject = "Investment Banking activation"
    message = "YOU HAVE SUCCESFULLY BEEN ACTIVATED FOR INVESTMENT BANKING"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True


def send_email_ticket_confirm(request, payment_info):
    mail_title = u"PyCon Korea 2015(Registration confirmation)"
    product = Product()
    variables = Context({
        'request': request,
        'payment_info': payment_info,
        'amount': product.price
    })

    html = get_template('Ib/credit_account_email_Ib').render(variables)
    text = get_template('Ib/credit_account_email_Ib').render(variables)
    
    msg = EmailMultiAlternatives(
        mail_title,
        text,
        settings.EMAIL_HOST_USER,
        [payment_info.email])

    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)





def another_one(receiver_email,wallet,account,thrift,month,year):
    plaintext = get_template('Ia/email.txt')
    htmly     = get_template('Ia/deposit_email.html')

    d = Context({ 'email': email,
        'wallet': wallet,
        'account': account,
        'thrift': thrift,
        'month': month,
        'year': year })

    subject = 'ACCOUNT CREDITED SUCCESFULLY'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def direct_depositIb(receiver_email):
    messageSent = False
    subject = "Investment Banking activation"
    message = "YOU HAVE SUCCESFULLY BEEN ACTIVATED FOR INVESTMENT BANKING "
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True


def direct_withrawalIb(receiver_email):
    messageSent = False
    subject = "Withdrawal SUCCESFUL"
    message = "YOU HAVE SUCCESFULLY WITHDREW CASH"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True



"""
'your loan is repaid for the month of %s, %d' % (month, year)

in the future, msg should be more detailed, giving the present month and year, and 
the number of months left or when the loan will be fully repaid 

"%s is %d years old." % (name, age)

moreso, we can send html emails, where u can follow a link and view the repayment history a
among other details
"""



def selenco(bra,fd,td):


	mybranch= tblBRANCH.objects.get(id = bra)
	allmerchant = tblIbco.objects.filter(branch=mybranch,status=1,thrift1b=1)

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


	if fd.year== td.year:

		merchant_sales=0
		for k in a: # a is the months covered in the search
			if k == a[0]: #if month is the first month
				if k == a[-1]: #use the boundaries set by the dates
					# dddd = td.day								
					# tttt = fd.day
					fff=0
					fff= fff + tttt
					while fff <= dddd : 
						fd1=date(yday,k,fff)
						salees = tblIbmerchantbank.objects.filter(
							branch=mybranch,
							status='Approved',
							wallet_type='Main',
							recdate=fd1)

						couunt = salees.count()

						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr

							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1								
					
				else: #boundaries = from_date to month end

					fff=0
					fff= fff+ fd.day
					dddd = (monthrange(fd.year, fd.month))[-1]

					while fff <= dddd : 
						fd1=date(yday,k,fff) #k is month integer

						salees = tblIbmerchantbank.objects.filter(
							branch=mybranch,
							status='Approved',
							wallet_type='Main',
							recdate=fd1)

						couunt = salees.count()
						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr

							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1

			else: 
				if k == a[-1]: #boundaries = 1st to to_date
					dddd = td.day
					
					fff=1
					fff += 1
					while fff <= dddd : 
						fd1=date(yday,k,fff)
						salees = tblIbmerchantbank.objects.filter(
							branch=mybranch,
							status='Approved',
							wallet_type='Main',
							recdate=fd1)

						couunt = salees.count() 
						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr
							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1	

				else: # loop thru the whole month
		
					fff=0
					fff += 1
					dddd= (monthrange(td.year, k))[-1]
					
					while fff <= dddd : 
						fd1=date(yday,k,fff)
						salees = tblIbmerchantbank.objects.filter(
							branch=mybranch,
							status='Approved',
							wallet_type='Main',
							recdate=fd1)

						couunt = salees.count() 
						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr

							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1

		
		if detli !=[] :
			ddd= {'total':toot}
			detli.append(ddd)


		return detli




def dateprofit(bra,fd,td):


	mybranch= tblBRANCH.objects.get(id = bra)
	allmerchant = tblIbco.objects.filter(branch=mybranch,status=1,thrift1b=1)

	dday,mday,yday = fd.split('/') #JSON Dates Object
	yday=int(yday)
	fmday=int(mday)
	fday=int(dday)

	fd=date(yday,fmday,fday) #python object

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


	if fd.year== td.year:

		merchant_sales=0
		for k in a: # a is the months covered in the search
			if k == a[0]: #if month is the first month
				if k == a[-1]: #use the boundaries set by the dates
					# dddd = td.day								
					# tttt = fd.day
					fff=0
					fff= fff + tttt
					while fff <= dddd : 
						fd1=date(yday,k,fff)

						salees =  tblIbsavings_trans.objects.filter(
							branch=mybranch,
							status='Service Charge',
							description='DR',
							wallet_type='Main',
							avalability='Not Available',
							recdate=fd1)

						couunt = salees.count()

						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr

							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1								
					
				else: #boundaries = from_date to month end

					fff=0
					fff= fff+ fd.day
					dddd = (monthrange(fd.year, fd.month))[-1]

					while fff <= dddd : 
						fd1=date(yday,k,fff) #k is month integer

						salees =  tblIbsavings_trans.objects.filter(
							branch=mybranch,
							status='Service Charge',
							description='DR',
							wallet_type='Main',
							avalability='Not Available',
							recdate=fd1)

						couunt = salees.count()
						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr

							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1

			else: 
				if k == a[-1]: #boundaries = 1st to to_date
					dddd = td.day
					
					fff=1
					fff += 1
					while fff <= dddd : 
						fd1=date(yday,k,fff)
						salees =  tblIbsavings_trans.objects.filter(
							branch=mybranch,
							status='Service Charge',
							description='DR',
							wallet_type='Main',
							avalability='Not Available',
							recdate=fd1)

						couunt = salees.count() 
						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr
							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1	

				else: # loop thru the whole month
		
					fff=0
					fff += 1
					dddd= (monthrange(td.year, k))[-1]
					
					while fff <= dddd : 
						fd1=date(yday,k,fff)
						salees =  tblIbsavings_trans.objects.filter(
							branch=mybranch,
							status='Service Charge',
							description='DR',
							wallet_type='Main',
							avalability='Not Available',
							recdate=fd1)

						couunt = salees.count() 
						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr

							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1

		
		if detli !=[] :
			ddd= {'total':toot}
			detli.append(ddd)


		return detli






def datewithdraw(bra,fd,td):


	mybranch= tblBRANCH.objects.get(id = bra)
	allmerchant = tblIbco.objects.filter(branch=mybranch,status=1,thrift1b=1)

	dday,mday,yday = fd.split('/') #JSON Dates Object
	yday=int(yday)
	fmday=int(mday)
	fday=int(dday)

	fd=date(yday,fmday,fday) #python object

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


	if fd.year== td.year:

		merchant_sales=0
		for k in a: # a is the months covered in the search
			if k == a[0]: #if month is the first month
				if k == a[-1]: #use the boundaries set by the dates
					# dddd = td.day								
					# tttt = fd.day
					fff=0
					fff= fff + tttt
					while fff <= dddd : 
						fd1=date(yday,k,fff)

						salees =  tblIbsavings_trans.objects.filter(
							branch=bra,
		                	status='Withdrawn',
		                	description='DR',
		                	wallet_type='Main',
		                	avalability='Not Available',
		                	recdate=fd1)

						couunt = salees.count()

						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr

							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1								
					
				else: #boundaries = from_date to month end

					fff=0
					fff= fff+ fd.day
					dddd = (monthrange(fd.year, fd.month))[-1]

					while fff <= dddd : 
						fd1=date(yday,k,fff) #k is month integer

						salees =  tblIbsavings_trans.objects.filter(
							branch=bra,
		                	status='Withdrawn',
		                	description='DR',
		                	wallet_type='Main',
		                	avalability='Not Available',
		                	recdate=fd1)

						couunt = salees.count()
						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr

							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1

			else: 
				if k == a[-1]: #boundaries = 1st to to_date
					dddd = td.day
					
					fff=1
					fff += 1
					while fff <= dddd : 
						fd1=date(yday,k,fff)

						salees =  tblIbsavings_trans.objects.filter(
							branch=bra,
		                	status='Withdrawn',
		                	description='DR',
		                	wallet_type='Main',
		                	avalability='Not Available',
		                	recdate=fd1)

						couunt = salees.count() 
						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr
							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1	

				else: # loop thru the whole month
		
					fff=0
					fff += 1
					dddd= (monthrange(td.year, k))[-1]
					
					while fff <= dddd : 
						fd1=date(yday,k,fff)
						salees =  tblIbsavings_trans.objects.filter(
							branch=bra,
		                	status='Withdrawn',
		                	description='DR',
		                	wallet_type='Main',
		                	avalability='Not Available',
		                	recdate=fd1)

						couunt = salees.count() 
						if couunt> 0: 
							add=salees.aggregate(Sum('amount'))
							add_cr = add['amount__sum']
							merchant_sales=add_cr
							toot = toot + add_cr

							df = {'sum':merchant_sales,'details':fd1}
							detli.append(df)

						fff += 1

		
		if detli !=[] :
			ddd= {'total':toot}
			detli.append(ddd)


		return detli




def account_balance(account):

	cus=tblIbCUSTOMER.objects.get(id =account)

	sav=tblIbsavings_trans.objects.filter(customer=cus,
		wallet_type='Main',
		status='Available',
		avalability='Available',
		description='CR') 
		
		# msg = sav
		# return render_to_response('Ib/selectloan.html',{'msg':msg})

	if sav.count()>0:
		add=sav.aggregate(Sum('amount'))
		add_cr = add['amount__sum']
	else:
		add_cr = 0


	sav_dr=tblIbsavings_trans.objects.filter(customer=cus,description='DR')

	if sav_dr.count()>0 :
		add=sav_dr.aggregate(Sum('amount'))
		add_dr = add['amount__sum']
	else:
		add_dr =0

	amount=add_cr - add_dr

	return amount


