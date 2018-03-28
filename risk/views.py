from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import AdvThreatEvent, NonAdvThreatEvent
from .models import AdvThreatSource, NonAdvThreatSource
from .models import Vulnerability, RiskCondition
from .models import Impact, RiskResponse

# Create your views here.

def index(request):
    return render(request, 'risk/index.html')

def at_index(request):
    return render(request, 'risk/at_index.html')

def nt_index(request):
    return render(request, 'risk/nt_index.html')

def help_index(request):
    return render(request, 'risk/help_index.html')

def help_adv_threat(request):
    return render(request, 'risk/help_adv_threat.html')

def help_nonadv_threat(request):
    return render(request, 'risk/help_nonadv_threat.html')

class ATEIndexView(ListView):
    model = AdvThreatEvent
    template_name = 'risk/ate_index.html'
    context_object_name = 'ate_list'
    permission_required = 'risk.view_advthreatevent'
    def get_queryset(self):
        return AdvThreatEvent.objects.order_by('-assigned_risk')

class NTEIndexView(ListView):
    model = NonAdvThreatEvent
    template_name = 'risk/nte_index.html'
    context_object_name = 'nte_list'
    permission_required = 'risk.view_nonadvthreatevent'
    def get_queryset(self):
        return NonAdvThreatEvent.objects.order_by('-assigned_risk')

class ATSIndexView(ListView):
    model = AdvThreatSource
    template_name = 'risk/ats_index.html'
    context_object_name = 'ats_list'
    permission_required = 'risk.view_advthreatsource'

class NTSIndexView(ListView):
    model = NonAdvThreatSource
    template_name = 'risk/nts_index.html'
    context_object_name = 'nts_list'
    permission_required = 'risk.view_nonadvthreatsource'

class VulnIndexView(ListView):
    model = Vulnerability
    template_name = 'risk/vuln_index.html'
    context_object_name = 'vuln_list'
    permission_required = 'risk.view_vulnerability'

class CondIndexView(ListView):
    model = RiskCondition
    template_name = 'risk/cond_index.html'
    context_object_name = 'cond_list'
    permission_required = 'risk.view_riskcondition'

class ImpactIndexView(ListView):
    model = Impact
    template_name = 'risk/impact_index.html'
    context_object_name = 'impact_list'
    permission_required = 'risk.view_impact'

class ResponseIndexView(ListView):
    model = RiskResponse
    template_name = 'risk/response_index.html'
    context_object_name = 'response_list'
    permission_required = 'risk.view_riskresponse'

class ATEDetailView(DetailView):
    model = AdvThreatEvent
    template_name = 'risk/ate_detail.html'
    context_object_name = 'ate'
    permission_required = 'risk.view_advthreatevent'

class NTEDetailView(DetailView):
    model = NonAdvThreatEvent
    template_name = 'risk/nte_detail.html'
    context_object_name = 'nte'
    permission_required = 'risk.view_nonadvthreatevent'

class ATSDetailView(DetailView):
    model = AdvThreatSource
    template_name = 'risk/ats_detail.html'
    context_object_name = 'ats'
    permission_required = 'risk.view_advthreatsource'

class NTSDetailView(DetailView):
    model = NonAdvThreatSource
    template_name = 'risk/nts_detail.html'
    context_object_name = 'nts'
    permission_required = 'risk.view_nonadvthreatsource'

class VulnDetailView(DetailView):
    model = Vulnerability
    template_name = 'risk/vuln_detail.html'
    context_object_name = 'vuln'
    permission_required = 'risk.view_vulnerability'

class CondDetailView(DetailView):
    model = RiskCondition
    template_name = 'risk/cond_detail.html'
    context_object_name = 'cond'
    permission_required = 'risk.view_riskcondition'

class ImpactDetailView(DetailView):
    model = Impact
    template_name = 'risk/impact_detail.html'
    context_object_name = 'impact'
    permission_required = 'risk.view_impact'

class ResponseDetailView(DetailView):
    model = RiskResponse
    template_name = 'risk/response_detail.html'
    context_object_name = 'response'
    permission_required = 'risk.view_riskresponse'

