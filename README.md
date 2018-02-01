# LogDissect Security Intelligence
A web application for managing security information. Still in early development.

## Applications
LDSI applications:
- Assets - Asset Management
- Risk - Risk Management (based on [NIST SP 800-30r1](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final))
- SIEM - Security Information and Event Management

## Design Principles
### [NIST](https://www.nist.gov/) guidelines
The LDSI risk management system is based on NIST [risk management](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final) guidelines, and the SIEM and forensics apps are designed to support the NIST [incident response](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final) and [forensics](https://csrc.nist.gov/publications/detail/sp/800-86/final) guidelines.

### Simplicity
LDSI embraces the Unix design philosophy. It is designed to be as simple as possible, in order to be easy to understand, use, maintain, and extend.

## Installing
Requirements: python 3.x, django >=2.0, git, pip.

Note: replace `python` with `python3` if Python 2 is your default version (or if you're not sure what I'm talking about).

- Step 1: Clone the repo:
```
git clone https://github.com/dogoncouch/ldsi.git
```

- Step 2: Create a virtual environment and install django:
```
virtualenv -p python3 ldsi_env
source ldsi_env/bin/activate
pip install django
```

- Step 3: Create/migrate the database:
```
cd ldsi
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

- Step 4: (Optional) Add NIST standard threat information:
```
python manage.py loaddata risk/fixtures/nist_threat_event_types.json risk/fixtures/nist_threat_src_types.json
python manage.py loaddata risk/fixtures/generic_nist_threat_events.json risk/fixtures/generic_nist_threat_sources.json
```

- Step 5: Create a superuser:
```
python manage.py createsuperuser
(provide username, password)
```

- Step 6: Start the server:
```
python manage.py runserver
```

- Step 7: Try it: http://localhost:8000

## Notes
### Parser Engine
To start the parser engine:

1. Edit the config file at `config/parser.conf`.
2. Run the parser inside a django shell:
```
python manage.py shell -c "import daemons.parser.parsecore ; daemons.parser.parsecore.start()"
```

The parser needs to be restarted on changes to the config file.

### Sentry Engine
To start the rule engine:

1. Add Limit Rules (in the SIEM section)
2. Run the sentry engine inside a django shell:
```
python manage.py shell -c "import daemons.sentry.sentrycore ; daemons.sentry.sentrycore.start()"
```
3. Add more Limit Rules, and change or delete old ones. The sentry engine will adapt.

### Cleaner
Events have two different EOL dates for local and backup copies of events. The cleaner can use either to delete old events. There are two options:

1. Run the cleaner inside a django shell using the backup EOL date:
```
python manage.py shell -c "import daemons.cleaner.clean ; daemons.cleaner.clean.clean()"
```
2. Run the cleaner inside a django shell using the local EOL date:
```
python manage.py shell -c "import daemons.cleaner.clean ; daemons.cleaner.clean.clean(local=True)"
```

In theory, the local date should not be used unless you back up your event data for offline long-term storage.

Cleaning should be handled by a cron job.
