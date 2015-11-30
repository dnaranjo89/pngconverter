import os
import time
from io import BytesIO
from django.db import models
from django.core.files.base import ContentFile
from PIL import Image as ImagePil
from celery import Celery
from celery.contrib.methods import task_method

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imageconverter.settings')
app = Celery('image_converter')


class Image(models.Model):
    WAITING = 'waiting'
    PROCESSING = 'processing'
    DONE = 'done'
    FAILED = 'failed'

    STATUS_CHOICES = (
        (WAITING, 'Waiting'),
        (PROCESSING, 'processing'),
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

    class Meta:
        app_label = 'pngconverter'

    @app.task(filter=task_method)
    def convert_to_jpg(self, delay=None):
        self.status = Image.PROCESSING
        self.save()
        if delay:
            time.sleep(delay)

        im = ImagePil.open(self.original)
        f = BytesIO()
        try:
            # Convert to JPG
            im.convert('RGB').save(f, format='jpeg')
        except Exception as e:
            # TODO Handle the exception
            self.status = Image.FAILED
            raise Exception("Impossible to convert to JPG")
        else:
            new_filename = os.path.splitext(self.original.name)[0] + '.jpg'
            self.converted.save(new_filename, ContentFile(f.getvalue()))
            self.status = Image.DONE
        finally:
            self.save()
            f.close()
            im.close()
