"""Build the PDF-targeted aggregate report after build_documents.py.
No record-level data or AI calls are required.
"""
from copy import deepcopy
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from build_documents import ROOT,setup,para,S

URL='https://github.com/xuean009/hospital-equipment-metadata-recovery/tree/v1.0.0'
d=setup(False)
d.styles['Normal'].paragraph_format.line_spacing=1.15
d.add_paragraph('Online Resource 2\nAggregate statistical results and reproducibility guide','Title')
para(d,'Reliability of generative AI workflows for recovering missing hospital equipment metadata: an expert-verified paired evaluation')
para(d,'Health Information Science and Systems')
para(d,'Yihan Qi and Zhenqi Zhang')
para(d,'Sichuan Cancer Hospital & Institute, Sichuan Clinical Research Center for Cancer, Sichuan Cancer Center, Affiliated Cancer Hospital of University of Electronic Science and Technology of China, Chengdu 610041, China')
para(d,'Corresponding author: Zhenqi Zhang; Email: 9xuean@gmail.com')
d.add_heading('1 Purpose and access to code',1)
para(d,'This resource presents the aggregate statistical results and instructions previously distributed with the code archive. It contains no new analyses. Code, original prompts, machine-readable aggregate data and the manuscript source are deposited in the public GitHub repository at the fixed submission version v1.0.0.')
para(d,URL,10)
para(d,'Online Resource 1 provides detailed methods and original prompts. The record-level inventory remains restricted by the hospital; access requests must be addressed to the corresponding author and are subject to institutional approval. The repository contains no individual asset records, API credentials, cover letter or internal proofs.')
d.add_heading('2 Analysis overview and interpretation',1)
para(d,'The evaluation included 1000 paired records sampled from 1101 eligible records, with 744 confirmed and 256 unresolved reference brands. There were 418 exact name–model clusters, of which 164 occurred more than once; the largest contained 41 records. Initial expert assessments agreed for 946 records, with 54 disagreements reconciled before AI output assessment.')
para(d,'Correctness pairs were: both correct, 294; reasoning only correct, 14; search only correct, 230; neither correct, 462. The exact two-sided record-level McNemar P value was 1.57 × 10⁻⁵¹; this test does not adjust for clustering. Cluster-bootstrap estimates use 6000 resamples and seed 20261029. Sampling seed 20260416 is a generator parameter, not a study date.')
para(d,'The record-weighted yield difference was 21.6 percentage points (95% CI 14.9–28.6), and the equally weighted name–model difference was 14.0 points (10.5–17.6). Intervals describe sampled-cluster variability, not repeated AI calls or between-hospital variation. Conditional correctness compares different output-selected populations. Unverified assignments are not automatically false or hallucinated. Processing times do not measure human labour.')
d.add_heading('3 Aggregate tables',1)
para(d,'Tables R1–R4 reproduce the main aggregate tables. Tables R5–R9 reproduce the classification rules, request settings, bootstrap intervals, category results and literal-string subsets from Online Resource 1. Values and denominators are unchanged. Table notes retain their original meaning; references to Online Resource 1 refer to the accompanying PDF.')
i=0
for filename in ['Main_Manuscript.docx','ESM_1.docx']:
    src=Document(ROOT/filename)
    for t in src.tables:
        i+=1
        prev=t._element.getprevious()
        title=''.join(prev.xpath('.//w:t/text()'))
        title=title.split('. ',1)[-1]
        p=d.add_paragraph(f'Table R{i}. '+title)
        p.paragraph_format.keep_with_next=True
        for run in p.runs:run.bold=True
        d._element.body.insert(len(d._element.body)-1,deepcopy(t._element))
        nxt=t._element.getnext()
        if nxt is not None and nxt.tag==qn('w:p'):
            para(d,''.join(nxt.xpath('.//w:t/text()')),10)
d.add_heading('4 Reproducing the published aggregates',1)
para(d,'Download or clone the repository and select tag v1.0.0. Use Python 3.12 in a virtual environment and install requirements.txt. Run the following commands from the repository root; they rebuild figures and documents from supplied aggregates without reading individual records or making model calls.')
for command in ['python -m pip install -r requirements.txt','python code/figures.py','python code/build_documents.py','python code/build_esm2.py']:
    para(d,command,10)
para(d,'On Windows with Microsoft Word installed, run powershell -ExecutionPolicy Bypass -File code/render_qa.ps1 to export ESM_1.pdf and ESM_2.pdf. Then run python code/qa.py for document and aggregate checks. Inspect rendered pages because font or renderer changes may affect pagination. A cover letter is generated only in the private author directory when its Markdown source is present.')
para(d,'Full record-level statistical reproduction requires authorised access to the adjudicated workbook. An authorised holder can run python code/analyze.py --input "PATH_TO_AUTHORISED_WORKBOOK.xlsx" before the figure and document builders. This access requirement is distinct from aggregate-based reconstruction. No original provider-controlled AI responses are regenerated by these scripts.')
d.add_heading('5 Provenance and software',1)
para(d,'Canonical source workbook: '+S['input_filename']+'; worksheet: 合并数据集.')
para(d,'Source workbook SHA-256: '+S['input_sha256'],9)
para(d,'Original analysis software: '+', '.join(k+' '+v for k,v in S['versions'].items())+'. Direct dependencies are pinned in requirements.txt.')
para(d,'Repository source_data/analysis_summary.json contains the stored numerical estimates, including unrounded bootstrap limits. Table CSV files and figure_source_data.csv provide machine-readable values. study_context.json records the author-confirmed upstream source pool and study periods. original_prompts.json retains the original instructions. These files are unchanged from the verified analysis; the final analytical workbook cannot reconstruct upstream missing-brand or year filters.')
d.core_properties.title='Online Resource 2 Aggregate statistical results and reproducibility guide'
d.save(ROOT/'ESM_2.docx')
print('Created ESM_2.docx with',i,'aggregate tables')
