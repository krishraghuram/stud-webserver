from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.generic.base import TemplateView

class MainView(TemplateView):
	template_name = "main/main.html"

