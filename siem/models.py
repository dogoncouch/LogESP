from django.db import models

from siem.choices import *

# Create your models here.

def validate_modifier_range(value):
    if not 0 < value <= 10:
        raise ValidationError('%s not in 0.1-10 range' % value)

class LogEvent(models.Model):
    parsed_at = models.DateTimeField(6,
            null=True, blank=True)
    time_zone = models.CharField(max_length=32,
            null=True, blank=True)
    eol_date = models.DateField()
    event_type = models.CharField(max_length=24, default='default')
    raw_text = models.CharField(max_length=1280)
    date_stamp = models.CharField(max_length=32,
            null=True, blank=True)
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
    ext_user = models.CharField(max_length=32,
            null=True, blank=True)
    ext_ip = models.CharField(max_length=32,
            null=True, blank=True)
    ext_session = models.CharField(max_length=24,
            null=True, blank=True)
    parsed_on = models.CharField(max_length=32,
            null=True, blank=True)
    source_path = models.CharField(max_length=200,
            null=True, blank=True)
    class Meta:
        permissions = (('view_logevent', 'Can view log events'),)


class LimitRule(models.Model):
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=200,
            null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    rule_events = models.BooleanField(default=False)
    rule_category = models.CharField(max_length=24, default='default')
    lifespan_days = models.IntegerField(null=True, blank=True)
    event_type = models.CharField(max_length=24, default='default')
    severity = models.IntegerField(choices=severity_choices)
    overkill_modifier = models.DecimalField(
            validators=[validate_modifier_range],
            decimal_places=1, max_digits=3, default=1)
    severity_modifier = models.DecimalField(
            validators=[validate_modifier_range],
            decimal_places=1, max_digits=3, default=1)
    time_int = models.IntegerField()
    event_limit = models.IntegerField()
    message_filter_regex = models.CharField(max_length=1024,
            null=True, blank=True)
    raw_text_filter_regex = models.CharField(max_length=1024,
            null=True, blank=True)
    source_host_filter = models.CharField(max_length=32,
            null=True, blank=True)
    process_filter = models.CharField(max_length=32,
            null=True, blank=True)
    rulename_filter = models.CharField(max_length=32,
            null=True, blank=True)
    magnitude_filter = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=1024)
    def __str__(self):
        return self.name
    class Meta:
        permissions = (('view_limitrule', 'Can view limit rules'),)


class RuleEvent(models.Model):
    date_stamp = models.DateTimeField()
    time_zone = models.CharField(max_length=32)
    eol_date = models.DateField()
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
    class Meta:
        permissions = (('view_ruleevent', 'Can view rule events'),)
