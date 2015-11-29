from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from pngconverter.models import Image, ImageForm
from celery import Celery

app = Celery('image_converter')


def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO Fetch the image
            # image = Image(original=request.FILES['image'])
            for _ in range(10):
                image = Image()
                image.save()
                image.convert_to_jpg.delay(3)
                pass

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ImageForm()  # A empty, unbound form

    # Load documents for the list page
    images = reversed(Image.objects.all())

    # Render list page with the documents and the form
    return render(request, 'index.html', {'images': images, 'form': form})


def image_download(request, filename):
    from django.core.servers.basehttp import FileWrapper
    import mimetypes

    wrapper = FileWrapper(open(filename, 'rb'))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def monitor(request):
    ids = request.GET.getlist("ids[]")
    images = list(Image.objects.filter(id__in=ids))
    response = {
        'status': {image.id: image.status for image in images},
    }
    return JsonResponse(response)
