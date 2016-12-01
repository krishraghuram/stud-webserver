from django.core.management.base import BaseCommand, CommandError
from chrono.models import Event, Email
import poplib
from email.parser import Parser
import re
from dateutil.parser import *
import datetime
import pytz

class Command(BaseCommand):
	help = 'Checks mails from server, updates Event and saves mails in Email for log'

	host = "202.141.80.13"
	port = 995
	username = "k.raghuram"
	password = "totallymypassword"
	encoding = 'UTF8'

	def handle(self, *args, **options):
		server = poplib.POP3_SSL(self.host, self.port)
		try: 
			server.user(self.username)
			if('+OK'):
				server.pass_(self.password)
				if("+OK Logged in."):
					self.stdout.write("Logged in")
					numMessages = server.stat()[0]
					for i in range(100):#range(numMessages):
						try: #Just to catch some shitty bugs
							self.stdout.write("Reading mail number : "+str(i+1))
							text = '\n'.join(server.retr(i+1)[1]) #Raw mail text retrieved via POP3
							message = Parser().parsestr(text) #email.message.Message object
							body = [] #The email body, as list of strings(Each string one line in the email body)
							#Logic to get the body from complex message objects
							if(message.get_content_type()=='text/plain'):
								body.append(message.get_payload())
							elif(message.get_content_type()=='multipart/mixed'):
								payload = message.get_payload()
								for j in payload:
									if(j.get_content_type()=='text/plain'):
										body.append(j.get_payload())
							body = '\n'.join(body) #Combine the lines into a single string
							#Store the email in database
							sent_from = message['from']
							sent_to = message['to']
							sent_on = parse(message['date']).replace(tzinfo=pytz.timezone("Asia/Calcutta")).strftime("%Y-%m-%d %H:%M%z")
							subject = message['subject']
							email = Email(sent_from=sent_from, sent_to=sent_to, sent_on=sent_on, subject=subject, body=body)
							email.save()
							#Regex for Event Details
							pattern = '^-----$\n^(.*)$\n^Date:(.*)$\n^Time:(.*)$\n^Venue:(.*)$\n^-----$'
							matches = re.findall(pattern, text)
							if (len(matches)==0):
								self.stderr.write("No matches in mail : \n"+email.header())
							elif(len(matches)==1):
								self.stdout.write("Exactly one match in mail : \n"+email.header())
								#Create and Save Event object
								title=matches[0][0];
								start_dt = parse(matches[0][1]+" "+matches[0][2])
								end_dt = start_dt+datetime.timedelta(hours=1)
								venue = matches[0][3]
								event = Event(title=title,start_dt=start_dt,end_dt=end_dt,venue=venue)
								event.save()
							else:
								self.stderr.write("More than one match in mail : \n"+email.header())
							#Mark mail for deletion from server
							# server.dele(i)
						except Exception as e:
							self.stderr.write(str(e))
					server.quit()
		except poplib.error_proto:
			self.stderr.write("Password Wrong")
		except Exception as e:
			self.stderr.write(str(e))