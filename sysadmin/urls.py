from django.conf.urls import patterns, include, url



urlpatterns = patterns('sysadmin.views',
	url(r'^sysadmin/sysadmin/guide/$', 'tutorial'),

	 )