
from django.conf.urls import patterns, include, url


urlpatterns = patterns('Ia.views',

	 url(r'^thrift/home/$', 'welcome'),

	 url(r'^thrift/admin/home/$', 'admindash'),
	 
	 url(r'^thrift/admin/user/$', 'adminuserguide'),



####Field agents*****************
url(r'^staff/merchant/$', 'regfieldagent'),
 url(r'^staff/merchant/mycos/$', 'mycos'),



##********************customers****************************
	 url(r'^thrift/newsub/$', 'subscribe_cus'),
	 url(r'^thrift/newsub/subscribe/$', 'gensave'),
	 url(r'^customer/customer/$', 'depositer'),
	 


##customers***********************************
 url(r'^customeria/list/$', 'cus_list'), 



#***********************Thrift********************
	 url(r'^thrift/addthrift/$', 'addthrift'),
	 url(r'^thrift/viewthrift/$', 'viewthrift'),
	 url(r'^thrift/changethrift/$', 'changethrift'),


	 url(r'^thrift/changethrift/change/$','thriftedit'),
	 


	 
	 url(r'^thrift/rolloverthrift/$', 'rolloverthrift'),
	 url(r'^thrift/thriftreport/$', 'thriftrep'),

	 url(r'^thrift/addthrift/account_type/$', 'account_type'),
	 url(r'^thrift/addthrift/account_history/$', 'account_history'),

	 url(r'^thrift/addthrift/account_statement_history/$', 'account_statement_history'),





	 url(r'^thrift/deposit/account_dep/$', 'account_dep'),



	 url(r'^thrift/addthrift/account_view/$', 'account_view'),
	 url(r'^thrift/addthrift/account_change/$', 'account_change'),
	 url(r'^thrift/edit/thrift/$', 'edit_thrift_popup'),


	 url(r'^thrift/changethrift/edit/$','safethriftedit'),

	 url(r'^thrift/addthrift/putthrift/$', 'putthrift'),
	 url(r'^thrift/addthrift/putinthrift/$', 'putinthrift'),



	 #*************** activity log********************

	 url(r'^thrift/log/$', 'log'),
	 url(r'^thrift/log/merchant_ajax/$', 'fillmerchant'),
	 
	 url(r'^thrift/log/autopostlog/$', 'fillmerchantb'),

	 url(r'^thrift/log/payouts/$', 'payouts'),

	 url(r'^thrift/log/payouts/merchant_ajax/$', 'fillmerchant'),

	 url(r'^thrift/log/payouts/autopostlog/$', 'fillmerchantb'),

	 

	 url(r'^thrift/log/approvals/$', 'logapprove'),
	 url(r'^thrift/log/approvals/merchant_ajax/$', 'fillmerchantappr'),
	 url(r'^thrift/log/approvals/autopostlog/$', 'showtrans'),


	 url(r'^thrift/log/dr/$', 'log7'),
	 url(r'^thrift/log/dr/merchant_ajax/$', 'fillmerchant7'),
	 url(r'^thrift/log/dr/autopostlog/$', 'fillmerchantb7'),

	 


	 #*************** pay request********************
	 url(r'^thrift/payrequest/$', 'payrequests'),
	 url(r'^findthrift//$', 'autocomplete'),
	 url(r'^thrift/history/$', 'history'),

	 url(r'^thrift/mystatement/$', 'statementtt'),

	 url(r'^thrift/addmythrift/$','addmythrift'),

	 
	 url(r'^thrift/requests/cashin/admin/$', 'admin_cashin'),
	 url(r'^thrift/requests/cashin/cashier/$', 'cashier_cashin'),
	 url(r'^thrift/requests/cashin/agent/$', 'agent_cashin'),
	 
	 url(r'^thrift/unremmitted/$', 'unremmitted'),

	 url(r'^thrift/unremmitted/fa/$', 'fa_unremmitted'),
	 
	url(r'^thrift/funding/getsource/$','source'),
     

 	 url(r'^thrift/cashout/$', 'cashout'),
     url(r'^thrift/cashout/admin/$', 'cashoutrequest'),
   	 url(r'^thrift/withdraw/account_withdraw/$', 'account_withdraw'),
     url(r'^thrift/cashout/cash/$', 'cashoutrequest_cash'),
 	url(r'^thrift/cashout/agent/$', 'cashoutrequest_to'),

	 #***********************8*Remittals***************	
	url(r'^thrift/remittals/$', 'individual'),
	 url(r'^thrift/seedit/$','seedit'),

	url(r'^thrift/requests/adminpayfund/canceloptions/$','canceloptions'),
	url(r'^thrift/requests/adminpayfund/withdraw/$','withdrawoptions'),
	 url(r'^thrift/reedit/$','reedit'),

 url(r'^thrift/approvalsmenu/delete/yes/$', 'approvalsmenuyes'),



	# url(r'^thrift/remittals/remit/$', 'remitcash'),
	url(r'^thrift/approvals/approvebulk/$', 'approvebulkcash'),

	# url(r'^thrift/remittals/individualremit/$', 'indremitcash'),
	url(r'^thrift/aprrovals/approvalsingletrans/$', 'approveone'),
	
	url(r'^thrift/report/$', 'report'),

	#******************Approvals****************
    url(r'^thrift/approvalsmenu/$', 'approvalsmenu'),
    url(r'^thrift/approvals/$', 'approvals'),
        url(r'^thrift/approvalsmenu/approvefund/$', 'approvecash'),
    url(r'^thrift/allapprovals/$', 'allapproval'),

	url(r'^thrift/approvals/approvereport/$','approvereport'),

	url(r'^thrift/approvalforindv/$','approveind'),
	url(r'^thrift/approvalsmenu/approvefundforcustomer/$','approveindividualcash'),

###***************************Payout***************
      url(r'^thrift/payouts/$', 'payout'),
       url(r'^thrift/requests/adminpayfund/$', 'adminpayfund'),
      url(r'^thrift/payoutreport/$', 'payoutreport'),

      url(r'^thrift/requests/adminpayfund/cancel/nos/$','cancelreq'),
      url(r'^thrift/payouts/adminwithdraw/yes/$','withdrawfunds'),





##****************General Reports***********************
      url(r'^thrift/reports/home/$', 'repome'),



 ###############****************##Vaults******************
      url(r'^thrift/reports/sales/merchant/$','merchantreport'),
      url(r'^thrift/reports/getmereport/$','getmereportajax'),
      url(r'^thrift/reports/getdatemereport/$','getmereportajaxdate'),



      url(r'^thrift/reports/sales/cashier/$','cashierreport'),



#####***********************profits*********************************
      url(r'^thrift/reports/sales/admn/$','adminreport'),
      url(r'^thrift/reports/getprofit/$','getprofit'),
      url(r'^thrift/reports/getdateprofit/$','getdateprofit'),




#####***********************withdrawals*********************************       
        # url(r'^thrift/reports/sales/withdrawwa/$','clientwithdraw'),
        url(r'^thrift/reports/getwithdraw/$','getwithdraw'),



        url(r'^thrift/reports/getdatewithdraw/$','getdatewithdraw'),




      		#******merchants*******
      url(r'^thrift/reports/getmerchants/$','getmerchantid'),
      url(r'^thrift/reports/getmyname/$','getmerchantname'),
      url(r'^thrift/reports/getmereport/$','getmereportajax'),


      #*****Cashier**************
      url(r'^thrift/reports/getcashid/$','getcashid'),
      url(r'^thrift/reports/getcashname/$','getcashname'),
       url(r'^thrift/reports/getcashreport/$','getcashreportajax'),

      #****Admin***************
      url(r'^thrift/reports/getadminid/$','getadminid'),
      url(r'^thrift/reports/getadminname/$','getadminname'),
      url(r'^thrift/reports/getadminreport/$','getadminreportajax'),
    
###*****************************MISC************************
	url(r'^thrift/misc/customers/$', 'customerslist'),
	# url(r'^thrift/misc/namesearch/$', 'namesearch'),
	url(r'^thrift/misc/switches/$', 'switches'),
	url(r'^thrift/misc/getstaff/$','getallstall'),
	url(r'^thrift/misc/getswitch/$','getbutton'),
	# url(r'^thrift/misc/showselect/$','openoption'),

	
	)
