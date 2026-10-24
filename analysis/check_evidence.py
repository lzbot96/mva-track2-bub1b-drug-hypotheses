#!/usr/bin/env python3
"""Offline consistency checks, not evidence interpretation or efficacy prediction."""
import argparse
import hashlib
import json
import math
from pathlib import Path

FIELDS = {
    'sources': 'id study_family_id title url source_type evidence_access observation limitation checked_date'.split(),
    'claims': 'id hypothesis_id from_node to_node sign evidence_status source_ids model transfer_assumption falsifier load_bearing prospective'.split(),
    'hypotheses': 'id drug role approval_verified approval_source_ids direction exposure_status safety_status evidence_class rationale strongest_source_id required_mechanism'.split(),
    'exposure_records': 'id hypothesis_id assay_uM human_total_uM matrix comparable note source_ids'.split(),
}
ENUMS = {
    'source_type': {'primary_study', 'regulator_label', 'official_rule'},
    'sign': {'+', '-', 'mixed', 'unknown'},
    'evidence_status': {'observed', 'supported_elsewhere', 'inferred', 'unknown'},
    'role': {'lead_screen', 'backup_screen', 'rejected', 'comparator'},
    'direction': {'conditional', 'coherent', 'wrong', 'unknown'},
    'exposure_status': {'comparable', 'unresolved', 'implausible', 'not_applicable'},
    'safety_status': {'hold', 'reject', 'bounded_test'},
    'evidence_class': {'direct_genotype_rescue', 'related_model_rescue', 'pathway_modulation', 'association_only'},
    'required_mechanism': {'oxidative_stress', 'mtorc1_activation', 'residual_bubr1', 'none'},
}
BOOLS = {'load_bearing', 'prospective', 'approval_verified', 'comparable'}
LISTS = {'source_ids', 'approval_source_ids'}
NUMBERS = {'assay_uM', 'human_total_uM'}
EMPIRICAL = {'observed', 'supported_elsewhere'}
SCENARIOS = {'no_oxidative_stress': 'oxidative_stress', 'no_mtorc1_activation': 'mtorc1_activation', 'near_null_bubr1': 'residual_bubr1', 'non_bubr1_cause': None, 'exposure_not_comparable': None}
DISCLAIMER = ('Manual lead_screen/backup_screen roles describe which uncertainty to investigate first; '
              'they never override gates. Conditional preclinical priority is not treatment endorsement. '
              'Observed means measured in the source model, never in this individual. Study-family counts are deduplication metadata, not evidence strength or ranking.')


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ['Ledger must be an object.']
    for group, required in FIELDS.items():
        rows = data.get(group)
        if not isinstance(rows, list):
            errors.append(f'{group}: must be an array')
            continue
        seen = set()
        for index, row in enumerate(rows):
            label = f'{group}[{index}]'
            if not isinstance(row, dict):
                errors.append(f'{label}: must be an object')
                continue
            for key in required:
                value = row.get(key)
                if key not in row:
                    errors.append(f'{label}: missing {key}')
                elif key in BOOLS:
                    if type(value) is not bool:
                        errors.append(f'{label}.{key}: must be Boolean')
                elif key in LISTS:
                    if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
                        errors.append(f'{label}.{key}: must be an array of nonempty IDs')
                elif key in NUMBERS:
                    if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or value <= 0):
                        errors.append(f'{label}.{key}: must be positive finite number or null')
                elif not isinstance(value, str) or not value.strip():
                    errors.append(f'{label}.{key}: must be nonempty text')
                elif key in ENUMS and value not in ENUMS[key]:
                    errors.append(f'{label}.{key}: invalid value {value!r}')
            identifier = row.get('id')
            if isinstance(identifier, str):
                if identifier in seen:
                    errors.append(f'{label}: duplicate id {identifier}')
                seen.add(identifier)
    if errors:
        return errors
    sources = {s['id']: s for s in data['sources']}
    hypotheses = {h['id']: h for h in data['hypotheses']}
    for group in ('claims', 'hypotheses', 'exposure_records'):
        for row in data[group]:
            refs = row.get('source_ids', row.get('approval_source_ids', []))
            if group == 'hypotheses':
                refs = refs + [row['strongest_source_id']]
            for ref in refs:
                if ref not in sources:
                    errors.append(f'{row["id"]}: unknown source {ref}')
            if 'hypothesis_id' in row and row['hypothesis_id'] not in hypotheses:
                errors.append(f'{row["id"]}: unknown hypothesis {row["hypothesis_id"]}')
            if group == 'claims':
                if row['prospective'] and row['evidence_status'] in EMPIRICAL:
                    errors.append(f'{row["id"]}: prospective experiment cannot be observed/supported_elsewhere')
                if row['evidence_status'] in EMPIRICAL and not row['source_ids']:
                    errors.append(f'{row["id"]}: empirical status requires source IDs')
    # Exact URL mirrors cannot masquerade as distinct study families.
    urls = {}
    for source in data['sources']:
        url = source['url'].rstrip('/')
        if url in urls and urls[url] != source['study_family_id']:
            errors.append(f'{source["id"]}: same source URL assigned conflicting study families')
        urls[url] = source['study_family_id']
    return errors


