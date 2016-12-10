from django import forms
from django.core.exceptions import *
from models import File, Folder, Drive

class FileForm(forms.Form):
	path = forms.CharField(max_length = 1000)
	file = forms.FileField()

	#Do validation here
	def clean(self):
		cleaned_data = super(FileForm, self).clean()
		path = cleaned_data.get('path')
		file = cleaned_data.get('file')

		#Files can only be uploaded to folders. Files cannot be uploaded to Drive directly
		#Thus, we have to validate that "parent" exists before uploading a "file"
		try:
			parent = Folder.objects.get(path=path)
		except Folder.DoesNotExist as e:
			raise ValidationError("Files can only be uploaded to folders. Files cannot be uploaded to Drive directly")


		return cleaned_data