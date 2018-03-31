
from django.shortcuts import render, redirect
from LogESP import __version__
# Create your views here.

def index(request):
    return render(request, 'index.html', {'version': __version__})
