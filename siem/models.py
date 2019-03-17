from django.db import models
from django.contrib.auth.models import User

from siem.choices import *

# Create your models here.

def validate_modifier_range(value):
    if not 0 < value <= 10:
        raise ValidationError('%s not in 0.1-10 range' % value)

class LogEventParser(models.Model):
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=200, null=True, blank=True)
    is_builtin = models.BooleanField(default=False, blank=True)
    match_regex = models.CharField(max_length=1024)
    backup_match_regex = models.CharField(max_length=1024,
            null=True, blank=True)
    fields = models.CharField(max_length=512)
    backup_fields = models.CharField(max_length=512,
            null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        #permissions = (('view_logeventparser', 'Can view log event parsers'),)
        unique_together = ('name', 'is_builtin')

class ParseHelper(models.Model):
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=200, null=True, blank=True)
    is_builtin = models.BooleanField(default=False, blank=True)
    helper_type = models.CharField(max_length=32)
    match_regex = models.CharField(max_length=1024)
    fields = models.CharField(max_length=512)
    def __str__(self):
        return self.name
    class Meta:
        #permissions = (('view_logeventparser', 'Can view log event parsers'),)
        unique_together = ('name', 'is_builtin')

class LogEvent(models.Model):
    parsed_at = models.DateTimeField(6, auto_now_add=True, db_index=True)
    time_zone = models.CharField(max_length=32,
            null=True, blank=True)
    eol_date_local = models.DateField(db_index=True)
    eol_date_backup = models.DateField(db_index=True)
    event_type = models.CharField(max_length=24, default='default')
    raw_text = models.CharField(max_length=1280)
    date_stamp = models.CharField(max_length=32,
            null=True, blank=True)
    log_source = models.CharField(max_length=32, default='')
    facility = models.IntegerField(choices=facility_choices,
            null=True, blank=True)
    severity = models.IntegerField(choices=severity_choices,
            null=True, blank=True)
    aggregated_events = models.IntegerField(default=1)
    source_host = models.CharField(max_length=32, default='')
    source_port = models.CharField(max_length=8, default='')
    dest_host = models.CharField(max_length=32, default='')
    dest_port = models.CharField(max_length=8, default='')
    source_process = models.CharField(max_length=24, default='')
    source_pid = models.IntegerField(
            null=True, blank=True)
    action = models.CharField(max_length=48, default='')
    command = models.CharField(max_length=64, default='')
    protocol = models.CharField(max_length=12, default='')
    packet_count = models.IntegerField(null=True, blank=True)
    byte_count = models.IntegerField(null=True, blank=True)
    tcp_flags = models.IntegerField(null=True, blank=True)
    class_of_service = models.IntegerField(null=True, blank=True)
    interface = models.CharField(max_length=32, default='')
    status = models.CharField(max_length=24, default='')
    start_time = models.CharField(max_length=32, null=True, blank=True)
    duration = models.CharField(max_length=32, null=True, blank=True)
    source_user = models.CharField(max_length=32, default='')
    target_user = models.CharField(max_length=32, default='')
    sessionid = models.CharField(max_length=24, default='')
    path = models.CharField(max_length=384, default='')
    parameters = models.CharField(max_length=384, default='')
    referrer = models.CharField(max_length=400, default='')
    message = models.CharField(max_length=1024, default='')
    ext0 = models.CharField(max_length=192, default='')
    ext1 = models.CharField(max_length=192, default='')
    ext2 = models.CharField(max_length=45, default='')
    ext3 = models.CharField(max_length=45, default='')
    ext4 = models.CharField(max_length=45, default='')
    ext5 = models.CharField(max_length=45, default='')
    ext6 = models.CharField(max_length=45, default='')
    ext7 = models.CharField(max_length=45, default='')
    parsed_on = models.CharField(max_length=32)
    source_path = models.CharField(max_length=200,)
    #class Meta:
        #permissions = (('view_logevent', 'Can view log events'),)


