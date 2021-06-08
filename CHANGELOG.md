# Change log
Change log for [LogESP](https://github.com/dogoncouch/LogESP)

## [0.2-beta-r10] 2021-06-06
### Added
- systemd daemon scripts for logespd, logesp-uwsgi
- Default search window is 1 day for log events, 7 for rule events
- Log event db index for `parsed_at` field
- Rule event db index for `date_stamp` field

### Fixed
- Django version vulnerabilities
- Hang on shutdown due to uwsgi not exiting properly

### Updated
- Rule efficiency tweaks, rules no longer run every minute if not fired

## [0.2-beta-r4] - 2018-04-18
### Updated
- More security in default nginx setup
- `make update` reloads uwsgi properly
- UI color scheme is easier to look at (based on xterm-256color/vim)

### Added
- Inline documentation in SIEM templates
- Inline documentation in Risk form templates
- Inline documentation in Asset form templates
- Package vendor, more IPs to software assets

## [0.2-beta-r2] 2018-04-10
### Added
- Block/allow lists for limit rules (match lists)
- Dead process rule option for limit rules (`reverse_logic` attribute)

## [0.2-beta-r1] 2018-04-07
### Fixed
- `make update` reboot option
- Recurring parser DB errors
- Parser threads now successfully update themselves

## [0.2-beta] 2018-04-04
### Added
- Many filters to limit rules
- Parse helper types for simpler config updates
- Event fields for netflows, web server logs, and more
- Email alerts for rules
- Password change pages
- Sanity check for entry field lengths, etc.
- Documentation
- `logesp` script for controlling daemons
- `hostname`, `domain_name`, and IP addresses to sw assets

### Updated
- Improved risk management workflows
- Split username field into `source_user`, `target_user`
- Improved event search (more fields, better formatting)
- Limit rules only sleep ~60s after not firing
- Rule types are now modular
- Parse helpers now work if parser fails
- Daemon thread errors are logged to LOG\_DAEMON
- Parser and sentry can now be run separately (distributed environments)
- Rule events now track source/dest host count
- Rules and searches use more regular expressions
- logesp daemon runs without privileges
- Parser threads re-read parsers/helpers every 6,000 events or 10 minutes
- `log_source` and `source_process` can be set in `config/parser.conf`

### Fixed
- Helper logic for single-field parse helpers

## [0.1-alpha] - 2018-02-06
- First test release
