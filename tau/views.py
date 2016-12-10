from django.shortcuts import render

# Create your views here.

from .models import Drive, Folder, File
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import os
from collections import OrderedDict

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
		if args[0]=='':
			self.path=None
		else:
			self.path=args[0]
			if self.path[-1]=='/':
				self.path = self.path[:-1]

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
		context["drive_home"] = ''

		#TEST CODE
		# print "Path : ",path
		# print "Folders : ",folders.values()
		# print "Path_Dicr :", path_dict
		# for i in path_dict:
		# 	print i,path_dict[i]
		# print context

		return context
