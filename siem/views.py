
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import LogEvent
from .models import RuleEvent
from .models import LimitRule
from .models import LogEventParser, ParseHelper

# Create your views here.

def index(request):
    return render(request, 'siem/index.html')

def event_index(request):
    return render(request, 'siem/event_index.html')

def help_index(request):
    return render(request, 'siem/help_index.html')

def parse_help(request):
    return render(request, 'siem/help_parse.html')

def rule_help(request):
    return render(request, 'siem/help_rules.html')

def event_help(request):
    return render(request, 'siem/help_event.html')

def daemon_help(request):
    return render(request, 'siem/help_daemons.html')

def regex_help(request):
    return render(request, 'siem/help_regex.html')

class LogEventSearchView(PermissionRequiredMixin, ListView):
    model = LogEvent
    permission_required = 'siem.view_logevent'
    template_name = 'siem/logevent_search.html'
    context_object_name = 'event_list'
    paginate_by = 50
    def get_queryset(self):
        log_source_val = self.request.GET.get('log_source_filter')
        process_val = self.request.GET.get('process_filter')
        source_host_val = self.request.GET.get('source_host_filter')
        source_port_val = self.request.GET.get('source_port_filter')
        dest_host_val = self.request.GET.get('dest_host_filter')
        dest_port_val = self.request.GET.get('dest_port_filter')
        source_user_val = self.request.GET.get('source_user_filter')
        target_user_val = self.request.GET.get('target_user_filter')
        action_val = self.request.GET.get('action_filter')
        command_val = self.request.GET.get('command_filter')
        session_val = self.request.GET.get('session_filter')
        interface_val = self.request.GET.get('interface_filter')
        status_val = self.request.GET.get('status_filter')
        path_val = self.request.GET.get('path_filter')
        parameters_val = self.request.GET.get('parameters_filter')
        referrer_val = self.request.GET.get('referrer_filter')
        type_val = self.request.GET.get('type_filter')
        message_val = self.request.GET.get('message_filter')
        raw_val = self.request.GET.get('raw_filter')
        starttime_val = self.request.GET.get('starttime_filter')
        endtime_val = self.request.GET.get('endtime_filter')
        if not type_val: type_val = ''
        if not log_source_val: log_source_val = ''
        if not process_val: process_val = ''
        if not source_host_val: source_host_val = ''
        if not source_port_val: source_port_val = ''
        if not dest_host_val: dest_host_val = ''
        if not dest_port_val: dest_port_val = ''
        if not source_user_val: source_user_val = ''
        if not target_user_val: target_user_val = ''
        if not action_val: action_val = ''
        if not command_val: command_val = ''
        if not session_val: session_val = ''
        if not interface_val: interface_val = ''
        if not status_val: status_val = ''
        if not path_val: path_val = ''
        if not parameters_val: parameters_val = ''
        if not referrer_val: referrer_val = ''
        if not message_val: message_val = ''
        if not raw_val: raw_val = ''
        if not starttime_val and not endtime_val:
            starttime_val = (timezone.localtime(timezone.now()) - \
                    timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        if endtime_val and starttime_val:
            new_context = LogEvent.objects.filter(
                parsed_at__gte=starttime_val,
                parsed_at__lte=endtime_val,
                event_type__iregex=type_val,
                log_source__iregex=log_source_val,
                source_process__iregex=process_val,
                source_host__iregex=source_host_val,
                source_port__iregex=source_port_val,
                dest_host__iregex=dest_host_val,
                dest_port__iregex=dest_port_val,
                source_user__iregex=source_user_val,
                target_user__iregex=target_user_val,
                action__iregex=action_val,
                command__iregex=command_val,
                sessionid__iregex=session_val,
                interface__iregex=interface_val,
                status__iregex=status_val,
                message__iregex=message_val,
                raw_text__iregex=raw_val).order_by('-id')
        elif endtime_val and not starttime_val:
            new_context = LogEvent.objects.filter(
                parsed_at__lte=endtime_val,
                event_type__iregex=type_val,
                log_source__iregex=log_source_val,
                source_process__iregex=process_val,
                source_host__iregex=source_host_val,
                source_port__iregex=source_port_val,
                dest_host__iregex=dest_host_val,
                dest_port__iregex=dest_port_val,
                source_user__iregex=source_user_val,
                target_user__iregex=target_user_val,
                action__iregex=action_val,
                command__iregex=command_val,
                sessionid__iregex=session_val,
                interface__iregex=interface_val,
                status__iregex=status_val,
                message__iregex=message_val,
                raw_text__iregex=raw_val).order_by('-id')
        else:
            new_context = LogEvent.objects.filter(
                parsed_at__gte=starttime_val,
                event_type__iregex=type_val,
                log_source__iregex=log_source_val,
                source_process__iregex=process_val,
                source_host__iregex=source_host_val,
                source_port__iregex=source_port_val,
                dest_host__iregex=dest_host_val,
                dest_port__iregex=dest_port_val,
                source_user__iregex=source_user_val,
                target_user__iregex=target_user_val,
                action__iregex=action_val,
                command__iregex=command_val,
                sessionid__iregex=session_val,
                interface__iregex=interface_val,
                status__iregex=status_val,
                message__iregex=message_val,
                raw_text__iregex=raw_val).order_by('-id')
        #else:
        #    new_context = LogEvent.objects.filter(
        #        event_type__iregex=type_val,
        #        log_source__iregex=log_source_val,
        #        source_process__iregex=process_val,
        #        source_host__iregex=source_host_val,
        #        source_port__iregex=source_port_val,
        #        dest_host__iregex=dest_host_val,
        #        dest_port__iregex=dest_port_val,
        #        source_user__iregex=source_user_val,
        #        target_user__iregex=target_user_val,
        #        action__iregex=action_val,
        #        command__iregex=command_val,
        #        sessionid__iregex=session_val,
        #        interface__iregex=interface_val,
        #        status__iregex=status_val,
        #        message__iregex=message_val,
        #        raw_text__iregex=raw_val).order_by('-id')
        return new_context
    def get_context_data(self, **kwargs):
        context = super(LogEventSearchView,self).get_context_data(**kwargs)
        context['log_source_filter'] = self.request.GET.get(
                'log_source_filter', '')
        context['process_filter'] = self.request.GET.get('process_filter', '')
        context['source_host_filter'] = self.request.GET.get(
                'source_host_filter', '')
        context['source_port_filter'] = self.request.GET.get(
                'source_port_filter', '')
        context['dest_host_filter'] = self.request.GET.get(
                'dest_host_filter', '')
        context['dest_port_filter'] = self.request.GET.get(
                'dest_port_filter', '')
        context['source_user_filter'] = self.request.GET.get(
                'source_user_filter', '')
        context['target_user_filter'] = self.request.GET.get(
                'target_user_filter', '')
        context['action_filter'] = self.request.GET.get(
                'action_filter', '')
        context['command_filter'] = self.request.GET.get(
                'command_filter', '')
        context['session_filter'] = self.request.GET.get(
                'session_filter', '')
        context['interface_filter'] = self.request.GET.get(
                'interface_filter', '')
        context['status_filter'] = self.request.GET.get(
                'status_filter', '')
        context['path_filter'] = self.request.GET.get(
                'path_filter', '')
        context['parameters_filter'] = self.request.GET.get(
                'parameters_filter', '')
        context['referrer_filter'] = self.request.GET.get(
                'referrer_filter', '')
        context['type_filter'] = self.request.GET.get(
                'type_filter', '')
        context['message_filter'] = self.request.GET.get(
                'message_filter', '')
        context['raw_filter'] = self.request.GET.get(
                'raw_filter', '')
        context['starttime_filter'] = self.request.GET.get(
                'starttime_filter', '')
        context['endtime_filter'] = self.request.GET.get(
                'endtime_filter', '')
        if not context['starttime_filter'] and \
                not context['endtime_filter']:
            context['starttime_filter'] = (
                    timezone.localtime(timezone.now()) - \
                    timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        context['order'] = 'desc'
        return context

class LogEventDetailView(PermissionRequiredMixin, DetailView):
    model = LogEvent
    permission_required = 'siem.view_logevent'
    template_name = 'siem/logevent_detail.html'
    context_object_name = 'event'

class RuleEventSearchView(PermissionRequiredMixin, ListView):
    model = RuleEvent
    permission_required = 'siem.view_ruleevent'
    template_name = 'siem/ruleevent_search.html'
    context_object_name = 'event_list'
    paginate_by = 20
    def get_queryset(self):
        category_val = self.request.GET.get('category_filter')
        type_val = self.request.GET.get('type_filter')
        mag_val = self.request.GET.get('mag_filter')
        message_val = self.request.GET.get('message_filter')
        starttime_val = self.request.GET.get('starttime_filter')
        endtime_val = self.request.GET.get('endtime_filter')
        if not category_val: category_val = ''
        if not type_val: type_val = ''
        if not mag_val: mag_val = 0
        if not message_val: message_val = ''
        if not starttime_val and not endtime_val:
            starttime_val = (timezone.localtime(timezone.now()) - \
                    timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        if starttime_val and endtime_val:
            new_context = RuleEvent.objects.filter(
                date_stamp__gte=starttime_val,
                date_stamp__lte=endtime_val,
                rule_category__iregex=category_val,
                event_type__iregex=type_val,
                magnitude__gte=mag_val,
                message__iregex=message_val).order_by('-id')
        elif endtime_val and not starttime_val:
            new_context = RuleEvent.objects.filter(
                date_stamp__lte=endtime_val,
                rule_category__iregex=category_val,
                event_type__iregex=type_val,
                magnitude__gte=mag_val,
                message__iregex=message_val).order_by('-id')
        else:
            new_context = RuleEvent.objects.filter(
                date_stamp__gte=starttime_val,
                rule_category__iregex=category_val,
                event_type__iregex=type_val,
                magnitude__gte=mag_val,
                message__iregex=message_val).order_by('-id')
        #else:
        #    new_context = RuleEvent.objects.filter(
        #        rule_category__iregex=category_val,
        #        event_type__iregex=type_val,
        #        magnitude__gte=mag_val,
        #        message__iregex=message_val).order_by('-id')
        return new_context
    def get_context_data(self, **kwargs):
        context = super(RuleEventSearchView,self).get_context_data(**kwargs)
        context['category_filter'] = self.request.GET.get('category_filter', '')
        context['type_filter'] = self.request.GET.get('type_filter', '')
        context['mag_filter'] = self.request.GET.get('mag_filter', '')
        context['message_filter'] = self.request.GET.get('message_filter', '')
        context['starttime_filter'] = self.request.GET.get(
                'starttime_filter', '')
        context['endtime_filter'] = self.request.GET.get(
                'endtime_filter', '')
        if not context['starttime_filter'] and \
                not context['endtime_filter']:
            context['starttime_filter'] = (
                    timezone.localtime(timezone.now()) - \
                    timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        return context

class RuleEventDetailView(PermissionRequiredMixin, DetailView):
    model = RuleEvent
    permission_required = 'siem.view_ruleevent'
    template_name = 'siem/ruleevent_detail.html'
    context_object_name = 'event'

class LRIndexView(PermissionRequiredMixin, ListView):
    model = LimitRule
    permission_required = 'siem.view_limitrule'
    template_name = 'siem/lr_index.html'
    context_object_name = 'lr_list'
    def get_queryset(self):
        return LimitRule.objects.order_by('is_builtin', 'is_enabled',
                'event_type', 'rule_events', 'name')

class LRDetailView(PermissionRequiredMixin, DetailView):
    model = LimitRule
    permission_required = 'siem.view_limitrule'
    template_name = 'siem/lr_detail.html'
    context_object_name = 'lr'

class LRCreateView(PermissionRequiredMixin, CreateView):
    model = LimitRule
    permission_required = 'siem.add_limitrule'
    fields = ['name', 'desc', 'is_enabled', 'rule_events',
            'reverse_logic', 'email_alerts', 'alert_users',
            'rule_category', 'event_type',
            'local_lifespan_days', 'backup_lifespan_days',
            'severity', 'overkill_modifier', 'severity_modifier',
            'time_int', 'event_limit', 'allowed_log_sources',
            'message_filter_regex', 'raw_text_filter_regex',
            'log_source_filter_regex', 'process_filter_regex',
            'action_filter_regex', 'command_filter_regex',
            'interface_filter_regex', 'status_filter_regex',
            'source_host_filter_regex', 'source_port_filter_regex',
            'dest_host_filter_regex', 'dest_port_filter_regex',
            'source_user_filter_regex', 'target_user_filter_regex',
            'path_filter_regex', 'parameters_filter_regex',
            'referrer_filter_regex',
            'rulename_filter_regex', 'magnitude_filter',
            'match_list_path', 'match_field',
            'match_allowlist',
            'message']
    def get_success_url(self):
        return reverse_lazy('siem:lr_detail', args=(self.object.id,))

class LRUpdateView(PermissionRequiredMixin, UpdateView):
    model = LimitRule
    permission_required = 'siem.change_limitrule'
    template_name = 'siem/limitrule_update_form.html'
    fields = ['name', 'desc', 'is_enabled', 'rule_events',
            'reverse_logic', 'email_alerts', 'alert_users',
            'rule_category', 'event_type',
            'local_lifespan_days', 'backup_lifespan_days',
            'severity', 'overkill_modifier', 'severity_modifier',
            'time_int', 'event_limit', 'allowed_log_sources',
            'message_filter_regex', 'raw_text_filter_regex',
            'log_source_filter_regex', 'process_filter_regex',
            'action_filter_regex', 'command_filter_regex',
            'interface_filter_regex', 'status_filter_regex',
            'source_host_filter_regex', 'source_port_filter_regex',
            'dest_host_filter_regex', 'dest_port_filter_regex',
            'source_user_filter_regex', 'target_user_filter_regex',
            'path_filter_regex', 'parameters_filter_regex',
            'referrer_filter_regex',
            'rulename_filter_regex', 'magnitude_filter',
            'match_list_path', 'match_field',
            'match_allowlist',
            'message']
    def get_success_url(self):
        return reverse_lazy('siem:lr_detail', args=(self.object.id,))

class LRDeleteView(PermissionRequiredMixin, DeleteView):
    model = LimitRule
    permission_required = 'siem.delete_limitrule'
    template_name = 'siem/lr_delete.html'
    context_object_name = 'lr'
    def get_success_url(self):
        return reverse('siem:lr_index')

class LPIndexView(PermissionRequiredMixin, ListView):
    model = LogEventParser
    permission_required = 'siem.view_logeventparser'
    template_name = 'siem/lp_index.html'
    context_object_name = 'lp_list'
    def get_queryset(self):
        return LogEventParser.objects.order_by('is_builtin', 'name')

class LPDetailView(PermissionRequiredMixin, DetailView):
    model = LogEventParser
    permission_required = 'siem.view_logeventparser'
    template_name = 'siem/lp_detail.html'
    context_object_name = 'lp'

class LPCreateView(PermissionRequiredMixin, CreateView):
    model = LogEventParser
    permission_required = 'siem.add_logeventparser'
    fields = ['name', 'desc', 'match_regex', 'fields',
            'backup_match_regex', 'backup_fields']
    def get_success_url(self):
        return reverse_lazy('siem:lp_detail', args=(self.object.id,))

class LPUpdateView(PermissionRequiredMixin, UpdateView):
    model = LogEventParser
    permission_required = 'siem.change_logeventparser'
    template_name = 'siem/logeventparser_update_form.html'
    fields = ['name', 'desc', 'match_regex', 'fields',
            'backup_match_regex', 'backup_fields']
    def get_success_url(self):
        return reverse_lazy('siem:lp_detail', args=(self.object.id,))

class LPDeleteView(PermissionRequiredMixin, DeleteView):
    model = LogEventParser
    permission_required = 'siem.delete_logeventparser'
    template_name = 'siem/lp_delete.html'
    context_object_name = 'lp'
    def get_success_url(self):
        return reverse('siem:lp_index')

class PHIndexView(PermissionRequiredMixin, ListView):
    model = ParseHelper
    permission_required = 'siem.view_logeventparser'
    template_name = 'siem/ph_index.html'
    context_object_name = 'ph_list'
    def get_queryset(self):
        return ParseHelper.objects.order_by('is_builtin',
                'helper_type', 'name')

class PHDetailView(PermissionRequiredMixin, DetailView):
    model = ParseHelper
    permission_required = 'siem.view_logeventparser'
    template_name = 'siem/ph_detail.html'
    context_object_name = 'ph'

class PHCreateView(PermissionRequiredMixin, CreateView):
    model = ParseHelper
    permission_required = 'siem.add_logeventparser'
    fields = ['name', 'desc', 'helper_type', 'match_regex', 'fields']
    def get_success_url(self):
        return reverse_lazy('siem:ph_detail', args=(self.object.id,))

class PHUpdateView(PermissionRequiredMixin, UpdateView):
    model = ParseHelper
    permission_required = 'siem.change_logeventparser'
    template_name = 'siem/parsehelper_update_form.html'
    fields = ['name', 'desc', 'helper_type', 'match_regex', 'fields']
    def get_success_url(self):
        return reverse_lazy('siem:ph_detail', args=(self.object.id,))

class PHDeleteView(PermissionRequiredMixin, DeleteView):
    model = ParseHelper
    permission_required = 'siem.delete_logeventparser'
    template_name = 'siem/ph_delete.html'
    context_object_name = 'ph'
    def get_success_url(self):
        return reverse('siem:ph_index')