def empirical_sources(claim, sources, removed):
    if claim['prospective'] or claim['evidence_status'] not in EMPIRICAL:
        return set()
    return {sid for sid in claim['source_ids'] if sid not in removed and sources[sid]['source_type'] == 'primary_study'}


def exposure_checks(data):
    result = []
    for row in data['exposure_records']:
        assay, human = row['assay_uM'], row['human_total_uM']
        ratio = assay / human if assay is not None and human is not None else None
        result.append(dict(row, nominal_assay_to_human_total_ratio=ratio,
                           noncomparability_flag=not row['comparable'],
                           interpretation='nonclinical nominal ratio only; no free/tissue exposure or efficacy inference' if not row['comparable'] else 'nominal ratio only; comparability is curator supplied, not verified by this tool',
                           missing_inputs=[key for key in sorted(NUMBERS) if row[key] is None]))
    return result


def classify(h, data, removed=frozenset(), scenario=None):
    sources = {s['id']: s for s in data['sources']}
    claims = [c for c in data['claims'] if c['hypothesis_id'] == h['id']]
    edges = [c for c in claims if c['load_bearing']]
    families = sorted({sources[s]['study_family_id'] for c in claims for s in empirical_sources(c, sources, removed)})
    reasons = []
    approval = h['approval_verified'] and any(s not in removed and sources[s]['source_type'] in {'regulator_label', 'official_rule'} for s in h['approval_source_ids'])
    if not approval:
        status, reasons = 'excluded_regulatory', ['No surviving verified regulatory approval source.']
    elif h['direction'] == 'wrong' or h['safety_status'] == 'reject':
        status, reasons = 'excluded_as_therapeutic_lead', ['Wrong direction or rejected safety.']
    else:
        if h['direction'] == 'unknown':
            reasons.append('Direction unknown.')
        if h['exposure_status'] != 'comparable':
            reasons.append('Exposure is not comparable.')
        records = [r for r in data['exposure_records'] if r['hypothesis_id'] == h['id']]
        if not records or any(not r['comparable'] or r['assay_uM'] is None or r['human_total_uM'] is None or not any(s not in removed for s in r['source_ids']) for r in records):
            reasons.append('Missing, noncomparable, or unsupported PK/exposure inputs.')
        if h['safety_status'] != 'bounded_test':
            reasons.append('Safety hold.')
        if not edges:
            reasons.append('No load-bearing causal chain supplied.')
        for edge in edges:
            if edge['sign'] == 'unknown' or not empirical_sources(edge, sources, removed):
                reasons.append(f'Unsupported or unknown load-bearing edge: {edge["id"]}.')
        if scenario == 'exposure_not_comparable':
            reasons.append('Scenario assumes exposure is not comparable.')
        elif scenario == 'non_bubr1_cause':
            reasons.append('Scenario removes the BUBR1 causal premise; reassessment required.')
        elif scenario and SCENARIOS[scenario] == h['required_mechanism']:
            reasons.append(f'Scenario removes required mechanism: {h["required_mechanism"]}.')
        status = 'hold_for_mechanism_or_exposure' if reasons else 'conditional_preclinical_priority'
    return dict(hypothesis_id=h['id'], role=h['role'], classification=status, reasons=reasons,
                empirical_study_family_count=len(families), empirical_study_family_ids=families)


