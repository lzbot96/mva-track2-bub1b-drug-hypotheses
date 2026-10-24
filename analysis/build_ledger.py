#!/usr/bin/env python3
"""Assemble explicitly curated public evidence; no network, case data, or model calls."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def read(name):
    obj=json.loads((ROOT/'evidence'/name).read_text())
    return obj['sources'] if isinstance(obj,dict) else obj

sets={}
for name in ('mechanism_sources.json','pharmacology_sources.json','pharmacology_acetylcysteine_addendum_sources.json','safety_sources.json','reproducibility_sources.json','coordinator_sources.json'):
    for s in read(name):
        if s['id'] in sets: raise ValueError('Duplicate curated source ID: '+s['id'])
        sets[s['id']]=(s,name)
selected=[f'M{i:02}' for i in range(1,10)]+[f'P{i:02}' for i in range(2,16) if i!=12]+['C01','C02','S03','S09']+[f'R{i:02}' for i in range(1,9)]
regulators={'P03','P04','P05','P08','P11'}
sources=[]
for sid in selected:
    s,filename=sets[sid]
    doi=s.get('doi') or s.get('DOI')
    family=('doi:'+doi.lower()) if doi else ('official-challenge-2026' if sid.startswith('R') else ('label:'+sid if sid in regulators else 'publication:'+(s.get('url') or s.get('primary_url'))))
    if sid in {'P03','P04'}: family='regulatory-sirolimus'
    sources.append(dict(id=sid,study_family_id=family,title=s['title'],url=s.get('url') or s.get('primary_url'),source_type='regulator_label' if sid in regulators else ('official_rule' if sid.startswith('R') else 'primary_study'),evidence_access=s['evidence_access'],observation=s['observation'],limitation=s.get('contrary_or_limit') or s.get('limit') or 'See original source and reviewer record.',checked_date=s.get('checked_date','2026-10-17'),provenance_file='evidence/'+filename,inspected_url=s.get('inspected_url',s.get('url') or s.get('primary_url'))))
# Coordinator second-pass source check; initial reviewer extraction remains frozen.
for source in sources:
    if source['id']=='P14':
        source['limitation']+=' Primary abstract links adverse reactions to early high concentrations; peak is not a tolerability benchmark.'
# The same study occurs in multiple independent reviews. It is one scientific family.
aliases={'P01':'M07','P12':'C01','S01':'M01','S02':'M07','S04':'M05','S05':'P09','S06':'P02','S10':'M08'}
H=[]
def hypothesis(i,drug,role,approval,mechanism,eclass,strongest,rationale,exposure='unresolved',safety='hold',direction='conditional'):
    H.append(dict(id=i,drug=drug,role=role,approval_verified=True,approval_source_ids=[approval],direction=direction,exposure_status=exposure,safety_status=safety,evidence_class=eclass,rationale=rationale,strongest_source_id=strongest,required_mechanism=mechanism))
hypothesis('NAC','Acetylcysteine','lead_screen','P11','oxidative_stress','related_model_rescue','C01','First uncertainty-reduction experiment only: direct segregation endpoints in oxidative-stress models; no established BUB1B rescue or exposure bridge.')
hypothesis('SIR','Sirolimus','backup_screen','P03','mtorc1_activation','pathway_modulation','P02','Distinct downstream compensation experiment only if harmful mTORC1/SASP phenotype exists; not checkpoint correction.')
hypothesis('MET','Metformin','rejected','P05','none','pathway_modulation','P06','Millimolar SASP experiments have a large nominal exposure mismatch; no segregation rescue.',exposure='implausible')
hypothesis('DAS','Dasatinib','comparator','P08','none','pathway_modulation','P09','Selective-cell-elimination comparator, rejected as corrective lead; healthy progenitor depletion and serious toxicity concerns.',safety='reject')
C=[]
def edge(i,h,a,b,sign,status,refs,model,assumption,falsifier,load=True,prospective=False):
    C.append(dict(id=i,hypothesis_id=h,from_node=a,to_node=b,sign=sign,evidence_status=status,source_ids=refs,model=model,transfer_assumption=assumption,falsifier=falsifier,load_bearing=load,prospective=prospective))
edge('N1','NAC','NAC exposure','Oxidative-stress-linked segregation errors','-','supported_elsewhere',['C01','P13'],'Aged mouse fibroblasts; Sod1-null mouse oocytes','A removable stress component exists in the BUB1B model. These are different genotypes and mitosis/meiosis contexts.','No per-division benefit when stress and exposure are measured.')
edge('N2','NAC','BUB1B dysfunction','NAC-sensitive oxidative/replication stress','+','inferred',['C02','M01'],'Unperformed BUB1B functional model','Oxidative stress is a causal mediator, not only an associated marker.','No elevated stress or no segregation improvement after stress normalization.',prospective=True)
edge('N3','NAC','Sustained plausible free/reduced NAC exposure','Preserved viable lineage output with fewer new errors','unknown','unknown',[],'Unperformed exposure-matched BUB1B model','Relevant analyte, duration and tissue exposure can be attained.','Benefit restricted to high nominal exposure, arrest, selective death or probe interference.',prospective=True)
edge('N4','NAC','NAC','Missing BubR1 checkpoint function restored','unknown','unknown',[],'No demonstrated disease-model drug rescue','Direct checkpoint restoration is not assumed.','Persistent checkpoint defects despite a redox change.',load=False,prospective=True)
edge('S1','SIR','Specific BubR1 allelic state','Muscle mTORC1 hyperactivity','+','observed',['M02'],'Engineered allele-specific mouse muscle','Allele and tissue context transfer only after direct measurement.','No elevated mTORC1 signaling in relevant model.')
edge('S2','SIR','Sirolimus','IL1A-associated SASP','-','supported_elsewhere',['P02'],'Senescent human fibroblasts unrelated to BUB1B','Suppressed secretory activity is harmful-state reversal, not merely a biomarker.','Target engagement without reduced conditioned-medium harm.')
edge('S3','SIR','SASP reduction','Tissue-relevant functional harm','-','inferred',['M07'],'Unperformed BUB1B model','Genetic cell-clearance evidence does not establish pharmacological secretory modulation.','No functional gain or impaired healthy-cell/progenitor output.',prospective=True)
edge('S4','SIR','Plausible tissue sirolimus exposure','Safe durable downstream benefit','unknown','unknown',[],'Unperformed exposure-matched study','Whole-blood concentration cannot substitute for unbound tissue exposure.','Only cytostatic or exposure-infeasible activity.',prospective=True)
edge('S5','SIR','Sirolimus','Segregation error rate','unknown','unknown',[],'No demonstrated corrective experiment','No checkpoint-repair claim is made.','Errors unchanged or increased despite reduced cytokines.',load=False,prospective=True)
edge('T1','MET','Millimolar metformin','IKK/NF-kappaB-associated SASP','-','supported_elsewhere',['P06'],'Oncogenic-RAS IMR90 fibroblasts','High nominal culture activity transfers to plausible tissue exposure.','Effect absent at measured exposure-matched concentrations.')
edge('T2','MET','Plausible metformin exposure','BUB1B-linked tissue benefit','unknown','unknown',[],'Unperformed BUB1B model','Transporter-dependent accumulation is measured, not assumed.','Benefit appears only in millimolar positive-control conditions.',prospective=True)
edge('D1','DAS','Dasatinib','Viability of selected senescent cells','-','supported_elsewhere',['P09'],'Human preadipocytes; cell-type-dependent response','Selective killing must preserve healthy progenitors and not be called correction.','Nonsenescent-cell loss or no net tissue-function gain.')
edge('D2','DAS','Senescent-cell elimination','Selected BubR1 mouse aging pathology','-','observed',['M07'],'INK-ATTAC genetic elimination in BubR1 hypomorphic mice','Genetic transgene-dependent clearance is not dasatinib monotherapy.','Drug fails selectivity/function or affects different cell populations.')
edge('D3','DAS','Dasatinib at plausible free exposure','Safe BUB1B tissue benefit','unknown','unknown',[],'Unperformed disease-model study','Cancer exposure/tolerability cannot establish chronic constitutional use.','Depletion, toxicity, genomic selection, or no benefit.',prospective=True)
E=[]
def exp(i,h,assay,human,matrix,note,refs):
    E.append(dict(id=i,hypothesis_id=h,assay_uM=assay,human_total_uM=human,matrix=matrix,comparable=False,note=note,source_ids=refs))
exp('NAC_late','NAC',5000,35/163.2*1000,'nominal culture / historical total plasma at 12 hours','48-hour culture versus acute poisoning; total, reduced, free and tissue NAC differ. This is a nonclinical nominal ratio, not a safe target.',['C01','P14','P11'])
exp('NAC_peak','NAC',5000,554/163.2*1000,'nominal culture / historical early mean total-plasma peak','Transient acute IV peak; no sustained or chronic safety bridge.',['C01','P14','P11'])
exp('NAC_oocyte','NAC',500,None,'nominal maturation medium / target-tissue exposure unavailable','Different genotype, meiotic process and compartment; exact exposure duration not independently verified.',['P13','P11'])
exp('SIR_blood','SIR',0.0125,15/914.2,'nominal culture / whole blood','MW914.2g/mol; 15ng/mL whole blood, adult transplant with co-medication. Blood/plasma partition and protein binding preclude free-tissue comparison.',['P02','P03','P04'])
exp('MET_low','MET',1000,1000/129.16,'nominal culture / upper benchmark total plasma','Usual plasma is below1microgram/mL; using metformin free-base MW129.16. Ratio is therefore a lower-bound benchmark, not an intracellular ratio.',['P06','P05'])
exp('MET_high','MET',5000,1000/129.16,'nominal culture / upper benchmark total plasma','Same lower-bound interpretation; no unmeasured tissue-accumulation rescue.',['P06','P05'])
exp('DAS_total','DAS',0.05,82.2/488.01,'nominal 3-day culture / transient total plasma peak','96%binding gives approximate free peak0.00674uM, not measured tissue exposure; half-life3–5h. Nominal total ratio does not pass exposure gate.',['P09','P08'])
ledger=dict(version='1.0',purpose='Public literature curation and falsifiable preclinical prioritization; no patient data, experiments or efficacy estimates.',sources=sources,source_aliases=aliases,claims=C,hypotheses=H,exposure_records=E,excluded_unverified_record='C03 omitted: title/full-text verification was inadequate; no conclusion depends on it.',deduplication_note='DOI families count one study regardless of mirrors or repeat reviewer citation. Different families are not necessarily independent laboratories or disease models.')
(ROOT/'evidence/ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
print(f'Built {len(sources)} sources, {len(C)} causal edges, {len(H)} hypotheses, {len(E)} exposure records.')