class ATECreateView(PermissionRequiredMixin, CreateView):
    model = AdvThreatEvent
    permission_required = 'risk.add_advthreatevent'
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact', 'vulnerabilities', 'impacts',
            'responses', 'assigned_risk']
    def get_success_url(self):
        return reverse_lazy('risk:ate_detail', args=(self.object.id,))

class NTECreateView(PermissionRequiredMixin, CreateView):
    model = NonAdvThreatEvent
    permission_required = 'risk.add_nonadvthreatevent'
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact', 'risk_conditions', 'impacts',
            'responses', 'assigned_risk']
    def get_success_url(self):
        return reverse_lazy('risk:nte_detail', args=(self.object.id,))

class ATSCreateView(PermissionRequiredMixin, CreateView):
    model = AdvThreatSource
    permission_required = 'risk.add_advthreatsource'
    fields = ['name', 'desc', 'source_type', 'info_source', 'tier',
            'in_scope', 'capability', 'intent', 'targeting']
    def get_success_url(self):
        return reverse_lazy('risk:ats_detail', args=(self.object.id,))

class NTSCreateView(PermissionRequiredMixin, CreateView):
    model = NonAdvThreatSource
    permission_required = 'risk.add_nonadvthreatsource'
    fields = ['name', 'desc', 'source_type', 'info_source', 'tier',
            'in_scope', 'range_of_effect']
    def get_success_url(self):
        return reverse_lazy('risk:nts_detail', args=(self.object.id,))

class VulnCreateView(PermissionRequiredMixin, CreateView):
    model = Vulnerability
    permission_required = 'risk.add_vulnerability'
    fields = ['name', 'desc', 'vuln_type', 'severity',
            'info_source', 'tier']
    def get_success_url(self):
        return reverse_lazy('risk:vuln_detail', args=(self.object.id,))

class CondCreateView(PermissionRequiredMixin, CreateView):
    model = RiskCondition
    permission_required = 'risk.add_riskcondition'
    fields = ['name', 'desc', 'condition_type', 'pervasiveness',
            'info_source', 'tier']
    def get_success_url(self):
        return reverse_lazy('risk:cond_detail', args=(self.object.id,))

class ImpactCreateView(PermissionRequiredMixin, CreateView):
    model = Impact
    permission_required = 'risk.add_impact'
    fields = ['name', 'desc', 'impact_type', 'info_source', 'tier',
            'severity', 'impact_tier']
    def get_success_url(self):
        return reverse_lazy('risk:impact_detail', args=(self.object.id,))

class ResponseCreateView(PermissionRequiredMixin, CreateView):
    model = RiskResponse
    permission_required = 'risk.add_riskresponse'
    fields = ['name', 'desc', 'response_type', 'effectiveness', 'status']
    def get_success_url(self):
        return reverse_lazy('risk:response_detail', args=(self.object.id,))

class ATEUpdateView(PermissionRequiredMixin, UpdateView):
    model = AdvThreatEvent
    permission_required = 'change_advthreatevent'
    template_name = 'risk/advthreatevent_update_form.html'
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact', 'vulnerabilities', 'impacts',
            'responses', 'assigned_risk']
    def get_success_url(self):
        return reverse_lazy('risk:ate_detail', args=(self.object.id,))

class NTEUpdateView(PermissionRequiredMixin, UpdateView):
    model = NonAdvThreatEvent
    permission_required = 'change_nonadvthreatevent'
    template_name = 'risk/nonadvthreatevent_update_form.html'
    fields = ['name', 'desc', 'event_type', 'sources', 'relevance',
            'info_source', 'tier', 'likelihood_initiation', 
            'likelihood_impact', 'risk_conditions', 'impacts',
            'responses', 'assigned_risk']
    def get_success_url(self):
        return reverse_lazy('risk:nte_detail', args=(self.object.id,))

class ATSUpdateView(PermissionRequiredMixin, UpdateView):
    model = AdvThreatSource
    permission_required = 'change_advthreatsource'
    template_name = 'risk/advthreatsource_update_form.html'
    fields = ['name', 'desc', 'source_type', 'info_source', 'tier',
            'in_scope', 'capability', 'intent', 'targeting']
    def get_success_url(self):
        return reverse_lazy('risk:ats_detail', args=(self.object.id,))