def scenario_interpretation(h, scenario):
    if scenario == 'near_null_bubr1' and h['required_mechanism'] != 'residual_bubr1':
        return ('No residual-BubR1 dependency is encoded for this hypothesis. '
                'Downstream modulation under near-null BubR1 remains unknown; '
                'an unchanged gate is not evidence that the intervention works in this scenario.')
    if SCENARIOS[scenario] is not None and SCENARIOS[scenario] != h['required_mechanism']:
        return ('The removed mechanism is not the encoded required mechanism; '
                'an unchanged gate does not establish robustness or efficacy in this scenario.')
    return 'Scenario removes an encoded prerequisite or requires causal reassessment; no revised probability is inferred.'


def analyze(data):
    sources = {s['id']: s for s in data['sources']}
    priorities, sensitivity = [], []
    for h in data['hypotheses']:
        baseline = classify(h, data)
        priorities.append(baseline)
        strongest = h['strongest_source_id']
        family = sources[strongest]['study_family_id']
        removals = {'strongest_source_removed': {strongest}, 'strongest_family_removed': {sid for sid, s in sources.items() if s['study_family_id'] == family}}
        cases = {}
        for name, removed in removals.items():
            claims = [c for c in data['claims'] if c['hypothesis_id'] == h['id']]
            cases[name] = dict(classify(h, data, removed), removed_source_ids=sorted(removed),
                               affected_claim_ids=[c['id'] for c in claims if removed.intersection(c['source_ids'])],
                               severed_claim_ids=[c['id'] for c in claims if empirical_sources(c, sources, set()) and not empirical_sources(c, sources, removed)])
        sensitivity.append(dict(hypothesis_id=h['id'], baseline=baseline, removals=cases,
                                scenarios={s: dict(classify(h, data, scenario=s), scenario_interpretation=scenario_interpretation(h, s)) for s in SCENARIOS}))
    return priorities, sensitivity, exposure_checks(data)


def release_errors(path):
    try:
        readiness = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        return [f'Readiness unavailable: {exc}']
    values = readiness.get('prerequisites', readiness) if isinstance(readiness, dict) else {}
    errors = []
    if not isinstance(values, dict):
        return ['Release prerequisites must be an object.']
    required = {'approval', 'rights', 'video', 'repository', 'privacy'}
    for key in sorted(required | set(values)):
        value = values.get(key)
        resolved = value is True or (isinstance(value, dict) and value.get('status') == 'resolved')
        if not resolved:
            errors.append(f'Release prerequisite unresolved: {key}')
    return errors


def main(argv=None):
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', type=Path, default=base.parent / 'evidence/ledger.json')
    parser.add_argument('--out', type=Path, default=base / 'generated')
    parser.add_argument('--release-check', action='store_true')
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    digest = None
    data = None
    try:
        raw = args.ledger.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw)
        errors = validate(data)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    release = release_errors(args.ledger.parent.parent / 'review/readiness.json') if args.release_check else []
    validation = dict(structurally_valid=not errors, errors=errors, input_sha256=digest,
                      release_check_requested=args.release_check, release_errors=release, disclaimer=DISCLAIMER)
    (args.out / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
    (args.out / 'input.sha256').write_text((digest or 'unavailable') + '\n')
    if errors:
        # Replace prior results so failed runs cannot leave apparently current outputs.
        for filename in ('sensitivity.json', 'exposure_checks.json'):
            (args.out / filename).write_text(json.dumps({'unavailable': 'structurally invalid input', 'input_sha256': digest}, indent=2) + '\n')
        (args.out / 'priorities.md').write_text('# Evidence checks unavailable\n\nStructural validation failed; see validation.json.\n')
    else:
        priorities, sensitivity, exposures = analyze(data)
        for filename, value in [('sensitivity.json', sensitivity), ('exposure_checks.json', exposures)]:
            (args.out / filename).write_text(json.dumps({'input_sha256': digest, 'results': value}, indent=2, allow_nan=False) + '\n')
        def cell(value):
            return str(value).replace('|', '\\|').replace('\n', ' ')
        lines = ['# Evidence gates', '', DISCLAIMER, '', '| Hypothesis | Manual screen role | Gate | Empirical families | Reasons |', '|---|---|---|---:|---|']
        for p in priorities:
            lines.append('| ' + ' | '.join(cell(v) for v in [p['hypothesis_id'], p['role'], p['classification'], p['empirical_study_family_count'], '; '.join(p['reasons']) or 'All encoded gates met; preclinical only.']) + ' |')
        (args.out / 'priorities.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps(validation, indent=2))
    return 1 if errors or release else 0


if __name__ == '__main__':
    raise SystemExit(main())
