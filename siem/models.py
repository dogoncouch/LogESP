from django.db import models

from siem.choices import *

# Create your models here.

class LogEvent(models.Model):
    parsed_at = models.DateTimeField(6,
            null=True, blank=True)
    date_stamp = models.CharField(max_length=32,
            null=True, blank=True)
    time_zone = models.CharField(max_length=32,
            null=True, blank=True)
    event_type = models.CharField(max_length=24, default='default')
    raw_text = models.CharField(max_length=1280)
    facility = models.IntegerField(choices=facility_choices,
            null=True, blank=True)
    severity = models.IntegerField(choices=severity_choices,
            null=True, blank=True)
    source_host = models.CharField(max_length=32,
            null=True, blank=True)
    source_port = models.CharField(max_length=8,
            null=True, blank=True)
    dest_host = models.CharField(max_length=32,
            null=True, blank=True)
    dest_port = models.CharField(max_length=8,
            null=True, blank=True)
    source_process = models.CharField(max_length=24,
            null=True, blank=True)
    source_pid = models.IntegerField(
            null=True, blank=True)
    protocol = models.CharField(max_length=12,
            null=True, blank=True)
    message = models.CharField(max_length=1024,
            null=True, blank=True)
    extended = models.CharField(max_length=1024,
            null=True, blank=True)
    parsed_on = models.CharField(max_length=32,
            null=True, blank=True)
    source_path = models.CharField(max_length=200,
            null=True, blank=True)
    class Meta:
        permissions = (('view_logevent', 'Can view default events'),)

class RuleEvent(models.Model):
    date_stamp = models.DateTimeField('date stamp')
    time_zone = models.CharField(max_length=32)
    rule_category = models.CharField(max_length=24, default='default')
    event_type = models.CharField(max_length=24, default='default')
    source_rule = models.CharField(max_length=32)
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
    class Meta:
        permissions = (('view_ruleevent', 'Can view rule events'),)

    
class LimitRule(models.Model):
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=200,
            null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    rule_events = models.BooleanField(default=False)
    rule_category = models.CharField(max_length=24, default='default')
    event_type = models.CharField(max_length=24, default='default')
    severity = models.IntegerField(choices=severity_choices)
    time_int = models.IntegerField()
    event_limit = models.IntegerField()
    message_filter = models.CharField(max_length=1024,
            null=True, blank=True)
    host_filter = models.CharField(max_length=32,
            null=True, blank=True)
    rulename_filter = models.CharField(max_length=32,
            null=True, blank=True)
    message = models.CharField(max_length=1024)
    def __str__(self):
        return self.name
    class Meta:
        permissions = (('view_limitrule', 'Can view limit rules'),)
