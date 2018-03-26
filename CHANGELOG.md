# Change log
Change log for [LogDissect Security Intelligence](https://github.com/dogoncouch/ldsi)

## [Unreleased]
### Added
- `start.sh` script for starting/restarting/stopping daemon
- Source and destination host filters to limit rules
- Parse helper types for simpler config updates
- Event fields for netflow parsing
- Email alerts to rules
- More filters to rules - action, interface, source/target user
- Password change pages
- Sanity check for entry field lengths, etc.
- Documentation
- Event fields for web server logs
- `ldsi` script for controlling daemons

### Updated
- Fixed helper logic for single-field parse helpers
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
- ldsi daemon runs without privileges

## [0.1-alpha] - 2018-02-06
- First test release
