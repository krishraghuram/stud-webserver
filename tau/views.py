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
from forms import FileForm
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader

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
		# if request.FILES:
		# 	form = FileForm(request.POST, request.FILES)
		# 	print "Cleaned Form Data : ",request.POST['path']
		# 	parent = Folder.objects.get(path=request.POST['path'])
		# 	print parent
		# 	file = File(drive=request.user.drive, parent=parent, file=request.FILES['file'])
		# 	file.save()
		if request.FILES:
			form = FileForm(request.POST, request.FILES)
			if form.is_valid():
				print "Cleaned Form Data : ",form.cleaned_data['path']
				parent = Folder.objects.get(path=form.cleaned_data['path'])
				print parent
				file = File(drive=request.user.drive, parent=parent, file=request.FILES['file'])
				file.save()
			else:
				print "RAISE"
				self.template_name = "tau/form_error.html"
				# print render(self.request, self.template_name)
				# template = loader.get_template(template_name)
				# context = {'form':form}
				# return HttpResponse(template.render(context,request))
				return render(self.request, self.template_name, {"form":form})

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
		# for i in path_dict:
		# 	print i,path_dict[i]
		print "Context : ",context

		return context




#Upload a file or a folder
# @method_decorator(login_required, name="dispatch")
# class UploadView(TemplateView):
# 	def post(self, request, *args, **kwargs):
# 		form = FileForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			print "YOO : ",form.cleaned_data['path']
# 			parent = Folder.objects.get(path=form.cleaned_data['path'])
# 			file = File(drive=request.user.drive, parent=parent, file=request.FILE['file'])
# 			file.save()

# 		return HttpResponse(reverse('FolderView'))

