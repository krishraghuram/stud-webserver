from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.conf import settings
from django.contrib.auth import get_user_model
import re
##### Setting User here would be better, since it would work globally, but we cant do it.
##### If we do, django raises "AppRegistryNotReady("Models aren't loaded yet.")"
##### User = get_user_model()

#We will use the login user model for users in tau
#We can use User.USERNAME_FIELD for unique folders inside MEDIA_ROOT/tau/
#But we cant load "User" at import time, else we will get "AppRegistryNotReady("Models aren't loaded yet.")" exception
#Thus we load it in upload_to function
#So, final complete path will be,
#MEDIA_ROOT/tau/self.user[User.USERNAME_FIELD]/path/filename

#Thus, we only need model for a file
#Each file will have
#Path
#Filename
#File
#User, as a Foreign Key

#Security Checks
#File size will be limited for every file 
	#Implementing this in Django isnt good enough, because if django is able to check file size, 
	#it means full file has already been uploaded.
	#This has to be done at apache level or nginx level.
#Before a file upload starts, a check will be made on user's space left
	#This will be done on django level
#If possible, work on something like chroot jail

#A callable upload_to for the FileField
#MEDIA_ROOT/tau/self.user[User.USERNAME_FIELD]/path/filename
def upload_to(instance, filename):
	#First, set instance.filename to the filename of the file that user is uploading
	instance.filename = filename
	#Now, return the path(including filename) to upload the file(relative to MEDIA_ROOT)
	User = get_user_model()
	username = instance.user.__dict__[User.USERNAME_FIELD] #Need to do this the roundabout way to make sure that this works with CUSTOM USER MODELS. Else, we could have simply went for self.user.username
	return "tau/"+username+"/"+instance.path+instance.filename

class File(models.Model):
	path = models.TextField() #The path does not include MEDIA_ROOT, obviously
	filename = models.CharField(max_length=500, editable=False)
	file = models.FileField(upload_to=upload_to)
	##### The method below is simpler and prefferable, but doesnt work.
	##### Because we cant convert the TextField and CharField into str
	##### file = models.FileField(upload_to=str(path)+str(filename))	
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT) #Protects User from being deleted when there are files left

	def clean(self):
		#Path is only allowed to have a-z, A-Z, 0-9, and - _ / .
		#Filename is only allowed to have a-z, A-Z, 0-9 and - _ . (Filename cant have /)
		self.path = "".join(re.findall('[0-9,a-z,A-Z,\.,_,-]',self.path))
		self.filename = "".join(re.findall('[0-9,a-z,A-Z,\.,_,-]',self.filename))

		#Path should have a trailing /. Filename shouldnt have a leading /
		if self.path[-1]!='/':
			self.path = self.path+"/"
		if self.filename and self.filename[0]=='/':
			self.filename = self.filename[1:]

		#Limit File Size to 25Mibi Bytes
		#This needs to be done at apache or nginx level.
		#Limit User total space to 1Gibi Byte
		user_files = File.objects.filter(user=user)
		user_space = sum([i.file.size for i in user_files])
		if (user_space>1073741824):
			#raise UserAccountFullException
			pass

		#TEST CODE
		print self.path
		if self.filename:	
			print self.filename
		print self.file.name
		print self.file.size
		print self.user
		print user_space


	def save(self, *args, **kwargs):
		self.full_clean()
		return super(File, self).save(*args, **kwargs)

	def __str__(self):
		if self.path[-1]=='/':
			text = "\n"+str(self.path)+str(self.filename)
		else:
			text = "\n"+str(self.path)+"/"+str(self.filename)
		return text

