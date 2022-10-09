

from django.conf.urls import patterns, include, url


urlpatterns = patterns('sms.views',

	#***********************Sms Subscription********************
	url(r'^daily_contribution/sms/well/$','well'),
	url(r'^daily_contribution/sms/$','sms_customer'),

	url(r'^daily_contribution/balance/$','sms_purchase'),
	url(r'^thrift/sms/register/customer/$', 'transactional'),
	url(r'^thrift/sms/sms_history/$', 'sms_history'),
	url(r'^daily_contribution/weeklysms/$', 'weeklysms'),
	url(r'^daily_contribution/monthlysms/$', 'monthlysms'),

	url(r'^daily_contribution/requests/buysms/$', 'buysms'),
	url(r'^daily_contribution/pay/unit/$', 'unit'),
	url(r'^daily_contribution/pay/sms/$', 'pay4sms'),
	)
