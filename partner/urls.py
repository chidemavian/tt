from django.conf.urls import patterns, include, url


urlpatterns = patterns('partner.views',
	 url(r'^partners/partner/$', 'welcome'),
	 url(r'^partner/business/reg/$','registration'),
	 url(r'^partner/business/branch/$','branch'),
	 url(r'^partner/business/branch1/$','branch1'),		
	 url(r'^partner/business/address/$','address'),
	 url(r'^partner/business/ceo/$','ceo'),
	 url(r'^partner/business/ceo1/$','ceo1'),
	 url(r'^partner/business/app/$','app'),
	 url(r'^partner/business/app/update/$','app_update'),

	 url(r'^partner/business/subscription/$','subscription'),
	 url(r'^partner/business/renew/$','renew'),
	 url(r'^partner/business/package/$','package'),
	 url(r'^partner/business/package/trial/$','trial'),
	 url(r'^partner/business/packages/paid/$', 'paid'),
	 # url(r'^partner/business/app/success/$','app_update_success'),
	 url(r'^partner/business/App1/$','app1'),
	url(r'^partner/business/ceodetails/$','regceo'),

	 )