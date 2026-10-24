"""Small synthetic fixtures only: no patient data, network or dependencies."""
import json
from pathlib import Path
import tempfile
import unittest
import check_evidence as checker


def fixture():
    def source(sid, family, kind):
        return dict(id=sid, study_family_id=family, title='Synthetic source', url='https://example.invalid/' + sid,
                    source_type=kind, evidence_access='synthetic', observation='synthetic', limitation='synthetic', checked_date='2026-01-01')
    return dict(sources=[source('s1', 'study1', 'primary_study'), source('approval', 'label1', 'regulator_label')],
                hypotheses=[dict(id='h1', drug='Synthetic compound', role='lead_screen', approval_verified=True,
                                 approval_source_ids=['approval'], direction='coherent', exposure_status='comparable',
                                 safety_status='bounded_test', evidence_class='related_model_rescue', rationale='Synthetic',
                                 strongest_source_id='s1', required_mechanism='residual_bubr1')],
                claims=[dict(id='c1', hypothesis_id='h1', from_node='A', to_node='B', sign='+', evidence_status='observed',
                             source_ids=['s1'], model='Synthetic cells', transfer_assumption='Synthetic', falsifier='Synthetic',
                             load_bearing=True, prospective=False)],
                exposure_records=[dict(id='e1', hypothesis_id='h1', assay_uM=2, human_total_uM=1,
                                       matrix='Synthetic total plasma', comparable=True, note='Synthetic', source_ids=['approval'])])


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()

    def result(self):
        self.assertEqual(checker.validate(self.data), [])
        return checker.analyze(self.data)

    def test_baseline(self):
        priorities, _, exposures = self.result()
        self.assertEqual(priorities[0]['classification'], 'conditional_preclinical_priority')
        self.assertEqual(exposures[0]['nominal_assay_to_human_total_ratio'], 2)

    def test_duplicate_urls_and_mirrors_do_not_inflate_families(self):
        for sid, url in [('mirror', 'https://example.invalid/mirror'), ('sameurl', 'https://example.invalid/s1')]:
            source = dict(self.data['sources'][0], id=sid, url=url)
            self.data['sources'].append(source)
            self.data['claims'][0]['source_ids'].append(sid)
        priorities, sensitivity, _ = self.result()
        self.assertEqual(priorities[0]['empirical_study_family_count'], 1)
        removal = sensitivity[0]['removals']
        self.assertEqual(removal['strongest_source_removed']['severed_claim_ids'], [])
        self.assertEqual(removal['strongest_family_removed']['severed_claim_ids'], ['c1'])
        self.assertEqual(removal['strongest_family_removed']['empirical_study_family_count'], 0)
        self.assertEqual(removal['strongest_family_removed']['classification'], 'hold_for_mechanism_or_exposure')

    def test_duplicate_url_conflicting_family_invalid(self):
        self.data['sources'].append(dict(self.data['sources'][0], id='mirror', study_family_id='fake2'))
        self.assertTrue(checker.validate(self.data))

    def test_prospective_cannot_be_observed_or_supported(self):
        self.data['claims'][0]['prospective'] = True
        for status in ['observed', 'supported_elsewhere']:
            self.data['claims'][0]['evidence_status'] = status
            self.assertTrue(checker.validate(self.data))

    def test_prospective_inferred_not_support(self):
        self.data['claims'][0].update(prospective=True, evidence_status='inferred')
        priorities, _, _ = self.result()
        self.assertEqual(priorities[0]['empirical_study_family_count'], 0)
        self.assertEqual(priorities[0]['classification'], 'hold_for_mechanism_or_exposure')

    def test_missing_pk_holds_and_stays_missing(self):
        self.data['exposure_records'][0]['human_total_uM'] = None
        priorities, _, exposures = self.result()
        self.assertEqual(priorities[0]['classification'], 'hold_for_mechanism_or_exposure')
        self.assertIsNone(exposures[0]['nominal_assay_to_human_total_ratio'])
        self.assertIsNone(exposures[0]['human_total_uM'])

    def test_unknown_edge_holds(self):
        self.data['claims'][0]['sign'] = 'unknown'
        priorities, _, _ = self.result()
        self.assertEqual(priorities[0]['classification'], 'hold_for_mechanism_or_exposure')

    def test_unknown_status_holds(self):
        self.data['claims'][0]['evidence_status'] = 'unknown'
        priorities, _, _ = self.result()
        self.assertEqual(priorities[0]['classification'], 'hold_for_mechanism_or_exposure')

    def test_noncomparable_ratio_explicitly_nonclinical(self):
        self.data['exposure_records'][0]['comparable'] = False
        priorities, _, exposures = self.result()
        self.assertTrue(exposures[0]['noncomparability_flag'])
        self.assertIn('nonclinical', exposures[0]['interpretation'])
        self.assertEqual(priorities[0]['classification'], 'hold_for_mechanism_or_exposure')

    def test_scenarios_remove_required_mechanisms(self):
        for mechanism, scenario in [('oxidative_stress', 'no_oxidative_stress'), ('mtorc1_activation', 'no_mtorc1_activation'), ('residual_bubr1', 'near_null_bubr1')]:
            self.data['hypotheses'][0]['required_mechanism'] = mechanism
            _, sensitivity, _ = self.result()
            self.assertEqual(sensitivity[0]['scenarios'][scenario]['classification'], 'hold_for_mechanism_or_exposure')
        for scenario in ['non_bubr1_cause', 'exposure_not_comparable']:
            self.assertEqual(sensitivity[0]['scenarios'][scenario]['classification'], 'hold_for_mechanism_or_exposure')

    def test_near_null_nonresidual_mechanisms_remain_unknown(self):
        for mechanism in ['oxidative_stress', 'mtorc1_activation']:
            self.data['hypotheses'][0]['required_mechanism'] = mechanism
            _, sensitivity, _ = self.result()
            scenario = sensitivity[0]['scenarios']['near_null_bubr1']
            self.assertIn('remains unknown', scenario['scenario_interpretation'])
            self.assertNotIn('Scenario removes required mechanism', ' '.join(scenario['reasons']))

    def test_gate_precedence(self):
        h = self.data['hypotheses'][0]
        h.update(approval_verified=False, direction='wrong')
        self.assertEqual(self.result()[0][0]['classification'], 'excluded_regulatory')
        h['approval_verified'] = True
        self.assertEqual(self.result()[0][0]['classification'], 'excluded_as_therapeutic_lead')

    def test_broken_references_and_boolean_types(self):
        self.data['claims'][0]['source_ids'] = ['absent']
        self.assertTrue(checker.validate(self.data))
        self.data = fixture()
        self.data['claims'][0]['prospective'] = 1
        self.assertTrue(checker.validate(self.data))

    def test_extra_unresolved_release_prerequisite_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'readiness.json'
            prerequisites = dict.fromkeys(['approval', 'rights', 'video', 'repository', 'privacy'], True)
            prerequisites['canonical_dataset_citation'] = {'status': 'unverified'}
            path.write_text(json.dumps({'prerequisites': prerequisites}))
            self.assertEqual(checker.release_errors(path),
                             ['Release prerequisite unresolved: canonical_dataset_citation'])
            prerequisites['canonical_dataset_citation'] = {'status': 'resolved'}
            path.write_text(json.dumps({'prerequisites': prerequisites}))
            self.assertEqual(checker.release_errors(path), [])

    def test_cli_invalid_overwrites_stale_and_release_is_opt_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'evidence').mkdir()
            ledger = root / 'evidence/ledger.json'
            out = root / 'generated'
            ledger.write_text(json.dumps(self.data))
            args = ['--ledger', str(ledger), '--out', str(out)]
            self.assertEqual(checker.main(args), 0)
            self.assertEqual(checker.main(args + ['--release-check']), 1)
            (root / 'review').mkdir()
            (root / 'review/readiness.json').write_text(json.dumps({'prerequisites': dict.fromkeys(['approval', 'rights', 'video', 'repository', 'privacy'], True)}))
            self.assertEqual(checker.main(args + ['--release-check']), 0)
            ledger.write_text('{}')
            self.assertEqual(checker.main(args), 1)
            self.assertIn('unavailable', json.loads((out / 'sensitivity.json').read_text()))


if __name__ == '__main__':
    unittest.main()
