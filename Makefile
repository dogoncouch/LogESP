
all:
	@echo No make target for all/default.
	@echo Try 'make help'
	@echo

default: all

install:
	@echo No make target for install.
	@echo Try 'make help'
	@echo

help:
	@echo --- View daemon help display
	@echo ------------------------------
	@echo make daemon-help
	@echo
	@echo --- New database setup
	@echo ------------------------
	@echo -- Set up new DB with fixtures-
	@echo make new-db
	@echo -- Set up new DB without fixtures-
	@echo make new-db-setup
	@echo
	@echo --- View help on individual fixtures
	@echo --------------------------------------
	@echo make fixture-help

fixture-help:
	@echo --- Fixtures
	@echo --------------
	@echo - Note- 'make new-db' installs fixtures automatically.
	@echo - Avoid installing them twice.
	@echo
	@echo -- Install all fixtures-
	@echo make fixtures
	@echo -- Install only risk management fixtures-
	@echo make risk-fixtures
	@echo -- Install only asset type fixtures-
	@echo make asset-fixtures
	@echo -- Install only siem parse fixtures-
	@echo make parser-fixtures
	@echo -- Install only example siem rules-
	@echo make example-rules
	@echo

daemon-help:
	@echo --- Daemon help
	@echo -----------------
	@echo -- Get help on parser engine-
	@echo make parser-help
	@echo
	@echo -- Get help on sentry engine-
	@echo make sentry-help
	@echo
	@echo -- Get help on cleaner-
	@echo make cleaner-help
	@echo

parser-help:
	@echo --- Starting the parser engine
	@echo --------------------------------
	@echo 1. Edit config file at 'config/parser.conf'
	@echo 2. Run the parser inside a django shell-
	@echo python manage.py shell -c "import daemons.parser.parsecore ; daemons.parser.parsecore.start()"
	@echo 

sentry-help:
	@echo --- Starting the sentry engine
	@echo --------------------------------
	@echo - Run the sentry engine inside of a django shell-
	@echo python manage.py shell -c "import daemons.sentry.sentrycore ; daemons.sentry.sentrycore.start()"
	@echo

cleaner-help:
	@echo --- Removing old entries
	@echo --------------------------
	@echo - Note- events have two different EOL dates for local and
	@echo - backup copies of events. The cleaner can use either to
	@echo - delete old  events. There are two options-
	@echo 1. Delete using the backup EOL date-
	@echo python manage.py shell -c "import daemons.cleaner.clean ; daemons.cleaner.clean.clean()"
	@echo 2. Delete using local EOL date-
	@echo python manage.py shell -c "import daemons.cleaner.clean ; daemons.cleaner.clean.clean(local=True)"
	@echo - Note- cleaning should be handled by a cron job.
	@echo

new-db: new-db-setup fixtures

new-db-setup:
	@echo --- Loading initial migrations...
	python manage.py migrate
	@echo --- Creating superuser...
	python manage.py createsuperuser

risk-fixtures:
	@echo --- Loading NIST threat data fixtures...
	python manage.py loaddata risk/fixtures/nist_threat_event_types.json risk/fixtures/nist_threat_src_types.json
	python manage.py loaddata risk/fixtures/generic_nist_threat_events.json risk/fixtures/generic_nist_threat_sources.json
	@echo --- Loading risk response type fixtures...
	python manage.py loaddata risk/fixtures/risk_response_types.json

asset-fixtures:
	@echo --- Loading basic asset type fixtures...
	python manage.py loaddata hwam/fixtures/hardware_asset_types.json hwam/fixtures/software_asset_types.json

parser-fixtures:
	@echo --- Loading standard syslog parser fixtures...
	python manage.py loaddata siem/fixtures/syslog_parsers.json
	@echo --- Loading authentication parse helpers...
	python manage.py loaddata siem/fixtures/example_auth_parse_helpers.json

example-rules:
	@echo --- Loading example rule fixtures...
	python manage.py loaddata siem/fixtures/example_auth_limit_rules.json

fixtures: risk-fixtures asset-fixtures parser-fixtures example-rules
	@echo --- Have a nice day!
