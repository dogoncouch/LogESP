# Change log
Change log for [LogDissect Security Intelligence](https://github.com/dogoncouch/ldsi)

## [Unreleased]
### Added
- Added start.sh script for starting/restarting/stopping daemon
- Added source and destination host filters to limit rules
- Added parse helper types for simpler config updates
- Added event fields for netflow parsing
- Added email alerts to rules
- Added more filters to rules - action, interface, source/target user
- Added password change pages
- Added sanity check for entry field lengths, etc.
- Added documentation

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

## [0.1-alpha] - 2018-02-06
- First test release
