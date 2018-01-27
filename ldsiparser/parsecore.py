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
import ldsiparser.parse
import sys
import os.path
from configparser import ConfigParser
from threading import Thread
from time import sleep


class ParseCore:

    def __init__(self, config='config/parser.conf'):
        """Initialize live parser"""
        self.conf = config
        self.threads = []
        signal.signal(signal.SIGTERM, self.sigterm_handler)


    def sigterm_handler(self, signal, frame):
        """Exit cleanly on sigterm"""
        exit(0)


    def get_config(self):
        """Read the config file"""

        config = ConfigParser()
        myconf = self.conf
        config.read(myconf)

        self.plist = []

        for sec in config.sections():
            p = {}
            p['filename'] = config.get(sec, 'filename')
            p['event_type'] = config.get(sec, 'event_type')
            try:
                p['parser'] = config.get(sec, 'parser')
            except Exception:
                p['parser'] = 'syslog'
            self.plist.append(p)

    
    def run_parse(self, conf=None):
        """Run the parser"""
        try:
            self.get_config()
            for entry in self.plist:
                thread = Thread(name=parse,
                        target=ldsiparser.parse.start_parse,
                        args=(entry))
                thread.daemon = True
                thread.start()
                self.threads.append(thread)

                while True:
                    isAlive = False
                    for thread in self.threads:
                        if thread.isAlive():
                            isAlive=True
                    if not isAlive: exit(0)
                    sleep(10)

        except KeyboardInterrupt:
            pass
        # except Exception as err:
        #     print('Error: ' + str(err))


    
def parse(conf='config/parser.conf'):
    parser = ParseCore(config=conf)
    parser.run_parse()
