from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from django.conf import settings
from pngconverter.models import Image, ImageForm
from celery import Celery
import mimetypes

app = Celery('image_converter')


def fake_upload():
    for _ in range(10):
        image = Image()
        image.save()
        image.convert_to_jpg.delay(3)

def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO Fetch the image
            # fake_upload()
            image = Image(original=request.FILES['file'])
            image.save()
            image.convert_to_jpg.delay(4)

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ImageForm()  # A empty, unbound form

    # Load documents for the list page
    images = reversed(Image.objects.all())

    # Render list page with the documents and the form
    return render(request, 'index.html', {'images': images, 'form': form})


def image_download(request, filename):
    wrapper = FileWrapper(open(filename, 'rb'))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def monitor(request):
    images = Image.objects.all()
    response = []
    for image in images:
        details = {'id': image.id,
                   'status': image.status
                   }
        if image.status == Image.DONE:
            details['filename'] = image.converted.name
            details['url_download'] = reverse('image_download', kwargs={'filename': image.converted.name})
        else:
            details['filename'] = image.original.name
            details['url_download'] = reverse('image_download', kwargs={'filename': image.original.name})
        response.append(details)
    return JsonResponse(response, safe=False)
