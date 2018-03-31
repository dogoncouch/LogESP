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

from time import sleep
from django.utils import timezone
from siem.models import LogEvent, RuleEvent


def clean(local=False):
    """Delete EOL events"""
    if local:
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                logevents = LogEvent.objects.filter(
                        eol_date_local__lte=timezone.localtime(
                            timezone.now()).date())
                connsuccess = True
            except Exception:
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP cleaner got 20 db errors. Error: ' + \
                            str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                dbtries -= 1
                sleep(0.2)
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                ruleevents = RuleEvent.objects.filter(
                        eol_date_local__lte=timezone.localtime(
                            timezone.now()).date())
                connsuccess = True
            except Exception:
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP cleaner got 20 db errors. Error: ' + \
                            str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                dbtries -= 1
                sleep(0.2)
    else:
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                logevents = LogEvent.objects.filter(
                        eol_date_backup__lte=timezone.localtime(
                            timezone.now()).date())
                connsuccess = True
            except Exception:
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP cleaner got 20 db errors. Error: ' + \
                            str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                dbtries -= 1
                sleep(0.2)
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                ruleevents = RuleEvent.objects.filter(
                        eol_date_backup__lte=timezone.localtime(
                            timezone.now()).date())
                connsuccess = True
            except Exception:
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP cleaner got 20 db errors. Error: ' + \
                            str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                dbtries -= 1
                sleep(0.2)
    
    for e in logevents:
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                e.delete()
                connsuccess = True
            except Exception:
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP cleaner got 20 db errors. Error: ' + \
                            str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                dbtries -= 1
                sleep(0.2)
    for e in ruleevents:
        connsuccess = False
        dbtries = 20
        while not connsuccess:
            try:
                e.delete()
                connsuccess = True
            except Exception:
                if dbtries == 0:
                    dbtries = 20
                    msg = 'LogESP cleaner got 20 db errors. Error: ' + \
                            str(err)
                    syslog.syslog(syslog.LOG_ERR, msg)
                dbtries -= 1
                sleep(0.2)
