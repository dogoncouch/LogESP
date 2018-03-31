# Parsing Documentation

LogESP (c) 2018 Dan Persons | [MIT License](../LICENSE)

- [Parse Daemon](#parse-daemon)
- [Event Parsing](#event-parsing)
    - [Parsers](#parsers)
    - [Parse Helpers](#parse-helpers)
- [Configuration](#configuration)

## Parse Daemon
The parse daemon is the program that parses log files into log events in the LogESP database. The files it parses are defined in the parser configuration file, at config/parser.conf in the repository. This configuration file also defines which event type to assign to events, which parser to use, the lifespan of the events, and optionally which parse helper type to use, and which syslog facility to assign.

For more on running the parse daemon, see the [daemon documentation](daemons.md).

## Event Parsing
The parse daemon parses events using instructions from a parser, and optionally a group of parse helpers. The parser parses basic fields that are present in all events in the file being parsed, and parse helpers can be used to parse extra fields that aren't present in every single event.

### Parsers
Parsers provide the parse daemon with instructions for parsing fields from events. Along with a name and description, parsers contain sets of matching information. Each set consists of a regular expression, and a comma-separated list of fields pulled by that regular expression. The fields can be any log event attribute (e.g. `source_host`, `dest_host`, `target_user`; see [Anatomy of a Log Event](events.md/#anatomy-of-a-log-event))

Each parser can have two sets of regex/field pairs: a primary, and a backup. If the primary regular expression doesn't find a match, the backup will be tried.

### Parse helpers
Parse helpers contain a regular expression and a comma-separated list of fields, similar to a parser. After parsing the main fields, the parse daemon tries each parse helper (of the helper type defined in the config file). If it finds a match, it pulls out extra fields; if not, it just moves on. Parse helpers are useful for parsing regular expressions and fields that aren't present in every single event.

## Configuration
The parser configuration file at `config/parser.conf` has one section per file. Here is an example section:

```
[auth]
filename=/var/log/auth.log
event_type=auth
parser=syslog
helper_type=auth
local_lifespan_days=185
backup_lifespan_days=366
```

- The section name must be unique, and should be meaningful; it is used in parser error logs.
- `filename` - the file to follow
- `event_type` - the `event_type` to set for parsed events
- `parser` - the parser to use when parsing events
- `helper_type` - the type of parse helpers to use for additional fields
- `local_lifespan_days` - the lifespan, in days, for the locally stored copy
- `backup_lifespan_days` - the lifespan, in days, for the backup copy

A few more settings are available, in addition to the ones used above:

- `log_source` - for logs that don't indicate the originating host (e.g. web access logs)
- `source_process` - `source_process` to assign to all events
- `facility` - sets the syslog facility (0-23)
