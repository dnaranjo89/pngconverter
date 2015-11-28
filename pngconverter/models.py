from django.db import models
from django import forms

class Document(models.Model):
    docfile = models.FileField(upload_to='imageStore')


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )