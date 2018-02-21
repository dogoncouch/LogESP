
all:
	@echo
	@echo No make target for all\/default.
	@echo Try \'make help\'
	@echo

default: all

install:
	@echo
	@echo No make target for install.
	@echo Try \'make help\'
	@echo

help:
	@echo
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
	@echo

fixture-help:
	@echo
	@echo --- Fixtures
	@echo --------------
	@echo - Note- \'make new-db\' installs fixtures automatically.
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
	@echo
	@echo --- Daemon help
	@echo -----------------
	@echo -- Use start.sh to start parser and sentry daemons-
	@echo ./start.sh -h
	@echo
	@echo Make sure to edit config/parser.conf
	@echo Restart daemons with ./start.sh -r to re-read config
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
	python manage.py loaddata siem/fixtures/example_parsers.json
	@echo --- Loading authentication parse helpers...
	python manage.py loaddata siem/fixtures/example_parse_helpers.json

example-rules:
	@echo --- Loading example rule fixtures...
	python manage.py loaddata siem/fixtures/example_auth_limit_rules.json

fixtures: risk-fixtures asset-fixtures parser-fixtures example-rules
	@echo --- Have a nice day!
