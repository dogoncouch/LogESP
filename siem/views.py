from django.shortcuts import render

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import LogEvent
from .models import RuleEvent
from .models import LimitRule

# Create your views here.

def index(request):
    return render(request, 'siem/index.html')

def event_index(request):
    return render(request, 'siem/event_index.html')

class LogEventSearchView(PermissionRequiredMixin, ListView):
    model = LogEvent
    permission_required = 'siem.view_logevent'
    template_name = 'siem/logevent_search.html'
    context_object_name = 'event_list'
    paginate_by = 50
    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        if filter_val and filter_val != '':
            new_context = LogEvent.objects.filter(
                raw_text__contains=filter_val,
            ).reverse()
            return new_context
        else:
            return LogEvent.objects.all().reverse()
    def get_context_data(self, **kwargs):
        context = super(LogEventSearchView,self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context

class LogEventDetailView(PermissionRequiredMixin, DetailView):
    model = LogEvent
    permission_required = 'siem.view_logeventrule'
    template_name = 'siem/logevent_detail.html'
    context_object_name = 'event'

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

class RuleEventDetailView(PermissionRequiredMixin, DetailView):
    model = RuleEvent
    permission_required = 'siem.view_ruleeventrule'
    template_name = 'siem/ruleevent_detail.html'
    context_object_name = 'event'

class LRIndexView(PermissionRequiredMixin, ListView):
    model = LimitRule
    permission_required = 'siem.view_limitrule'
    template_name = 'siem/lr_index.html'
    context_object_name = 'lr_list'

class LRDetailView(PermissionRequiredMixin, DetailView):
    model = LimitRule
    permission_required = 'siem.view_limitrule'
    template_name = 'siem/lr_detail.html'
    context_object_name = 'lr'

class LRCreateView(PermissionRequiredMixin, CreateView):
    model = LimitRule
    permission_required = 'siem.add_limitrule'
    fields = ['name', 'is_enabled', 'severity', 'time_int', 'event_limit',
            'sql_query', 'source_table', 'out_table', 'message']
    def get_success_url(self):
        return reverse_lazy('siem/lr_detail', args=(self.object.id,))

class LRUpdateView(PermissionRequiredMixin, UpdateView):
    model = LimitRule
    permission_required = 'siem.change_limitrule'
    fields = ['name', 'is_enabled', 'severity', 'time_int', 'event_limit',
            'sql_query', 'source_table', 'out_table', 'message']
    def get_success_url(self):
        return reverse_lazy('siem/lr_detail', args=(self.object.id,))

class LRDeleteView(PermissionRequiredMixin, DeleteView):
    model = LimitRule
    permission_required = 'siem.delete_limitrule'
    template_name = 'siem/lr_delete.html'
    context_object_name = 'lr'
    def get_success_url(self):
        return reverse('siem:lr_index')
