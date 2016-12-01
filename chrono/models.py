from __future__ import unicode_literals

from django.db import models

# Create your models here.

#Event according to end user will only have the following
#Title, Date, Time, Venue, Organizer
class Event(models.Model):
	title = models.CharField(max_length=200)
	start_dt = models.DateTimeField()
	end_dt = models.DateTimeField()
	venue = models.CharField(max_length=200)
	organizer_name = models.CharField(max_length=200)
	organizer_contact = models.CharField(max_length=200)
	organizer_mail = models.CharField(max_length=200)

	def __str__(self):
		text = "\nTitle:"+str(self.title)+"\nStart_Datetime:"+str(self.start_dt)+"\nEnd_Datetime:"+str(self.end_dt)+"\nVenue:"+str(self.venue)
		return text

#Raw mails stored in database for log purposes
class Email(models.Model):
	sent_from = models.CharField(max_length=1000)
	sent_to = models.CharField(max_length=1000)
	sent_on = models.DateTimeField()
	subject = models.CharField(max_length=1000)
	body = models.TextField()

	def header(self):
		text = "\nFrom : "+self.sent_from+"\nTo : "+self.sent_to+"\nDate : "+self.sent_on+"\nSubject : "+self.subject
		return text

	def __str__(self):
		text = "\nFrom : "+self.sent_from+"\nTo : "+self.sent_to+"\nDate : "+self.sent_on+"\nSubject : "+self.subject+"\nBody : "+self.body
		return text
