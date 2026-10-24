# Evidence gates

Manual lead_screen/backup_screen roles describe which uncertainty to investigate first; they never override gates. Conditional preclinical priority is not treatment endorsement. Observed means measured in the source model, never in this individual. Study-family counts are deduplication metadata, not evidence strength or ranking.

| Hypothesis | Manual screen role | Gate | Empirical families | Reasons |
|---|---|---|---:|---|
| NAC | lead_screen | hold_for_mechanism_or_exposure | 2 | Exposure is not comparable.; Missing, noncomparable, or unsupported PK/exposure inputs.; Safety hold.; Unsupported or unknown load-bearing edge: N2.; Unsupported or unknown load-bearing edge: N3. |
| SIR | backup_screen | hold_for_mechanism_or_exposure | 2 | Exposure is not comparable.; Missing, noncomparable, or unsupported PK/exposure inputs.; Safety hold.; Unsupported or unknown load-bearing edge: S3.; Unsupported or unknown load-bearing edge: S4. |
| MET | rejected | hold_for_mechanism_or_exposure | 1 | Exposure is not comparable.; Missing, noncomparable, or unsupported PK/exposure inputs.; Safety hold.; Unsupported or unknown load-bearing edge: T2. |
| DAS | comparator | excluded_as_therapeutic_lead | 2 | Wrong direction or rejected safety. |
