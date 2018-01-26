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

from ldsiparser import __version__
from ldsiparser.parse import LiveParser
import sys
import os.path
from argparse import ArgumentParser
import ConfigParser


class ParseCore:

    def __init__(self, section='default'):
        """Initialize live parser"""

        self.args = None
        self.arg_parser = ArgumentParser()
        self.config = None

        self.parser = None
        self.parsername = None
        self.db = {}
        self.table = None



    def get_args(self):
        """Set argument options"""

        self.arg_parser.add_argument('--version', action = 'version',
                version = '%(prog)s ' + str(__version__))
        self.arg_parser.add_argument('-c',
                action = 'store', dest = 'config',
                default = 'config/parser.conf',
                help = ('set the config file'))

        self.args = self.arg_parser.parse_args()



    def get_config(self):
        """Read the config file"""

        config = ConfigParser.ConfigParser()
        if os.path.isfile(self.args.config):
            myconf = self.args.config
        else: myconf = 'config/parser.conf'
        config.read(myconf)

        self.plist = []

        self.db['dbfile'] = config.get('database', 'dbfile')
        
        for sec in config.sections():
            if sec != 'database':
                f = config.get(sec, 'filename')
                p = config.get(sec, 'parser')
                t = config.get(sec, 'table')
                h = config.get(sec, 'helpers')
                self.plist.append([f, p, t, h])

        try:
            self.parsername = config.get(self.args.section, 'parser')
        except Exception:
            # To Do: narrow down exception
            self.parsername = 'syslogbsd'


    def run_parse(self):
        try:
            self.get_args()
            self.get_config()
            for entry in self.plist:
                # To Do: Start background daemon processes
                parser = LiveParser(self.db, entry[2], entry[3])
                parser.parse_file(entry[0], entry[1])

        except KeyboardInterrupt:
            pass
        # except Exception as err:
        #     print('Error: ' + str(err))

    
    
def main():
    parser = ParseCore()
    parser.run_parse()


if __name__ == "__main__":
    parser = ParseCore()
    parser.run_parse()
