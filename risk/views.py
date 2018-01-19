from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import AdvThreatEvent, NonAdvThreatEvent
from .models import AdvThreatSource, NonAdvThreatSource

# Create your views here.

def index(request):
    return render(request, 'risk/index.html')

class ATEIndexView(ListView):
    model = AdvThreatEvent
    template_name = 'risk/ate_index.html'
    context_object_name = 'ate_list'

class ATEDetailView(DetailView):
    model = AdvThreatEvent
    template_name = 'risk/ate_detail.html'
    context_object_name = 'ate'

class NTEIndexView(ListView):
    model = NonAdvThreatEvent
    template_name = 'risk/nte_index.html'
    context_object_name = 'nte_list'

class NTEDetailView(DetailView):
    model = NonAdvThreatEvent
    template_name = 'risk/nte_detail.html'
    context_object_name = 'nte'

class ATECreateView(CreateView):
    model = AdvThreatEvent
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact']
    def get_success_url(self):
        return reverse_lazy('risk:ate_detail', args=(self.object.id,))

class NTECreateView(CreateView):
    model = NonAdvThreatEvent
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact']
    def get_success_url(self):
        return reverse_lazy('risk:nte_detail', args=(self.object.id,))

class ATEUpdateView(UpdateView):
    model = AdvThreatEvent
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact']
    def get_success_url(self):
        return reverse_lazy('risk:ate_detail', args=(self.object.id,))

class NTEUpdateView(UpdateView):
    model = NonAdvThreatEvent
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact']
    def get_success_url(self):
        return reverse_lazy('risk:nte_detail', args=(self.object.id,))


