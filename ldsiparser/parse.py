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

import ldsiparser.parsers
import time.sleep
from datetime import datetime
import re
import sqlite3 as mydb
import json



class LiveParser:

    #def __init__(self, db, helpers):
    def __init__(self, db):
        """Initialize live parser"""

        self.parser = None
        self.db = db
        self.table = table
        #self.helpers = helpers


    def get_parser(self, parsername):
        """Load the parser"""

        if parsername == 'syslogbsd':
            self.parser = ldsiparser.parsers.syslogbsd.ParseModule()
        elif parsername == 'syslogiso':
            self.parser = ldsiparser.parsers.syslogiso.ParseModule()
        elif parsername == 'nohost':
            self.parser = ldsiparser.parsers.nohost.ParseModule()


    def parse_entries(self, inputfile):
        """Parse log entries from a file like object"""

        # Get hostname, file name, tzone:
        parsepath = os.path.abspath(inputfile.name)
        parsehost = socket.getfqdn()

        # Read to the end of the file:
        inputfile.read()
        
        self.sqlstatement = 'INSERT INTO ' + self.db['table'] + \
                ' (parsed_at, date_stamp,' + \
                'time_zone, raw_text, facility, severity, source_host, ' + \
                'source_port, dest_host, dest_port, source_process, ' + \
                'source_pid, protocol, ' + \
                #'message, extended, parsed_on, source_path) VALUES ' + \
                'message, parsed_on, source_path) VALUES ' + \
                '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' + \
                '%s, %s, %s, %s, %s, %s)'
        
        #rehelpers = []
        #for h in helpers:
        #    reh = {}
        #    reh['var_name'] = h['var_name']
        #    reh['reg_exp'] = re.compile(h['reg_exp'])
        #    rehelpers.append(reh)

        is_connected = False
        
        while True:

            # Check for a new line:
            line = inputfile.readline()

            if line:
                # Do the parsing
                ourline = line.rstrip()
                
                entry = self.parser.parse_line(ourline)

                if entry:
                    parsedat = datetime.now()
                    # Parse extended attributes from helpers:
                    #extattrs = {}
                    #
                    #for h in rehelpers:
                    #    mlist = h['reg_exp'].findall(entry['message'])
                    #
                    #    try:
                    #        extattrs[h['var_name']] += mlist
                    #    except KeyError:
                    #        extattrs[h['var_name']] = mlist
                    #
                    #extattrs = json.dumps(extattrs)

                    # To Do: switch to django models

                    if not is_connected:
                        con = mydb.connect(self.db['dbfile'])
                    # Put our attributes in our table:
                    with con:
                        cur = con.cursor()
                        cur.execute(self.sqlstatement,
                                (parsedat, datestamp,
                                    entry['time_zone'], ourline, 
                                    entry['facility'], entry['severity'],
                                    entry['source_host'], entry['source_port'],
                                    entry['dest_host'], entry['dest_port'],
                                    entry['source_process'],
                                    entry['source_pid'],
                                    entry['protocol'], entry['message'],
                                    parsehost, parsepath))
                                    #extattrs, parsehost, parsepath))
                        con.commit()
                        cur.close()
                    #con.close()


                else:
                    # No match!?
                    # To Do: raise an error here.
                    print('No Match: ' + ourline)

            else:
                con.close()
                is_connected = False
                time.sleep(0.1)


    def parse_file(self, filename, parser):
        try:
            self.get_parser(parser)
            self.parse_entries(filename)

        except KeyboardInterrupt:
            pass
        # except Exception as err:
        #     print('Error: ' + str(err))


def start_parse(db, parseinfo):
    #parser = LiveParser(db, parseinfo['helpers'])
    parser = LiveParser(db)
    parser.parse_file(parseinfo['filename'], parseinfo['parser']
    
    
#def main():
#    parser = LiveParser()
#    parser.run_parse()


#if __name__ == "__main__":
#    parser = LiveParser()
#    parser.run_parse()
