from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import AdvThreatEvent, NonAdvThreatEvent
from .models import AdvThreatSource, NonAdvThreatSource
from .models import Vulnerability, RiskCondition, Impact

# Create your views here.

def index(request):
    return render(request, 'risk/index.html')

class ATEIndexView(ListView):
    model = AdvThreatEvent
    template_name = 'risk/ate_index.html'
    context_object_name = 'ate_list'

class NTEIndexView(ListView):
    model = NonAdvThreatEvent
    template_name = 'risk/nte_index.html'
    context_object_name = 'nte_list'

class ATSIndexView(ListView):
    model = AdvThreatSource
    template_name = 'risk/ats_index.html'
    context_object_name = 'ats_list'

class NTSIndexView(ListView):
    model = NonAdvThreatSource
    template_name = 'risk/nts_index.html'
    context_object_name = 'nts_list'

class VulnIndexView(ListView):
    model = Vulnerability
    template_name = 'risk/vuln_index.html'
    context_object_name = 'vuln_list'

class CondIndexView(ListView):
    model = RiskCondition
    template_name = 'risk/cond_index.html'
    context_object_name = 'cond_list'

class ImpactIndexView(ListView):
    model = Impact
    template_name = 'risk/impact_index.html'
    context_object_name = 'impact_list'

class ATEDetailView(DetailView):
    model = AdvThreatEvent
    template_name = 'risk/ate_detail.html'
    context_object_name = 'ate'

class NTEDetailView(DetailView):
    model = NonAdvThreatEvent
    template_name = 'risk/nte_detail.html'
    context_object_name = 'nte'

class ATSDetailView(DetailView):
    model = AdvThreatSource
    template_name = 'risk/ats_detail.html'
    context_object_name = 'ats'

class NTSDetailView(DetailView):
    model = NonAdvThreatSource
    template_name = 'risk/nts_detail.html'
    context_object_name = 'nts'

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

class ATSCreateView(CreateView):
    model = AdvThreatSource
    fields = ['name', 'desc', 'source_type', 'info_source', 'tier',
            'in_scope', 'capability', 'intent', 'targeting']
    def get_success_url(self):
        return reverse_lazy('risk:ats_detail', args=(self.object.id,))

class NTSCreateView(CreateView):
    model = NonAdvThreatSource
    fields = ['name', 'desc', 'source_type', 'info_source', 'tier',
            'in_scope', 'range_of_effect']
    def get_success_url(self):
        return reverse_lazy('risk:nts_detail', args=(self.object.id,))

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

class ATSUpdateView(UpdateView):
    model = AdvThreatSource
    fields = ['name', 'desc', 'source_type', 'info_source', 'tier',
            'in_scope', 'capability', 'intent', 'targeting']
    def get_success_url(self):
        return reverse_lazy('risk:ats_detail', args=(self.object.id,))

class NTSUpdateView(UpdateView):
    model = NonAdvThreatSource
    fields = ['name', 'desc', 'source_type', 'info_source', 'tier',
            'in_scope', 'range_of_effect']
    def get_success_url(self):
        return reverse_lazy('risk:nts_detail', args=(self.object.id,))


