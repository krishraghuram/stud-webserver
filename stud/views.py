from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def StudView(request):
	return HttpResponse("Welcome to IITG Stud Website")