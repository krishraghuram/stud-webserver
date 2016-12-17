from django.shortcuts import render

# Create your views here.

from .models import Drive, Folder, File
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import os
from collections import OrderedDict
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.conf import settings
from django.core.exceptions import *


#Splits path into components
def split_path(path):
	path = os.path.normpath(path)
	return path.split(os.sep)


#Folder Operations
@method_decorator(login_required, name="dispatch")
class FolderView(ListView):
	template_name = "tau/folder.html"
	queryset = Drive.objects.none() #Just to keep django happy
	path = None

	#POST with action=create -> Create Folder
	def create(self):
		try:
			drive = self.request.user.drive
			path = self.request.POST['path']
			parent = Folder.objects.filter(drive=drive, path=path).first()
			name = self.request.POST['name']
			Folder(drive=drive, parent=parent, name=name).save()
			return HttpResponse(status=200)
		except:
			pass

		error = "An error has occurred in Folder Create. Please contact devs."
		return HttpResponse(error,status=400)

	#POST with action=delete -> Delete Folder
	def delete(self):
		try:
			drive = self.request.user.drive
			path = self.request.POST['path']
			parent = Folder.objects.filter(drive=drive, path=path).first()
			name = self.request.POST['name']
			Folder.objects.filter(drive=drive, parent=parent, name=name).delete()
			return HttpResponse(status=200)
		except:
			pass

		error = "An error has occurred in Folder Delete. Please contact devs."
		return HttpResponse(error,status=400)


	def get(self, request, *args, **kwargs):
		if args: 
			if args[0]=='':
				self.path=None
			else:
				self.path=args[0]

		if hasattr(request.user, 'drive'): #User has a drive
			return super(FolderView, self).get(request, *args, **kwargs)
		else: #User doesnt have a drive
			#Redirect him to DriveView so that he can create a drive
			return HttpResponseRedirect(reverse('DriveView'))

	def post(self, request, *args, **kwargs):
		if hasattr(request.user, 'drive'): #User has a drive
			if request.POST['action'] is not None:
				action = request.POST['action']
				if action=='create':
					return self.create()
				elif action=='delete':
					return self.delete()
				#To be implemented
				# elif action=='send':
					# self.send()
				# elif action=='rename'
					# self.rename()
			else: #No action specified
				error = "An error has occurred in Folder. Please contact devs."
				return HttpResponse(error,status=400)
		else: #User doesnt have a drive
			return HttpResponseRedirect(reverse('FolderView'))
	
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

		return context


#File Operations
@method_decorator(login_required, name="dispatch")
class FileView(View):
	#POST with action=upload -> Upload File
	def upload(self):
		try:
			drive = self.request.user.drive
			path = self.request.POST['path']
			parent = Folder.objects.filter(drive=drive, path=path).first()
			file = self.request.FILES['file']
			File(drive=drive, parent=parent, file=file).save()
			return HttpResponse(status=200)
		except:
			pass

		error = "An error has occurred in File Upload. Please contact devs."
		return HttpResponse(error,status=400)

	#POST with action=delete -> Delete File
	def delete(self):
		try:
			drive = self.request.user.drive
			path = self.request.POST['path']
			parent = Folder.objects.filter(drive=drive, path=path).first()
			name = self.request.POST['name']
			File.objects.filter(drive=drive, parent=parent, name=name).first().delete()
			return HttpResponse(status=200)
		except:
			pass

		error = "An error has occurred in File Delete. Please contact devs."
		return HttpResponse(error,status=400)

	#GET -> Download File
	def get(self, request, *args, **kwargs):
		if hasattr(request.user, 'drive'): #User has a drive
			try:
				file_id = request.GET['file_id']
				file = File.objects.get(pk=file_id)
				#Check if user is authorized to get this file
				if request.user.drive == file.drive:
					return HttpResponseRedirect(file.get_url_path())
				else:
					return HttpResponseForbidden("<h1 style='text-align:center;'>600 : Not your file.</h1>")	
			except File.DoesNotExist:
				error = "An error has occurred in File. Please contact devs."
				return HttpResponseRedirect(reverse('ErrorView', kwargs={'error':error}))
		else: #User doesnt have a drive
			return HttpResponseRedirect(reverse('FolderView'))

	def post(self, request, *args, **kwargs):
		if hasattr(request.user, 'drive'): #User has a drive
			if request.POST['action'] is not None:
				action = request.POST['action']
				if action=='upload':
					return self.upload()
				elif action=='delete':
					return self.delete()
				#To be implemented
				# elif action=='send':
					# self.send()
				# elif action=='move'
					# self.move()
			else: #No action specified
				error = "An error has occurred in File. Please contact devs."
				return HttpResponse(error,status=400)
		else: #User doesnt have a drive
			return HttpResponseRedirect(reverse('FolderView'))
		

#Drive Operations
@method_decorator(login_required, name="dispatch")
class DriveView(TemplateView):
	template_name = "tau/drive.html"

	def create(self):
		try:
			user = self.request.user
			print user
			Drive(user=user).save()
			return HttpResponse(status=200)
		except:
			error = "An error has occurred in Drive Create. Please contact devs."
			return HttpResponse(error,status=400)


	def post(self, request, *args, **kwargs):
		if request.POST['action'] is not None:
			action = request.POST['action']
			if action=='create':
				return self.create()
			#Future Actions
		else: #No action specified
			error = "An error has occurred in Drive. Please contact devs."
			return HttpResponse(error,status=400)

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


class NavView(TemplateView):
	template_name = "tau/error.html"

	def get(self, request, *args, **kwargs):
		if args: 
			url=args[0]
			if(url=="howto"):
				self.template_name = "tau/howto.html" 
			elif(url=="contact"):
				self.template_name = "tau/contact.html" 


		return super(NavView, self).get(request, *args, **kwargs)

