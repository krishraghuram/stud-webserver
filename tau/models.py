from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.conf import settings
from django.contrib.auth import get_user_model
import re
from django.core.exceptions import ValidationError
import Constants
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
##### Setting User here would be better, since it would work globally, but we cant do it.
##### If we do, django raises "AppRegistryNotReady("Models aren't loaded yet.")"
##### User = get_user_model()




#We will use the login user model for users in tau
#We need a model for the User's Remote Directory and a model for a file
#Drive and File
	#Drive
		#One-One relation with a user. 
		#Space Used
		#Total Space should be defined in tau.constants
	#File
		#Path
		#Filename
		#File
		#UserDrive, as a Foreign Key
		#MEDIA_ROOT/tau/self.user[User.USERNAME_FIELD]/path/filename
#Security Checks
	#File size will be limited for every file 
		#Implementing this in Django isnt good enough, because if django is able to check file size, 
		#it means full file has already been uploaded.
		#This has to be done at apache level or nginx level.
	#Before a file upload starts, a check will be made on user's space left
		#This will be done on django level
	#If possible, work on something like chroot jail

class Drive(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
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
		return str(self.user)+"\nSpace Used in Drive : "+str(space_used)+"\nSpace Left in Drive : "+str(space_left)

#A callable upload_to for the FileField
def upload_to(instance, filename):
	#First, set instance.filename to the filename of the file that user is uploading
	instance.filename = filename
	#Now, return the path(including filename) to upload the file(relative to MEDIA_ROOT)
	User = get_user_model()
	username = instance.drive.get_user().__dict__[User.USERNAME_FIELD] #Need to do this the roundabout way to make sure that this works with CUSTOM USER MODELS. Else, we could have simply went for self.user.username
	return "tau/"+username+"/"+instance.path+instance.filename

class File(models.Model):
	path = models.TextField() #The path does not include MEDIA_ROOT, obviously
	filename = models.CharField(max_length=500, editable=False)
	file = models.FileField(upload_to=upload_to)
	##### The method below is simpler and prefferable, but doesnt work.
	##### Because we cant convert the TextField and CharField into str
	##### file = models.FileField(upload_to=str(path)+str(filename))	
	# user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT) 
	drive = models.ForeignKey(Drive, models.PROTECT) #Protects Drive from being deleted when files are left

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
		#Limit User total space to 250 Mibi Bytes.
		try:
			this = File.objects.get(id=self.id) #Get the file object from database	
			extra = this.file.size #The extra space that will be obtained due to deletion of old file.
		except:
			extra = 0 #No extra space will be obtained, since there is no old file.
		if ((self.drive.space_left()+extra)<self.file.size):
			self.file.delete(save=False) #save=False since we dont want to save database object 
			raise ValidationError(str(self.drive.get_user())+"\'s Drive Space Limit Reached.")

		#TEST CODE
		#For some reason, clean() is being called twice.
		#And self.filename is undefined below
		#Also, self.file.name still contains characters besides 0-9, a-z, A-z and _ - .
		#But database entries and files are being created properly, so no harm
		# print self.path
		# if self.filename:	
		# 	print self.filename
		# print self.file.name
		# print self.file.size
		# print self.user
		# print user_space

	def save(self, *args, **kwargs):
		#Sanitize the path and filename, as well as validate for remaining space on drive
		self.full_clean()

		#In case user changes the uploaded file,
		#Make sure the old file is deleted from filesystem
		try:
			this = File.objects.get(id=self.id) #Get the file object from database
			if this.file != self.file: #If database file object and current one are diff, user is changing the file
				this.file.delete(save=False) #So we should delete old file. Passing False so that it doesnt cause a infinite recursion
		except: 
			pass #Exception occurs when save is called for first time, since database has no File object with id=self.id

		return super(File, self).save(*args, **kwargs)

	def __str__(self):
		if self.path[-1]=='/':
			text = "\n"+str(self.path)+str(self.filename)
		else:
			text = "\n"+str(self.path)+"/"+str(self.filename)
		return text

#Make sure file is deleted from filesystem when File Model object is deleted from database
@receiver(post_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(save=False)
