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

import daemons.parser.parsecore
import daemons.sentry.sentrycore
from threading import Thread
import syslog
import signal
from sys import exit
from time import sleep


class DaemonCore:
    def __init__(self):
        """Initialize daemon core object"""
        # Open our log facility:
        syslog.openlog(facility=syslog.LOG_DAEMON)

    def sigterm_handler(self, signal, frame):
        """Exit cleanly on sigterm"""
        syslog.syslog(syslog.LOG_INFO, 'LDSI Daemon received sigterm, exiting')
        exit(0)

    def sighup_handler(self, signal, frame):
        """Exit cleanly so restart can happen on sighup"""
        syslog.syslog(syslog.LOG_INFO, 'LDSI Daemon received sighup, restarting')
        exit(1)

    def sigint_handler(self, signal, frame):
        """Exit cleanly on sigint"""
        syslog.syslog(syslog.LOG_INFO, 'LDSI Daemon received sigint, exiting')
        exit(0)

    def start(self):
        """Start parser and sentry engines"""
        # Log start:
        syslog.syslog(syslog.LOG_INFO, 'LDSI Daemon has started')

        # Handle signals:
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        signal.signal(signal.SIGHUP, self.sighup_handler)
        signal.signal(signal.SIGINT, self.sigint_handler)

        # Start parser and sentry threads:
        parser = Thread(name='parser', target=daemons.parser.parsecore.start)
        sentry = Thread(name='sentry', target=daemons.sentry.sentrycore.start)
        parser.daemon = True
        sentry.daemon = True

        parser.start()
        sentry.start()

        while True:
            if not parser.isAlive():
                syslog.syslog(syslog.LOG_ALERT, 'LDSI parser has crashed!')
            if not sentry.isAlive():
                syslog.syslog(syslog.LOG_ALERT, 'LDSI sentry has crashed!')
            sleep(120)

if __name__ == "__main__":
    daemoncore = DaemonCore()
    daemoncore.start()

def main():
    daemoncore = DaemonCore()
    daemoncore.start()
