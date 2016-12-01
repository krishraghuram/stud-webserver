from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.generic import TemplateView
from .models import Event
from django.core import serializers
from dateutil.parser import *
import datetime

class ChronoView(TemplateView):
	template_name = 'chrono.html'

# class EventView(ListView):
# 	model = Events
# 	template_name = 'event.html'
# 	context_object_name = 'events'
# 	def get_queryset(self):
# 		return Events.objects.order_by('start_datetime')[:5]

# date_ev = ''
# @csrf_exempt
# def date_of_events(request):
# 	if request.method == 'POST':
# 		date_ev = request.POST.get('e_date')
# 		today = parse(date_ev).date()
# 	#	e = Events.objects.all()
# 		e = Events.objects.filter(start_datetime__gte = today).order_by('start_datetime')
# 		d = [o.stringconv() for o in e]		
# 		print d
# 		if e == 'None':
# 			return HttpResponse("no event")
# 		else:
# 			return HttpResponse(d)
# 	else:
# 		return HttpResponse("no date")

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