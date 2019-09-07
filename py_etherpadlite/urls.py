from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView


app_name = 'py_etherpadlite'
urlpatterns = [ 
	'',
	path(r'^login$', LoginView.as_view(template_name='etherpad-lite/login.html'), name="login"),
	path('etherpad', LoginView.as_view(template_name='etherpad-lite/login.html'), name="login"),
	path(r'^logout$', LoginView.as_view(template_name='etherpad-lite/logout.html'), name="logout"),
	
	path(r'^etherpad/(?P<pk>\d+)/$', 'views.pad', name="pad_view"),
	path(r'^etherpad/create/(?P<pk>\d+)/$', 'padCreate', name="pad_create"),
	path(r'^etherpad/delete/(?P<pk>\d+)/$', 'padDelete', name="pad_delete"),
	
	path(r'^group/create/$', 'groupCreate', name="group_create"),
	path(r'^accounts/profile/$', 'profile', name="account_profile"),
]
