

from django.conf import settings
from django.shortcuts import render_to_response
from django.core.mail import send_mail

import smtplib, ssl


# from staff.models import *
# from Ia.models import *
# from datetime import *
# from django.db.models import Max,Sum
# from calendar import monthrange



from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.template.loader import render_to_string

import random




##Sending alternative content types
def customeuor_activationIaa(emails):
    subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def anothiu9er_one(receiver_email,wallet,account,thrift,month,year):
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





def generate_pin():
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





"""
'your loan is repaid for the month of %s, %d' % (month, year)

in the future, msg should be more detailed, giving the present month and year, and 
the number of months left or when the loan will be fully repaid 

"%s is %d years old." % (name, age)

moreso, we can send html emails, where u can follow a link and view the repayment history a
among other details. This is called MIME emails.........woooow
"""

