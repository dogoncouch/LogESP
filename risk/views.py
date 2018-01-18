from django.shortcuts import render
from django.views import generic

from .models import AdvThreatEvent, NonAdvThreatEvent

# Create your views here.

def index(request):
    return render(request, 'risk/index.html')

class ATEIndexView(generic.ListView):
    model = AdvThreatEvent
    template_name = 'risk/ate_index.html'
    context_object_name = 'ate_list'

class ATEDetailView(generic.DetailView):
    model = AdvThreatEvent
    template_name = 'risk/ate_detail.html'
    context_object_name = 'ate'

class NTEIndexView(generic.ListView):
    model = NonAdvThreatEvent
    template_name = 'risk/nte_index.html'
    context_object_name = 'nte_list'

class NTEDetailView(generic.DetailView):
    model = NonAdvThreatEvent
    template_name = 'risk/nte_detail.html'
    context_object_name = 'nte'

