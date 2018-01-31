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

from django.utils import timezone
import daemons.parser.parsers
from siem.models import LogEvent
from ldsi.settings import TIME_ZONE

class LiveParser:

    def __init__(self):
        """Initialize live parser"""
        self.parser = None


    def get_parser(self, parser):
        """Load parser modules"""
        parsers = {}
        for p in sorted(daemons.parser.parsers.__all__):
            parsers[p] = \
                    __import__('daemons.parser.parsers.' + p, globals(),
                            locals(), [daemons.parser]).ParseModule()
        
        self.parser = parsers[parser]


    def parse_entries(self, filename, eventtype):
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

                    if entry:
                        e = LogEvent()
                        e.parsed_at = timezone.localtime(timezone.now())
                        e.time_zone = TIME_ZONE
                        e.eol_date_local = timezone.localtime(
                                timezone.now()).date() + \
                                        self.locallifespandelta
                        e.eol_date_backup = timezone.localtime(
                                timezone.now()).date() + \
                                        self.backuplifespandelta
                        e.event_type = eventtype
                        e.date_stamp = entry['date_stamp']
                        e.raw_text = ourline
                        e.facility = entry['facility']
                        e.severity = entry['severity']
                        e.source_host = entry['source_host']
                        e.source_port = entry['source_port']
                        e.dest_host = entry['dest_host']
                        e.dest_port = entry['dest_port']
                        e.source_process = entry['source_process']
                        e.source_pid = entry['source_pid']
                        e.protocol = entry['protocol']
                        e.message = entry['message']
                        e.extended = entry['extended']
                        e.ext_user = entry['ext_user']
                        e.ext_ip = entry['ext_ip']
                        e.ext_session = entry['ext_session']
                        e.parsed_on = self.parsehost
                        e.source_path = self.parsepath
                        e.save()
        
                    else:
                        # No match
                        e = LogEvent()
                        e.parsed_at = timezone.localtime(timezone.now())
                        e.time_zone = TIME_ZONE
                        e.eol_date = timezone.localtime(
                                timezone.now()).date() + \
                                        self.lifespandelta
                        e.event_type = eventtype
                        e.raw_text = ourline
                        e.parsed_on = self.parsehost
                        e.source_path = self.parsepath
        
                else:
                    # Check if file has been rotated:
                    if os.path.getctime(filename) != filectime:
                        break
                    sleep(0.1)


    def parse_file(self, filename, parser, eventtype,
            locallifespan, backuplifespan):
        """Parse a file into ldsi"""
        # Set EOL time delta:
        if locallifespan == 0:
            self.locallifespandelta = timedelta(days=36524)
        else:
            self.locallifespandelta = \
                    timedelta(days=locallifespan)
        if backuplifespan == 0:
            self.backuplifespandelta = timedelta(days=36524)
        else:
            self.backuplifespandelta = \
                    timedelta(days=backuplifespan)
        self.get_parser(parser)
        self.parsepath = os.path.abspath(filename)
        self.parsehost = socket.getfqdn()
        try:
            while True:
                self.parse_entries(filename, eventtype)

        except KeyboardInterrupt:
            pass
        # except Exception as err:
        #     print('Error: ' + str(err))


def start_parse(filename, parser, eventtype, locallifespan, backuplifespan):
    """Start a parser"""
    parseengine = LiveParser()
    parseengine.parse_file(filename, parser, eventtype,
            locallifespan, backuplifespan)
