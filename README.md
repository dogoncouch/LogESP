# LogDissect Security Intelligence
A web application for managing security information. Still in early development; use at your own risk.

## Functions
LDSI applications:
- HWAM - Asset Management
- Risk - Risk Management (based on [NIST SP 800-30r1](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final))
- SIEM - Security Information and Event Management

## Design Principles
### [NIST](https://www.nist.gov/) guidelines
The LDIS risk management system based on NIST guidelines, and the SIEM and forensics apps are based on the NIST incident response and forensics guidelines.

### Simplicity
LDSI embraces the Unix design philosophy. It is designed to be as simple as possible, in order to be easy to understand, use, maintain, and extend.

### Accessibility
LDSI's target audience for UX design is blind people, and others who use screen readers, or other non-standard input and output devices.

## Installing
Requirements: python 3.x, django >=2.0, git, pip.

Note: replace `python` with `python3` if Python 2 is your default version (or if you're not sure what I'm talking about).

- Step 1: Clone the repo:
```
git clone https://github.com/dogoncouch/ldsi.git
```

- Step 2: (Optional) Create a virtual environment and install django:
```
virtualenv ldsi_env
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
python manage.py loaddata risk.fixtures.nist_threat_event_types.json risk.fixtures.nist_threat_src_types.json
python manage.py loaddata risk.fixtures.generic_nist_threat_events.json risk.fixtures.generic_nist_threat_sources.json
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

## Near Future

- Finish SIEM app
- Switch default database to MariaDB
- Dockerize
