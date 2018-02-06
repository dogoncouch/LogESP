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

import re

from siem.models import LogEventParser, ParseHelper

match_regex = '^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+)\[?(\d*?)\]?:'


class ParseModule:
    def __init__(self, parser, parsehelpers=[]):
        """Initialize a parsing module"""
        self.parser = LogEventParser.objects.get(name=parser)
        self.regex_format = re.compile(r'{}'.format(self.parser.match_regex))
        if self.parser.backup_match_regex:
            self.backup_regex_format = re.compile(
                    r'{}'.format(self.parser.backup_match_regex))
        else:
            self.backup_regex_format = None
        self.fields = self.parser.fields.split(',')
        if self.parser.backup_fields:
            self.backup_fields = self.parser.backup_fields.split(',')
        else:
            self.backup_fields = None

        # Get parse helpers:
        helperobjects = [ParseHelper.objects.get(
            name=n) for n in parsehelpers]
        self.parsehelpers = []
        for h in helperobjects:
            helper = {}
            helper['name'] = h.name
            helper['regex_format'] = re.compile(
                    r'{}'.format(h.match_regex))
            helper['fields'] = h.fields.split(',')
            self.parsehelpers.append(helper)


    def parse_line(self, line):
        """Parse a line into a dictionary"""
        entry = self.match_line(self.regex_format,
                self.fields, line)
        if self.backup_regex_format and self.backup_fields and not entry:
            entry = self.match_line(self.backup_regex_format,
                    self.backup_fields, line)
        return entry

    def match_line(self, regexformat, fields, line):
        """Try matching a line with a regex format"""
        match = re.findall(regexformat, line)
        if match:
            # Create empty entry:
            entry = {}


            entry['date_stamp'] = None
            entry['facility'] = ''
            entry['severity'] = ''
            entry['log_source'] = ''
            entry['aggregated_events'] = 1
            entry['source_host'] = ''
            entry['source_port'] = ''
            entry['source_process'] = ''
            entry['action'] = ''
            entry['source_pid'] = ''
            entry['dest_host'] = ''
            entry['dest_port'] = ''
            entry['protocol'] = ''
            entry['message'] = ''
            entry['username'] = ''
            entry['sessionid'] = ''
            entry['ext0'] = ''
            entry['ext1'] = ''
            entry['ext2'] = ''
            entry['ext3'] = ''
            entry['ext4'] = ''
            entry['ext5'] = ''
            entry['ext6'] = ''
            entry['ext7'] = ''

            linelist = list(zip(fields, match[0]))

            for f, v in linelist:
                entry[f] = v

            # Parse helpers:
            for h in self.parsehelpers:
                extmatch = re.findall(h['regex_format'], line)
                if extmatch:
                    extlist = list(zip(h['fields'], extmatch[0]))
                    for f, v in extlist:
                        entry[f] = v

            # Convert integer fields:
            if entry['aggregated_events']:
                entry['aggregated_events'] = int(entry['aggregated_events'])
            else:
                entry['aggregated_events'] = 1
            if entry['facility']:
                entry['facility'] = int(entry['facility'])
            else:
                entry['facility'] = None
            if entry['severity']:
                entry['severity'] = int(entry['severity'])
            else:
                entry['severity'] = None
            if entry['source_pid']:
                entry['source_pid'] = int(entry['source_pid'])
            else:
                entry['source_pid'] = None

            return entry

        else: return None
