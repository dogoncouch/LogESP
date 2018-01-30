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
import os
from sys import exit
from configparser import ConfigParser
import json
import signal
from time import sleep
import daemonssentry.sentry
from siem.models import LimitRule


class SentryCore:

    def __init__(self):
        """Initialize trigger engine"""
        self.rlist = []
        self.rules = []
        self.newrules = []
        self.threads = {}
        signal.signal(signal.SIGTERM, self.sigterm_handler)


    def sigterm_handler(self, signal, frame):
        """Exit cleanly on sigterm"""
        exit(0)


    def get_rules(self):
        """Get rules from tables"""
        rules = LimitRule.objects.all()
        for r in rules:
            if not r.id in self.rules:
                self.newrules.append(r)
        self.rules = [r.id for r in rules]
        

    def start_triggers(self):
        """Start siemstress event triggers"""
        # Start one thread per rule:
        for r in self.newrules:
            thread = threading.Thread(name=r.id,
                    target=daemons.sentry.sentry.start_rule,
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
                sleep(600)

        except KeyboardInterrupt:
            exit(0)
        #except Exception as err:
        #    exit(0)
        #    print('Error: ' + str(err))

    
def start():
    sentry = SentryCore()
    sentry.run_sentry()
