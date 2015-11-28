from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from pngconverter.models import Image, ImageForm
import time
from django.conf import settings
from imageconverter.celery import long_task


def monitor(request):
    return render(request, 'monitor.html', {})

def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO Fetch the image
            image = Image(original=request.FILES['image'])
            # image = Image()

            # Delay the task here
            # time.sleep(3)

            image.save()
            # long_task.delay()

            image.convert_to_jpg()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ImageForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Image.objects.filter(status=Image.DONE)

    # Render list page with the documents and the form
    return render(request, 'index.html', {'documents': documents, 'form': form})


def image_download(request, filename):
    from django.core.servers.basehttp import FileWrapper
    import mimetypes

    wrapper = FileWrapper(open(filename, 'rb'))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
