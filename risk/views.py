from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView

from .models import AdvThreatEvent, NonAdvThreatEvent
from .models import AdvThreatSource, NonAdvThreatSource
from .models import Vulnerability, RiskCondition, Impact

# Create your views here.

def index(request):
    return render(request, 'risk/index.html')

def at_index(request):
    return render(request, 'risk/at_index.html')

def nt_index(request):
    return render(request, 'risk/nt_index.html')

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

class VulnDetailView(DetailView):
    model = Vulnerability
    template_name = 'risk/vuln_detail.html'
    context_object_name = 'vuln'

class CondDetailView(DetailView):
    model = RiskCondition
    template_name = 'risk/cond_detail.html'
    context_object_name = 'cond'

class ImpactDetailView(DetailView):
    model = Impact
    template_name = 'risk/impact_detail.html'
    context_object_name = 'impact'

class ATECreateView(CreateView):
    model = AdvThreatEvent
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact', 'vulnerabilities', 'impacts']
    def get_success_url(self):
        return reverse_lazy('risk:ate_detail', args=(self.object.id,))

class NTECreateView(CreateView):
    model = NonAdvThreatEvent
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact', 'risk_conditions', 'impacts']
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

class VulnCreateView(CreateView):
    model = Vulnerability
    fields = ['name', 'desc', 'vuln_type', 'severity',
            'info_source', 'tier']
    def get_success_url(self):
        return reverse_lazy('risk:vuln_detail', args=(self.object.id,))

class CondCreateView(CreateView):
    model = RiskCondition
    fields = ['name', 'desc', 'condition_type', 'pervasiveness',
            'info_source', 'tier']
    def get_success_url(self):
        return reverse_lazy('risk:cond_detail', args=(self.object.id,))

class ImpactCreateView(CreateView):
    model = Impact
    fields = ['name', 'desc', 'impact_type', 'info_source', 'tier',
            'severity', 'impact_tier']
    def get_success_url(self):
        return reverse_lazy('risk:ate_detail', args=(self.object.id,))

class ATEUpdateView(UpdateView):
    model = AdvThreatEvent
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact', 'vulnerabilities', 'impacts']
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

class VulnUpdateView(UpdateView):
    model = Vulnerability
    fields = ['name', 'desc', 'vuln_type', 'severity',
            'info_source', 'tier']
    def get_success_url(self):
        return reverse_lazy('risk:vuln_detail', args=(self.object.id,))

class CondUpdateView(UpdateView):
    model = RiskCondition
    fields = ['name', 'desc', 'condition_type', 'pervasiveness',
            'info_source', 'tier']
    def get_success_url(self):
        return reverse_lazy('risk:cond_detail', args=(self.object.id,))

class ImpactUpdateView(UpdateView):
    model = Impact
    fields = ['name', 'desc', 'impact_type', 'info_source', 'tier',
            'severity', 'impact_tier']
    def get_success_url(self):
        return reverse_lazy('risk:impact_detail', args=(self.object.id,))

class ATEDeleteView(DeleteView):
    model = AdvThreatEvent
    template_name = 'risk/ate_delete.html'
    context_object_name = 'ate'
    def get_success_url(self):
        return reverse('risk:ate_index')

class NTEDeleteView(DeleteView):
    model = NonAdvThreatEvent
    template_name = 'risk/nte_delete.html'
    context_object_name = 'nte'
    def get_success_url(self):
        return reverse('risk:nte_index')

class ATSDeleteView(DeleteView):
    model = AdvThreatSource
    template_name = 'risk/ats_delete.html'
    context_object_name = 'ats'
    def get_success_url(self):
        return reverse('risk:ats_index')

class NTSDeleteView(DeleteView):
    model = NonAdvThreatSource
    template_name = 'risk/nts_delete.html'
    context_object_name = 'nts'
    def get_success_url(self):
        return reverse('risk:nts_index')

class VulnDeleteView(DeleteView):
    model = Vulnerability
    template_name = 'risk/vuln_delete.html'
    context_object_name = 'vuln'
    def get_success_url(self):
        return reverse('risk:vuln_index')

class CondDeleteView(DeleteView):
    model = RiskCondition
    template_name = 'risk/cond_delete.html'
    context_object_name = 'cond'
    def get_success_url(self):
        return reverse('risk:cond_index')

class ImpactDeleteView(DeleteView):
    model = Impact
    template_name = 'risk/impact_delete.html'
    context_object_name = 'impact'
    def get_success_url(self):
        return reverse('risk:impact_index')
