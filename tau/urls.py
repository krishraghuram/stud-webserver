from django.conf.urls import url
from . import views
from views import FolderView
# from views import UploadView

urlpatterns = [
    # url(r'^upload/$', UploadView.as_view(), name='UploadView'),
    url(r'^$', FolderView.as_view(), name='FolderView'),
]

