

from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json
from thrift.forms import *


from sysadmin.models import *
from customer.models import *
from merchant.models import *
from savings.models import *


from datetime import *
import calendar


#######import only merchant.models******
from calendar import monthrange


from django.db.models import Max,Sum

import random


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
		
		if staff.thrift_officer==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('thrift/welcome.html',{'company':mybranch, 'user':varuser})
	
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

		
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
	
		return render_to_response('thrift/adminwelcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/')