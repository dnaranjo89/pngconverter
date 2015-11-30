from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpRequest,HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from pngconverter.models import Image
from celery import Celery
from PIL import Image as ImagePil
import mimetypes
from random import randrange

app = Celery('image_converter')


def index(request):
    images = reversed(Image.objects.all())
    return render(request, 'index.html', {'images': images})


@require_http_methods(["POST"])
def image_upload(request):
    # Validate image
    try:
        im = ImagePil.open(request.FILES['file'])
    except Exception:
        return HttpResponseBadRequest("Are you sure that's an image? :/")
    if im.format is not 'PNG':
        return HttpResponseBadRequest("That's not a PNG!")

    # Save the image
    image = Image(original=request.FILES['file'])
    image.save()
    # Start the conversion
    delay = randrange(3, 6) if 'add-delay' in request.POST else 0
    try:
        image.convert_to_jpg.delay(delay)
    except Exception as e:
        return HttpResponseBadRequest(e)
    return HttpResponse()


def image_download(request, filename):
    wrapper = FileWrapper(open(filename, 'rb'))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def monitor(request):
    """
     This method should only return the files uploaded for the current user
     or within a particular session... Of course not the whole DB, its just
     for testing purposes.
    """
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
