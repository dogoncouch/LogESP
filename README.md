# LogDissect Security Intelligence
A web application for managing security information. Still in early development; use at your own risk.

## Functions
LDSI applications:
- HWAM - Asset Management
- RISK - Risk Management
- SIEM - Security Information and Event Management

## Installing
LDSI is still under development, but you can try it out:
- Requirements: python 3.x, django >=2.0, git, pip
- Clone the repo:
```
git clone https://github.com/dogoncouch/ldsi.git
```

- (Optional) Create a virtual environment and install django:
```
virtualenv ldsi_env
source ldsi_env/bin/activate
pip install django
```

- Create/migrate the database:
```
cd ldsi
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

- Create a superuser:
```
python manage.py createsuperuser
(provide username, password)
```

- Start the server:
```
python manage.py runserver
```

- Create some objects:

Navigate to `http://localhost:8000/admin` and log in as the superuser account you just created. First create an organizational unit, then some hardware and software assets. You can also create users and groups.
- View your assets:
    - http://localhost:8000/hwam/ou
    - http://localhost:8000/hwam/hw
    - http://localhost:8000/hwam/sw

## Notes
LDSI is still in early development. Database changes that break backwards compatibility are still being made on a regular basis.
