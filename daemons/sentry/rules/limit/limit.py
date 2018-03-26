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


class LimitSentry:

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
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                e = LogEvent.objects.last()
                connsuccess = True
            except Exception as err:
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LDSI sentry thread for rule ' + \
                            self.rule.name + \
                            ' got 20 db errors. Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                dbtries -= 1
                sleep(0.2)
        if e:
            self.lasteventid = e.id
            connsuccess = False
            dbtries = 20
            while not connsuccess:
                try:
                    erange = LogEvent.objects.filter(
                            parsed_at__gt=timezone.localtime(
                                timezone.now()) - self.timeint)
                    connsuccess = True
                except Exception as err:
                    if dbtries == 0:
                        dbtries = 20
                        msg = 'LDSI sentry thread for rule ' + \
                                self.rule.name + \
                                ' got 20 db errors. Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                    dbtries -= 1
                    sleep(0.2)
            if len(erange) != 0:
                self.lasteventid = erange.first().id - 1
        else:
            self.lasteventid = 0

    def get_last_logevent(self):
        """Set the last event id"""
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                e = LogEvent.objects.last()
                connsuccess = True
            except Exception as err:
                dbtries -= 1
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LDSI sentry thread for rule ' + \
                            self.rule.name + \
                            ' got 20 db errors. Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                sleep(0.2)
        if e:
            self.lasteventid = e.id
        else:
            self.lasteventid = 0

    def get_first_ruleevent(self):
        """Get the starting log event"""
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                e = RuleEvent.objects.last()
                connsuccess = True
            except Exception as err:
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LDSI sentry thread for rule ' + \
                            self.rule.name + \
                            ' got 20 db errors. Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                dbtries -= 1
                sleep(0.2)
        if e:
            self.lasteventid = e.id
            connsuccess = False
            dbtries = 20
            while not connsuccess:
                try:
                    erange = RuleEvent.objects.filter(
                            date_stamp__gt=timezone.localtime(
                                timezone.now()) - self.timeint)
                    connsuccess = True
                except Exception as err:
                    if dbtries == 0:
                        dbtries = 20
                        msg = 'LDSI sentry thread for rule ' + \
                                self.rule.name + \
                                ' got 20 db errors. Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                    dbtries -= 1
                    sleep(0.2)
            if len(erange) != 0:
                self.lasteventid = erange.first().id - 1
        else:
            self.lasteventid = 0

    def get_last_ruleevent(self):
        """Set the last event id"""
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                e = RuleEvent.objects.last()
                connsuccess = True
            except Exception as err:
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LDSI sentry thread for rule ' + \
                            self.rule.name + \
                            ' got 20 db errors. Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                dbtries -= 1
                sleep(0.2)
        if e:
            self.lasteventid = e.id
        else:
            self.lasteventid = 0


    def send_email_alerts(self, magnitude, eventcount, logsources,
            sourcehosts, desthosts):
        """Send email alerts for rule"""
        msgsubject = 'LDSI rule broken: ' + self.rule.name
        msglist = []
        msglist.append(msgsubject + '\n')
        msglist.append('Magnitude: ' + str(magnitude))
        msglist.append('Event count: ' + str(eventcount))
        msglist.append('Event limit: ' + str(self.rule.event_limit))
        msglist.append('Time interval: ' + str(self.rule.time_int))
        msglist.append('Log sources: ' + str(logsources))
        msglist.append('source Hosts: ' + str(sourcehosts))
        msglist.append('Dest Hosts: ' + str(desthosts))
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
            msg = 'LDSI sentry failed to send email alerts for rule ' + \
                    self.rule_name
            syslog.syslog(syslog.LOG_ERR, msg)



    def watch_events(self):
        """Watch log events based on a rule"""
        if self.rule.rule_events:
            self.get_first_ruleevent()
            expectrule = True
        else:
            self.get_first_logevent()
            expectrule = False
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
        while True:
            try:
                # Check the rule:
                if self.rule.is_enabled:
                    if self.rule.rule_events: self.check_ruleevent()
                    else: self.check_logevent()
                # Refresh the rule:
                locallifespan = self.rule.local_lifespan_days
                backuplifespan = self.rule.backup_lifespan_days
                t = self.rule.time_int
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        self.rule = LimitRule.objects.get(
                                pk=self.rule.id)
                        connsuccess = True
                    except LimitRule.DoesNotExist:
                        msg = 'LDSI sentry thread for ' + self.rule.name + \
                                ' exiting. Rule no longer exists.'
                        syslog.syslog(syslog.LOG_NOTICE, msg)
                        exit(0)
                    except Exception:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
                if self.rule.time_int != t:
                    self.timeint = timedelta(minutes=self.rule.time_int)
                # Set EOL time delta:
                if self.rule.local_lifespan_days != locallifespan:
                    if self.rule.local_lifespan_days == 0:
                        self.locallifespandelta = timedelta(days=36524)
                    else:
                        self.locallifespandelta = \
                                timedelta(
                                        days=self.rule.local_lifespan_days)
                if self.rule.backup_lifespan_days != backuplifespan:
                    if self.rule.backup_lifespan_days == 0:
                        self.backuplifespandelta = timedelta(days=36524)
                    else:
                        self.backuplifespandelta = \
                                timedelta(
                                        days=self.rule.backup_lifespan_days)
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
                    sleep(randrange(45, 60))
            except Exception as err:
                msg = 'LDSI sentry thread for ' + self.rule.name + \
                        ' crashing. Error: ' + str(err)
                syslog.syslog(syslog.LOG_ERR, msg)
                exit(0)


    def check_logevent(self):
        """Check log events based on a rule"""
        
        if self.rule.log_source_filter_regex:
            logsourcefilter = '.*{}.*'.format(
                    self.rule.log_source_filter_regex)
        else:
            logsourcefilter = '.*'
        if self.rule.process_filter_regex:
            processfilter = '.*{}.*'.format(
                    self.rule.process_filter_regex)
        else:
            processfilter = '.*'
        if self.rule.action_filter_regex:
            actionfilter = '.*{}.*'.format(
                    self.rule.action_filter_regex)
        else:
            actionfilter = '.*'
        if self.rule.interface_filter_regex:
            interfacefilter = '.*{}.*'.format(
                    self.rule.interface_filter_regex)
        else:
            interfacefilter = '.*'
        if self.rule.status_filter_regex:
            statusfilter = '.*{}.*'.format(
                    self.rule.status_filter_regex)
        else:
            statusfilter = '.*'
        if self.rule.source_host_filter_regex:
            sourcehostfilter = '.*{}.*'.format(
                    self.rule.source_host_filter_regex)
        else:
            sourcehostfilter = '.*'
        if self.rule.source_port_filter_regex:
            sourceportfilter = '.*{}.*'.format(
                    self.rule.source_port_filter_regex)
        else:
            sourceportfilter = '.*'
        if self.rule.dest_host_filter_regex:
            desthostfilter = '.*{}.*'.format(
                    self.rule.dest_host_filter_regex)
        else:
            desthostfilter = '.*'
        if self.rule.dest_port_filter_regex:
            destportfilter = '.*{}.*'.format(
                    self.rule.dest_port_filter_regex)
        else:
            destportfilter = '.*'
        if self.rule.source_user_filter_regex:
            sourceuserfilter = '.*{}.*'.format(
                    self.rule.source_user_filter_regex)
        else:
            sourceuserfilter = '.*'
        if self.rule.target_user_filter_regex:
            targetuserfilter = '.*{}.*'.format(
                    self.rule.target_user_filter_regex)
        else:
            targetuserfilter = '.*'
        if self.rule.path_filter_regex:
            pathfilter = '.*{}.*'.format(
                    self.rule.path_filter_regex)
        else:
            pathfilter = '.*'
        if self.rule.parameters_filter_regex:
            parametersfilter = '.*{}.*'.format(
                    self.rule.parameters_filter_regex)
        else:
            parametersfilter = '.*'
        if self.rule.referrer_filter_regex:
            referrerfilter = '.*{}.*'.format(
                    self.rule.referrer_filter_regex)
        else:
            referrerfilter = '.*'
        if self.rule.message_filter_regex:
            messagefilter = '.*{}.*'.format(
                    self.rule.message_filter_regex)
        else:
            messagefilter = '.*'
        if self.rule.raw_text_filter_regex:
            rawtextfilter = '.*{}.*'.format(
                    self.rule.raw_text_filter_regex)
        else:
            rawtextfilter = '.*'
        if self.justfired:
            if self.rule.event_type:
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        e = LogEvent.objects.filter(
                                id__gt=self.lasteventid,
                                event_type=self.rule.event_type,
                                log_source__iregex=logsourcefilter,
                                source_process__iregex=processfilter,
                                action__iregex=actionfilter,
                                interface__iregex=interfacefilter,
                                status__iregex=statusfilter,
                                source_host__iregex=sourcehostfilter,
                                source_port__iregex=sourceportfilter,
                                dest_host__iregex=desthostfilter,
                                dest_port__iregex=destportfilter,
                                source_user__iregex=sourceuserfilter,
                                target_user__iregex=targetuserfilter,
                                path__iregex=pathfilter,
                                parameters__iregex=parametersfilter,
                                referrer__iregex=referrerfilter,
                                message__iregex=messagefilter,
                                raw_text__iregex=rawtextfilter)
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
            else:
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        e = LogEvent.objects.filter(
                                id__gt=self.lasteventid,
                                log_source__iregex=logsourcefilter,
                                source_process__iregex=processfilter,
                                action__iregex=actionfilter,
                                interface__iregex=interfacefilter,
                                status__iregex=statusfilter,
                                source_host__iregex=sourcehostfilter,
                                source_port__iregex=sourceportfilter,
                                dest_host__iregex=desthostfilter,
                                dest_port__iregex=destportfilter,
                                source_user__iregex=sourceuserfilter,
                                target_user__iregex=targetuserfilter,
                                path__iregex=pathfilter,
                                parameters__iregex=parametersfilter,
                                referrer__iregex=referrerfilter,
                                message__iregex=messagefilter,
                                raw_text__iregex=rawtextfilter)
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
        else:        
            startdatestamp = timezone.localtime(timezone.now()) - \
                    self.timeint
            if self.rule.event_type:
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        e = LogEvent.objects.filter(
                                parsed_at__gt=startdatestamp,
                                event_type=self.rule.event_type,
                                log_source__iregex=logsourcefilter,
                                source_process__iregex=processfilter,
                                action__iregex=actionfilter,
                                interface__iregex=interfacefilter,
                                status__iregex=statusfilter,
                                source_host__iregex=sourcehostfilter,
                                source_port__iregex=sourceportfilter,
                                dest_host__iregex=desthostfilter,
                                dest_port__iregex=destportfilter,
                                source_user__iregex=sourceuserfilter,
                                target_user__iregex=targetuserfilter,
                                path__iregex=pathfilter,
                                parameters__iregex=parametersfilter,
                                referrer__iregex=referrerfilter,
                                message__iregex=messagefilter,
                                raw_text__iregex=rawtextfilter)
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
            else:
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        e = LogEvent.objects.filter(
                                parsed_at__gt=startdatestamp,
                                log_source__iregex=logsourcefilter,
                                source_process__iregex=processfilter,
                                action__iregex=actionfilter,
                                interface__iregex=interfacefilter,
                                status__iregex=statusfilter,
                                source_host__iregex=sourcehostfilter,
                                source_port__iregex=sourceportfilter,
                                dest_host__iregex=desthostfilter,
                                dest_port__iregex=destportfilter,
                                source_user__iregex=sourceuserfilter,
                                target_user__iregex=targetuserfilter,
                                path__iregex=pathfilter,
                                parameters__iregex=parametersfilter,
                                referrer__iregex=referrerfilter,
                                message__iregex=messagefilter,
                                raw_text__iregex=rawtextfilter)
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)

        if len(e) == 0:
            self.justfired = False
        else:
            totalevents = sum([x.aggregated_events for x in e])
            logsources = {x.log_source for x in e}
            sourcehosts = {x.source_host for x in e}
            desthosts = {x.dest_host for x in e}
            try: logsources.remove(None)
            except KeyError: pass
            try: sourcehosts.remove(None)
            except KeyError: pass
            try: desthosts.remove(None)
            except KeyError: pass
            numlogsources = len(logsources)
            numsourcehosts = len(sourcehosts)
            numdesthosts = len(desthosts)
            if totalevents > self.rule.event_limit and \
                    numlogsources > self.rule.allowed_log_sources:
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
                event.event_count = totalevents
                event.time_int = self.rule.time_int
                event.severity = self.rule.severity
                magnitude = int((1 + \
                        ((totalevents / (self.rule.event_limit + 1)) * \
                        float(self.rule.overkill_modifier)) - 1) * \
                        ((8 - self.rule.severity) * \
                        float(self.rule.severity_modifier)))
                event.magnitude = magnitude
                event.message = self.rule.message
                event.log_source_count = numlogsources
                event.source_host_count = numsourcehosts
                event.dest_host_count = numdesthosts
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        event.save()
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        event.source_ids_log.set(list(e))
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        event.save()
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
                self.lasteventid = e.latest('id').id
                if self.rule.email_alerts:
                    self.send_email_alerts(magnitude, totalevents,
                            numlogsources, numsourcehosts, numdesthosts)
                self.justfired = True
            else:
                self.justfired = False


    def check_ruleevent(self):
        """Check rule events based on a rule"""

        if self.rule.rulename_filter_regex:
            rulenamefilter = '.*{}.*'.format(
                    self.rule.rulename_filter_regex)
        else:
            rulenamefilter = '.*'
        if self.rule.message_filter_regex:
            messagefilter = '.*{}.*'.format(
                    self.rule.message_filter_regex)
        else:
            messagefilter = '.*'
        if self.rule.magnitude_filter:
            magnitudefilter = self.rule.magnitude_filter
        else: magnitudefilter = 0
        if self.justfired:
            if self.rule.event_type:
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        e = RuleEvent.objects.filter(
                                id__gt=self.lasteventid,
                                event_type=self.rule.event_type,
                                source_rule__name__iregex=rulenamefilter,
                                magnitude__gte=magnitudefilter,
                                message__iregex=messagefilter)
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
            else:
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        e = RuleEvent.objects.filter(
                                id__gt=self.lasteventid,
                                source_rule__name__iregex=rulenamefilter,
                                magnitude__gte=magnitudefilter,
                                message__iregex=messagefilter)
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
        else:
            startdatestamp = timezone.localtime(
                    timezone.now()) - self.timeint
            if self.rule.event_type:
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        e = RuleEvent.objects.filter(
                                date_stamp__gt=startdatestamp,
                                event_type=self.rule.event_type,
                                source_rule__name__iregex=rulenamefilter,
                                magnitude__gte=magnitudefilter,
                                message__iregex=messagefilter)
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
            else:
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        e = RuleEvent.objects.filter(
                                date_stamp__gt=startdatestamp,
                                source_rule__name__iregex=rulenamefilter,
                                magnitude__gte=magnitudefilter,
                                message__iregex=messagefilter)
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)

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
                event.magnitude = int(
                        ((len(e) / (self.rule.event_limit + 1)) * \
                        float(self.rule.overkill_modifier)) * \
                        ((8 - self.rule.severity) * \
                        float(self.rule.severity_modifier)))
                event.message = self.rule.message
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        event.save()
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        event.source_ids_rule.set(list(e))
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        dbtries -= 1
                        sleep(0.2)
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        event.save()
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 0:
                            dbtries = 20
                            msg = 'LDSI sentry thread for rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                            dbtries = 20
                        dbtries -= 1
                        sleep(0.2)
                self.lasteventid = e.latest('id').id
                if self.rule.email_alerts:
                    self.send_email_alerts(magnitude, totalevents,
                            numlogsources, numsourcehosts, numdesthosts)
                self.justfired = True
            else:
                self.justfired = False


def start_rule(rule):
    """Initialize trigger object and start watching"""
    
    sentry = LimitSentry(rule)

    # Before starting, sleep randomly up to rule interval to stagger
    # database use:
    timeint = int(rule.time_int) * 60
    sleep(randrange(timeint * 2 // 3, timeint))

    sentry.watch_events()
