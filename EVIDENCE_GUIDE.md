# Evidence guide

This guide explains the evidence behind the [proposed laboratory study](report/zoul6_track2_report.md). It uses the existing [source ledger](evidence/ledger.json), which contains **34 source records, 14 causal links, four compounds and seven exposure comparisons**. These are counts of organized records, not measures of validation, independent replication or likely treatment benefit. The sources include studies, drug labels and organizer documents. Several records can belong to the same study or document family.

No new experiments were performed. NAC is the first conditional laboratory test; sirolimus is a separate backup. Neither has demonstrated correction of the relevant BUB1B defect in the evidence reviewed. The ranking does not recommend treatment.

## How to read a record

| Term | Plain-language meaning |
|---|---|
| Source ledger | A structured list of sources, what was available to read, what each supports and its limitations. A source ID such as C01 identifies a record; it is not a quality score. |
| Study family | Records referring to the same underlying study or related source. A duplicate citation or database copy is not an independent experiment. |
| Causal link | A proposed connection from one process or intervention to an outcome. The record states the supporting evidence and the assumptions needed to apply it here. Calling it a link does not prove causation. |
| Sign | The proposed direction: **+** means more of the stated outcome, **−** means less, and **unknown** means the direction is not established. A minus sign can describe fewer errors or fewer surviving cells; it does not automatically mean benefit. |
| Observed / supported elsewhere | A result reported in the source's experimental model. “Observed” does not mean that this project reproduced it. “Supported elsewhere” explicitly marks evidence from another model. |
| Inferred | A connection suggested by the evidence that has not been demonstrated in the proposed model. |
| Proposed / unknown | A future test or unresolved outcome. A proposed experiment can test an inference; these descriptions are not mutually exclusive. |
| Tissue and compartment | The biological location and sample measured: for example, mouse muscle, cells in culture, whole blood, plasma or the inside of a cell. Results from one location cannot simply substitute for another. |
| HOLD | A required condition is unresolved, so the idea cannot advance on the present evidence. It is not a calculated probability of failure. |
| Analyte | The chemical form actually measured, such as total NAC or reduced NAC. Different forms cannot be treated as the same measurement. |
| Checkpoint / kinetochore | The checkpoint helps delay division when chromosome attachments are not ready. The kinetochore is the chromosome structure that connects to the division machinery. |
| Euploid / aneuploid | Having the expected chromosome set / having an abnormal chromosome number. |
| Exposure comparison | A comparison of the concentration and duration used in a laboratory assay with a human measurement. It identifies gaps; it does not supply a dose, safety threshold or prediction of benefit. |

A useful reading order is **result → original model → limitation → proposed test**. Check whether the proposed model has the same defect before transferring a finding to it.

## The four candidate questions

BUB1B is the gene encoding BubR1, a protein involved in checking chromosome division and attaching chromosomes to the division machinery. A segregation error means chromosomes were distributed incorrectly. **NAC** means acetylcysteine. **mTORC1** is the signaling complex measured in the sirolimus rationale. **SASP**, the senescence-associated secretory phenotype, describes substances released by cells in a senescent, persistently growth-arrested state.

