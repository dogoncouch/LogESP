# LogESP Adversarial Threat Documentation

LogESP (c) 2018 Dan Persons | [MIT License](../LICENSE)

The LogESP risk management system is based on the [NIST risk assessment guidelines](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final).

## Index

- [Adversarial Threat Events](#adversarial-threat-events)
- [Adversarial Threat Sources](#adversarial-threat-sources)
- [Vulnerabilities](#vulnerabilities)
- [Responses](#responses)
- [Impacts](#impacts)

## Adversarial Threat Events
An adversarial threat event is an event that is caused intentionally (by an adversary or other malicious entity), and could have negative impacts.

### Adversarial Threat Event Anatomy

- `name` - the event name
- `desc` - a description of the event
- `event_type` - the event type
- `info_source` - the source of information on the threat
- `tier` - the information source tier (organization-wide, department-wide, or localized)
- [sources](#adversarial-threat-sources) - adversarial threat sources that could cause the event
- `relevance` - the relevance, or likelihood, of the event
- [vulnerabilities](#vulnerabilities) - vulnerabilities related to the event
- [responses](#responses) - measures taken in response to the threat
- `likelihood_initiation` - the likelihood of the event being initiated (scale of 1 to 100)
- `likelihood_impact` - the likelihood of adverse impact if the event is initiated (scale of 1 to 100)
- [impacts](#impacts) - potential impacts of the event
- `assigned_risk` - the level of risk assigned to the event (scale of 1 to 100)

## Adversarial Threat Sources
An adversarial threat source is a person or entity with intent to cause harm to an organization.

- `name` - the threat source name
- `desc` - a description of the threat source
- `event_type` - the threat source type
- `info_source` - the source of information on the threat source
- `tier` - the information source tier (organization-wide, department-wide, or localized)
- `in_scope` - whether or not the threat source in within the scope of risk management
- `capability` - the threat source's level of capability (scale of 1 to 100)
- `intent` - the threat source's level of intent (scale of 1 to 100)
- `targeting` - the threat source's level of intent on specific targets (scale of 1 to 100)

## Vulnerabilities
Vulnerabilities are conditions that make a threat event more likely to happen.

- `name` - the vulnerability name
- `desc` - a description of the vulnerability
- `vuln_type` - the vulnerability type
- `info_source` - the source of information on the threat source
- `tier` - the information source tier (organization-wide, department-wide, or localized)
- `severity` - the vulnerability's level of severity (scale of 1 to 100)

## Responses
Responses are measures taken to reduce the risk from a threat.

- `name` - the response name
- `desc` - a description of the response
- `response_type` - the response type
- `effectiveness` - the effectiveness of the response (scale of 1 to 100)
- `status` - the status of the response (enabled, planned, declined, etc)

## Impacts
Impacts are the unwanted results if a threat event were to occur.

- `name` - the impact name
- `desc` - a description of the impact
- `impact_type` - the impact type
- `info_source` - the source of information on the threat source
- `tier` - the information source tier (organization-wide, department-wide, or localized)
- `severity` - the impact's level of severity (scale of 1 to 100)
- `impact_tier` - the impact tier (organization-wide, department-wide, or localized)
