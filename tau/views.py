from django.shortcuts import render

# Create your views here.

from django.db.models import Model
from .models import Drive, Folder, File
from django.views.generic.list import ListView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import os
from collections import OrderedDict
import re

#Splits path into components
def split_path(path):
	path = os.path.normpath(path)
	return path.split(os.sep)

#View files in a given folder
@method_decorator(login_required, name="dispatch")
class FolderView(ListView):
	template_name = "tau/folder.html"
	queryset = Drive.objects.none()
	#If user send a GET, we will show him Root Folder.
	#If user sends a POST, we will look for "path", and show him that folder.

	def get(self, request, *args, **kwargs):
		if hasattr(request.user, 'drive'): #User has a drive
			pass			
		else: #User doesnt have a drive
			#Create a new drive for the user
			drive = Drive(user=request.user)
			drive.save()
			#Welcome the new user to tau
			self.template_name = "tau/welcome.html"

		return super(FolderView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return super(FolderView, self).get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		#Get the base's context
		context = super(FolderView, self).get_context_data(**kwargs)
		
		#Get the path
		path = None
		if self.request.method == 'GET':
		    pass
		elif self.request.method == 'POST':
		    path = self.request.POST.get('path')

		try:
			if path=="Drive":
				path = None
			elif path.startswith("Drive"):
				path = path[len("Drive")+1:]
		except AttributeError as e: #Arises during GET requests
			pass

		#Get the folders and files in that path
		folders = Folder.objects.filter(drive=self.request.user.drive, parent__path=path).order_by('name')
		# folders = Folder.objects.all()
		files = File.objects.filter(drive=self.request.user.drive, parent__path=path).order_by('name')

		#Add path, folders and files to context
		if path is None:
			path = "Drive"
		else:
			path = os.path.join("Drive",path)
		path = split_path(path)
		path_dict = OrderedDict()
		for i in range(len(path)):
			path_dict[path[i]] = '/'.join(path[:i+1]) 
		context["path"] = path_dict
		context["folders"] = folders
		context["files"] = files

		#TEST CODE
		# print "Path : ",path
		# for i in path_dict:
		# 	print i,path_dict[i]
		# print context

		return context
