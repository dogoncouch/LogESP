#!/usr/bin/env python

# MIT License
# 
# Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from time import sleep
from datetime import timedelta
from random import randrange
import json
import threading
import os
import syslog
from sys import exit
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from ldsi.settings import TIME_ZONE
try:
    from ldsi.settings import EMAIL_ALERT_FROM_ADDRESS
except ImportError:
    EMAIL_ALERT_FROM_ADDRESS = 'noreply@example.com'
from siem.models import LogEvent, RuleEvent, LimitRule


class SiemSentry:

    def __init__(self, rule):
        """Initialize trigger object"""
        self.rule = rule
        self.tzone = TIME_ZONE
        self.lasteventid = None
        self.justfired = False
        self.timeint = timedelta(minutes=self.rule.time_int)
        syslog.openlog(facility=syslog.LOG_DAEMON)


    def get_first_logevent(self):
        """Get the starting log event"""
        e = LogEvent.objects.all()
        if len(e) == 0:
            self.lasteventid = 0
        else:
            erange = LogEvent.objects.filter(
                    parsed_at__gt=timezone.localtime(
                        timezone.now()) - self.timeint)
            if len(erange) == 0:
                self.lasteventid = LogEvent.objects.latest('id').id
            else:
                self.lasteventid = erange.first().id - 1

    def get_last_logevent(self):
        """Set the last event id"""
        e = LogEvent.objects.all()
        if len(e) == 0:
            self.lasteventid = 0
        else:
            self.lasteventid = e.latest('id').id

    def get_first_ruleevent(self):
        """Get the starting log event"""
        e = RuleEvent.objects.all()
        if len(e) == 0:
            self.lasteventid = 0
        else:
            erange = RuleEvent.objects.filter(
                    date_stamp__gt=timezone.localtime(
                        timezone.now()) - self.timeint)
            if len(erange) == 0:
                self.lasteventid = RuleEvent.objects.latest('id').id
            else:
                self.lasteventid = erange.first().id - 1

    def get_last_ruleevent(self):
        """Set the last event id"""
        e = RuleEvent.objects.all()
        if len(e) == 0:
            self.lasteventid = 0
        else:
            self.lasteventid = e.latest('id').id


    def send_email_alerts(self, magnitude, eventcount, logsources):
        """Send email alerts for rule"""
        msgsubject = 'LDSI rule broken: ' + self.rule.name
        msglist = []
        msglist.append(msgsubject + '\n')
        msglist.append('Magnitude: ' + str(magnitude))
        msglist.append('Event count: ' + str(eventcount))
        msglist.append('Event limit: ' + str(self.rule.event_limit))
        msglist.append('Time interval: ' + str(self.rule.time_int))
        msglist.append('Log sources: ' + str(logsources))
        msglist.append('Message: ' + self.rule.message)
        msg = '\n'.join(msglist)
        emaillist = []
        for u in self.rule.alert_users.all():
            emailattrs = (msgsubject, msg, EMAIL_ALERT_FROM_ADDRESS, [u.email])
            emaillist.append(emailattrs)
        emaillist = tuple(emaillist)
        try:
            send_mass_mail(emaillist, fail_silently=False)
        except smtplib.SMTPException:
            syslog.syslog(syslog.LOG_ERR, 
                    'LDSI sentry failed to send email for rule ' + \
                            self.rule.name)



    def watch_events(self):
        """Watch log events based on a rule"""
        if self.rule.rule_events:
            self.get_first_ruleevent()
            expectrule = True
        else:
            self.get_first_logevent()
            expectrule = False
        while True:
            # Set EOL time delta:
            if self.rule.local_lifespan_days == 0:
                self.locallifespandelta = timedelta(days=36524)
            else:
                self.locallifespandelta = \
                        timedelta(days=self.rule.local_lifespan_days)
            if self.rule.backup_lifespan_days == 0:
                self.backuplifespandelta = timedelta(days=36524)
            else:
                self.backuplifespandelta = \
                        timedelta(days=self.rule.backup_lifespan_days)
            # Check the rule:
            if self.rule.is_enabled:
                if self.rule.rule_events: self.check_ruleevent()
                else: self.check_logevent()
            # Refresh the rule:
            try:
                t = self.rule.time_int
                self.rule = LimitRule.objects.get(pk=self.rule.id)
                if self.rule.time_int != t:
                    self.timeint = timedelta(minutes=self.rule.time_int)
            except LimitRule.DoesNotExist:
                break
            # Check for change in event type:
            if expectrule:
                if not self.rule.rule_events:
                    self.get_last_logevent()
                    expectrule = False
            else:
                if self.rule.rule_events:
                    self.get_last_ruleevent()
                    expectrule = True
            # Wait until next interval if firedr,; otherwise ~60 seconds:
            if self.justfired:
                sleep(int(self.rule.time_int) * 60)
            else:
                sleep(randrange(50, 70))


    def check_logevent(self):
        """Check log events based on a rule"""
        
        if self.rule.log_source_filter:
            logsourcefilter = self.rule.log_source_filter
        else: logsourcefilter = ''
        if self.rule.process_filter:
            processfilter = self.rule.process_filter
        else: processfilter = ''
        if self.rule.source_host_filter:
            sourcehostfilter = self.rule.source_host_filter
        else: sourcehostfilter = ''
        if self.rule.dest_host_filter:
            desthostfilter = self.rule.dest_host_filter
        else: desthostfilter = ''
        if self.rule.message_filter_regex:
            messagefilter = '.*{}.*'.format(self.rule.message_filter_regex)
        else:
            messagefilter = '.*{}.*'.format('.*')
        if self.rule.raw_text_filter_regex:
            rawtextfilter = '.*{}.*'.format(self.rule.raw_text_filter_regex)
        else:
            rawtextfilter = '.*{}.*'.format('.*')
        if self.justfired:
            if self.rule.event_type:
                e = LogEvent.objects.filter(id__gt=self.lasteventid,
                        event_type=self.rule.event_type,
                        log_source__icontains=logsourcefilter,
                        source_process__icontains=processfilter,
                        source_host__icontains=sourcehostfilter,
                        dest_host__icontains=desthostfilter,
                        message__iregex=messagefilter,
                        raw_text__iregex=rawtextfilter)
            else:
                e = LogEvent.objects.filter(id__gt=self.lasteventid,
                        log_source__contains=logsourcefilter,
                        source_process__contains=processfilter,
                        source_host__icontains=sourcehostfilter,
                        dest_host__icontains=desthostfilter,
                        message__iregex=messagefilter,
                        raw_text__iregex=rawtextfilter)
        else:
            startdatestamp = timezone.localtime(timezone.now()) - self.timeint
            if self.rule.event_type:
                e = LogEvent.objects.filter(date_stamp__gt=startdatestamp,
                        event_type=self.rule.event_type,
                        log_source__icontains=logsourcefilter,
                        source_process__icontains=processfilter,
                        source_host__icontains=sourcehostfilter,
                        dest_host__icontains=desthostfilter,
                        message__iregex=messagefilter,
                        raw_text__iregex=rawtextfilter)
            else:
                e = LogEvent.objects.filter(date_stamp__gt=startdatestamp,
                        log_source__contains=logsourcefilter,
                        source_process__contains=processfilter,
                        source_host__icontains=sourcehostfilter,
                        dest_host__icontains=desthostfilter,
                        message__iregex=messagefilter,
                        raw_text__iregex=rawtextfilter)
        
        if len(e) == 0:
            self.justfired = False
        else:
            totalevents = sum([x.aggregated_events for x in e])
            numhosts = len({x.log_source for x in e})
            if totalevents > self.rule.event_limit and \
                    numhosts > self.rule.allowed_log_sources:
                event = RuleEvent()
                event.date_stamp = timezone.localtime(timezone.now())
                event.time_zone = TIME_ZONE
                event.rule_category = self.rule.rule_category
                event.eol_date_local = timezone.localtime(
                        timezone.now()).date() + \
                                self.locallifespandelta
                event.eol_date_backup = timezone.localtime(
                        timezone.now()).date() + \
                                self.backuplifespandelta
                event.event_type = self.rule.event_type
                event.source_rule = self.rule
                event.log_source = self.rule.log_source_filter
                event.event_limit = self.rule.event_limit
                event.event_count = totalevents
                event.time_int = self.rule.time_int
                event.severity = self.rule.severity
                magnitude = int((1 + \
                        (((totalevents / (self.rule.event_limit + 1)) * \
                        float(self.rule.overkill_modifier))) - 1) * \
                        ((8 - self.rule.severity) * \
                        float(self.rule.severity_modifier)))
                event.magnitude = magnitude
                event.message = self.rule.message
                event.log_source_count = numhosts
                event.save()
                event.source_ids_log.set(list(e))
                event.save()
                self.lasteventid = e.latest('id').id
                if self.rule.email_alerts:
                    self.send_email_alerts(magnitude, totalevents, numhosts)
                self.justfired = True
            else:
                self.justfired = False


    def check_ruleevent(self):
        """Check rule events based on a rule"""

        if self.rule.rulename_filter: rulenamefilter = self.rule.rulename_filter
        else: rulenamefilter = ''
        if self.rule.message_filter_regex:
            messagefilter = '.*{}.*'.format(self.rule.message_filter_regex)
        else:
            messagefilter = '.*{}.*'.format('.*')
        if self.rule.magnitude_filter: magnitudefilter = self.rule.magnitude_filter
        else: magnitudefilter = 0
        if self.justfired:
            if self.rule.event_type:
                e = RuleEvent.objects.filter(id__gt=self.lasteventid,
                        event_type=self.rule.event_type,
                        source_rule__name__icontains=rulenamefilter,
                        magnitude__gte=magnitudefilter,
                        message__iregex=messagefilter)
            else:
                e = RuleEvent.objects.filter(id__gt=self.lasteventid,
                        source_rule__name__icontains=rulenamefilter,
                        magnitude__gte=magnitudefilter,
                        message__iregex=messagefilter)
        else:
            startdatestamp = timezone.localtime(timezone.now()) - self.timeint
            if self.rule.event_type:
                e = RuleEvent.objects.filter(date_stamp__gt=startdatestamp,
                        event_type=self.rule.event_type,
                        source_rule__name__icontains=rulenamefilter,
                        magnitude__gte=magnitudefilter,
                        message__iregex=messagefilter)
            else:
                e = RuleEvent.objects.filter(date_stamp__gt=startdatestamp,
                        source_rule__name__icontains=rulenamefilter,
                        magnitude__gte=magnitudefilter,
                        message__iregex=messagefilter)

        if len(e) == 0:
            self.justfired = False
        else:
            if len(e) > self.rule.event_limit:
                event = RuleEvent()
                event.date_stamp = timezone.localtime(timezone.now())
                event.time_zone = TIME_ZONE
                event.rule_category = self.rule.rule_category
                event.eol_date_local = timezone.localtime(
                        timezone.now()).date() + \
                                self.locallifespandelta
                event.eol_date_backup = timezone.localtime(
                        timezone.now()).date() + \
                                self.backuplifespandelta
                event.event_type = self.rule.event_type
                event.source_rule = self.rule
                event.event_limit = self.rule.event_limit
                event.event_count = len(e)
                event.time_int = self.rule.time_int
                event.severity = self.rule.severity
                event.magnitude = int((1 + \
                        (((len(e) / (self.rule.event_limit + 1)) * \
                        float(self.rule.overkill_modifier))) - 1) * \
                        ((8 - self.rule.severity) * \
                        float(self.rule.severity_modifier)))
                event.message = self.rule.message
                event.save()
                event.source_ids_rule.set(list(e))
                event.save()
                self.lasteventid = e.latest('id').id
                if self.rule.email_alerts:
                    self.send_email_alerts(magnitude, totalevents, numhosts)
                self.justfired = True
            else:
                self.justfired = False


def start_rule(rule):
    """Initialize trigger object and start watching"""
    
    sentry = SiemSentry(rule)

    # Before starting, sleep randomly up to rule interval to stagger
    # database use:
    timeint = int(rule.time_int) * 60
    sleep(randrange(timeint * 2 // 3, timeint))

    sentry.watch_events()
