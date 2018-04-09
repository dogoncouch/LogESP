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
import threading
import syslog
from sys import exit
from os import listdir
from os.path import join, isfile, isdir
from django import db
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User

from LogESP.settings import TIME_ZONE
try:
    from LogESP.settings import EMAIL_ALERT_FROM_ADDRESS
except ImportError:
    EMAIL_ALERT_FROM_ADDRESS = 'noreply@example.com'
from siem.models import LogEvent, RuleEvent, LimitRule


class Sentry:

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
                if dbtries == 20:
                    db.connections.close_all()
                    msg = 'LogESP sentry thread for limit rule ' + \
                            self.rule.name + \
                            ' got a db error. Resetting conn. ' + \
                            'Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                elif dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP sentry thread for limit rule ' + \
                            self.rule.name + \
                            ' got 20 db errors. Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                    exit(1)
                else:
                    sleep(0.2)
                dbtries -= 1
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
                    if dbtries == 20:
                        db.connections.close_all()
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got a db error. Resetting conn. ' + \
                                'Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                    elif dbtries == 0:
                        dbtries = 20
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got 20 db errors. Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                        exit(1)
                    else:
                        sleep(0.2)
                    dbtries -= 1
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
                if dbtries == 20:
                    db.connections.close_all()
                    msg = 'LogESP sentry thread for limit rule ' + \
                            self.rule.name + \
                            ' got a db error. Resetting conn. ' + \
                            'Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                elif dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP sentry thread for limit rule ' + \
                            self.rule.name + \
                            ' got 20 db errors. Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                    exit(1)
                else:
                    sleep(0.2)
                dbtries -= 1
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
                if dbtries == 20:
                    db.connections.close_all()
                    msg = 'LogESP sentry thread for limit rule ' + \
                            self.rule.name + \
                            ' got a db error. Resetting conn. ' + \
                            'Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                elif dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP sentry thread for limit rule ' + \
                            self.rule.name + \
                            ' got 20 db errors. Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                    exit(1)
                else:
                    sleep(0.2)
                dbtries -= 1
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
                    if dbtries == 20:
                        db.connections.close_all()
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got a db error. Resetting conn. ' + \
                                'Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                    elif dbtries == 0:
                        dbtries = 20
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got 20 db errors. Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                        exit(1)
                    else:
                        sleep(0.2)
                    dbtries -= 1
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
                if dbtries == 20:
                    db.connections.close_all()
                    msg = 'LogESP sentry thread for limit rule ' + \
                            self.rule.name + \
                            ' got a db error. Resetting conn. ' + \
                            'Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                elif dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP sentry thread for limit rule ' + \
                            self.rule.name + \
                            ' got 20 db errors. Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                    exit(1)
                else:
                    sleep(0.2)
                dbtries -= 1
        if e:
            self.lasteventid = e.id
        else:
            self.lasteventid = 0


    def send_email_alerts(self, magnitude, eventcount, logsources,
            sourcehosts, desthosts):
        """Send email alerts for rule"""
        msgsubject = 'LogESP rule broken: ' + self.rule.name
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
            msg = 'LogESP sentry failed to send email alerts for ' + \
                    'limit rule ' + self.rule_name
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
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' exiting. Rule no longer exists.'
                        syslog.syslog(syslog.LOG_NOTICE, msg)
                        exit(0)
                    except Exception:
                        if dbtries == 20:
                            db.connections.close_all()
                            msg = 'LogESP sentry thread for limit rule ' + \
                                    self.rule.name + \
                                    ' got a db error. Resetting conn. ' + \
                                    'Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        elif dbtries == 0:
                            dbtries = 20
                            msg = 'LogESP sentry thread for limit rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Crashing. Error: ' + \
                                    str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                            exit(1)
                        else:
                            sleep(0.2)
                        dbtries -= 1
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
                msg = 'LogESP sentry thread for limit rule ' + \
                        self.rule.name + \
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
            connsuccess = False
            dbtries = 20
            while not connsuccess:
                try:
                    if self.rule.event_type:
                        events = LogEvent.objects.filter(
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
                    else:
                        events = LogEvent.objects.filter(
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
                    if dbtries == 20:
                        db.connections.close_all()
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got a db error. Resetting conn. ' + \
                                'Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                    elif dbtries == 0:
                        dbtries = 20
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got 20 db errors. Crashing. Error: ' + \
                                str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                        exit(1)
                    else:
                        sleep(0.2)
                    dbtries -= 1
        else:        
            startdatestamp = timezone.localtime(timezone.now()) - \
                    self.timeint
            connsuccess = False
            dbtries = 20
            while not connsuccess:
                try:
                    if self.rule.event_type:
                        events = LogEvent.objects.filter(
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
                    else:
                        events = LogEvent.objects.filter(
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
                    if dbtries == 20:
                        db.connections.close_all()
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got a db error. Resetting conn. ' + \
                                'Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                    elif dbtries == 0:
                        dbtries = 20
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got 20 db errors. Crashing. Error: ' + \
                                str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                        exit(1)
                    else:
                        sleep(0.2)
                    dbtries -= 1

        if len(events):
            # To Do: Add logic here to filter events based on match list
            if self.rule.match_list_path:
                if isfile(self.rule.match_list_path):
                    with open(self.rule.match_list_path, 'r') as f:
                        matchset = set([x.rstrip() for x in f.readlines()])
                elif isdir(self.rule.match_list_path):
                    matchset = set()
                    matchfiles = [join(
                        self.rule.match_list_path, x) for x in listdir(
                            self.rule.match_list_path) if isfile(
                                join(self.rule.match_list_path, x))]
                    for mf in matchfiles:
                        with open(mf, 'r') as f:
                            matchset.add(set([x.rstrip() for x in f.readlines()]))
                else:
                    msg = 'LogESP sentry thread for limit rule ' + \
                            self.rule.name + \
                            ' got error for match file/directory ' + \
                            self.rule.match_list_path + \
                            ' - File/dir not found'
                    syslog.syslog(syslog.LOG_ERR, msg)
            else:
                matchset = None

            if matchset:
                matchedevents = []
                # Get selected field from events, compare
                # To Do: update to include matches in part of field only
                if self.rule.match_field == 'log_source':
                    for e in events:
                        if e.log_source in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'source_host':
                    for e in events:
                        if e.source_host in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'dest_host':
                    for e in events:
                        if e.dest_host in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'source_user':
                    for e in events:
                        if e.source_user in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'target_user':
                    for e in events:
                        if e.target_user in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'command':
                    for e in events:
                        if e.command in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'interface':
                    for e in events:
                        if e.interface in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'path':
                    for e in events:
                        if e.path in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'referrer':
                    for e in events:
                        if e.referrer in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'status':
                    for e in events:
                        if e.status in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'ext0':
                    for e in events:
                        if e.ext0 in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'ext1':
                    for e in events:
                        if e.ext1 in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'ext2':
                    for e in events:
                        if e.ext2 in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'ext3':
                    for e in events:
                        if e.ext3 in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'ext4':
                    for e in events:
                        if e.ext4 in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'ext5':
                    for e in events:
                        if e.ext5 in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'ext6':
                    for e in events:
                        if e.ext6 in matchset:
                            matchedevents.append(e)
                elif self.rule.match_field == 'ext7':
                    for e in events:
                        if e.ext7 in matchset:
                            matchedevents.append(e)
                events = matchedevents


            totalevents = sum([x.aggregated_events for x in events])
            logsources = set(x.log_source for x in events)
            sourcehosts = set(x.source_host for x in events)
            desthosts = set(x.dest_host for x in events)
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
                if self.rule.event_type:
                    event.event_type = self.rule.event_type
                else:
                    event.event_type = 'all'
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
                        event.source_ids_log.set(list(events))
                        event.save()
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 20:
                            db.connections.close_all()
                            msg = 'LogESP sentry thread for limit rule ' + \
                                    self.rule.name + \
                                    ' got a db error. Resetting conn. ' + \
                                    'Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        elif dbtries == 0:
                            dbtries = 20
                            msg = 'LogESP sentry thread for limit rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Crashing. Error: ' + \
                                    str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                            exit(1)
                        else:
                            sleep(0.2)
                        dbtries -= 1
                self.lasteventid = events.latest('id').id
                if self.rule.email_alerts:
                    self.send_email_alerts(magnitude, totalevents,
                            numlogsources, numsourcehosts, numdesthosts)
                self.justfired = True
            else:
                self.justfired = False
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
            connsuccess = False
            dbtries = 20
            while not connsuccess:
                try:
                    if self.rule.event_type:
                        e = RuleEvent.objects.filter(
                                id__gt=self.lasteventid,
                                event_type=self.rule.event_type,
                                source_rule__name__iregex=rulenamefilter,
                                magnitude__gte=magnitudefilter,
                                message__iregex=messagefilter)
                    else:
                        e = RuleEvent.objects.filter(
                                id__gt=self.lasteventid,
                                source_rule__name__iregex=rulenamefilter,
                                magnitude__gte=magnitudefilter,
                                message__iregex=messagefilter)
                    connsuccess = True
                except Exception as err:
                    if dbtries == 20:
                        db.connections.close_all()
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got a db error. Resetting conn. ' + \
                                'Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                    elif dbtries == 0:
                        dbtries = 20
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got 20 db errors. Crashing. Error: ' + \
                                str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                    else:
                        sleep(0.2)
                    dbtries -= 1
        else:
            startdatestamp = timezone.localtime(
                    timezone.now()) - self.timeint
            connsuccess = False
            dbtries = 20
            while not connsuccess:
                try:
                    if self.rule.event_type:
                        e = RuleEvent.objects.filter(
                                date_stamp__gt=startdatestamp,
                                event_type=self.rule.event_type,
                                source_rule__name__iregex=rulenamefilter,
                                magnitude__gte=magnitudefilter,
                                message__iregex=messagefilter)
                    else:
                        e = RuleEvent.objects.filter(
                                date_stamp__gt=startdatestamp,
                                source_rule__name__iregex=rulenamefilter,
                                magnitude__gte=magnitudefilter,
                                message__iregex=messagefilter)
                    connsuccess = True
                except Exception as err:
                    if dbtries == 20:
                        db.connections.close_all()
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got a db error. Resetting conn. ' + \
                                'Error: ' + str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                    elif dbtries == 0:
                        dbtries = 20
                        msg = 'LogESP sentry thread for limit rule ' + \
                                self.rule.name + \
                                ' got 20 db errors. Crashing. Error: ' + \
                                str(err)
                        syslog.syslog(syslog.LOG_ERR, msg)
                        exit(1)
                    else:
                        sleep(0.2)
                    dbtries -= 1

        if len(e):
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
                        event.source_ids_rule.set(list(e))
                        event.save()
                        connsuccess = True
                    except Exception as err:
                        if dbtries == 20:
                            db.connections.close_all()
                            msg = 'LogESP sentry thread for limit rule ' + \
                                    self.rule.name + \
                                    ' got a db error. Resetting conn. ' + \
                                    'Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        elif dbtries == 0:
                            dbtries = 20
                            msg = 'LogESP sentry thread for limit rule ' + \
                                    self.rule.name + \
                                    ' got 20 db errors. Crashing. Error: ' + \
                                    str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                            exit(1)
                        else:
                            sleep(0.2)
                        dbtries -= 1
                self.lasteventid = e.latest('id').id
                if self.rule.email_alerts:
                    self.send_email_alerts(magnitude, totalevents,
                            numlogsources, numsourcehosts, numdesthosts)
                self.justfired = True
            else:
                self.justfired = False
        else:
            self.justfired = False


def main(rule):
    """Initialize trigger object and start watching"""
    
    sentry = Sentry(rule)

    # Before starting, sleep randomly up to rule interval to stagger
    # database use:
    timeint = int(rule.time_int) * 60
    sleep(randrange(timeint * 2 // 3, timeint))

    sentry.watch_events()
