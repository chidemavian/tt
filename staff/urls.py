from django.conf.urls import patterns, include, url



urlpatterns = patterns('staff.views',
	url(r'^staff/staff/guide/$', 'tutorial'),
	 url(r'^staff/home/$', 'welcome'),
	 url(r'^staff/staffdet/$', 'newst'),
	 url(r'^staff/registeration/mass/$', 'massReg'),
	 url(r'^staff/roleplay/$', 'roles'),
	 url(r'^staff/staff_list/$', 'stafflist'),
	 url(r'^staff/deactivate/$', 'deactivate'),
	 url(r'^staff/activate/$', 'activate'),
	  url(r'^staff/delete/$', 'delete'),
	   url(r'^staff/reset/$', 'reset'),

	 url(r'^staff/selectrole/$','setroles'),
	 url(r'^staff/updaterole/(\d+)/$','updaterole'),
	 url(r'^staff/viewstaffdet/$','viewdetail')
	 )