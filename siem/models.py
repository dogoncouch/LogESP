from django.db import models

from siem.choices import *

# Create your models here.

class DefaultEvent(models.Model):
    date_stamp = models.DateTimeField('date stamp',
            null=True, blank=True)
    date_stamp_utc = models.DateTimeField('utc date stamp',
            null=True, blank=True)
    time_zone = models.CharField(max_length=5,
            null=True, blank=True)
    raw_text = models.CharField(max_length=1280)
    facility = models.IntegerField(choices=facility_choices,
            null=True, blank=True)
    severity = models.IntegerField(choices=severity_choices,
            null=True, blank=True)
    source_host = models.CharField(max_length=32,
            null=True, blank=True)
    source_port = models.IntegerField(
            null=True, blank=True)
    dest_host = models.CharField(max_length=32,
            null=True, blank=True)
    dest_port = models.IntegerField(
            null=True, blank=True)
    source_process = models.IntegerField(
            null=True, blank=True)
    source_pid = models.IntegerField(
            null=True, blank=True)
    protocol = models.CharField(max_length=12,
            null=True, blank=True)
    message = models.CharField(max_length=1024,
            null=True, blank=True)
    extended = models.CharField(max_length=1000,
            null=True, blank=True)
    parsed_on = models.CharField(max_length=32,
            null=True, blank=True)
    source_path = models.CharField(max_length=200,
            null=True, blank=True)

class AuthEvent(models.Model):
    date_stamp = models.DateTimeField('date stamp',
            null=True, blank=True)
    date_stamp_utc = models.DateTimeField('utc date stamp',
            null=True, blank=True)
    time_zone = models.CharField(max_length=5,
            null=True, blank=True)
    raw_text = models.CharField(max_length=1280)
    facility = models.IntegerField(choices=facility_choices,
            null=True, blank=True)
    severity = models.IntegerField(choices=severity_choices,
            null=True, blank=True)
    source_host = models.CharField(max_length=32,
            null=True, blank=True)
    source_port = models.IntegerField(
            null=True, blank=True)
    dest_host = models.CharField(max_length=32,
            null=True, blank=True)
    dest_port = models.IntegerField(
            null=True, blank=True)
    source_process = models.IntegerField(
            null=True, blank=True)
    source_pid = models.IntegerField(
            null=True, blank=True)
    protocol = models.CharField(max_length=12,
            null=True, blank=True)
    message = models.CharField(max_length=1024,
            null=True, blank=True)
    extended = models.CharField(max_length=1000,
            null=True, blank=True)
    parsed_on = models.CharField(max_length=32,
            null=True, blank=True)
    source_path = models.CharField(max_length=200,
            null=True, blank=True)

class RuleEvent(models.Model):
    date_stamp = models.DateTimeField('date stamp')
    date_stamp_utc = models.DateTimeField('utc date stamp')
    time_zone = models.CharField(max_length=5)
    source_rule = models.CharField(max_length=32)
    severity = models.IntegerField(choices=severity_choices)
    event_limit = models.IntegerField()
    event_count = models.IntegerField()
    magnitude = models.IntegerField()
    time_int = models.IntegerField()
    message = models.CharField(max_length=1024)
    source_ids_def = models.ManyToManyField(DefaultEvent,
            related_name='rules_triggered',
            blank=True, symmetrical=False)
    source_ids_auth = models.ManyToManyField(AuthEvent,
            related_name='rules_triggered',
            blank=True, symmetrical=False)
    source_ids_rule = models.ManyToManyField('self',
            related_name='rules_triggered',
            blank=True, symmetrical=False)

    
class LimitRule(models.Model):
    name = models.CharField(max_length=32)
    is_enabled = models.BooleanField(default=True)
    severity = models.IntegerField(choices=severity_choices)
    time_int = models.IntegerField()
    event_limit = models.IntegerField()
    sql_query = models.CharField(max_length=1024)
    source_table = models.CharField(max_length=32) # To Do: point to table
    out_table = models.CharField(max_length=32) # To Do:
    message = models.CharField(max_length=1024)

class ParseHelper(models.Model):
    name = charField(max_length=32)
    var_name = CharField(max_length=24)
    reg_ext = CharField(max_length=200)
