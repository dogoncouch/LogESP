
all:
	@echo No make target for all/default.

default: all

new-db: new-db-setup fixtures

new-db-setup:
	@echo Loading initial migrations...
	python manage.py migrate
	@echo Creating superuser...
	python manage.py createsuperuser

risk-fixtures:
	@echo Loading NIST threat data fixtures...
	python manage.py loaddata risk/fixtures/nist_threat_event_types.json risk/fixtures/nist_threat_src_types.json
	python manage.py loaddata risk/fixtures/generic_nist_threat_events.json risk/fixtures/generic_nist_threat_sources.json
	@echo Loading risk response type fixtures...
	python manage.py loaddata risk/fixtures/risk_response_types.json

asset-fixtures:
	@echo Loading basic asset type fixtures...
	python manage.py loaddata hwam/fixtures/hardware_asset_types.json hwam/fixtures/software_asset_types.json
	
parser-fixtures:
	@echo Loading standard syslog parser fixtures...
	python manage.py loaddata siem/fixtures/syslog_parsers.json
	@echo Loading authentication parse helpers...
	python manage.py loaddata siem/fixtures/example_auth_parse_helpers.json

example-rules:
	@echo Loading example rule fixtures...
	python manage.py loaddata siem/fixtures/example_auth_limit_rules.json

fixtures: nist-fixtures asset-fixtures parser-fixtures example-rules
	@echo Have a nice day!
