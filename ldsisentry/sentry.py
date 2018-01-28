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
from ldsi.settings import TIME_ZONE
from siem.models import LogEvent
from siem.models import RuleEvent
#import signal


class SiemSentry:

    def __init__(self, rule):
        """Initialize trigger object"""
        
        self.rule = rule
        self.tzone = TIME_ZONE


    def watch_logevent(self):
        """Watch log events based on a rule"""

        timeint = timedelta(seconds=self.rule.time_int)
        erange = LogEvent.objects.filter(parsed_at__gt= \
                timezone.localtime(timezone.now()) - timeint)
        lasteventid = erange.first()
        del(erange)

        while True:
            
            # Check the rule:
            lasteventid = self.check_logevent(lasteventid)
        
            # Wait until the next interval
            sleep(int(self.rule.time_int) * 60)


    def check_logevent(self, lasteventid):
        """Check log events based on a rule"""
        
        if self.rule.host_filter:
            e = LogEvent.objects.filter(id__gt=lastevent,
                    event_type=self.rule.event_type,
                    host=self.rule.host_filter,
                    message__contains=self.rule.message_filter)
        else:
            e = LogEvent.objects.filter(id__gt=lastevent,
                    event_type=self.rule.event_type,
                    message__contains=self.rule.message_filter)

        if len(e) > self.rule.event_limit:
            event = RuleEvent()
            event.date_stamp = timezone.localtime(timezone.now())
            event.time_zone = TIME_ZONE
            event.event_type = self.rule.event_type
            event.source_rule = self.rule.name
            event.source_host = self.rule.host_filter
            event.event_limit = self.rule.event_limit
            event.event_count = len(e)
            event.time_int = self.rule.time_int
            event.severity = self.rule.severity
            event.magnitude = (((len(rows) // 2) // \
                    (self.rule.event_limit + 1) // 2) + 5) * \
                    ( 7 - self.rule.severity)
            event.message = self.rule.message
            event.source_ids_log = [e]
            event.save()

        lasteventid = e.latest('id').id
        return lasteventid


    def watch_ruleevent(self:
        """Watch rule events based on a rule"""

        timeint = timedelta(seconds=self.rule.time_int)
        erange = RuleEvent.objects.filter(parsed_at__gt= \
                timezone.localtime(timezone.now()) - timeint)
        lasteventid = erange.first()
        del(erange)

        while True:

            # Check the rule:
            lasteventid = self.check_ruleevent(lasteventid)
        
            # Wait until the next interval
            sleep(int(self.rule.time_int) * 60)


    def check_ruleevent(self, lasteventid):
        """Check rule events based on a rule"""

        if self.rule.rulename_filter:
            e = RuleEvent.objects.filter(id__gt=lasteventid,
                    event_type=self.rule.event_type,
                    source_rule=self.rule.rulename_filter,
                    message__contains=self.rule.message_filter)
        else:
            e = RuleEvent.objects.filter(id__gt=lasteventid,
                    event_type=self.rule.event_type,
                    message__contains=self.rule.message_filter)

        if len(e) > self.rule.event_limit:
            event = RuleEvent()
            event.date_stamp = timezone.localtime(timezone.now())
            event.time_zone = TIME_ZONE
            event.event_type = self.rule.event_type
            event.source_rule = self.rule.name
            event.event_limit = self.rule.event_limit
            event.event_count = len(e)
            event.time_int = self.rule.time_int
            event.severity = self.rule.severity
            event.magnitude = (((len(rows) // 2) // \
                    (self.rule.event_limit + 1) // 2) + 5) * \
                    ( 7 - self.rule.severity)
            event.message = self.rule.message
            event.source_ids_rule = [e]
            event.save()
        
        lasteventid = e.latest('id').id
        return lasteventid


def start_rule(rule):
    """Initialize trigger object and start watching"""
    
    sentry = SiemSentry(rule)

    # Before starting, sleep randomly up to rule interval to stagger
    # database use:
    sleep(randrange(0, int(rule.time_int) * 60))

    if self.rule.rule_events = True:
        sentry.watch_ruleevents()
    else:
        sentry.watch_logevents()
