# Record definitions

`evidence/ledger.json` contains four lists: `sources`, `claims`, `hypotheses` and `exposure_records`. Together they form the evidence ledger: a structured source list and its interpretation. The checker validates consistency, not biological truth.

## Sources

Each source has `id`, `study_family_id`, `title`, `url`, `source_type`, `evidence_access`, `observation`, `limitation` and `checked_date`.

`source_type` is `primary_study`, `regulator_label` or `official_rule`. `study_family_id` groups related or duplicate evidence. Source and family counts are organizational information, not biological validation.

## Claims and proposed links

Each claim has `id`, `hypothesis_id`, `from_node`, `to_node`, `sign`, `evidence_status`, `source_ids`, `model`, `transfer_assumption`, `falsifier`, `load_bearing` and `prospective`.

A **causal edge** is a proposed link from one biological step to another. **Signed** means its direction is recorded: `+` for increase, `-` for decrease, or `mixed` or `unknown`. A **compartment** is the model, tissue or location where evidence applies; `model` and `transfer_assumption` describe that context and the proposed transfer.

`evidence_status` is `observed`, `supported_elsewhere`, `inferred` or `unknown`. Observed means measured in the named source model. It does not mean measured in a person with MVA. A planned experiment (`prospective: true`) cannot be recorded as observed or supported elsewhere. `load_bearing` marks an essential link; `falsifier` describes a result that would challenge it.

## Compound assessments

Each hypothesis has `id`, `drug`, `role`, `approval_verified`, `approval_source_ids`, `direction`, `exposure_status`, `safety_status`, `evidence_class`, `rationale`, `strongest_source_id` and `required_mechanism`.

Allowed values:

- `role`: `lead_screen`, `backup_screen`, `rejected`, `comparator`.
- `direction`: `conditional`, `coherent`, `wrong`, `unknown`.
- `exposure_status`: `comparable`, `unresolved`, `implausible`, `not_applicable`.
- `safety_status`: `hold`, `reject`, `bounded_test`.
- `evidence_class`: `direct_genotype_rescue`, `related_model_rescue`, `pathway_modulation`, `association_only`.
- `required_mechanism`: `oxidative_stress`, `mtorc1_activation`, `residual_bubr1`, `none`.

`approval_verified` is Boolean and requires supporting references. Regulatory approval does not establish benefit for MVA. Screen roles describe the proposed order of investigation, not efficacy.

## Exposure records

Each record has `id`, `hypothesis_id`, `assay_uM`, `human_total_uM`, `matrix`, `comparable`, `note` and `source_ids`. `human_total_uM` may be null. `comparable` is Boolean.

A nominal concentration ratio requires both measurements. If they are not comparable, the ratio remains explicitly nonclinical. It cannot establish equivalent free-drug or tissue exposure. Missing values stay missing.

## Results

The checker writes `validation.json`, `priorities.md`, `sensitivity.json`, `exposure_checks.json` and the input SHA-256 in `analysis/generated/`. It produces no efficacy score or probability.

Missing verified approval gives `excluded_regulatory`. Wrong direction or rejected safety gives `excluded_as_therapeutic_lead`. Unresolved exposure, safety or an essential inferred/unknown link gives `hold_for_mechanism_or_exposure`. Only a supported chain with comparable exposure and bounded-test safety can receive `conditional_preclinical_priority`; this remains a laboratory proposal.

Sensitivity checks remove the strongest source and its study family separately. They test `no_oxidative_stress`, `no_mtorc1_activation`, `near_null_bubr1`, `non_bubr1_cause` and `exposure_not_comparable`. Affected and unsupported claims are listed without inventing revised probabilities.
