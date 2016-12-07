# from django.shortcuts import render

# # Create your views here.

# from .models import Drive, Folder, File
# from django.views.generic.list import ListView

# #View files in a given folder
# @login_required
# class FolderView(ListView):
# 	def get(self, request):
# 		user = request.user
# 		if hasattr(user, 'drive'): #User has a drive
# 			folders = Folder.objects.filter(drive=user.drive)
# 		else: #User doesnt have a drive
# 			#Create a new drive, and welcome him
			

# 	self.object_list = 