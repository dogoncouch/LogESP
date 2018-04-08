# LogESP Search Regex Tips
Regular expression tips for use with LogESP.

## Searches and Rules
### Reminders
- Search/rule regex is case insensitive

### Tricks
-  Match either EXPRESSION1 or EXPRESSION2:
`(EXPRESSION1|EXPRESSION2)`

- Match an expression literally (not just any field that contains it):
`^EXPRESSION$`

- Filter out an expression in a field:
`^(?!EXPRESSIOON)`

