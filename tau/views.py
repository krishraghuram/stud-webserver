from django.shortcuts import render

# Create your views here.

from .models import Drive, Folder, File
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import os
from collections import OrderedDict
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.conf import settings
from django.core.exceptions import *


#Splits path into components
def split_path(path):
	path = os.path.normpath(path)
	return path.split(os.sep)


#View files in a given folder
@method_decorator(login_required, name="dispatch")
class FolderView(ListView):
	template_name = "tau/folder.html"
	queryset = Drive.objects.none() #Just to keep django happy
	path = None

	def get(self, request, *args, **kwargs):
		if args: 
			if args[0]=='':
				self.path=None
			else:
				self.path=args[0]

		if hasattr(request.user, 'drive'): #User has a drive
			pass			
		else: #User doesnt have a drive
			#Create a new drive for the user
			drive = Drive(user=request.user)
			drive.save()
			#Welcome the new user to tau
			self.template_name = "tau/welcome.html"

		return super(FolderView, self).get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		#Get the base's context
		context = super(FolderView, self).get_context_data(**kwargs)
		
		#Get the path
		path = self.path

		#Get the folders and files in that path
		folders = Folder.objects.filter(drive=self.request.user.drive, parent__path=path).order_by('name')
		files = File.objects.filter(drive=self.request.user.drive, parent__path=path).order_by('name')

		if path is not None:
			path = split_path(path)
			path_dict = OrderedDict()
			for i in range(len(path)):
				path_dict[path[i]] = '/'.join(path[:i+1]) 
			context["path"] = "/".join(path)
			context["path_dict"] = path_dict
		context["folders"] = folders
		context["files"] = files

		#TEST CODE
		# print "Path : ",path
		# print "Folders : ",folders.values()
		# print "Path_Dicr :", path_dict
		# for i in path_dict:
		# 	print i,path_dict[i]
		# print context

		return context


#View files in a given folder
@method_decorator(login_required, name="dispatch")
class FileView(View):
	#GET - Download File
	def get(self, request, *args, **kwargs):
		if hasattr(request.user, 'drive'): #User has a drive
			try:
				file_id = request.GET['file_id']
				file = File.objects.get(pk=file_id)
				return HttpResponseRedirect(settings.MEDIA_URL+"tau/techsec/1/File.pdf")
			except File.DoesNotExist:
				error = "The Requested File Does Not Exist"
				return HttpResponseRedirect(reverse('ErrorView', kwargs={'error':error}))
		else: #User doesnt have a drive
			return HttpResponseRedirect(reverse('FolderView'))

#View to show errors to user
@method_decorator(login_required, name="dispatch")
class ErrorView(TemplateView):
	template_name = "tau/error.html"

	def get_context_data(self, **kwargs):
		#Get the base's context
		context = super(ErrorView, self).get_context_data(**kwargs)

		#Get Error
		error = kwargs['error']

		context['error'] = error

		return context

