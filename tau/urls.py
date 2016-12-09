from django.conf.urls import url
from . import views
from views import FolderView 

urlpatterns = [
    url(r'^$', FolderView.as_view(), name='FolderView')
]

