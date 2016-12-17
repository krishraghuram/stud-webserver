from django.conf.urls import url
from . import views
from views import MainView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name' : 'main/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name' : 'main/login.html'}, name='logout'),
	url(r'^$', MainView.as_view(), name='MainView'), #Stud Main Page (Landing Page)
]

