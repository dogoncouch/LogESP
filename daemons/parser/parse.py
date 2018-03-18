#!/usr/bin/env python

# MIT License
# 
# Copyright (c) 2018 Dan Persons (dpersonsdev@gmail.com)
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
import socket
import re
import os.path
import json
import syslog

from django.utils import timezone
#import daemons.parser.parsers
from daemons.parser.parser import ParseModule
from siem.models import LogEvent
from ldsi.settings import TIME_ZONE

class LiveParser:

    def __init__(self):
        """Initialize live parser"""
        self.parser = None
        syslog.openlog(facility=syslog.LOG_DAEMON)


    def parse_entries(self, filename):
        """Parse log entries from a file like object"""
        # Get hostname, file name, tzone:
        
        with open(filename, 'r') as inputfile:
            filectime = os.path.getctime(filename)
        
            # Read to the end of the file:
            inputfile.read()
            
            while True:
                # Check for a new line:
                line = inputfile.readline()
        
                if line:
                    # Do the parsing
                    ourline = line.rstrip()
                    
                    entry = self.parser.parse_line(ourline)

                    #if entry:
                    e = LogEvent()
                    e.parsed_at = timezone.localtime(timezone.now())
                    e.time_zone = entry['time_zone']
                    e.eol_date_local = timezone.localtime(
                            timezone.now()).date() + \
                                    self.locallifespandelta
                    e.eol_date_backup = timezone.localtime(
                            timezone.now()).date() + \
                                    self.backuplifespandelta
                    e.event_type = entry['event_type']
                    e.date_stamp = entry['date_stamp']
                    e.raw_text = entry['raw_text']
                    if entry['facility']:
                        e.facility = entry['facility']
                    else:
                        e.facility = self.facility
                    e.severity = entry['severity']
                    e.log_source = entry['log_source']
                    e.aggregated_events = entry['aggregated_events']
                    e.source_host = entry['source_host']
                    e.source_port = entry['source_port']
                    e.dest_host = entry['dest_host']
                    e.dest_port = entry['dest_port']
                    e.source_process = entry['source_process']
                    e.source_pid = entry['source_pid']
                    e.action = entry['action']
                    e.command = entry['command']
                    e.protocol = entry['protocol']
                    e.packet_count = entry['packet_count']
                    e.byte_count = entry['byte_count']
                    e.tcp_flags = entry['tcp_flags']
                    e.class_of_service = entry['class_of_service']
                    e.interface = entry['interface']
                    e.start_time = entry['start_time']
                    e.duration = entry['duration']
                    e.message = entry['message']
                    e.source_user = entry['source_user']
                    e.target_user = entry['target_user']
                    e.sessionid = entry['sessionid']
                    e.ext0 = entry['ext0']
                    e.ext1 = entry['ext1']
                    e.ext2 = entry['ext2']
                    e.ext3 = entry['ext3']
                    e.ext4 = entry['ext4']
                    e.ext5 = entry['ext5']
                    e.ext6 = entry['ext6']
                    e.ext7 = entry['ext7']
                    e.parsed_on = entry['parsed_on']
                    e.source_path = entry['source_path']
                    while not connsuccess:
                        try:
                            e.save()
                            connsuccess = True
                        except Exception:
                            msg = 'LDSI parser thread for ' + filename + \
                                    ' got db error. Error: ' + err
                            syslog.syslog(syslog.LOG_ERR, msg)
                            sleep(0.2)

                else:
                    # Check if file has been rotated:
                    if os.path.getctime(filename) != filectime:
                        break
                    sleep(0.1)


    def parse_file(self, parseinfo):
            #self, filename, parser, eventtype,
            #locallifespan, backuplifespan, facility):
        """Parse a file into ldsi"""
        self.facility = parseinfo['facility']
        # Set EOL time delta:
        if parseinfo['local_lifespan_days'] == 0:
            self.locallifespandelta = timedelta(days=36524)
        else:
            self.locallifespandelta = \
                    timedelta(days=parseinfo['local_lifespan_days'])
        if parseinfo['backup_lifespan_days'] == 0:
            self.backuplifespandelta = timedelta(days=36524)
        else:
            self.backuplifespandelta = \
                    timedelta(days=parseinfo['backup_lifespan_days'])
        self.parsepath = os.path.abspath(parseinfo['filename'])
        self.parsehost = socket.getfqdn()
        self.parser = ParseModule(parseinfo['parser'],
                parseinfo['event_type'],
                TIME_ZONE,
                self.parsepath, self.parsehost,
                parsehelpers=parseinfo['parse_helpers'])
        try:
            while True:
                self.parse_entries(parseinfo['filename'])

        except KeyboardInterrupt:
            pass
        except Exception as err:
            msg = 'LDSI parser thread for ' + self.parsepath + \
                    ' crashing. Error: ' + str(err)
            syslog.syslog(syslog.LOG_ERR, msg)


def start_parse(parseinfo):
    """Start a parser"""
    parseengine = LiveParser()
    parseengine.parse_file(parseinfo)
