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


def get_blank_entry():
    """Return a blank entry dictionary"""
    # Create empty entry:
    entry = {}

    entry['date_stamp'] = ''
    entry['time_zone'] = ''
    entry['event_type'] = ''
    entry['raw_text'] = ''
    entry['facility'] = None
    entry['severity'] = None
    entry['log_source'] = ''
    entry['aggregated_events'] = 1
    entry['source_host'] = ''
    entry['source_port'] = ''
    entry['source_process'] = ''
    entry['action'] = ''
    entry['command'] = ''
    entry['source_pid'] = None
    entry['dest_host'] = ''
    entry['dest_port'] = ''
    entry['protocol'] = ''
    entry['packet_count'] = None
    entry['byte_count'] = None
    entry['tcp_flags'] = None
    entry['class_of_service'] = None
    entry['interface'] = ''
    entry['status'] = ''
    entry['start_time'] = ''
    entry['duration'] = ''
    entry['source_user'] = ''
    entry['target_user'] = ''
    entry['sessionid'] = ''
    entry['path'] = ''
    entry['parameters'] = ''
    entry['referrer'] = ''
    entry['message'] = ''
    entry['ext0'] = ''
    entry['ext1'] = ''
    entry['ext2'] = ''
    entry['ext3'] = ''
    entry['ext4'] = ''
    entry['ext5'] = ''
    entry['ext6'] = ''
    entry['ext7'] = ''

    return entry

def check_entry(entry):
    """Sanity check entry fields for length, type"""
    # Convert integer fields:
    entry['aggregated_events'] = int(entry['aggregated_events'])
    if entry['facility']:
        entry['facility'] = int(entry['facility'])
    else: entry['facility'] = None
    if entry['severity']:
        entry['severity'] = int(entry['severity'])
    else: entry['severity'] = None
    if entry['source_pid']:
        entry['source_pid'] = int(entry['source_pid'])
    else: entry['source_pid'] = None
    if entry['packet_count']:
        entry['packet_count'] = int(entry['packet_count'])
    else: entry['packet_count'] = None
    if entry['byte_count']:
        entry['byte_count'] = int(entry['byte_count'])
    else: entry['byte_count'] = None
    if entry['tcp_flags']:
        entry['tcp_flags'] = int(entry['tcp_flags'])
    else: entry['tcp_flags'] = None
    if entry['class_of_service']:
        entry['class_of_service'] = int(entry['class_of_service'])
    else: entry['class_of_service'] = None
    
    # Truncate fields to avoid errors:
    if len(entry['date_stamp']) > 32:
        entry['date_stamp'] = entry['date_stamp'][:32]
    if len(entry['time_zone']) > 32:
        entry['time_zone'] = entry['time_zone'][:32]
    if len(entry['event_type']) > 24:
        entry['event_type'] = entry['event_type'][:24]
    if len(entry['raw_text']) > 1280:
        entry['raw_text'] = entry['raw_text'][:1280]
    if len(entry['log_source']) > 32:
        entry['log_source'] = entry['log_source'][:32]
    if entry['facility'] and not 0 <= entry['facility'] < 24:
        entry['facility'] = None
    if entry['severity'] and not 0 <= entry['severity'] < 8:
        entry['severity'] = None
    #if entry['aggregated_events'] > :
    #    entry[''] = entry[''][:]
    if len(entry['source_host']) > 32:
        entry['source_host'] = entry['source_host'][:32]
    if len(entry['source_port']) > 8:
        entry['source_port'] = entry['source_port'][:8]
    if len(entry['dest_host']) > 32:
        entry['dest_host'] = entry['dest_host'][:32]
    if len(entry['dest_port']) > 8:
        entry['dest_port'] = entry['dest_port'][:8]
    if len(entry['source_process']) > 24:
        entry['source_process'] = entry['source_process'][:24]
    #if entry['source_pid'] > :
    #    entry[''] = entry[''][:]
    if len(entry['action']) > 48:
        entry['action'] = entry['action'][:48]
    if len(entry['command']) > 64:
        entry['command'] = entry['command'][:64]
    if len(entry['protocol']) > 12:
        entry['protocol'] = entry['protocol'][:12]
    #if entry['packet_count'] > :
    #    entry[''] = entry[''][:]
    #if entry['byte_count'] > :
    #    entry[''] = entry[''][:]
    #if entry['tcp_flags'] > :
    #    entry[''] = entry[''][:]
    #if entry['class_of_service'] > :
    #    entry[''] = entry[''][:]
    if len(entry['interface']) > 32:
        entry['interface'] = entry['interface'][:32]
    if len(entry['status']) > 24:
        entry['status'] = entry['status'][:24]
    if len(entry['start_time']) > 32:
        entry['start_time'] = entry['start_time'][:32]
    if len(entry['duration']) > 32:
        entry['duration'] = entry['duration'][:32]
    if len(entry['source_user']) > 32:
        entry['source_user'] = entry['source_user'][:32]
    if len(entry['target_user']) > 32:
        entry['target_user'] = entry['target_user'][:32]
    if len(entry['sessionid']) > 24:
        entry['sessionid'] = entry['sessionid'][:24]
    if len(entry['path']) > 384:
        entry['path'] = entry['path'][:384]
    if len(entry['parameters']) > 384:
        entry['parameters'] = entry['parameters'][:384]
    if len(entry['referrer']) > 400:
        entry['referrer'] = entry['referrer'][:400]
    if len(entry['message']) > 1024:
        entry['message'] = entry['message'][:1024]
    if len(entry['ext0']) > 192:
        entry['ext0'] = entry['ext0'][:192]
    if len(entry['ext1']) > 192:
        entry['ext1'] = entry['ext1'][:192]
    if len(entry['ext2']) > 45:
        entry['ext2'] = entry['ext2'][:45]
    if len(entry['ext3']) > 45:
        entry['ext3'] = entry['ext3'][:45]
    if len(entry['ext4']) > 45:
        entry['ext4'] = entry['ext4'][:45]
    if len(entry['ext5']) > 45:
        entry['ext5'] = entry['ext5'][:45]
    if len(entry['ext6']) > 45:
        entry['ext6'] = entry['ext6'][:45]
    if len(entry['ext7']) > 45:
        entry['ext7'] = entry['ext7'][:45]
    if len(entry['parsed_on']) > 32:
        entry['parsed_on'] = entry['parsed_on'][:32]
    if len(entry['source_path']) > 200:
        entry['source_path'] = entry['source_path'][:200]

    return entry
