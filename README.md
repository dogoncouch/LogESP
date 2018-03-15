# LogDissect Security Intelligence

LogDissect Security Intelligence (c) 2018 Dan Persons | [MIT License](LICENSE)

## Index

- [Introduction](#introduction)
- [Installing on Ubuntu](doc/install-ubuntu.md)
- [Screenshots](doc/screenshots.md)
### SIEM documentation
- [Parsing](doc/parsing.md)
  - [Parse Daemon](doc/parsing.md/#parse-daemon)
  - [Event Parsing](doc/parsing.md/#event-parsing)
    - [Parsers](doc/parsing.md/#parsers)
    - [Parse Helpers](doc/parsing.md/#parse-helpers)
- [Rules](doc/rules.md)
  - [Sentry Daemon](doc/rules.md/#sentry-daemon)
  - [Limit Rules](doc/rules.md/#limit-rules)
    - [Rule vs. Log Events](doc/rules.md/#rule-vs-log-events)
    - [Filters](doc/rules.md/#filters)
    - [Magnitude Calculation](doc/rules.md/#magnitude-calculation)
- [Events](doc/events.md)
  - [Anatomy of a Log Event](doc/events.md/#anatomy-of-a-log-event)
  - [Anatomy of a Rule Event](doc/events.md/#anatomy-of-a-rule-event)
- [Daemons](doc/daemons.md)

## Introduction
LDSI is a SIEM (Security Information and Event Management system) written in Python Django. It features a web frontend, and handles log management and forensics, risk management, and asset management.

### Design Principles
#### Security
LDSI was designed and built as a security application, and minimalism can be good for security.

- LDSI does not require credentials, or installation of its software, on log sources. Event forwarding is left entirely up to syslog daemons.
- LDSI uses no client-side scripting.

#### [NIST](https://www.nist.gov/) guidelines
The LDSI risk management system is based on NIST [risk assessment](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final) guidelines, and the SIEM and forensics apps are designed to support the NIST [incident response](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final) and [forensics](https://csrc.nist.gov/publications/detail/sp/800-86/final) guidelines.

#### Simplicity
LDSI embraces the Unix design philosophy. It is designed to be as simple as possible, in order to be easy to understand, use, maintain, and extend.

### Applications
LDSI includes a few different applications:
- SIEM - Security Information and Event Management
- Assets - Asset Management
- Risk - Risk Management
