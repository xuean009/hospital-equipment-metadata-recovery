# Hospital equipment metadata recovery

Article: Reliability of generative AI workflows for recovering missing hospital equipment metadata: an expert-verified paired evaluation

Target journal: BMC Medical Informatics and Decision Making

Authors: Yihan Qi and Zhenqi Zhang

Affiliation: Sichuan Cancer Hospital & Institute, Sichuan Clinical Research Center for Cancer, Sichuan Cancer Center, Affiliated Cancer Hospital of University of Electronic Science and Technology of China, Chengdu 610041, China

Corresponding author: Zhenqi Zhang; 9xuean@gmail.com

Version: **v1.1.0**, prepared 20 November 2026. This journal-transfer revision updates framing, references, declarations, supplementary-file names and reproducibility documentation. Study data, workflow settings, analyses and numerical results are unchanged. It does not report new model calls, a new governance framework, clinical decision-support performance, patient outcomes or deployment benefits. The earlier HISS deposits remain available under tags v1.0.0 and v1.0.1. Preparing this package does not submit it to a journal.

## Public contents and author deliverables

This repository contains analysis and document-generation code, the manuscript Markdown source, original prompts, aggregate data and dependency specifications. Generated Word/PDF documents and figures are excluded from Git. The cover letter, internal proofs, author reports and complete author delivery archive are private local deliverables.

| Generated file | Purpose |
|---|---|
| Main_Manuscript.docx | Research article with three embedded figures and four editable tables |
| Additional_file_1.pdf | Additional file 1: supplementary methods and results |
| Additional_file_2.pdf | Additional file 2: aggregate statistical results and reproducibility guide |
| Additional_file_1.docx and Additional_file_2.docx | Editable sources for the two supplementary PDFs |
| Cover_Letter.docx | Journal-specific letter, generated only when its private Markdown source is present |
| figures/ | Three figures in editable SVG, PDF, TIFF and PNG formats |

The local BMC_MIDM_submission_package.zip is an author convenience archive. Extract it and upload only the individual files required by the submission system. The complete archive is not a supplementary file for publication.

## Rebuild from aggregate data

Use the fixed version at https://github.com/xuean009/hospital-equipment-metadata-recovery/tree/v1.1.0. Clone the repository and check out v1.1.0, or download that tag as a ZIP. Use Python 3.12 and an isolated environment:

```sh
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python code/figures.py
python code/build_documents.py
python code/build_additional2.py
python code/qa.py
```

These commands generate figures, Main_Manuscript.md, Main_Manuscript.docx and both supplementary DOCX files from supplied aggregates. They need neither individual asset records nor API credentials. The QA script verifies document structure, citations, aggregate invariants and supplementary table agreement. If PDF proofs are present under qa/, it also checks their bounds and freshness. The cover letter is built only when Cover_Letter.md exists locally.

On Windows with Microsoft Word installed, export PDF proofs and supplementary PDFs using:

```powershell
powershell -ExecutionPolicy Bypass -File code/render_qa.ps1
python code/qa.py
```

Alternatively, with LibreOffice available on macOS/Linux, export the three public documents into qa/ and copy the supplementary PDFs to the package root:

```sh
soffice --headless --convert-to pdf --outdir qa Main_Manuscript.docx Additional_file_1.docx Additional_file_2.docx
cp qa/Additional_file_1.pdf Additional_file_1.pdf
cp qa/Additional_file_2.pdf Additional_file_2.pdf
python code/qa.py
```

Inspect every rendered page before submission. Different fonts and renderers can change pagination. The transfer documents use Arial and Arial Unicode MS for retained Chinese prompt text. Main-manuscript and cover-letter PDFs and page images are internal proofs. Each supplementary PDF must remain below the journal's 20 MB limit.

## Authorised record-level analysis

The canonical workbook is 数据集_全_已核查.xlsx, worksheet 合并数据集, SHA-256:

`1e7e116478cf5fa646645b77936f5eec2dc4dd2922419ca0f87a97f227b2ec12`

The workbook is **not public**. Requests should be addressed to the corresponding author and are subject to hospital approval. An authorised holder can run the original analysis before rebuilding figures and documents:

```sh
python code/analyze.py --input "PATH_TO_AUTHORISED_WORKBOOK.xlsx"
```

The analysis reads the workbook and exports aggregates only. Its assertions are specific to this 1000-record study and must not be bypassed to force different data through. Aggregate-based reconstruction does not independently reproduce record-level adjudication. No script reproduces the original provider-controlled model calls, changing web sources or historical model snapshots.

source_data/study_context.json records the author-confirmed source pool and study periods. The analytical workbook does not retain upstream missing-brand and registration-year fields. Years were not inferred from identifiers; random seeds are generator inputs, not study dates. Original analysis software versions remain documented in analysis_summary.json; the pinned requirements support reconstruction.

## Interpretation and version integrity

Verified yield uses all 1000 records. Conditional correctness uses each workflow's own specific-output denominator. Unverified assignments concern unresolved expert references and are not automatically false or hallucinated. The primary paired difference is record-weighted; sensitivity analysis weights each of 418 exact name–model combinations equally. Cluster-bootstrap intervals use 6000 replicates and seed 20261029, recalculating conditional denominators in every draw. The exact McNemar test is a conventional record-level comparison without cluster adjustment.

These analyses do not measure repeated AI-call variability, generalisation to other hospitals, approved registry completion, human labour savings or deployment benefits. Review strata are exploratory and not validated acceptance rules.

Run `python code/package_delivery.py` only from the complete private author directory to create the delivery ZIP and its SHA-256 manifest. The script does not publish anything. Public files exclude individual workbooks, secrets, proofs and correspondence. No software reuse licence is asserted by this deposit.

reference_verification.csv maps the 20 references to their sources and roles. Nineteen references are retained from the preceding manuscript and reformatted to Vancouver style; the versioned repository citation is added. WHO's equipment information-system guidance and the two BMC data-quality reviews were rechecked for this transfer. Other retained verification dates remain explicit; the CoT-CC citation supports contextual discussion only.
