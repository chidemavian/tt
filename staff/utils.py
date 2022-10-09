
from django.core.mail import send_mail
from django.conf import settings


from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


from django.template.loader import render_to_string

import random

import smtplib, ssl




# send_mail(
# 	subject,
# 	message, 
# 	EMAIL_HOST_USER, 
# 	[recepient], 
# 	fail_silently = False)




def staff_registration5(receiver_email):
    subject = 'LOGIN CREATED FOR YOU'
    from_email = settings.EMAIL_HOST_USER,
    to = [receiver_email]
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def staff_registration(receiver_email,surname,password):
    plaintext = get_template('staff/team_login.html')
    htmly     = get_template('staff/team_login.html')

    d = Context({ 'username': surname,'password':password })

    subject = 'YOUR ACCOUNT IS ACTIVATED'
    from_email = settings.EMAIL_HOST_USER,
    to = receiver_email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)


    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()




def staff_registration3(receiver_email):

    msg_plain = render_to_string('templates/email.txt', {'some_params': some_params})
    msg_html = render_to_string('staff/profdetail.html', {'some_params': some_params})

    send_mail(
        'email title',
        msg_plain,
        'some@sender.com',
        ['some@receiver.com'],
        html_message=msg_html,
    )




def staff_registration2(receiver_email,):
    subject = 'LOGIN CREATED FOR YOU'
    from_email = settings.EMAIL_HOST_USER,
    to = [receiver_email]


    plaintext = get_template('email.txt')
    htmly     = get_template('email.html')
    d = Context({ 'username': username })
    subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



    msg_plain = render_to_string('templates/email.txt', {'some_params': some_params})
    msg_html = render_to_string('templates/email.html', {'some_params': some_params})

    send_mail(
        'email title',
        msg_plain,
        'some@sender.com',
        ['some@receiver.com'],
        html_message=msg_html,
    )






def staff_registrarion(receiver_email):
    messageSent = False
    subject = "LOGIN CREATED FOR YOU"
    message = "A LOGIN HAS BEEN CREATED FOR YOU"
    send_mail(subject,
    	message,
    	settings.EMAIL_HOST_USER,
    	[receiver_email],
    	fail_silently=False)
    messageSent = True



def generate_staff_pin():
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



def generate_password():
    krt = random.randint(0,9)
    pyb = random.randint(0,9)
    qtv = random.randint(0,9)
    bb = random.randint(0,9)
    vb = random.randint(0,9)
    hz = random.randint(0,9)

    password =  str(krt) + str(pyb) + str(qtv) + str(bb)+ str(vb) + str(hz)

    return password


"""
'your loan is repaid for the month of %s, %d' % (month, year)

in the future, msg should be more detailed, giving the present month and year, and 
the number of months left or when the loan will be fully repaid 

"%s is %d years old." % (name, age)

moreso, we can send html emails, where u can follow a link and view the repayment history a
among other details. This is called MIME emails.........woooow
"""

