from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView
from .views import *

app_name = 'py_etherpadlite'
urlpatterns = [
	url(r'login$', LoginView.as_view(template_name='etherpad-lite/login.html'), name="login"),
	url(r'^logout$', LoginView.as_view(template_name='etherpad-lite/logout.html'), name="logout"),

	url(r'^etherpads/$', pad, name="pad_view"),
	url(r'^etherpad/(?P<pk>\d+)/$', pad, name="pad_view"),

	url(r'^etherpad/create/(?P<pk>\d+)/$', padCreate, name="pad_create"),
	url(r'^etherpad/delete/(?P<pk>\d+)/$', padDelete, name="pad_delete"),

	url(r'^group/create/$', groupCreate, name="group_create"),
	url(r'^accounts/profile/$', profile, name="account_profile"),
]
