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
from os.path import isfile, join
from django import db
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User

from LogESP.settings import TIME_ZONE
try:
    from LogESP.settings import EMAIL_ALERT_FROM_ADDRESS
except ImportError:
    EMAIL_ALERT_FROM_ADDRESS = 'noreply@example.com'
from siem.models import LogEvent, ListRule


class ListSentry:

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
                    'list rule ' + self.rule_name
            syslog.syslog(syslog.LOG_ERR, msg)



    def watch_events(self):
        """Watch log events based on a rule"""
        self.get_first_logevent()
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
                # Refresh the rule:
                locallifespan = self.rule.local_lifespan_days
                backuplifespan = self.rule.backup_lifespan_days
                t = self.rule.time_int
                connsuccess = False
                dbtries = 20
                while not connsuccess:
                    try:
                        self.rule = ListRule.objects.get(
                                pk=self.rule.id)
                        connsuccess = True
                    except ListRule.DoesNotExist:
                        msg = 'LogESP sentry thread for list rule ' + \
                                self.rule.name + \
                                ' exiting. Rule no longer exists.'
                        syslog.syslog(syslog.LOG_NOTICE, msg)
                        exit(0)
                    except Exception:
                        if dbtries == 20:
                            db.connections.close_all()
                            msg = 'LogESP sentry thread for list rule ' + \
                                    self.rule.name + \
                                    ' got a db error. Resetting conn. ' + \
                                    'Error: ' + str(err)
                            syslog.syslog(syslog.LOG_ERR, msg)
                        elif dbtries == 0:
                            dbtries = 20
                            msg = 'LogESP sentry thread for list rule ' + \
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

                # To Do: Load set from file
                # Reload every 20 minutes or so.
                self.matchset = set()
                if self.rule.full_directory:
                    # Read all files in directory
                    pass
                else:
                    # To Do: add file_path attribute to list rules
                    if isfile(self.rule.file_path):
                        with open(self.rule.file_path, 'r') as f:
                            matchset.add(set(
                                [line.rstrip() for line in f.readlines()]))

                # Check the rule:
                if self.rule.is_enabled:
                    self.check_logevent()
                # Wait until next interval if firedr,; otherwise ~60 seconds:
                if self.justfired:
                    sleep(int(self.rule.time_int) * 60)
                else:
                    sleep(randrange(45, 60))
            except Exception as err:
                msg = 'LogESP sentry thread for list rule ' + \
                        self.rule.name + \
                        ' crashing. Error: ' + str(err)
                syslog.syslog(syslog.LOG_ERR, msg)
                exit(0)


    def check_logevent(self):
        """Check log events based on a rule"""
        
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                if self.rule.event_type:
                    events = LogEvent.objects.filter(
                            event_type=self.rule.event_type,
                            id__gt=self.lasteventid).only(
                                    self.rule.match_field, 'log_source',
                                    'aggregated_events', 'source_host',
                                    'dest_host')
                else:
                    events = LogEvent.objects.filter(
                            id__gt=self.lasteventid).only(
                                    self.rule.match_field, 'log_source',
                                    'aggregated_events', 'source_host',
                                    'dest_host')
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
                        #e = LogEvent.objects.filter(
                        #        log_source__iregex=logsourcefilter,
                        #        source_process__iregex=processfilter,
                        #        action__iregex=actionfilter,
                        #        interface__iregex=interfacefilter,
                        #        status__iregex=statusfilter,
                        #        source_host__iregex=sourcehostfilter,
                        #        source_port__iregex=sourceportfilter,
                        #        dest_host__iregex=desthostfilter,
                        #        dest_port__iregex=destportfilter,
                        #        source_user__iregex=sourceuserfilter,
                        #        target_user__iregex=targetuserfilter,
                        #        path__iregex=pathfilter,
                        #        parameters__iregex=parametersfilter,
                        #        referrer__iregex=referrerfilter,
                        #        message__iregex=messagefilter,
                        #        raw_text__iregex=rawtextfilter)

        if len(events):

            matchedevents = []
            for e in events:
                # To Do:
                # Check if field is in the set we loaded
                # if matchfield == self.rule.match_field:
                #     if not self.rule.friendlist: matchedevents.append(e)
                # else:
                #     if self.rule.friendlist: matchedevents.append(e)

            totalevents = sum([x.aggregated_events for x in matchedevents])
            logsources = {x.log_source for x in matchedevents}
            sourcehosts = {x.source_host for x in matchedevents}
            desthosts = {x.dest_host for x in matchedevents}
            try: logsources.remove(None)
            except KeyError: pass
            try: sourcehosts.remove(None)
            except KeyError: pass
            try: desthosts.remove(None)
            except KeyError: pass
            numlogsources = len(logsources)
            numsourcehosts = len(sourcehosts)
            numdesthosts = len(desthosts)


            # Begin old stuff ###########################################
            event = RuleEvent()
            event.date_stamp = timezone.localtime(timezone.now())
            event.time_zone = TIME_ZONE
            # To Do: Add rule type to rule events
            event.rule_category = self.rule.rule_category
            event.eol_date_local = timezone.localtime(
                    timezone.now()).date() + \
                            self.locallifespandelta
            event.eol_date_backup = timezone.localtime(
                    timezone.now()).date() + \
                            self.backuplifespandelta
            event.event_type = self.rule.event_type
            event.source_rule = self.rule
            # To Do: Add field_matched to rule events
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
            connsuccess = False
            dbtries = 20
            while not connsuccess:
                try:
                    event.source_ids_log.set(list(e))
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
            connsuccess = False
            dbtries = 20
            while not connsuccess:
                try:
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


def start_rule(rule):
    """Initialize trigger object and start watching"""
    
    sentry = ListSentry(rule)

    # Before starting, sleep randomly up to rule interval to stagger
    # database use:
    timeint = int(rule.time_int) * 60
    sleep(randrange(timeint * 2 // 3, timeint))

    sentry.watch_events()
