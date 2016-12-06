from django.contrib import admin

# Register your models here.

from .models import Drive,File

admin.site.register(Drive)
admin.site.register(File)
