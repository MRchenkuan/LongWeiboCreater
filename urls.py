from django.conf.urls.defaults import patterns, include, url


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LWBCTR.views.home', name='home'),
    # url(r'^LWBCTR/', include('LWBCTR.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^m$','LWBCTR.IMGCTR.views.cpage'),
    url(r'^$','LWBCTR.IMGCTR.views.displayhome'),
    url(r'^c$','LWBCTR.IMGCTR.views.c'),
    url(r'^s$','LWBCTR.IMGCTR.views.s'),
    url(r'^sendCapture/$','LWBCTR.IMGCTR.views.sendCapture'),
    url(r'^validCapture/$','LWBCTR.IMGCTR.views.validCapture'),
    url(r'^adReveiw/$','LWBCTR.IMGCTR.views.adReveiw'),
    url(r'^adReveiw-ad/$','LWBCTR.IMGCTR.views.adReveiwAd'),
    url(r'^addAd/$','LWBCTR.IMGCTR.views.addAd'),
    url(r'^adAddPage/$','LWBCTR.IMGCTR.views.adAddPage'),
    url(r'^review/$','LWBCTR.IMGCTR.views.review'),
    url(r'^api/$','LWBCTR.IMGCTR.views.API'),
    url(r'^home/$','LWBCTR.IMGCTR.views.displayhome'),
    url(r'^login/$','LWBCTR.IMGCTR.views.login'),
    url(r'^logout/$','LWBCTR.IMGCTR.views.logout'),
    url(r'^test/$','LWBCTR.IMGCTR.views.test'),
    url(r'^testpage/$','LWBCTR.IMGCTR.views.testpage'),
    url(r'^loginpage/$','LWBCTR.IMGCTR.views.loginpage'),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './js'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './images'}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './css'}),
    # url(r'^static/$','LWBCTR.static'),
)
