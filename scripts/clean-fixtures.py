#!/usr/bin/env python

# MIT License
# 
# Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
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

from argparse import ArgumentParser
from argparse import FileType
import re


__version__ = '0.1'


class CleanFixtureCore:

    def __init__(self):
        """Initialize a total waste of CPU time"""

        self.args = None
        self.arg_parser = ArgumentParser()


    def get_args(self):
        """Set argument options"""

        self.arg_parser.add_argument('--version', action = 'version',
                version = '%(prog)s ' + str(__version__))
        self.arg_parser.add_argument('files',
                metavar='FILE', nargs = '*',
                help = ('set a file from which to erase primary keys'))

        self.args = self.arg_parser.parse_args()


    def clean_fixtures(self):
        """Clean primary keys from fixtures file"""
        rex = re.compile(r'^  "pk": \d+,')

        for fi in self.args.files:
            with open(fi, 'r') as f:
                content = f.readlines()
            newcontent = []
            for line in content:
                if not rex.match(line):
                    newcontent.append(line)
            with open(fi, 'w') as f:
                f.write(''.join(newcontent))



    def run_script(self):
        """Run the program"""
        try:
            self.get_args()
            self.clean_fixtures()

        except KeyboardInterrupt:
            print('\nExiting on KeyboardInterrupt')

        #except Exception as err:
        #    print('Error: ' + str(err))

    
    
def main():
    thing = CleanFixtureCore()
    thing.run_script()


if __name__ == "__main__":
    thing = CleanFixtureCore()
    thing.run_script()
