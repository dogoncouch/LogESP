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

import threading
from sys import exit
import syslog
from time import sleep
from django import db

import daemons.sentry.rules.list.list
from siem.models import ListRule


class SentryCore:

    def __init__(self):
        """Initialize trigger engine"""
        self.rlist = []
        self.rules = []
        self.newrules = []
        self.threads = {}
        syslog.openlog(facility=syslog.LOG_DAEMON)


    def get_rules(self):
        """Get rules from tables"""
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                rules = ListRule.objects.all()
                connsuccess = True
            except ListRule.DoesNotExist:
                msg = 'LogESP sentry thread for list rule ' + self.rule.name + \
                        ' exiting. Rule no longer exists.'
                exit(0)
            except Exception:
                if dbtries == 20:
                    db.connections.close_all()
                    msg = 'LogESP parser thread for ' + filename + \
                            ' got a db error. Resetting conn. ' + \
                            'Event: ' + str(ourline[:160]) + \
                            '... Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                elif dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP sentry thread for ' + self.rule.name + \
                            ' got 20 db errors while retrieving rules. ' + \
                            'Error: ' + str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                    exit(1)
                else:
                    sleep(0.2)
                dbtries -= 1
        for r in rules:
            if not r.id in self.rules:
                self.newrules.append(r)
        self.rules = [r.id for r in rules]
        

    def start_triggers(self):
        """Start siemstress event triggers"""
        # Start one thread per rule:
        for r in self.newrules:
            thread = threading.Thread(name=r.id,
                    target=daemons.sentry.rules.list.list.start_rule,
                    args=(r,))
            thread.daemon = True
            thread.start()

            self.threads[r.id] = thread
        self.newrules = []


    def run_sentry(self):
        """Start trigger engine"""
        try:
            while True:
                self.get_rules()
                self.start_triggers()
                for t in self.threads:
                    if not self.threads[t].isAlive():
                        msg = 'LogESP sentry thread for list rule id ' + \
                                str(t) + 'has crashed'
                        syslog.syslog(syslog.LOG_ERR, msg)
                sleep(120)

        except KeyboardInterrupt:
            exit(0)
        except Exception as err:
            msg = 'LogESP sentry core list rule thread crashing. Error: ' + \
                    str(err)
            syslog.syslog(syslog.LOG_ERR, msg)

    
def main():
    sentry = SentryCore()
    sentry.run_sentry()
