# What the checks do

The code checks the consistency of a manually curated literature review. It does not test a drug, verify every source interpretation or estimate clinical benefit.

An **evidence ledger** is a structured source list with claims, compound assessments and exposure records. A **causal edge** is a proposed link between biological steps. Its **sign** says whether one step increases or decreases another. A **compartment** is the model, tissue or location where an observation applies. Differences between compartments must be considered before transferring a finding.

## Run locally

Run from the project root with Python 3 and its standard library:

```sh
python3 analysis/check_evidence.py
python3 -m unittest discover -s analysis -p 'test_*.py'
python3 analysis/check_evidence.py --release-check
```

Default paths are relative to the script, so they work from other directories too. `--ledger PATH` and `--out PATH` select different input and output locations. The checks use no network or patient records. Tests use synthetic examples and temporary directories.

## Read the results

The checker writes `validation.json`, `priorities.md`, `sensitivity.json`, `exposure_checks.json` and `input.sha256` in `analysis/generated/`. The hash identifies the exact input bytes.

Missing fields, invalid types or broken source references return exit code 1 and replace stale results with unavailable markers. Valid records return 0 even when the proposed study must wait for biological or exposure evidence. The optional `--release-check` is a maintainer check for private release prerequisites. It is not needed for scientific review and fails closed when those records are absent or unresolved.

The code rejects planned experiments described as observations. It groups repeated sources and known mirrors so they do not inflate support counts. Counts organize the evidence; they are not measures of efficacy or certainty. Hidden duplicates and scientific interpretation still need review.

Uncertain essential biological links, missing exposure evidence and safety concerns prevent advancement. Choosing NAC as the first screen or sirolimus as a backup does not override these limits. A conditional preclinical priority means a laboratory question worth testing, not a treatment recommendation.

Exposure records distinguish assay concentrations from human measurements. A nominal ratio cannot establish equivalent free-drug or tissue exposure. Missing measurements remain missing.

Sensitivity checks remove the strongest source and then its study family. They also remove required biological assumptions. These checks show what a conclusion depends on; they do not produce a revised probability of success. An unchanged result under a scenario does not establish benefit.

See [field definitions](SCHEMA.md) for the exact record structure.
