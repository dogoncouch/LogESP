# Rule Documentation

LogESP (c) 2018 Dan Persons | [MIT License](../LICENSE)

- [Sentry Daemon](#sentry-daemon)
- [Limit Rules](#limit-rules)
    - [Rule vs. Log Events](#rule-vs-log-events)
    - [Filters](#filters)
    - [Match Lists](#match-lists)
    - [Magnitude Calculation](#magnitude-calculation)

## Sentry Daemon
The sentry daemon watches the database, checking for criteria defined by rules. If a rule's criteria are met (i.e. the rule is broken), the sentry creates a rule event (defined by the rule), and optionally emails alerts (if email has been configured).

## Limit Rules
Limit rules define a set of event criteria, an event limit, and a time interval. If the number of events that meet the criteria in a time interval is over the event limit, a rule event is created (and email alerts can be sent, if email is configured). Rules can also have a defined number of allowable log sources, and some attributes for calculating the magnitude of rule events. A severity and some modifiers that are used to calculate magnitude, based on the ratio of event count to event limit.

### Rule vs. Log Events
If a rule's `rule_events` attribute is set to True, it will monitor rule events; otherwise, it will monitor log events.

### Filters
Filters check to see if a certain field contains a certain string. They are case insensitive. If left blank, they will always match. If all of the filters in a rule are met, the rule is considered to be broken. Mostfields can use regular expressions.

Rules can filter on the following fields:
```
Field               Event
                    Type    Regex?
----------------------------------
message             Any     Yes
raw_text            Log     Yes
log_source          Log     Yes
process             Log     Yes
action              Log     Yes
command             Log     Yes
interface           Log     Yes
status              Log     Yes
source_host         Log     Yes
source_port         Log     Yes
dest_host           Log     Yes
dest_port           Log     Yes
source_user         Log     Yes
target_user         Log     Yes
path                Log     Yes
parameters          Log     Yes
referrer            Log     Yes
source_rule__name   Rule    Yes
magnitude           Rule    No
```
In addition to these filters, rule events have an optional `event_type` attribute. Event types must match exactly, if present.

### Match Lists
Rules can also compare a field in events to a file containing one item per line. Events will only be counted toward the rule if the specified field matches a line in the file (this can be reversed by setting the `match_friendlist` attribute to `True`).

To configure a match list, set the `match_list_path` attribute to the desired file or directory, and set the `match_field` attribute to the desired field. Choose from the following fields:

- `log_source`
- `source_host`
- `dest_host`
- `source_user`
- `target_user`
- `command`
- `interface`
- `path`
- `referrer`
- `status`
- `ext0`
- `ext1`
- `ext2`
- `ext3`
- `ext4`
- `ext5`
- `ext6`
- `ext7`

### Magnitude Calculation
Rule event magnitude is calculated using the following factors:

- Rule severity (0-7; 0 is the most severe)
- Event limit
- Event count
- Severity modifier
- Overkill modifier

The actual calculation:
```
((event_count / (event_limit + 1)) * overkill_modifier)

*

((8 - severity) * severity_modifier)
```
(Formatting added to aid in comprehension)
