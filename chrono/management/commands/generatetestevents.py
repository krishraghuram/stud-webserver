from django.core.management.base import BaseCommand, CommandError
from chrono.models import Event
import datetime
import pytz

class Command(BaseCommand):
	help = 'Creates 25 events in database for testing'

	def handle(self, *args, **options):
		now = datetime.datetime.now()+datetime.timedelta(hours=1)
		now = now.replace(minute=0,second=0,microsecond=0,tzinfo=pytz.timezone("Asia/Calcutta"))
		hour = datetime.timedelta(hours=1)
		day = datetime.timedelta(days=1)
		for i in range(25):
			e = Event(title="Title No:"+str(i+1),start_dt=now+i*day,end_dt=now+i*day+hour,venue="Venue No:"+str(i+1))
			e.save()
			self.stdout.write("Added Event :\n"+str(e))

