from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from pngconverter.models import ImageForm, DocumentForm, Document
from django.conf import settings


def index(request):
    if request.method == 'POST':
        form = ImageForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = ImageForm()

    return render(request, 'index.html', {'form': form})


def monitor(request):
    return render(request, 'monitor.html', {})

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'index.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def image_download(request, filename):
    from django.core.servers.basehttp import FileWrapper
    import mimetypes

    wrapper = FileWrapper(open(filename, 'rb'))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
