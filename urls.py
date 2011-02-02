from django.conf.urls.defaults import *
from Pickem import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^pickem2/', include('pickem2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'$^', views.index),
    (r'^live/$', views.live),
    (r'^allteams/$', views.allteams),
    #url(r'^team/city/(\w+)/$', teamcity, name='teamcity'),
    url(r'^team/name/(\w+)/$', views.teamname, name='teamname'),
    (r'^registration/register/$', views.register),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^user/(\w+)/$', views.profile),
    (r'^create_pick/$', views.create_pick),
    (r'^add_game/$', views.add_game),
)