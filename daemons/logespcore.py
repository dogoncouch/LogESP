# MIT License
# 
# Copyright (c) 2018 Dan Persons <dpersonsdev@gmail.com>
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
# 

import daemons.parser.core
import daemons.sentry.core
from threading import Thread
import syslog
import signal
from sys import exit
from time import sleep

from django.db.utils import OperationalError
from siem.models import LogEvent

class DaemonCore:
    def __init__(self):
        """Initialize daemon core object"""
        # Open our log facility:
        syslog.openlog(facility=syslog.LOG_DAEMON)

    def sigterm_handler(self, signal, frame):
        """Exit cleanly on sigterm"""
        msg = 'LogESP Daemon received sigterm, exiting'
        syslog.syslog(syslog.LOG_INFO, msg)
        sleep(0.2)
        exit(0)

    def sighup_handler(self, signal, frame):
        """Exit cleanly so restart can happen on sighup"""
        msg = 'LogESP Daemon received sighup, restarting'
        syslog.syslog(syslog.LOG_INFO, msg)
        sleep(0.2)
        exit(1)

    def sigint_handler(self, signal, frame):
        """Exit cleanly on sigint"""
        msg = 'LogESP daemon received sigint, exiting'
        syslog.syslog(syslog.LOG_INFO, msg)
        sleep(0.2)
        exit(0)

    def start(self, runparser=True, runsentry=True):
        """Start parser and sentry engines"""
        # Handle signals:
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGHUP, self.sighup_handler)
        signal.signal(signal.SIGINT, self.sigint_handler)

        # Wait for database:
        dbconnection = False
        while not dbconnection:
            try:
                x = LogEvent.objects.last()
                dbconnection = True
                del(x)
            except OperationalError:
                pass

        if runparser:
            # Start parser threads:
            parser = Thread(name='parser',
                    target=daemons.parser.core.main)
            parser.daemon = True
            parser.start()
        if runsentry:
            # Start sentry threads:
            sentry = Thread(name='sentry',
                    target=daemons.sentry.core.main)
            sentry.daemon = True
            sentry.start()

        # Log start:
        sleep(0.2)
        syslog.syslog(syslog.LOG_INFO, 'LogESP Daemon has started')

        while True:
            if runparser and not parser.isAlive():
                msg = 'LogESP parser has crashed!'
                syslog.syslog(syslog.LOG_ALERT, msg)
            if runsentry and not sentry.isAlive():
                msg = 'LogESP sentry has crashed!'
                syslog.syslog(syslog.LOG_ALERT, msg)
            sleep(120)

if __name__ == "__main__":
    main()

def main(parser=True, sentry=True):
    daemoncore = DaemonCore()
    daemoncore.start(runparser=parser, runsentry=sentry)
