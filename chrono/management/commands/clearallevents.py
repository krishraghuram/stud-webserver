from django.core.management.base import BaseCommand, CommandError
from chrono.models import Event

class Command(BaseCommand):
	help = 'Clears all Events from the database'

	def handle(self, *args, **options):
		e = Event.objects.all()
		self.stdout.write("Objects remaining in database : "+str(len(e)))
		self.stdout.write("Deleting all objects")		
		e.delete()
		e = Event.objects.all()
		self.stdout.write("Objects remaining in database : "+str(len(e)))