| Candidate and role | Practical next question | Supporting result | Critical gap |
|---|---|---|---|
| **NAC — first conditional test** | If the model has oxidative or DNA-copying stress, does reducing it lower new division errors while preserving surviving daughter cells? | Fewer segregation errors after NAC in aged mouse fibroblasts, a connective-tissue cell type, and in Sod1-null mouse egg cells. [C01](https://journals.biologists.com/jcs/article/136/11/jcs260688/316611/Oxidative-stress-induces-chromosomal-instability), [P13](https://pubmed.ncbi.nlm.nih.gov/39845481/) | Different genetic defects and division contexts. An NAC-sensitive stress component and plausible sustained exposure remain unproven in the BUB1B model. |
| **Sirolimus — separate backup** | If abnormal mTORC1 and harmful secretions are present, does reducing them improve cell or tissue function? | Selected BubR1 mouse alleles had increased muscle mTORC1 activity. Separately, sirolimus reduced SASP signaling in senescent human fibroblasts without reversing growth arrest. [M02](https://www.jci.org/articles/view/126863), [P02](https://eriba.umcg.nl/wp-content/uploads/2016/01/Demaria-2015-07-06-Nat-Cell-Biol.pdf) | The mouse finding was not a drug-rescue experiment. Lower secretory markers do not establish functional benefit or correction of division. |
| **Metformin — deprioritized lead** | Can the secretory effect occur at measured, plausible exposure? | Secretory-response transcripts were suppressed at 1–5 mM in culture. [P06](https://www.mcgill.ca/pollak-lab/files/pollak-lab/metformin_inhibits_the_senescence-associated_secretory_phenotype_by_interfering_with_ikk.pdf) | The large comparison gap with usual plasma exposure remains unresolved. Accumulation inside cells was not measured; no disease-specific segregation rescue was shown. [P05](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=ec3a9070-3745-41fb-b610-8d06129d8fd9) |
| **Dasatinib — restricted comparator** | Does eliminating selected cells merely change the population, or preserve useful tissue function? | Dasatinib reduced survival of selected senescent cell types. Separately, genetic cell removal delayed selected pathology in BubR1 mice. [P09](https://onlinelibrary.wiley.com/doi/10.1111/acel.12344), [M07](https://doi.org/10.1038/nature10600) | Genetic removal is not dasatinib monotherapy evidence. Cell killing is not chromosome repair; loss of healthy cells and drug toxicities remain concerns. [P08](https://packageinserts.bms.com/pi/pi_sprycel.pdf) |

For NAC, **oxidative stress** concerns oxidant-related cellular stress; **replication stress** concerns difficulty copying DNA. **Alleles** are versions of a gene. The sirolimus branch requires both abnormal mTORC1 activity and demonstrably harmful secretions. It stops if either is absent.

## Examples of the main causal links

These IDs refer to the 14-link list in the ledger. The table shows selected links, including the unproven steps needed to connect published observations to the proposal.

| Link | Direction and claim | Evidence status and model | Sources and limit |
|---|---|---|---|
| N1 | NAC **−** stress-associated segregation errors | Supported elsewhere: aged mouse fibroblasts and Sod1-null mouse egg cells | [C01](https://journals.biologists.com/jcs/article/136/11/jcs260688/316611/Oxidative-stress-induces-chromosomal-instability), [P13](https://pubmed.ncbi.nlm.nih.gov/39845481/). Neither establishes BUB1B disease-model rescue. |
| N2 | BUB1B dysfunction **+** NAC-sensitive stress | Inferred; proposed BUB1B model | [C02](https://pmc.ncbi.nlm.nih.gov/articles/PMC3799279/), [M01](https://doi.org/10.1158/0008-5472.CAN-09-4319) motivate the question but do not demonstrate this link. |
| N3 | Sustained plausible NAC exposure → fewer errors with preserved surviving cell lineages | Unknown; proposed experiment | No supporting source assigned. A lineage is a cell and its descendants; survival must be counted alongside errors. |
| S1 | Specific BubR1 alleles **+** muscle mTORC1 activity | Observed in selected engineered mouse muscle | [M02](https://www.jci.org/articles/view/126863). The allele and tissue restriction matters; no sirolimus rescue was demonstrated. |
| S2 | Sirolimus **−** SASP signaling | Supported elsewhere: senescent human fibroblasts | [P02](https://eriba.umcg.nl/wp-content/uploads/2016/01/Demaria-2015-07-06-Nat-Cell-Biol.pdf). Reduced secretion did not reverse growth arrest. |
| S3 | Reduced SASP **−** tissue-relevant harm | Inferred; proposed BUB1B model | [M07](https://doi.org/10.1038/nature10600) provides genetic cell-clearance context, not proof that drug-mediated secretory reduction works. |
| T1 | Millimolar metformin **−** SASP-associated signaling | Supported elsewhere: cultured fibroblasts | [P06](https://www.mcgill.ca/pollak-lab/files/pollak-lab/metformin_inhibits_the_senescence-associated_secretory_phenotype_by_interfering_with_ikk.pdf). High culture exposure cannot establish a plausible human exposure. |
| D1 | Dasatinib **−** survival of selected senescent cells | Supported elsewhere; response depended on cell type | [P09](https://onlinelibrary.wiley.com/doi/10.1111/acel.12344). The negative sign describes cell loss, not repaired division. |

## Reading the seven exposure comparisons

**mM** and **µM** are concentration units, millimolar and micromolar. **Nominal** means the concentration added to the culture, rather than a measured concentration inside cells. **Total** includes bound forms; **free/unbound** refers to drug not bound to proteins. For NAC, its reduced chemical form is another distinction. **Peak** is a transient maximum, not sustained exposure. Plasma is the liquid part of blood; whole blood also contains blood cells.

All seven ledger comparisons are marked **not directly comparable**. The values below repeat existing records and report summaries; they are not new calculations.

| Record | Laboratory exposure | Human comparison | Why it remains unresolved |
|---|---|---|---|
| NAC_late | 5,000 µM for 48 hours | Historical acute-IV total plasma ~214 µM at 12 hours | Duration, chemical form and target-tissue exposure differ. [C01](https://journals.biologists.com/jcs/article/136/11/jcs260688/316611/Oxidative-stress-induces-chromosomal-instability), [P14](https://pubmed.ncbi.nlm.nih.gov/2598989/), [P11](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/021539s021lbl.pdf) |
| NAC_peak | Same 5,000 µM assay | Historical early mean total-plasma peak ~3,395 µM | An acute intravenous peak does not establish sustained exposure or chronic safety. [C01](https://journals.biologists.com/jcs/article/136/11/jcs260688/316611/Oxidative-stress-induces-chromosomal-instability), [P14](https://pubmed.ncbi.nlm.nih.gov/2598989/), [P11](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/021539s021lbl.pdf) |
| NAC_oocyte | 500 µM in egg-cell culture | No target-tissue comparison available | Different genetic defect and egg-cell division; detailed duration was not independently verified. [P13](https://pubmed.ncbi.nlm.nih.gov/39845481/), [P11](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/021539s021lbl.pdf) |
| SIR_blood | 0.0125 µM nominal | ~0.0164 µM whole blood in adult transplant context | Blood distribution, binding and other medicines prevent a direct free-tissue comparison. [P02](https://eriba.umcg.nl/wp-content/uploads/2016/01/Demaria-2015-07-06-Nat-Cell-Biol.pdf), [P03](https://www.ema.europa.eu/en/documents/product-information/rapamune-epar-product-information_en.pdf), [P04](https://www.accessdata.fda.gov/drugsatfda_docs/label/2020/021083s067,021110s085lbl.pdf) |
| MET_low | 1,000 µM nominal | Usual total plasma <7.74 µM | The benchmark is not a measured concentration inside cells. [P06](https://www.mcgill.ca/pollak-lab/files/pollak-lab/metformin_inhibits_the_senescence-associated_secretory_phenotype_by_interfering_with_ikk.pdf), [P05](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=ec3a9070-3745-41fb-b610-8d06129d8fd9) |
| MET_high | 5,000 µM nominal | Same usual total-plasma benchmark <7.74 µM | A higher culture concentration does not resolve the same exposure gap. [P06](https://www.mcgill.ca/pollak-lab/files/pollak-lab/metformin_inhibits_the_senescence-associated_secretory_phenotype_by_interfering_with_ikk.pdf), [P05](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=ec3a9070-3745-41fb-b610-8d06129d8fd9) |
| DAS_total | ≥0.05 µM nominal for three days | Transient total peak ~0.168 µM; estimated free peak ~0.0067 µM | The free value is an estimate, and a transient plasma peak does not match prolonged culture exposure. [P09](https://onlinelibrary.wiley.com/doi/10.1111/acel.12344), [P08](https://packageinserts.bms.com/pi/pi_sprycel.pdf) |

The proposed experiments measure actual exposure and follow every observed entry into division, including arrest, death and both daughter cells. This is necessary because fewer errors among the remaining dividing cells can result from selection. A useful result must preserve viable output, meet the candidate's mechanism requirements and reproduce in independent culture or model preparations. Internal consistency checks can verify the records and calculations; they cannot validate the biology.
