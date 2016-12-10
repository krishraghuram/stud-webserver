from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.conf import settings
from django.contrib.auth import get_user_model
import re
from django.core.exceptions import *
import Constants
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
import shutil, os, errno
##### Setting User here would be better, since it would work globally, but we cant do it.
##### If we do, django raises "AppRegistryNotReady("Models aren't loaded yet.")"
##### User = get_user_model()





#We will use the login user model for users in tau
#We need a model for the User's Remote Directory, a model for Folders and a model for Files
#Security Checks
	#File size will be limited for every file 
		#Implementing this in Django isnt good enough, because if django is able to check file size, 
		#it means full file has already been uploaded.
		#This has to be done at apache level or nginx level.
	#Before a file upload starts, a check will be made on user's space left
		#This will be done on django level
	#Maximum subfolders in any folder
	#Maximum Folder Depth - Can be a field in folder model - Counted by no of slashes in the path
	#If possible, work on something like chroot jail





class Drive(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	space_used = models.PositiveIntegerField(editable=False, default=0)

	def space_left(self):
		#First make sure space_used is up to date
		self.space_used = sum([i.file.size for i in File.objects.filter(drive=self)])
		#Return the space left
		return (Constants.total_drive_space - self.space_used)

	def get_user(self):
		return self.user

	def __str__(self):
		space_used = sum([i.file.size for i in File.objects.filter(drive=self)])		
		space_left = Constants.total_drive_space - space_used
		space_used = '%.2f' % (float(space_used)/(1024*1024)) + "MiB"
		space_left = '%.2f' % (float(space_left)/(1024*1024)) + "MiB"
		return str(self.user)+" : space used = "+space_used+", space left = "+space_left





#Actions
	#Deleting Folder object should delete all subfolders and all files
	#Changing Folder should reflect in database and filesystem 
	#Moving Folder to a different location should reflect in database and filesystem
	#Sending Folder to another user should create a copy of the folder in given user's drive
class Folder(models.Model):
	drive = models.ForeignKey("Drive", models.CASCADE) 
	parent = models.ForeignKey("Folder", models.CASCADE, null=True, blank=True) #Need null and blank to be true so that root folder can be "NULL"
	name = models.CharField(max_length = 100)
	path = models.TextField(editable=False) #Doesnt contain a trailing slash

	def update_path(self):
		#Set path
		if self.parent:
			self.path = os.path.join(self.parent.path, self.name)
		else:
			self.path = self.name

	def get_path(self):
		return self.path

	def get_full_path(self):
		User = get_user_model()
		full_path = os.path.join(settings.MEDIA_ROOT, "tau", self.drive.get_user().__dict__[User.USERNAME_FIELD], self.path)
		return full_path

	def clean(self):
		#Update Path
		self.update_path()

		#Check for max subfolders in a folder
		subfolders = Folder.objects.filter(parent = self.parent)
		print len(subfolders)
		if len(subfolders)+1>Constants.max_subfolders:
			raise ValidationError("Max Subfolders in any folder is "+str(Constants.max_subfolders))

		#Check for max folder depth
		path_depth = len(os.path.normpath(self.path).split(os.sep))
		if path_depth>Constants.max_folder_depth:
			raise ValidationError("Maximum Folder Depth Allowed is "+str(Constants.max_folder_depth))
		

	def save(self, *args, **kwargs):
		#Validate for remaining space on drive
		self.full_clean()

		#Make sure path is updated before saving
		self.update_path()

		#Check if user has made changes
		try:
			this = Folder.objects.get(id=self.id) #Get the Folder Model object from database				
			if this.name != self.name: #User has renamed folder
				if (os.path.isdir(self.get_full_path()) or os.path.isfile(self.get_full_path())):
					raise OSError(errno.EEXIST, self.get_path() + " Already Exists")			
				else:
					os.rename(this.get_full_path(), self.get_full_path())
			elif this.parent != self.parent: #User has moved folder
				if (os.path.isdir(self.get_full_path()) or os.path.isfile(self.get_full_path())):
					raise OSError(errno.EEXIST, self.get_path() + " Already Exists")			
				else:
					shutil.move(this.get_full_path(), self.get_full_path())
		except Folder.DoesNotExist: #Exception occurs when Folder is being saved first time(in line 79)
			os.makedirs(self.get_full_path())

		return super(Folder, self).save(*args, **kwargs)

	def __str__(self):
		self.update_path()
		return self.path


#Make sure folder is deleted from filesystem when Folder Model object is deleted from database
@receiver(post_delete, sender=Folder)
def folder_delete(sender, instance, **kwargs):
	#Since its post_delete, the files should have been deleted from filesystem
	os.rmdir(instance.get_full_path())

#Make sure subfolders are saved after a folder is modified and saved
@receiver(post_save, sender=Folder)
def folder_save(sender, instance, **kwargs):
	subfolders = Folder.objects.filter(parent=instance)
	for i in subfolders:
		if i.path != os.path.join(instance.path,i.name):
			i.save()





#A callable upload_to for the FileField
def upload_to(instance, filename):
	instance.name = filename
	return os.path.join(instance.parent.get_full_path(),filename)

class File(models.Model):
	drive = models.ForeignKey("Drive", models.PROTECT) #Protects Drive from being deleted when files exist
	parent = models.ForeignKey("Folder", models.CASCADE) #Parent cant be null or blank, so files cant be in root folder. They should be inside a folder. 
	file = models.FileField(upload_to=upload_to)
	name = models.CharField(max_length=100, editable=False)

	def clean(self):
		#name is only allowed to have a-z, A-Z, 0-9 and - _ .
		self.name = "".join(re.findall('[0-9,a-z,A-Z,\.,_,-]',self.name))

		#Limit File Size to 25Mibi Bytes
		#This needs to be done at apache or nginx level.
		#Limit User total space to 250 Mibi Bytes.
		try:
			this = File.objects.get(id=self.id) #Get the file object from database	
			extra = this.file.size #The extra space that will be obtained due to deletion of old file.
		except:
			extra = 0 #No extra space will be obtained, since there is no old file.
		if ((self.drive.space_left()+extra)<self.file.size):
			self.file.delete(save=False) #save=False since we dont want to save database object 
			raise ValidationError(str(self.drive.get_user())+"\'s Drive Space Limit Reached.")

	def save(self, *args, **kwargs):
		#Validate for remaining space on drive
		self.full_clean()

		#In case user changes the uploaded file,
		#Make sure the old file is deleted from filesystem
		try:
			this = File.objects.get(id=self.id) #Get the file object from database
			if this.file != self.file: #If database file object and current one are diff, user is changing the file
				this.file.delete(save=False) #So we should delete old file. Passing False so that it doesnt cause a infinite recursion
		except: 
			pass #Exception occurs when save is called for first time, since database has no File Model object with id=self.id

		return super(File, self).save(*args, **kwargs)

	def __str__(self):
		return "\n"+os.path.join(self.parent.get_path(),self.name)

#Make sure file is deleted from filesystem when File Model object is deleted from database
#Make sure drive space is recalculated and then saved
@receiver(post_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(save=False)
    instance.drive.space_left()
    instance.drive.save()

#Make sure drive space is recalculated and then saved
@receiver(post_save, sender=File)
def file_save(sender, instance, **kwargs):
	instance.drive.space_left()
	instance.drive.save()

