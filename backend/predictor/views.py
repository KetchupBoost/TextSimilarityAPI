from django.shortcuts import render, redirect
from .apps import PredictorConfig
from .models import Document
from .forms import DocumentForm

def pdf(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('PDF')
        else:
            message = 'The form is not valid!!'
    else:
        form = DocumentForm() # An Empty form

    # Load document for list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}

    return render(request, 'list.html', context)