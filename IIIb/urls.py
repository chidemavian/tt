from django.conf.urls import patterns, include, url


urlpatterns = patterns('IIIb.views',


	#********************How it works************
	 url(r'^threeb/home/$', 'welcome'),


	 url(r'^threeb/admin/home/$', 'adminwelcome'),



	 #*********************membership***************
	 url(r'^threeb/registeration/$', 'newregistration'),
	 url(r'^threeb/registeration/mass/$', 'massReg'),

	 url(r'^threeb/vas/utils/$', 'massReg'),

	 url(r'^threeb/staff/home/$', 'staffwelcome'), 




  	##***************Aprovals***********
	 url(r'^threeb/loans/approvals/$', 'loan_approvals'),

	url(r'^threeb/loans/approval/ajax/$', 'loanscene45'),

     url(r'^threeb/loans/approvals/approvell/$','loanapprvopt'),
     
    url(r'^threeb/staff/approvals/approveall/yes/$','pwallapprove'),
    
     url(r'^threeb/loans/scenarios/$', 'loanscene'),

   

 

  	##***************Pay outs***********
	 url(r'^threeb/loans/payouts/$', 'loan_payout'),
	 url(r'^threeb/loans/payout/ajax/$', 'payout45'),

     url(r'^threeb/loans/scenarios/$', 'loanscene'),

     url(r'^threeb/loans/approvals/approvell/$','loanapprvopt'),

 	 url(r'^threeb/staff/approvals/approveall/yes/$','pwallapprove'),






   





  	##***************Porations***********
	 url(r'^threeb/loans/approve/$', 'bookloan'),
     url(r'^threeb/loans/approval/ajax/$', 'loanscene45'),

     url(r'^threeb/loans/lr/$', 'lr'),
     url(r'^threeb/loans/approves/$', 'loanscene_old'),
     url(r'^threeb/loans/salary/$', 'loandem'),


     url(r'^threeb/loans/purchases/$', 'lr'),
     url(r'^threeb/loans/log/$', 'bookloan'),

    url(r'^threeb/loans/decline/$','declineoptions'),
    url(r'^threeb/staff/request_loan/decline/yes/$','yesdecline'),



    url(r'^threeb/loans/approve/all/$','approveoptions'),

 url(r'^threeb/staff/savings/approve/yes/$','wallapprove'),





	 ####*******set ups*****************
	 url(r'^threeb/loans/settings/$', 'loan_setup'),
	 url(r'^threeb/loans/settings/limit/$', 'loan_limit'), 
 	url(r'^threeb/openingbalances/settings/$', 'opening'),
 	url(r'^threeb/upload/settings/$', 'uppld'),
 	url(r'^threeb/savings/settings/$', 'savings_setup'),

  	url(r'^threeb/items/settings/$', 'loan_setup'), 
   	url(r'^threeb/log/settings/$', 'loan_setup'), 





	 ####*******Manage set ups*****************
	 url(r'^threeb/manage/settings/$', 'manage_setup'), 

 url(r'^threeb/savings/settings/$', 'savings_setup'), 





		####*******cooperatorst*******************
url(r'^threeb/staff_list/$', 'stafflist'),





		####*******My wallet*******************
	 url(r'^threeb/staff/mywallet/$', 'history'), 
	 url(r'^threeb/staff/statement/$', 'statement'),
	 url(r'^threeb/staff/withdraw/$', 'history'),
	 url(r'^threeb/staff/transfer/$', 'history'),





#************************my savings***********************
	 url(r'^threeb/savings/deposit/$', 'deposit'),
	 url(r'^threeb/savings/wallet/$', 'checkdep'),
	 url(r'^threeb/savings/deposit/save/$', 'save_deposit'),
	 url(r'^threeb/savings/save_packages/$', 'safepack'),
	  url(r'^threeb/staff/deposit/apply/$', 'applydep'),
	  url(r'^threeb/savings/deposit/packages/$', 'save_pack'),
	 url(r'^threeb/savings/deposit/view_transactions/$', 'savelog'),
	 url(r'^threeb/staff/deposit/log/$', 'deplogs'),



			#*********************MY loan******************************
	url(r'^threeb/staff/request_loan/$', 'reqloan'),
    url(r'^threeb/staff/request_loan/individual/$', 'loandetails'),
	url(r'^threeb/staff/request_loan/performance/$', 'loanperformance'),
	url(r'^threeb/staff/request_loan/history/$', 'loanhistory'),

	url(r'^threeb/staff/repay_loan/$', 'repay'),

     url(r'^threeb/staff/request_loan/loan_packages/$', 'getloanpacks'),

     url(r'^threeb/staff/request_loan/apply/$', 'apply'),


     #******************MISC****************************
     url(r'^threeb/staff/changepass/$', 'changepass'),
     # url(r'^threeb/staff/profile/$', 'my_Profile'),




     url(r'^threeb/loans/repayment/$', 'optionx'),
     url(r'^threeb/staff/repay_loan/repay/$', 'yesrepayloan'),



		####*******my deductions******************
	 url(r'^threeb/staff/allmydeductions/$', 'dedopts'),
	 url(r'^threeb/staff/allmydeduction/dedajax/$', 'ajaxded'),




		####*******H-R*******************
	 url(r'^threeb/staff/myh-r/$', 'hr'), 
	 url(r'^threeb/staff/mydeductions/$', 'deductions'),
	 url(r'^threeb/staff/mydeductions/ajax/$', 'deajax'),

	 url(r'^threeb/staff/myadditions/$', 'additions'),
	 url(r'^threeb/staff/myadditions/$', 'additions'),
	 url(r'^threeb/staff/nets/$', 'allnets'),

     

     # url(r'^threeb/staff/request_loan/decline/yes/$','yesdecline'),
	)

