# Testing NAC and sirolimus in cell models of BUB1B-related MVA

This is a proposed laboratory study by zoul6. No experiments were performed. It asks whether NAC or sirolimus could improve specific cell outcomes in BUB1B-related mosaic variegated aneuploidy (MVA). It does not establish a treatment benefit.

[Read the report](report/zoul6_track2_report.md) for the rationale, proposed experiments, controls and reasons to stop. The [evidence guide](EVIDENCE_GUIDE.md) explains the terms and tables. NAC is the first proposed screen; sirolimus is a separate backup hypothesis. These choices describe what to investigate, not proven efficacy.

The work combines a public-literature review, a structured source list called an **evidence ledger**, proposed links between biological steps, and code that checks whether the records agree. A **causal edge** is one such proposed link. A **signed** link records whether one step increases or decreases another; uncertain directions remain marked uncertain. A **compartment** means the relevant model, tissue or location: evidence from one cannot automatically transfer to another.

The [ledger](evidence/ledger.json) organizes 34 source records, 14 links, four compound assessments and seven exposure records. These counts describe organization, not biological validation. The six source-extraction files record the observations and their limits. Source papers and figures are not bundled.

## Reproduce the checks

Use Python 3 with its standard library. No network, patient data or additional packages are needed. Run from this directory:

```sh
python3 analysis/build_ledger.py
python3 analysis/check_evidence.py
python3 -m unittest discover -s analysis -p 'test_*.py'
```

These commands rebuild the source list, check consistency and run synthetic tests. See [analysis instructions](analysis/README.md) and [field definitions](analysis/SCHEMA.md). A successful consistency check is not proof that a drug works. An unresolved biological question is a valid result.

[AI disclosure](AI_DISCLOSURE.md) · [Dataset references](DATASET_REFERENCE.md) · [Rights notice](NOTICE.md)

## License

Copyright 2026 zoul6. The original contributions in this repository are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for license terms and third-party rights. Controlled source data are not included.
