from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Create your views here.


def index(request):
    # Render the HTML template index.html
    context = {}
    return render(request, 'index.html', context=context)