class NTSUpdateView(PermissionRequiredMixin, UpdateView):
    model = NonAdvThreatSource
    permission_required = 'change_nonadvthreatsource'
    template_name = 'risk/nonadvthreatsource_update_form.html'
    fields = ['name', 'desc', 'source_type', 'info_source', 'tier',
            'in_scope', 'range_of_effect']
    def get_success_url(self):
        return reverse_lazy('risk:nts_detail', args=(self.object.id,))

class VulnUpdateView(PermissionRequiredMixin, UpdateView):
    model = Vulnerability
    permission_required = 'change_vulnerability'
    template_name = 'risk/vulnerability_update_form.html'
    fields = ['name', 'desc', 'vuln_type', 'severity',
            'info_source', 'tier']
    def get_success_url(self):
        return reverse_lazy('risk:vuln_detail', args=(self.object.id,))

class CondUpdateView(PermissionRequiredMixin, UpdateView):
    model = RiskCondition
    permission_required = 'change_riskconditions'
    template_name = 'risk/riskcondition_update_form.html'
    fields = ['name', 'desc', 'condition_type', 'pervasiveness',
            'info_source', 'tier']
    def get_success_url(self):
        return reverse_lazy('risk:cond_detail', args=(self.object.id,))

class ImpactUpdateView(PermissionRequiredMixin, UpdateView):
    model = Impact
    permission_required = 'change_impact'
    template_name = 'risk/impact_update_form.html'
    fields = ['name', 'desc', 'impact_type', 'info_source', 'tier',
            'severity', 'impact_tier']
    def get_success_url(self):
        return reverse_lazy('risk:impact_detail', args=(self.object.id,))

class ResponseUpdateView(PermissionRequiredMixin, UpdateView):
    model = RiskResponse
    permission_required = 'change_riskresponse'
    template_name = 'risk/riskresponse_update_form.html'
    fields = ['name', 'desc', 'response_type', 'effectiveness', 'status']
    def get_success_url(self):
        return reverse_lazy('risk:response_detail', args=(self.object.id,))

class ATEDeleteView(PermissionRequiredMixin, DeleteView):
    model = AdvThreatEvent
    permission_required = 'delete_advthreatevent'
    template_name = 'risk/ate_delete.html'
    context_object_name = 'ate'
    def get_success_url(self):
        return reverse('risk:ate_index')

class NTEDeleteView(PermissionRequiredMixin, DeleteView):
    model = NonAdvThreatEvent
    permission_required = 'delete_nonadvthreatevent'
    template_name = 'risk/nte_delete.html'
    context_object_name = 'nte'
    def get_success_url(self):
        return reverse('risk:nte_index')

class ATSDeleteView(PermissionRequiredMixin, DeleteView):
    model = AdvThreatSource
    permission_required = 'delete_advthreatsource'
    template_name = 'risk/ats_delete.html'
    context_object_name = 'ats'
    def get_success_url(self):
        return reverse('risk:ats_index')

class NTSDeleteView(PermissionRequiredMixin, DeleteView):
    model = NonAdvThreatSource
    permission_required = 'delete_nonadvthreatsource'
    template_name = 'risk/nts_delete.html'
    context_object_name = 'nts'
    def get_success_url(self):
        return reverse('risk:nts_index')

class VulnDeleteView(PermissionRequiredMixin, DeleteView):
    model = Vulnerability
    permission_required = 'delete_vulnerability'
    template_name = 'risk/vuln_delete.html'
    context_object_name = 'vuln'
    def get_success_url(self):
        return reverse('risk:vuln_index')

class CondDeleteView(PermissionRequiredMixin, DeleteView):
    model = RiskCondition
    permission_required = 'delete_riskcondition'
    template_name = 'risk/cond_delete.html'
    context_object_name = 'cond'
    def get_success_url(self):
        return reverse('risk:cond_index')

class ImpactDeleteView(PermissionRequiredMixin, DeleteView):
    model = Impact
    permission_required = 'delete_impact'
    template_name = 'risk/impact_delete.html'
    context_object_name = 'impact'
    def get_success_url(self):
        return reverse('risk:impact_index')

class ResponseDeleteView(PermissionRequiredMixin, DeleteView):
    model = RiskResponse
    permission_required = 'delete_riskresponse'
    template_name = 'risk/response_delete.html'
    context_object_name = 'response'
    def get_success_url(self):
        return reverse('risk:response_index')
