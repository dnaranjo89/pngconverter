from django.db import models
from django import forms


class Image(models.Model):
    file = models.ImageField(upload_to='pic_folder/')


class ImageForm(forms.ModelForm):
    file = forms.FileField(label='Select a file')

    class Meta:
        model = Image
        fields = ('file',)


class Document(models.Model):
    docfile = models.FileField(upload_to='imageStore')


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )