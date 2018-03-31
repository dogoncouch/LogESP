# LogESP Non-Adversarial Threat Documentation

LogESP (c) 2018 Dan Persons | [MIT License](../LICENSE)

The LogESP risk management system is based on the [NIST risk assessment guidelines](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final).

## Index

  - [Non-Adversarial Threat Events](#non-adversarial-threat-events)
  - [Non-Adversarial Threat Sources](#non-adversarial-threat-sources)
  - [Risk Conditions](#risk-conditions)
  - [Responses](#responses)
  - [Impacts](#impacts)

## Non-Adversarial Threat Events
A non-adversarial threat event is an event that is not caused intentionally, but could cause harm to an organization (i.e. an earthquake, a configuration mistake).

### Non-Adversarial Threat Event Anatomy

- `name` - the event name
- `desc` - a description of the event
- `event_type` - the event type
- `info_source` - the source of information on the threat
- `tier` - the information source tier (organization-wide, department-wide, or localized)
- `relevance` - the relevance, or likelihood, of the event
- [sources](#non-adversarial-threat-sources) - non-adversarial threat sources that could cause the event
- [risk conditions](#risk-conditions) - predisposing conditions related to the event
- [responses](#responses) - measures taken in response to the threat
- `likelihood_initiation` - the likelihood of the event being initiated (scale of 1 to 100)
- `likelihood_impact` - the likelihood of adverse impact if the event is initiated (scale of 1 to 100)
- [impacts](#impacts) - potential impacts of the event
- `assigned_risk` - the level of risk assigned to the event (scale of 1 to 100)

## Adversarial Threat Sources
A non-adversarial threat source is a person, entity, or occurance that could cause harm to an organization without intent.

- `name` - the threat source name
- `desc` - a description of the threat source
- `event_type` - the threat source type
- `info_source` - the source of information on the threat source
- `tier` - the information source tier (organization-wide, department-wide, or localized)
- `in_scope` - whether or not the threat source in within the scope of risk management
- `range_of_effect` - the threat source's range of effect (scale of 1 to 100)

## Risk Conditions
Risk conditions are predisposing conditions that make a threat event more likely to happen.

- `name` - the condition name
- `desc` - a description of the condition
- `vuln_type` - the condition type
- `info_source` - the source of information on the condition
- `tier` - the information source tier (organization-wide, department-wide, or localized)
- `pervasiveness` - the vulnerability's level of severity (scale of 1 to 100)

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
