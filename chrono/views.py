from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.generic import TemplateView
from .models import Event
from django.core import serializers
from dateutil.parser import *
import datetime

class ChronoView(TemplateView):
	template_name = 'chrono/chrono.html'

def EventView(request):
	# print request.method
	if(request.method=='POST'):	
		# print request.POST
		date = parse(request.POST.get('date'))
		events = Event.objects.filter(start_dt__gte = date).order_by('start_dt')#.defer('start_dt','end_dt')
		# print date
		# print type(date)
		# for i in events:
		# 	print i.title
		data = serializers.serialize('json', events)
			# for i in data:
				# i['fields']['start_dt'] = parse(i['fields']['start_dt']).strftime('%a %b %d %Y %I:%M %p')
				# i['fields']['end_dt'] = parse(i['fields']['end_dt']).strftime('%a %b %d %Y %I:%M %p')
		# print data
		return HttpResponse(data, content_type='application/json')
	else:
		return HttpResponseNotAllowed(['POST'])