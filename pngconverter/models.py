import os
import time
from io import BytesIO
from django.db import models
from django import forms
from django.core.files.base import ContentFile
from PIL import Image as ImagePil
from celery import Celery
from celery.contrib.methods import task_method

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imageconverter.settings')
app = Celery('proj')


class Image(models.Model):
    WAITING = 'WAITING'
    CONVERTING = 'CONVERTING'
    DONE = 'DONE'
    FAILED = 'FAILED'

    STATUS_CHOICES = (
        (WAITING, 'Waiting'),
        (CONVERTING, 'Converting'),
        (DONE, 'Done'),
        (FAILED, 'Failed'),
    )

    # TODO Original has to be REQUIRED
    original = models.ImageField(upload_to='imageStore/original', blank=True, null=True)
    converted = models.ImageField(upload_to='imageStore/jpg', blank=True, null=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=WAITING
                              )

    @app.task(filter=task_method)
    def convert_to_jpg(self, delay=None):
        self.status = Image.CONVERTING
        if delay:
            time.sleep(delay)
            self.status = Image.DONE
            self.save()
            return

        im = ImagePil.open(self.original)
        f = BytesIO()
        try:
            # Convert to PNG
            im.save(f, format='jpeg')
        except Exception:
            # TODO Handle the exception
            self.status = Image.FAILED
        else:
            new_filename = os.path.splitext(self.original.name)[0] + '.jpg'
            self.converted.save(new_filename, ContentFile(f.getvalue()))
        finally:
            f.close()

        # Commit everything
        self.status = Image.DONE
        self.save()


class ImageForm(forms.Form):
    image = forms.ImageField(
        label='Select a file',
        required=False,  # TODO The image field has to be required
    )

