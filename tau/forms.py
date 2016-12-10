from django import forms

class FileForm(forms.Form):
	path = forms.CharField(max_length = 1000)
	file = forms.FileField()
	# name =