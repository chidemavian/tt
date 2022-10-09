from django.conf.urls import patterns, include, url


urlpatterns = patterns('customer.views',
##********************Create Wallet***************
	 url(r'^customers/createwallet/$', 'createwallet'),
	 url(r'^customers/editwallet/$', 'editwallet'),
	 url(r'^customers/editwallet/wallet/$', 'doedit'),
	 url(r'^customers/viewwallet/$', 'viewwallet'),
	 url(r'^customers/customer_list/$', 'customerslist'),



###*****Customers' Area**************
	 url(r'^customers/myprofileview/$', 'viewwallet'),    
###*****************************MISC************************

	
	)