class LimitRule(models.Model):
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=200,
            null=True, blank=True)
    is_builtin = models.BooleanField(default=False, blank=True)
    is_enabled = models.BooleanField(default=True)
    reverse_logic = models.BooleanField(default=False)
    email_alerts = models.BooleanField(default=False)
    alert_users = models.ManyToManyField(User,
            related_name='alert_rules', blank=True)
    rule_events = models.BooleanField(default=False)
    rule_category = models.CharField(max_length=24, default='default')
    local_lifespan_days = models.IntegerField(default=185)
    backup_lifespan_days = models.IntegerField(default=366)
    event_type = models.CharField(max_length=24,
            null=True, blank=True)
    severity = models.IntegerField(choices=severity_choices)
    overkill_modifier = models.DecimalField(
            validators=[validate_modifier_range],
            decimal_places=1, max_digits=3, default=1)
    severity_modifier = models.DecimalField(
            validators=[validate_modifier_range],
            decimal_places=1, max_digits=3, default=1)
    time_int = models.IntegerField(default=5)
    event_limit = models.IntegerField(default=0)
    allowed_log_sources = models.IntegerField(default=0)
    message_filter_regex = models.CharField(max_length=1024,
            null=True, blank=True)
    raw_text_filter_regex = models.CharField(max_length=1024,
            null=True, blank=True)
    log_source_filter_regex = models.CharField(max_length=32,
            null=True, blank=True)
    process_filter_regex = models.CharField(max_length=24,
            null=True, blank=True)
    action_filter_regex = models.CharField(max_length=48,
            null=True, blank=True)
    interface_filter_regex = models.CharField(max_length=32,
            null=True, blank=True)
    status_filter_regex = models.CharField(max_length=24,
            null=True, blank=True)
    source_host_filter_regex = models.CharField(max_length=32,
            null=True, blank=True)
    source_port_filter_regex = models.CharField(max_length=8,
            null=True, blank=True)
    dest_host_filter_regex = models.CharField(max_length=32,
            null=True, blank=True)
    dest_port_filter_regex = models.CharField(max_length=8,
            null=True, blank=True)
    source_user_filter_regex = models.CharField(max_length=32,
            null=True, blank=True)
    target_user_filter_regex = models.CharField(max_length=32,
            null=True, blank=True)
    command_filter_regex = models.CharField(max_length=64,
            null=True, blank=True)
    path_filter_regex = models.CharField(max_length=128, default='',
            null=True, blank=True)
    parameters_filter_regex = models.CharField(max_length=128, default='',
            null=True, blank=True)
    referrer_filter_regex = models.CharField(max_length=128, default='',
            null=True, blank=True)
    rulename_filter_regex = models.CharField(max_length=32,
            null=True, blank=True)
    magnitude_filter = models.IntegerField(null=True, blank=True)
    match_list_path = models.CharField(max_length=64,
            null=True, blank=True)
    match_field = models.CharField(max_length=32,
            null=True, blank=True)
    match_allowlist = models.BooleanField(default=False)
    message = models.CharField(max_length=1024)
    def __str__(self):
        return self.name
    class Meta:
        #permissions = (('view_limitrule', 'Can view limit rules'),)
        unique_together = ('name', 'is_builtin')


class RuleEvent(models.Model):
    date_stamp = models.DateTimeField(auto_now_add=True, db_index=True)
    time_zone = models.CharField(max_length=32)
    eol_date_local = models.DateField()
    eol_date_backup = models.DateField()
    rule_category = models.CharField(max_length=24, default='default')
    event_type = models.CharField(max_length=24, default='default')
    source_rule = models.ForeignKey(LimitRule,
            related_name='triggered_events',
            on_delete=models.PROTECT)
    severity = models.IntegerField(choices=severity_choices)
    event_limit = models.IntegerField()
    event_count = models.IntegerField()
    magnitude = models.IntegerField()
    time_int = models.IntegerField()
    message = models.CharField(max_length=1024)
    source_ids_log = models.ManyToManyField(LogEvent,
            related_name='rules_triggered',
            blank=True)
    source_ids_rule = models.ManyToManyField('self',
            related_name='rules_triggered',
            blank=True, symmetrical=False)
    log_source_count = models.IntegerField(
            null=True, blank=True)
    source_host_count = models.IntegerField(
            null=True, blank=True)
    dest_host_count = models.IntegerField(
            null=True, blank=True)
    #class Meta:
        #permissions = (('view_ruleevent', 'Can view rule events'),)
