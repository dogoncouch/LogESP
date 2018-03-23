#!/bin/sh

rm tmp/*.json

python manage.py dumpdata --indent 2 siem.LimitRule > tmp/example_limit_rules.json
python manage.py dumpdata --indent 2 siem.LogEventParser > tmp/example_parsers.json
python manage.py dumpdata --indent 2 siem.ParseHelper > tmp/example_parse_helpers.json

/home/notroot/src/dogoncouch-misc/clean-fixtures.py tmp/*.json

#sed -i 's/  "is_enabled": true,/  "is_enabled": false,/g' tmp/example_limit_rules.json
sed -i 's/  "is_enabled": \w+,\n//g' tmp/example_limit_rules.json

cp -r tmp /home/notroot/
chown -R notroot.notroot /home/notroot/tmp

