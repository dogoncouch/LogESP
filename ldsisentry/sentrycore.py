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
import ldsisentry.sentry
from siem.models import LimitRule


class SentryCore:

    def __init__(self, config='ldsisentry/sentry'):
        """Initialize trigger engine"""

        self.conf = config
        self.rlist = []
        self.rules = []
        self.threads = []

        signal.signal(signal.SIGTERM, self.sigterm_handler)


    def sigterm_handler(self, signal, frame):
        """Exit cleanly on sigterm"""
        exit(0)


    def get_rules(self):
        """Get rules from tables"""

        self.rules = LimitRule.objects.filter(is_enabled=True)
        

    def start_triggers(self):
        """Start siemstress event triggers"""

        # Start one thread per rule:
        self.threads = []
        for r in self.rules:
            thread = threading.Thread(name=r,
                    target=ldsisentry.sentry.start_rule,
                    args=(r,))
            thread.daemon = True
            thread.start()

            self.threads.append(thread)


    def run_sentry(self):
        """Start trigger engine"""
        try:
            self.get_rules()
            self.start_triggers()

            while True:
                isAlive = False
                for thread in self.threads:
                    if thread.isAlive():
                        isAlive = True
                if not isAlive: exit(0)
                sleep(10)

        except KeyboardInterrupt:
            exit(0)
        #except Exception as err:
        #    exit(0)
        #    print('Error: ' + str(err))

    
def sentry(conf='ldsisentry/sentry.conf'):
    sentry = SentryCore(config=conf)
    sentry.run_sentry()
