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

class ParseModule:
    def __init__(self):
        """Initialize the syslog ISODATE parsing module"""
        self.name = 'syslogiso'
        self.desc = 'syslog ISODATE parsing module'
        self.date_format = \
                re.compile(r"^(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.?\d+?[+-]\d\d:?\d\d\s+\S+\s+\S+\[?\d*?\]?):")

    def parse_line(self, line):
        """Parse a syslog line (with ISO 8601 timestamp) into a dictionary"""
        match = re.findall(self.date_format, line)
        if match:
            attr_list = str(match[0]).split(' ')
            try:
                attr_list.remove('')
            except ValueError:
                pass
            
            # Set our attributes:
            datestamp = attr_list[0]
            
            sourceproclist = attr_list[2].split('[')
            if len(sourceproclist) > 1:
                sourcepid = sourceproclist[1].strip(']')
            else: sourcepid = None
            
            entry = {}
            entry['date_stamp'] = datestamp
            entry['facility'] = None
            entry['severity'] = None
            entry['source_host'] = attr_list[1]
            entry['source_port'] = ''
            entry['dest_host'] = ''
            entry['dest_port'] = ''
            entry['protocol'] = ''
            entry['source_process'] = sourceproclist[0]
            entry['source_pid'] = sourcepid
            entry['message'] = line[len(match[0]) + 2:]
            entry['extended'] = ''
            entry['ext_user'] = ''
            entry['ext_ip'] = ''
            entry['ext_session'] = ''

            return entry
        

        else: return None
