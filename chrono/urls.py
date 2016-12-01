from django.conf.urls import url
from . import views
from views import ChronoView,EventView

urlpatterns = [
    url(r'^event', EventView, name='EventView'),
    url(r'^$', ChronoView.as_view(), name='ChronoView')
]

