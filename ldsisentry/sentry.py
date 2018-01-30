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
from sys import exit
from django.utils import timezone
from ldsi.settings import TIME_ZONE
from siem.models import LogEvent, RuleEvent, LimitRule
#import signal


class SiemSentry:

    def __init__(self, rule):
        """Initialize trigger object"""
        
        self.rule = rule
        self.tzone = TIME_ZONE
        self.lasteventid = None


    def get_first_logevent(self):
        """Get the starting log event"""
        e = LogEvent.objects.all()
        if len(e) == 0:
            self.lasteventid = 0
        else:
            timeint = timedelta(minutes=self.rule.time_int)
            erange = LogEvent.objects.filter(
                    parsed_at__gt=timezone.localtime(
                        timezone.now()) - timeint)
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
            timeint = timedelta(minutes=self.rule.time_int)
            erange = LogEvent.objects.filter(
                    parsed_at__gt=timezone.localtime(
                        timezone.now()) - timeint)
            if len(erange) == 0:
                self.lasteventid = LogEvent.objects.latest('id').id
            else:
                self.lasteventid = erange.first().id - 1

    def get_last_ruleevent(self):
        """Set the last event id"""
        e = RuleEvent.objects.all()
        if len(e) == 0:
            self.lasteventid = 0
        else:
            self.lasteventid = e.latest('id').id


    def watch_logevents(self):
        """Watch log events based on a rule"""
        self.get_first_logevent()
        while True:
            # Check the rule:
            if self.rule.is_enabled: self.check_logevent()
            # Refresh the rule:
            try:
                self.rule = LimitRule.objects.get(pk=self.rule.id)
            except siem.models.DoesNotExist:
                break
            # Set EOL time delta:
            if self.rule.lifespan_days:
                self.lifespandelta = timedelta(days=self.rule.lifespan_days)
            else:
                self.lifespandelta = None
            # Wait until the next interval
            sleep(int(self.rule.time_int) * 60)


    def check_logevent(self):
        """Check log events based on a rule"""
        
        if self.rule.host_filter: hostfilter = self.rule.host_filter
        else: hostfilter = ''
        if self.rule.message_filter: messagefilter = self.rule.message_filter
        else: messagefilter = ''
        if self.rule.raw_text_filter: rawtextfilter = self.rule.raw_text_filter
        else: rawtextfilter = ''
        if self.rule.event_type:
            e = LogEvent.objects.filter(id__gt=self.lasteventid,
                    event_type=self.rule.event_type,
                    source_host__contains=hostfilter,
                    message__contains=messagefilter,
                    raw_text__contains=rawtextfilter)
        else:
            e = LogEvent.objects.filter(id__gt=self.lasteventid,
                    source_host__contains=self.rule.host_filter,
                    message__contains=self.rule.message_filter,
                    raw_text__contains=rawtextfilter)

        if len(e) == 0:
            self.get_last_logevent()
        else:
            if len(e) > self.rule.event_limit:
                event = RuleEvent()
                event.date_stamp = timezone.localtime(timezone.now())
                event.time_zone = TIME_ZONE
                event.rule_category = self.rule.rule_category
                if self.lifespandelta:
                    event.eol_date = timezone.localtime(timezone.now()).date() + \
                        self.lifespandelta
                event.event_type = self.rule.event_type
                event.source_rule = self.rule
                event.source_host = self.rule.host_filter
                event.event_limit = self.rule.event_limit
                event.event_count = len(e)
                event.time_int = self.rule.time_int
                event.severity = self.rule.severity
                event.magnitude = (((len(e) // 2) // \
                        (self.rule.event_limit + 1) // 2) + 5) * \
                        ( 7 - self.rule.severity)
                event.message = self.rule.message
                event.save()
                event.source_ids_log.set(list(e))
                event.save()
                self.lasteventid = e.latest('id').id


    def watch_ruleevents(self):
        """Watch rule events based on a rule"""
        self.get_first_ruleevent()
        while True:
            # Check the rule:
            if self.rule.is_enabled: self.check_ruleevent()
            # Refresh the rule:
            try:
                self.rule = LimitRule.objects.get(pk=self.rule.id)
            except siem.models.DoesNotExist:
                break
            # Set EOL time delta:
            if self.rule.lifespan_days:
                self.lifespandelta = timedelta(days=self.rule.lifespan_days)
            # Wait until the next interval
            sleep(int(self.rule.time_int) * 60)


    def check_ruleevent(self):
        """Check rule events based on a rule"""

        if self.rule.rulename_filter: rulenamefilter = self.rule.rulename_filter
        else: rulenamefilter = ''
        if self.rule.message_filter: messagefilter = self.rule.message_filter
        else: messagefilter = ''
        if self.rule.mag_filter: magnitudefilter = self.rule.magnitude_filter
        else: magfilter = 0
        if self.rule.event_type:
            e = RuleEvent.objects.filter(id__gt=self.lasteventid,
                    event_type=self.rule.event_type,
                    source_rule__contains=rulenamefilter,
                    magnitude__gte=magnitudefilter,
                    message__contains=messagefilter)
        else:
            e = RuleEvent.objects.filter(id__gt=self.lasteventid,
                    source_rule__contains=rulenamefilter,
                    magnitude__gte=magnitudefilter,
                    message__contains=messagefilter)

        if len(e) == 0:
            self.get_last_ruleevent()
        else:
            if len(e) > self.rule.event_limit:
                event = RuleEvent()
                event.date_stamp = timezone.localtime(timezone.now())
                event.time_zone = TIME_ZONE
                event.rule_category = self.rule.rule_category
                if self.lifespandelta:
                    event.eol_date = timezone.localtime(timezone.now()).date() + \
                        self.lifespandelta
                event.event_type = self.rule.event_type
                event.source_rule = self.rule
                event.event_limit = self.rule.event_limit
                event.event_count = len(e)
                event.time_int = self.rule.time_int
                event.severity = self.rule.severity
                event.magnitude = (((len(e) // 2) // \
                        (self.rule.event_limit + 1) // 2) + 5) * \
                        ( 7 - self.rule.severity)
                event.message = self.rule.message
                event.save()
                event.source_ids_rule.set(list(e))
                event.save()
                self.lasteventid = e.latest('id').id


def start_rule(rule):
    """Initialize trigger object and start watching"""
    
    sentry = SiemSentry(rule)

    # Before starting, sleep randomly up to rule interval to stagger
    # database use:
    sleep(randrange(0, int(rule.time_int) * 60))

    if rule.rule_events:
        sentry.watch_ruleevents()
    else:
        sentry.watch_logevents()
