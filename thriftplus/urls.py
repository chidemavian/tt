from django.conf.urls import patterns, include, url
from sysadmin.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^login/$', index),
    url(r'^login/user/$', login),
    url(r'^logout/$', logoutuser),
    url(r'^changepass/$', changepass),
    url(r'^switch/$', switchuser),
    url(r'^dashboard/$', dashboard),
    url(r'^home/$', dashboard_client),
    url(r'^dashboard/name_search_ajax/$', namesearch),
    url(r'^dashboard/search/details/$', cusdetailS),
    # Examples:

    url(r'^customer/', include('customer.urls')),
    url(r'^fts/', include('Ia.urls')),
    url(r'^vts/', include('Ib.urls')),
    url(r'^IIIa/', include('IIIa.urls')),
    url(r'^IIIb/', include('IIIb.urls')),
    url(r'^loans/', include('loans.urls')),
    url(r'^sms/', include('sms.urls')),
    url(r'^savings/', include('savings.urls')),
    url(r'^staff/', include('staff.urls')),
    url(r'^corperative/', include('corperative.urls')),
    url(r'^partner/', include('partner.urls')),
    url(r'^sysadmin/', include('sysadmin.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
