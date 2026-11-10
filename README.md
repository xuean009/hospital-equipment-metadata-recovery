# HISS manuscript and reproducibility package

Article: Reliability of generative AI workflows for recovering missing hospital equipment metadata: an expert-verified paired evaluation

Journal: Health Information Science and Systems

Authors: Yihan Qi and Zhenqi Zhang

Affiliation: Sichuan Cancer Hospital & Institute, Sichuan Clinical Research Center for Cancer, Sichuan Cancer Center, Affiliated Cancer Hospital of University of Electronic Science and Technology of China, Chengdu 610041, China

Corresponding author: Zhenqi Zhang; 9xuean@gmail.com

Prepared: 10 November 2026. Version v1.0.1 corrects a figure-label inequality, completes the supplementary rebuild instructions and embeds existing 600 dpi figure exports; statistical results are unchanged. Version v1.0.0 remains available as the initial deposit. Code and machine-readable aggregates are published in the repository below; no submission to the journal is performed by these scripts.

## Author deliverables and generated outputs

The table below describes the author submission files and generated outputs. The public repository contains code, Markdown sources and aggregate data; the Word/PDF deliverables and figure exports are generated locally by the commands below. The cover letter and complete author delivery archive are not included in GitHub.

| File | Use |
|---|---|
| Main_Manuscript.docx | Research article with three embedded 600 dpi TIFF figures and four editable tables |
| Cover_Letter.docx | Editorial cover letter; excluded from the public GitHub repository |
| ESM_1.pdf | Online Resource 1, supplementary methods and results |
| ESM_2.pdf | Online Resource 2, aggregate statistical results and reproducibility guide |
| ESM_1.docx | Editable author source for Online Resource 1; submit the PDF |
| ESM_2.docx | Editable author source for Online Resource 2; submit the PDF |
| figures/ | Original figure exports for editing or requested separate uploads |

The complete HISS_submission_package.zip is an author convenience bundle. Extract it and upload the manuscript, cover letter and two online resources to their respective submission categories. Do not upload the whole delivery archive as a public supplement. Figures are embedded in the manuscript; independent copies are retained as source assets.

## Rebuild from aggregate data

Download the fixed submission version from https://github.com/xuean009/hospital-equipment-metadata-recovery/tree/v1.0.1 into a clean directory (Code > Download ZIP), or clone https://github.com/xuean009/hospital-equipment-metadata-recovery and check out tag v1.0.1. Use Python 3.12 and install the pinned direct dependencies in an isolated environment:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe code/figures.py
.venv\Scripts\python.exe code/build_documents.py
.venv\Scripts\python.exe code/build_esm2.py
```

These commands create the three figure exports, Main_Manuscript.md, Main_Manuscript.docx, ESM_1.docx and ESM_2.docx using the supplied aggregates. They do not require record-level data or API credentials. The cover letter is rebuilt only when the local Cover_Letter.md is available; it is intentionally absent from the public GitHub repository.

To export PDFs on Windows with Microsoft Word installed:

```powershell
powershell -ExecutionPolicy Bypass -File code/render_qa.ps1
.venv\Scripts\python.exe code/qa.py
```

Word export opens the documents read-only. ESM_1.pdf and ESM_2.pdf are the submission supplements. Main-manuscript and cover-letter PDFs and page PNGs remain internal proofs in qa/. The supplied QA script checks structure, references, aggregate invariants, embedded figures and PDF boundaries. Authors should also inspect rendered pages. Fonts used in the verified rendering were Arial and Microsoft YaHei. Different fonts or renderers may change pagination.

## Optional authorised record-level analysis

The canonical workbook is 数据集_全_已核查.xlsx, worksheet 合并数据集, SHA-256:

`1e7e116478cf5fa646645b77936f5eec2dc4dd2922419ca0f87a97f227b2ec12`

This workbook is not included. An authorised holder can reproduce the original record-level analysis before rebuilding figures and documents:

```powershell
.venv\Scripts\python.exe code/analyze.py --input "PATH_TO_AUTHORISED_WORKBOOK.xlsx"
```

The analysis opens the workbook read-only and exports only aggregates. Its assertions are specific to this 1000-record evaluation and must not be disabled to force a different dataset through. No record-level analysis or AI inference was repeated for this journal transfer.

source_data/study_context.json records the previously author-confirmed source-pool and study periods. The final analytical workbook does not retain upstream missing-brand and registration-year fields. The years were not inferred from identifiers. Random seeds are numerical generator parameters, not dates of study activities.

## Statistical interpretation

The primary difference is record-weighted. The sensitivity analysis gives each of 418 exact equipment name–model combinations equal weight. Cluster bootstrap intervals use 6000 replicates with seed 20261029 and recalculate conditional denominators in each draw. They do not quantify repeated AI-call variability or between-hospital variation. The exact McNemar test is a conventional record-level comparison without cluster adjustment.

Conditional correctness values describe different output-selected populations. Unverified assignments occur when expert reference brands remain unresolved; they are not automatically classified as false or hallucinated. Exploratory review strata were not independently validated. Candidate coverage does not measure approved registry completion or human time saved.

## Package integrity and access

Run `python code/package_delivery.py` from the complete local author directory to rebuild HISS_submission_package.zip. The archive is for author convenience and is not a journal supplement. The public repository contains only explicitly selected code, manuscript source, prompts and aggregates. It excludes individual workbooks, secrets, local runtimes, proofs and author correspondence. The fixed submission tag is v1.0.1. Repository access: https://github.com/xuean009/hospital-equipment-metadata-recovery. No software reuse licence is asserted by this deposit.

Record-level access remains restricted by the hospital. Requests should be addressed to the corresponding author and remain subject to institutional approval. The public repository reproduces figures and documents from aggregates; it does not independently reproduce record-level adjudication or grant access to the inventory.

## Reference verification

reference_verification.csv maps each of the 19 cited references to its source and role. Sixteen retained sources carry the prior 2 November 2026 verification date. Three added sources were checked against publisher pages on 10 November 2026. The CoT-CC citation is limited to the publicly available abstract and metadata; it is contextual, not evidence of equipment-metadata performance.
