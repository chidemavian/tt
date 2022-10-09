

from django.conf import settings
from django.shortcuts import render_to_response
from django.core.mail import send_mail

import smtplib, ssl


from staff.models import *
from Ia.models import *
from datetime import *
from django.db.models import Max,Sum
from calendar import monthrange



from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.template.loader import render_to_string

import random




def deposit_email(receiver_email,surname,firstname,amount,month,year):
    plaintext = get_template('IIIb/email.txt')
    htmly     = get_template('IIIb/deposit_email.html')

    d = Context({ 'surname': surname,
        'firstname': firstname,
        'amount': amount,
        'month': month,
        'year': year })

    subject = 'THRIFTPLUS'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def savingscheme_email(receiver_email,surname,firstname,amount,year,package,a,b):
    plaintext = get_template('IIIb/email.txt')
    htmly     = get_template('IIIb/deposit_email.html')

    d = Context({ 'surname': surname,
        'firstname': firstname,
        'amount': amount,
        'month': month,
        'package':package,
        'start':a,
        'end':b,
        'year': year})

    subject = 'THRIFTPLUS'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()




def loanbook_email(receiver_email,surname,firstname,amount,coop_man):
    plaintext = get_template('IIIb/email.txt')
    htmly     = get_template('IIIb/loan-request-email..html')

    d = Context({ 'surname': surname,
        'firstname': firstname,
        'amount': amount,
        'coop_man': coop_man})

    subject = 'THRIFTPLUS'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()




def loanapproval_email(receiver_email,surname,firstname,amount,year,package,a,b):
    plaintext = get_template('IIIb/email.txt')
    htmly     = get_template('IIIb/deposit_email.html')

    d = Context({ 'surname': surname,
        'firstname': firstname,
        'amount': amount,
        'month': month,
        'package':package,
        'start':a,
        'end':b,
        'year': year})

    subject = 'THRIFTPLUS'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def rrt(receiver_email):
    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()




def Direct_creditingIa(receiver_email,surname,thrift,amount,month):

    subject = 'Your account is credited'
    from_email = settings.EMAIL_HOST_USER
    to = receiver_email

    text_content = render_to_string('Ia/direct_credit.txt', { 'surname': surname,'thrift':thrift,'amount':amount })
    html_content = render_to_string('Ia/direct_credit.html', { 'surname': surname,'month':month,'thrift':thrift,'amount':amount })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()




def account_balance():


    www=int(month)

    monthname = calendar.month_name[www] #converts month_index to month_name

    staff = Userprofile.objects.get(email=user,status=1)
    staffid = staff.staffrec.id

    memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff= staffid ,status=1)

    details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
    details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details,status=1)

    thrift=tblIathrift.objects.get(account_type = acccode, month=monthname,customer=details)
    code=thrift.code



    thriftrec= tblIasavings_trans.objects.filter(
        branch=mybranch,
        customer=details,
        code=code,
        wallet_type='Main',
        account_type = acccode).order_by('recdate').reverse().exclude(status='Account Maintenance')


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

    return add



def selenco(bra,fd,td):


    mybranch= tblBRANCH.objects.get(id = bra)
    allmerchant = tblIaMERCHANT.objects.filter(branch=mybranch,status=1,thrift1a=1)

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
                        salees = tblIamerchantBank.objects.filter(
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

                        salees = tblIamerchantBank.objects.filter(
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
                        salees = tblIamerchantBank.objects.filter(
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
                        salees = tblIamerchantBank.objects.filter(
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





def generate_trans_pin():
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




def direct_credit(request): #customer - admin transaction

    if  add_count + lump <= p :

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


def contribution_count():


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

    return add_count


"""
'your loan is repaid for the month of %s, %d' % (month, year)

in the future, msg should be more detailed, giving the present month and year, and 
the number of months left or when the loan will be fully repaid 

"%s is %d years old." % (name, age)

moreso, we can send html emails, where u can follow a link and view the repayment history a
among other details. This is called MIME emails.........woooow
"""

