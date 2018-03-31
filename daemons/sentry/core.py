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
import syslog
from time import sleep
from daemons.sentry.rules import __all__ as ruletype_list


class SentryMgrCore:

    def __init__(self):
        """Initialize sentry core"""
        self.rule_types = {}
        self.threads = {}
        syslog.openlog(facility=syslog.LOG_DAEMON)


    def load_rule_types(self):
        """Load all sentry rule types"""
        for ruletype in sorted(ruletype_list):
            self.rule_types[ruletype] = \
                    __import__('daemons.sentry.rules.' + ruletype + '.core',
                            globals(), locals(), ['sentry'])


    def start_rule_types(self):
        """Start all sentry rule types"""
        for t in self.rule_types:
            s = threading.Thread(name=t,
                    target=self.rule_types[t].main())
            s.daemon = True
            s.start()
            self.threads[t] = s


    def watch_rule_types(self):
        """Monitor rule types for crashes"""
        while True:
            for t in self.threads:
                if not self.threads[t].isAlive():
                    msg = 'LogESP rule sentry thread for rule type ' + \
                            t + ' has crashed'
                    syslog.syslog(syslog.LOG_ERR, msg)
            sleep(120)


    def run_sentry(self):
        """Start sentry engine"""
        try:
            self.load_rule_types()
            self.start_rule_types()
            self.watch_rule_types()
        except KeyboardInterrupt:
            exit(0)
        except Exception as err:
            msg = 'LogESP core sentry thread crashing. Error: ' + str(err)
            syslog.syslog(syslog.LOG_ERR, msg)

    
def main():
    sentry = SentryMgrCore()
    sentry.run_sentry()
