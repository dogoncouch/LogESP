# Event Documentation

LogESP (c) 2018 Dan Persons | [MIT License](../LICENSE)

- [Anatomy of a Log Event](#anatomy-of-a-log-event)
- [Anatomy of a Rule Event](#anatomy-of-a-rule-event)

## Anatomy of a Log Event
Log events have the following attributes that can be parsed using parser fields:
```
Attribute
Name                Description
-------------------------------
date_stamp          A string representing the date stamp.
log_source          The log source from which the event originated.
facility            The syslog facility of the event (0-23).
severity            The syslog severity of the event (0-7).
aggregated_events   The number of aggregated events represented.
source_host         The source host (IP, FQDN, etc).
source_port         The source port (i.e. 443, https, smtp, etc).
dest_host           The destination host.
dest_port           The destination port.
source_process      The source process.
source_pid          The source process ID.
action              The action being taken.
command             The command being executed.
protocol            The protocol involved in the event (ssh, https, etc).
packet_count        The number of packets involved (for flows).
byte_count          The number of bytes involved.
tcp_flags           The TCP flags (an integer).
class_of_service    The ToS (type of service) field (an integer).
interface           The network interface involved.
status              The status (interface status, http status code, etc).
start_time          A string representing the start time (for flows, videos, motion sensor events).
duration            A string representing the duration.
source_user         The user who initiated the event.
target_user         The user targeted in the event.
sessionid           The session ID of the session involved in the event.
path                The URI or file path
parameters          The parameters (web server logs, etc).
referrer            The referrer (web server logs, etc).
message             The message conveyed.
ext0                A field meant to be defined by the user.
ext1                A field meant to be defined by the user.
ext2                A field meant to be defined by the user.
ext3                A field meant to be defined by the user.
ext4                A field meant to be defined by the user.
ext5                A field meant to be defined by the user.
ext6                A field meant to be defined by the user.
ext7                A field meant to be defined by the user.
```
In addition, log events have the following fields that are not defined by the parser and parse helpers:
```
Attribute
Name            Description
---------------------------
parsed_at           The time the event was parsed (a datetime object, with 6 decimal places).
time_zone           The time zone associated with the parsed_at datetime object.
parsed_on           The hostname of the system on which the event was parsed.
source_path         The full path of the file from which the event originated.
event_type          The event type defined by the parser configuration.
eol_date_local      Event end-of-life date in the LogESP database.
eol_date_backup     Event end-of-life date for backup copies.
raw_text            The entire raw text of the event.
```

### Anatomy of a Rule Event
Rule events have the following attributes:
```
Attribute
Name                Description
-------------------------------
date_stamp          A datetime object representing the rule event was created.
time_zone           The time zone associated with the date_stamp datetime object.
source_rule         The rule that created the event.
rule_category       The rule category of the rule broken.
event_type          The event type being monitored by the rule.
severity            The severity of the rule.
event_limit         The event limit for the rule.
event_count         The number of events involved.
magnitude           The magnitude of the rule event.
time_int            The time interval at which the rule is checked.
source_ids_log      The source IDs of the log events involved.
source_ids_rule     The source IDs of the rule events involved.
log_source_count    The number of different log sources involved.
source_host_count   The number of different source hosts involved.
dest_host_count     The number of different destination hosts involved.
message             The message conveyed by the rule.
eol_date_local      Event end-of-life date in the LogESP database
eol_date_backup     Event end-of-life date for backup copies
```
For more on how magnitude is calculated, see the [rule documentation](rules.md).
