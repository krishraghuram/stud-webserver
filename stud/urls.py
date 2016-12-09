"""stud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
#For now, we use predefined login views. Later, we will have a custom login app with custon User model and custom Auth Backend
from django.contrib.auth import views as auth_views
from .views import StudView

urlpatterns = [
	#For now, we use default auth mechanism. 
	#Later, we will have custom login app with custom user model and custom auth backend(webmail based)
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^$', StudView, name='stud'), #Stud Main Page
    url(r'^chrono/', include('chrono.urls')),
    url(r'^tau/', include('tau.urls')),
    url(r'^admin/', admin.site.urls),
]
