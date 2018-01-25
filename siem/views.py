from django.shortcuts import render

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import DefaultEvent
from .models import AuthEvent
from .models import RuleEvent
from .models import LimitRule
from .models import ParseHelper

# Create your views here.

def index(request):
    return render(request, 'siem/index.html')

def event_index(request):
    return render(request, 'siem/event_index.html')

class DefaultEventSearchView(PermissionRequiredMixin, ListView):
    model = DefaultEvent
    permission_required = 'siem.view_defaultevent'
    template_name = 'siem/defaultevent_search.html'
    context_object_name = 'event_list'
    paginate_by = 50
    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        if filter_val and filter_val != '':
            new_context = DefaultEvent.objects.filter(
                raw_text__contains=filter_val,
            ).reverse()
            return new_context
        else:
            return DefaultEvent.objects.all().reverse()
    def get_context_data(self, **kwargs):
        context = super(DefaultEventSearchView,self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context

class AuthEventSearchView(PermissionRequiredMixin, ListView):
    model = AuthEvent
    permission_required = 'siem.view_authevent'
    template_name = 'siem/authevent_search.html'
    context_object_name = 'event_list'
    paginate_by = 50
    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        if filter_val and filter_val != '':
            new_context = AuthEvent.objects.filter(
                raw_text__contains=filter_val,
            ).reverse()
            return new_context
        else:
            return AuthEvent.objects.all().reverse()
    def get_context_data(self, **kwargs):
        context = super(AuthEventSearchView,self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context

class RuleEventSearchView(PermissionRequiredMixin, ListView):
    model = RuleEvent
    permission_required = 'siem.view_ruleevent'
    template_name = 'siem/ruleevent_search.html'
    context_object_name = 'event_list'
    paginate_by = 50
    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        if filter_val and filter_val != '':
            new_context = RuleEvent.objects.filter(
                raw_text__contains=filter_val,
            ).reverse()
            return new_context
        else:
            return RuleEvent.objects.all().reverse()
    def get_context_data(self, **kwargs):
        context = super(RuleEventSearchView,self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context

class LRIndexView(PermissionRequiredMixin, ListView):
    model = LimitRule
    permission_required = 'siem.view_limitrule'
    template_name = 'siem/lr_index.html'
    context_object_name = 'lr_list'

class PHIndexView(PermissionRequiredMixin, ListView):
    model = ParseHelper
    permission_required = 'siem.view_parsehelper'
    template_name = 'siem/ph_index.html'
    context_object_name = 'ph_list'

class LRDetailView(PermissionRequiredMixin, DetailView):
    model = LimitRule
    permission_required = 'siem.view_limitrule'
    template_name = 'siem/lr_detail.html'
    context_object_name = 'lr'

class PHDetailView(PermissionRequiredMixin, DetailView):
    model = ParseHelper
    permission_required = 'siem.view_parsehelper'
    template_name = 'siem/ph_detail.html'
    context_object_name = 'ph'

class LRCreateView(PermissionRequiredMixin, CreateView):
    model = LimitRule
    permission_required = 'siem.add_limitrule'
    fields = ['name', 'is_enabled', 'severity', 'time_int', 'event_limit',
            'sql_query', 'source_table', 'out_table', 'message']
    def get_success_url(self):
        return reverse_lazy('siem/lr_detail', args=(self.object.id,))

class PHCreateView(PermissionRequiredMixin, CreateView):
    model = ParseHelper
    permission_required = 'siem.add_parsehelper'
    fields = ['name', 'var_name', 'reg_exp']
    def get_success_url(self):
        return reverse_lazy('siem/ph_detail', args=(self.object.id,))

class LRUpdateView(PermissionRequiredMixin, UpdateView):
    model = LimitRule
    permission_required = 'siem.change_limitrule'
    fields = ['name', 'is_enabled', 'severity', 'time_int', 'event_limit',
            'sql_query', 'source_table', 'out_table', 'message']
    def get_success_url(self):
        return reverse_lazy('siem/lr_detail', args=(self.object.id,))

class PHUpdateView(PermissionRequiredMixin, UpdateView):
    model = ParseHelper
    permission_required = 'siem.change_parsehelper'
    fields = ['name', 'var_name', 'reg_exp']
    def get_success_url(self):
        return reverse_lazy('siem/ph_detail', args=(self.object.id,))

class LRDeleteView(PermissionRequiredMixin, DeleteView):
    model = LimitRule
    permission_required = 'siem.delete_limitrule'
    template_name = 'siem/lr_delete.html'
    context_object_name = 'lr'
    def get_success_url(self):
        return reverse('siem:lr_index')

class PHDeleteView(PermissionRequiredMixin, DeleteView):
    model = ParseHelper
    permission_required = 'siem.delete_parsehelper'
    template_name = 'siem/ph_delete.html'
    context_object_name = 'ph'
    def get_success_url(self):
        return reverse('siem:ph_index')
