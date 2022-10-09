from django.conf.urls import patterns, include, url


urlpatterns = patterns('IIIa.views',
	 url(r'^thrift/home/$', 'welcome'),
	 url(r'^thrift/admin/home/$', 'adminwelcome'),

# ##********************Create Wallet***************
# 	 url(r'^thrift/createwallet/$', 'createwallet'),
# 	 url(r'^thrift/editwallet/$', 'editwallet'),
# 	 url(r'^thrift/viewwallet/$', 'viewwallet'),

# #***********************Thrift********************
# 	 url(r'^thrift/addthrift/$', 'addthrift'),
# 	 url(r'^thrift/addthrift/account_type/$', 'account_type'),
# 	 url(r'^thrift/addthrift/account_history/$', 'account_history'),

# 	 url(r'^thrift/withdraw/account_withdraw/$', 'account_withdraw'),

# 	 url(r'^thrift/deposit/account_dep/$', 'account_dep'),
# 	 url(r'^thrift/addthrift/account_view/$', 'account_view'),
# 	 url(r'^thrift/addthrift/account_change/$', 'account_change'),
# 	 url(r'^thrift/edit/thrift/$', 'edit_thrift_popup'),
# 	 # url(r'^thrift/edit/thrift/$', 'edit_thrift'),	 
# 	 url(r'^thrift/addthrift/putthrift/$', 'putthrift'),
# 	 url(r'^thrift/addthrift/putinthrift/$', 'putinthrift'),
# 	 url(r'^thrift/viewthrift/$', 'viewthrift'),
# 	 url(r'^thrift/changethrift/$', 'changethrift'),

# 	 url(r'^thrift/changethrift/change/$','thriftedit'),
# 	 url(r'^thrift/changethrift/safechange/$', 'safethriftedit'),
	 
# 	 url(r'^thrift/rolloverthrift/$', 'rolloverthrift'),
# 	 url(r'^thrift/thriftreport/$', 'thriftrep'),

# 	 #*************** pay request********************
# 	 url(r'^thrift/payrequest/$', 'payrequests'),
# 	 url(r'^findthrift//$', 'autocomplete'),
# 	 url(r'^thrift/history/$', 'history'),
# 	 url(r'^thrift/addmythrift/$','addmythrift'),
# 	 url(r'^thrift/requests/cashin/$', 'cashin'),
# 	 url(r'^thrift/unremmitted/$', 'unremmitted'),
# 	 url(r'^thrift/cashout/$', 'cashout'),
# 	url(r'^thrift/funding/getsource/$','source'),
#      url(r'^thrift/requests/payout_request/$', 'cashoutrequest'),


# 	 #***********************8*Remittals***************	
# 	url(r'^thrift/remittals/$', 'individual'),
# 	 url(r'^thrift/seedit/$','seedit'),

# 	url(r'^thrift/requests/adminpayfund/canceloptions/$','canceloptions'),
# url(r'^thrift/requests/adminpayfund/withdraw/$','withdrawoptions'),
# 	 url(r'^thrift/reedit/$','reedit'),

# 	url(r'^thrift/remittals/remit/$', 'remitcash'),
# 	url(r'^thrift/remittals/individualremit/$', 'indremitcash'),
	
# 	url(r'^thrift/report/$', 'report'),

# 	#******************Approvals****************
#     url(r'^thrift/approvalsmenu/$', 'approvalsmenu'),
#     url(r'^thrift/approvals/$', 'approvals'),
#         url(r'^thrift/approvalsmenu/approvefund/$', 'approvecash'),
#     url(r'^thrift/allapprovals/$', 'allapproval'),

# 	url(r'^thrift/approvals/approvereport/$','approvereport'),

# 	url(r'^thrift/approvalforindv/$','approveind'),
# 	url(r'^thrift/approvalsmenu/approvefundforcustomer/$','approveindividualcash'),

# ###***************************Payout***************
#       url(r'^thrift/payouts/$', 'payout'),
#        url(r'^thrift/requests/adminpayfund/$', 'adminpayfund'),
#       url(r'^thrift/payoutreport/$', 'payoutreport'),

#       url(r'^thrift/requests/adminpayfund/cancel/nos/$','cancelreq'),
#       url(r'^thrift/payouts/adminwithdraw/yes/$','withdrawfunds'),
# ##****************Reports***********************

#       url(r'^thrift/reports/home/$', 'repome'),
#       url(r'^thrift/reports/sales/merchant/$','merchantreport'),
#       url(r'^thrift/reports/sales/cashier/$','cashierreport'),
#       url(r'^thrift/reports/sales/admn/$','adminreport'),
#       		#******merchants*******
#       url(r'^thrift/reports/getmerchants/$','getmerchantid'),
#       url(r'^thrift/reports/getmyname/$','getmerchantname'),
#       url(r'^thrift/reports/getmereport/$','getmereportajax'),


#       #*****Cashier**************
#       url(r'^thrift/reports/getcashid/$','getcashid'),
#       url(r'^thrift/reports/getcashname/$','getcashname'),
#        url(r'^thrift/reports/getcashreport/$','getcashreportajax'),

#       #****Admin***************
#       url(r'^thrift/reports/getadminid/$','getadminid'),
#       url(r'^thrift/reports/getadminname/$','getadminname'),





      
      # url(r'^thrift/reports/getadminreport/$','getadminreportajax'),
    
###*****************************MISC************************
	# url(r'^thrift/misc/customers/$', 'customerslist'),
	# url(r'^thrift/misc/namesearch/$', 'namesearch'),
	# url(r'^thrift/misc/switches/$', 'switches'),
	# url(r'^thrift/misc/getstaff/$','getallstall'),
	# url(r'^thrift/misc/getswitch/$','getbutton'),
	# url(r'^thrift/misc/showselect/$','openoption'),

	
	)
