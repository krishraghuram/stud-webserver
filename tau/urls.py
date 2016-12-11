from django.conf.urls import url
from . import views
from views import FolderView
from views import FileView
from views import ErrorView

urlpatterns = [
	url(r'^file/$', FileView.as_view(), name='FileView'), #File Operations
	url(r'^error/(?P<error>.*)/$', ErrorView.as_view(), name='ErrorView'), #Errors
    url(r'^$', FolderView.as_view(), name='Home'), #Drive Home
    url(r'^(.*)/$', FolderView.as_view(), name='FolderView'), #Drive Folders
]
