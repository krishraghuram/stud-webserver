from django.conf.urls import url
from . import views
from views import FolderView
from views import FileView
from views import DriveView
from views import NavView
from views import ErrorView

urlpatterns = [
	url(r'^file/$', FileView.as_view(), name='FileView'), #File Operations
	url(r'^drive/$', DriveView.as_view(), name='DriveView'), #Drive Operations
	url(r'^nav/(.*)/$', NavView.as_view(), name='NavView'), #Display Static Pages of NavBar
	url(r'^error/(?P<error>.*)/$', ErrorView.as_view(), name='ErrorView'), #Display Errors
    url(r'^$', FolderView.as_view(), name='Home'), #Drive Home
    url(r'^(.*)/$', FolderView.as_view(), name='FolderView'), #Main Drive Navigation and Folder Operations
]
