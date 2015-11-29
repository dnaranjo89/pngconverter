from django.apps import AppConfig
from pngconverter.models import Image


class PngConverterConfig(AppConfig):
    name = 'pngconverter'
    verbose_name = "PNG Converter"

    def ready(self):
        """
        If, in any case, the server breaks and tasks are pending
        recover them on restart
        """
        images = Image.objects.filter(status__in=[
            Image.PROCESSING,
            Image.WAITING])
        for image in images:
            image.convert_to_jpg.delay()
