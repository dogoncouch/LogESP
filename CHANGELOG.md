# Change log
Change log for [LogDissect Security Intelligence](https://github.com/dogoncouch/ldsi)

## [Unreleased]
### Added
- Added start.sh script for starting/restarting/stopping daemon
- Added source and destination host filters to limit rules
- Added parse helper types for simpler config updates
- Added event fields for netflow parsing


### Updated
- Fixed helper logic for single-field parse helpers
- Improved risk management workflows
- Split username field into `source_user`, `target_user`
- Improved event search (more fields, better formatting)
- Rule threads now only sleep for ~60 seconds if not just fired

## [0.1-alpha] - 2018-02-06
- First test release
