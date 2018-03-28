# LogDissect Security Intelligence

LogDissect Security Intelligence (c) 2018 Dan Persons | [MIT License](LICENSE)

## Index

- [Introduction](#introduction)
- [Installing on Ubuntu](docs/install-ubuntu.md)
- [Screenshots](docs/screenshots.md)
### Asset Management Documentation
- [Asset Management](docs/hwam.md)
### Risk Management Documentation
- [Adversarial Threats](docs/risk/adv_threat.md)
  - [Adversarial Threat Events](docs/risk/adv_threat.md#adversarial-threat-event-anatomy)
  - [Adversarial Threat Sources](docs/risk/adv_threat.md#adversarial-threat-sources)
  - [Vulnerabilities](docs/risk/adv_threat.md@vulnerabilities)
  - [Responses](docs/risk/adv_threat.md#responses)
  - [Impacts](docs/risk/adv_threat.md@impacts)
- [Non-Adversarial Threats](docs/risk/nonadv_threat.md)
### SIEM Documentation
- [Parsing](docs/siem/parsing.md)
  - [Parse Daemon](docs/siem/parsing.md/#parse-daemon)
  - [Event Parsing](docs/siem/parsing.md/#event-parsing)
    - [Parsers](docs/siem/parsing.md/#parsers)
    - [Parse Helpers](docs/siem/parsing.md/#parse-helpers)
  - [Configuration](docs/siem/parsing.md/#configuration)
- [Rules](docs/siem/rules.md)
  - [Sentry Daemon](docs/siem/rules.md/#sentry-daemon)
  - [Limit Rules](docs/siem/rules.md/#limit-rules)
    - [Rule vs. Log Events](docs/siem/rules.md/#rule-vs-log-events)
    - [Filters](docs/siem/rules.md/#filters)
    - [Magnitude Calculation](docs/siem/rules.md/#magnitude-calculation)
  - [Events](docs/siem/events.md)
    - [Anatomy of a Log Event](docs/siem/events.md/#anatomy-of-a-log-event)
    - [Anatomy of a Rule Event](docs/siem/events.md/#anatomy-of-a-rule-event)
- [Daemons](docs/siem/daemons.md)

## Introduction
LDSI is a SIEM (Security Information and Event Management system) written in Python Django. It features a web frontend, and handles log management and forensics, risk management, and asset management.

### Design Principles
#### Security
LDSI was designed and built as a security application, and minimalism can be good for security.

- LDSI is built on the Python Django framework
- LDSI does not require credentials, or installation of its software, on log sources. Event forwarding is left entirely up to syslog daemons.
- The LDSI web interface uses no client-side scripting.

#### [NIST](https://www.nist.gov/) guidelines
The LDSI risk management system is based on NIST [risk assessment](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final) guidelines, and the SIEM and forensics apps are designed to support the NIST [incident response](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final) and [forensics](https://csrc.nist.gov/publications/detail/sp/800-86/final) guidelines.

#### Simplicity
LDSI embraces the Unix design philosophy. It is designed to be as simple as possible, in order to be easy to understand, use, maintain, and extend.

### Applications
LDSI includes a few different applications:
- SIEM - Security Information and Event Management
- Assets - Asset Management
- Risk - Risk Management
