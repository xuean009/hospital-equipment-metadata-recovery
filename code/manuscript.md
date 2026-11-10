# Reliability of generative AI workflows for recovering missing hospital equipment metadata: an expert-verified paired evaluation

Yihan Qi, Zhenqi Zhang

Sichuan Cancer Hospital & Institute, Sichuan Clinical Research Center for Cancer, Sichuan Cancer Center, Affiliated Cancer Hospital of University of Electronic Science and Technology of China, Chengdu 610041, China

Corresponding author: Zhenqi Zhang; Email: 9xuean@gmail.com

Article type: Research article

Acknowledgements: The authors thank two non-author colleagues at their institution for independently reviewing all 1000 asset records, consulting internet sources and equipment manuals, reconciling discrepancies through discussion and further checks, and jointly evaluating the AI outputs against the reconciled reference using brand equivalence. Both colleagues agreed to this acknowledgement without being named.

## Abstract

### Purpose

Historical hospital equipment registries can lack brand metadata, while original documentation may be unavailable. We evaluated two generative artificial intelligence (AI) workflows for recovering verifiable candidate brands from retained equipment names and models.

### Methods

In this retrospective paired evaluation, 1000 records were randomly sampled from 1101 eligible entries in a Chinese tertiary hospital's missing-brand remediation pool. Reasoning and web-enabled search workflows processed identical record fields. Two experts independently established reference brands while blinded to AI outputs, reconciled disagreements, and then jointly assessed outputs. We assessed verified yield, coverage, incorrect and unverified assignments, and paired differences using name–model cluster-bootstrap intervals.

### Results

Experts confirmed brands for 744 records; 256 remained unresolved. Reasoning and search yielded 308 (30.8%) and 524 (52.4%) verified correct brands, respectively (difference, 21.6 percentage points; cluster-bootstrap 95% confidence interval, 14.9–28.6). Specific brands were returned for 373 and 720 records, with conditional correctness of 82.6% and 72.8%. Incorrect assignments numbered 60 and 121; unverified assignments numbered 5 and 75.

### Conclusion

Both workflows generated verifiable candidate brands from incomplete hospital equipment metadata, but higher coverage accompanied more incorrect and unverified assignments. The differences characterize complete workflows rather than the isolated effect of web retrieval. Expert verification remains necessary before candidate values are entered into official registries.

Keywords: Health information systems; Equipment metadata; Data quality; Large language models; Information retrieval; Human verification

## 1 Introduction

Healthcare information resources include equipment metadata used to identify devices and connect inventory entries with supporting documentation. Equipment names, models and brands provide reference points for organising those resources. World Health Organization (WHO) guidance places inventories within equipment information and maintenance systems [1,2,3]. Missing metadata therefore presents an information-quality problem as well as an operational difficulty. Reviews of health information systems distinguish multiple data-quality dimensions and show considerable variation in their definitions and assessment methods [4,5]. Filling an empty field alone does not establish that the resulting information is correct or adequately supported.

Historical records can make the distinction between completeness and correctness particularly consequential. At the study hospital, brand fields were missing from a historical equipment remediation pool, and original procurement contracts and acceptance records were often unavailable. Retained names and models provided clues for searching public sources and available equipment manuals. However, a plausible candidate could remain difficult to confirm when product descriptions were ambiguous or documentary evidence was incomplete. Established data-quality research distinguishes accuracy from other aspects of fitness for use and separates completeness from correctness, conformance and plausibility [6,7,8]. Applied to missing equipment metadata, these distinctions require evaluation of both recovered information and the uncertainty that remains.

Generative artificial intelligence (AI) can propose candidate values from limited descriptions, potentially supplemented by retrieved information. Related health-informatics research includes CoT-CC, which combines reasoning and correction for zero-shot extraction of medical relations from text [9]. That task concerns entities and semantic relations, rather than recovery of missing equipment brands. Almanac evaluated retrieval-augmented language models using medical resources and expert assessment [10]. A scoping review also describes heterogeneous retrieval architectures and gaps between medical and nursing evaluations and operational workflows [11]. These studies motivate task-specific evaluation; their results do not establish reliability for historical equipment records. More specific outputs may improve candidate coverage while increasing incorrect or unsupported assignments.

The question addressed here is how much verifiable brand metadata two implemented AI workflows recover, and what assignment risks accompany that recovery. We evaluated reasoning and web-enabled search workflows on the same 1000 historical records, using independently established expert references and subsequent joint output assessment. Verified brand identification yield, specific-output coverage, conditional correctness and unresolved outcomes were distinguished, with paired analyses accounting for repeated equipment name–model combinations. The contribution is an empirical evaluation of recovery and reliability in a selected healthcare information resource. The study does not introduce a new extraction algorithm or validate an autonomous registry-completion system.

## 2 Methods

### 2.1 Study design and data source

This retrospective, single-centre study used a paired design: each sampled asset record was processed by both workflows and assessed against the same reference. The source was a historical fixed-asset ledger remediation pool covering assets from 2010–2025 at a tertiary public hospital in China. Before export for sampling, the hospital asset-management team had restricted this pool to records with a missing brand field. Both AI workflows were run in March 2026. Independent expert reference assessment, reconciliation and subsequent output evaluation were completed during April–May 2026. The asset-year window describes the upstream source pool and was not inferred from asset identifiers. No patients were enrolled, and the analytical records did not contain patient information. The hospital authorised the use of de-identified asset data. Figure 1 summarises the study design.

The sampling script selected records with equipment classification codes beginning with A023, a unit price of at least CNY 1000, and a valid specification/model field. Empty model fields and placeholders such as “none”, “not provided”, dashes and slashes were excluded according to the script. After these restrictions, 1101 records were eligible. A simple random sample without replacement selected 1000 records using random seed 20260416. The sample was therefore conditional on these eligibility criteria and was not a random sample of every hospital asset.

The missing-brand and 2010–2025 restrictions were upstream work-pool criteria, not conditions reconstructed from the final analysis workbook. This selected sample does not estimate the prevalence of defective brand entries across the hospital or the number of corrections actually approved in operational use. Reporting the source frame, selection steps and retained fields follows the transparency principle emphasised by RECORD for routinely collected data, although this equipment study is outside its clinical epidemiological scope [12]. The retained analytical fields included equipment name, classification code and label, broad classification, and specification/model. Only equipment name and specification/model were supplied to the AI workflows. The final adjudicated file contained one paired result per record. All 1000 records were included in this analysis; no outcome-based exclusions were applied.

### 2.2 AI-assisted metadata recovery workflows

The reasoning workflow called the DeepSeek chat-completions application programming interface (API) with model identifier deepseek-reasoner. No search tool was configured in its request. The script set max_tokens to 64000, used a 120-second request timeout, and allowed up to five attempts after request or parsing failures. The web-enabled search workflow called Tencent Cloud with model identifier deepseek-v3.2. Its request enabled search and thinking, used streaming output, set max_tokens to 8192, and specified a 180-second read timeout with up to five attempts. Temperature and top-p were not explicitly supplied in either request. These are script-level settings, not measurements of tokens consumed or attempts completed.

Both prompts requested a JavaScript Object Notation (JSON) object containing a brand, a generic equipment name, confidence and a brief rationale. Both prioritised the specification/model and permitted the Chinese token “未知” (“unknown”) when a brand could not be reliably determined. The search prompt additionally requested use of web-search information. The prompts were therefore similar in purpose but not identical. Complete original prompts, English translations and request settings are provided in Online Resource 1.

The comparison concerns these two implemented workflows. It does not hold platform, model identifier, reasoning configuration, prompt wording or output budget constant. In particular, the search workflow also enabled thinking. The available records do not establish that both identifiers resolved to identical underlying model snapshots. We therefore avoid interpreting the observed difference as a causal effect of retrieval alone. Provider-controlled retrieval, search indexing and model updates also limit exact reproduction of the original calls.

The adjudicated workbook contained one retained output and elapsed-time value for each workflow and record. The present analysis did not rerun either model. Parsing normalised an absent or empty returned brand to “unknown”; unresolved failures raised an error in the original scripts. The adjudicated workbook alone does not identify the number of retries or distinguish every parser-generated unknown from an intentional model abstention. Output confidence values and rationales were not used to redefine the expert correctness labels.

### 2.3 Expert reference establishment

Two experts, each with more than eight years of experience related to fixed-asset management, independently assessed all sampled records without seeing the AI outputs. They queried internet sources and consulted available equipment manuals to identify the relevant brand. Historical procurement contracts and acceptance records were often unavailable; access to such original vouchers was not assumed for all records. Initial assessments agreed for 946 records. The remaining 54 were resolved through discussion and additional searches before the final reference was established. The source file's recorded agreement indicator was used because literal string comparison would misclassify some brand aliases as disagreements.

The final reference identified a brand when the experts could reliably confirm it from the available information. Otherwise, the record remained unresolved. An unresolved reference means that the experts could not establish a brand; it does not prove that the asset had no brand. After reconciliation, the same two experts jointly assessed AI output correctness against the reference. Their assessment recognised equivalent Chinese and English names, abbreviations and other brand aliases. This stage necessarily involved viewing AI answers, whereas initial reference formation was blinded. No additional independent adjudicator was used.

### 2.4 Data-quality and reliability outcomes

The primary analytical outcome was verified brand identification yield: the number of specific brand outputs judged correct, divided by all 1000 records. Specific-output coverage was the proportion of records for which the workflow supplied a brand rather than unknown. Conditional correctness was the number of correct brand outputs divided by the number of specific outputs from that workflow. These denominators answer different questions and were reported explicitly.

Candidate coverage measures the availability of proposed values; verified yield measures supported recovery across all evaluated records. Conditional correctness includes unverified specific outputs in its denominator. Incorrect assignments indicate contradictions with confirmed references, whereas unverified assignments indicate unresolved reference evidence. Unknown outputs retain missing information and are separated by whether a reference brand could be established. These outcomes apply existing data-quality concepts to this task; they do not constitute an independently validated assessment framework.

Each workflow's results were partitioned into five mutually exclusive categories. Correct assignments were specific outputs accepted against a confirmed reference. Incorrect assignments were specific outputs rejected when the reference brand was known. Unverified assignments were specific outputs for records with unresolved reference brands. Missed identifications occurred when the workflow returned unknown despite a confirmed reference. The remaining category comprised records for which both the workflow and the reference remained unknown. Unverified assignments were not automatically classified as hallucinations.

For the paired three-category table, the original adjudication labels were retained: correct, not correct, and both unknown. “Not correct” includes incorrect assignments, unverified assignments and missed identifications. For exploratory review-stratum analysis, records were stratified by whether both workflows, search only, reasoning only, or neither workflow supplied a specific brand. Both supplying a brand did not require those brands to match. Exact-string agreement was examined only as a supplementary description, without replacing expert synonym-aware assessment.

### 2.5 Statistical analysis

Counts and percentages describe categorical outcomes. We calculated the paired difference in verified yield as search minus reasoning. A two-sided exact McNemar test used discordant pairs for correct versus not-correct outcomes, treating all remaining outcomes as not correct. Because repeated equipment descriptions violate a simple independent-record interpretation, this test is reported as a conventional record-level comparison alongside cluster-based intervals.

Clusters were defined by the exact stored equipment name and specification/model combination. We used a non-parametric cluster bootstrap to preserve dependence within these combinations [13]. In each of 6000 replicates, 418 clusters were sampled with replacement and all their records retained, including both workflow outcomes. We recalculated the record-weighted yield difference and conditional proportions using each replicate's actual denominators. Percentiles 2.5 and 97.5 defined 95% confidence intervals (CIs). Clusters were sorted before resampling, and the NumPy random generator used seed 20261029.

As a sensitivity analysis, we calculated the mean within-cluster yield difference, assigning equal weight to each name–model combination. The record-weighted estimand describes performance across the sampled inventory records; the combination-weighted estimand describes the average difference across observed combinations. Neither interval quantifies variation across repeated model calls or different hospitals. No finite-population correction was applied: the intervals describe variation across represented equipment combinations, rather than design-based uncertainty confined to the 1101-record source frame. The sample size followed the available evaluation design, without a reported prospective power calculation.

Device-category and review-stratum analyses were exploratory. We did not conduct multiple subgroup significance tests or an independent validation of a review rule. The two conditional correctness proportions were not compared using McNemar's test because their denominators contain different selected records. Elapsed-time summaries were reported descriptively and were not treated as human labour. Analyses used Python 3.12.14, NumPy 2.5.4, SciPy 1.18.1 and openpyxl 3.1.5. Online Resource 1 describes the analysis and reproduction procedure; Online Resource 2 provides aggregate statistical results and reproducibility instructions. Executable code, dependencies and machine-readable aggregates are available at https://github.com/xuean009/hospital-equipment-metadata-recovery/tree/v1.0.1. The sampling seed 20260416 and bootstrap seed 20261029 are numeric random-generator inputs, not dates of study activities.

### 2.6 AI assistance and reproducibility

OpenAI Codex (OpenAI) [14] assisted with analysis-code support, English-language editing, manuscript restructuring, document preparation and Python/Matplotlib figure production. The researchers checked the statistical outputs against the adjudicated data and reviewed the manuscript, references and figures; they retain responsibility for the analyses and content. This assistance is distinct from the two DeepSeek workflows evaluated as the research intervention. Further software-disclosure details are provided in Statements and Declarations.

## 3 Results

### 3.1 Inventory composition and reference assessment

The 1000 records represented 24 equipment categories and 418 distinct equipment name–model combinations (Table 1). Of these combinations, 164 occurred more than once. Experts confirmed reference brands for 744 records (74.4%); 256 (25.6%) remained unresolved. Initial expert agreement was 94.6%, with reconciliation required for 5.4%. All paired outputs and correctness labels required for analysis were present.

The largest category was ward nursing and hospital equipment, comprising 235 records. Disinfection and sterilisation equipment accounted for 118, and medical electrophysiological equipment accounted for 109. Radiotherapy equipment contributed 93 records, and emergency and life-support equipment contributed 76. These categories illustrate the sample's uneven composition; the full category distribution and descriptive results are provided in Online Resource 1.

### 3.2 Verified identification and output coverage

The reasoning workflow produced 308 verified correct brands (30.8% of records), compared with 524 (52.4%) for web-enabled search (Table 2). The difference was 21.6 percentage points, with a cluster-bootstrap 95% CI of 14.9–28.6. Among the 744 records with confirmed reference brands, the corresponding proportions were 41.4% and 70.4%. These latter proportions exclude unresolved records and are distinct from the all-record primary outcome.

Reasoning supplied a specific brand for 373 records (37.3%), whereas search supplied one for 720 (72.0%). Conditional correctness was 82.6% (308/373) and 72.8% (524/720), respectively. Thus, search generated 347 additional specific outputs and 216 additional verified correct identifications in aggregate. Unknown outputs decreased from 627 to 280. This comparison shows the simultaneous increase in coverage and decrease in conditional correctness.

### 3.3 Paired transitions and sensitivity analysis

Both workflows were correct for 294 records, and neither was correct for 462. Search was correct and reasoning was not for 230 records; reasoning was correct and search was not for 14 (Figure 2a). The exact McNemar P value was 1.57 × 10⁻⁵¹. This record-level test did not account for repeated name–model combinations and should be interpreted with that limitation. The full three-category paired table is presented in Table 3.

The combination-weighted difference was 14.0 percentage points (cluster-bootstrap 95% CI, 10.5–17.6), compared with the record-weighted difference of 21.6 points (Figure 2b). Both estimates favoured the search workflow within this sample. Their different magnitudes indicate that inventory repetition affected the aggregate comparison. The combination-weighted estimate gives a frequently repeated description the same total weight as a description observed only once.

### 3.4 Assignment errors and unresolved records

Reasoning made 60 incorrect assignments against known reference brands, while search made 121 (Table 2; Figure 3a,b). On the 256 unresolved records, reasoning supplied five specific brands and search supplied 75, corresponding to 2.0% and 29.3%. These were unverified assignments, not proven falsehoods. The workflows retained unknown for 251 and 181 unresolved records, respectively.

For records with confirmed reference brands, reasoning missed 376 identifications by returning unknown; search missed 99. Overall, 65 reasoning outputs and 196 search outputs were specific but not accepted as correct. Those totals combine incorrect and unverified assignments, which have different evidential meanings. All five outcome categories summed to 1000 for each workflow.

### 3.5 Exploratory review strata and elapsed time

Both workflows output specific brands for 366 records, search alone for 354, reasoning alone for seven, and neither for 273 (Table 4). In the first stratum, 326 search outputs were correct (89.1%; cluster-bootstrap 95% CI, 83.0–93.8). In the search-only stratum, 198 were correct (55.9%; 95% CI, 43.0–66.7). There were three unresolved reference brands in the first stratum and 72 in the second. Figure 3c presents these within-sample associations without implying that either stratum can be accepted automatically.

Summed recorded processing times were 36785.51 seconds for reasoning and 32614.01 seconds for search. Median times were 35.18 seconds (interquartile range, 30.20–41.90) and 31.27 seconds (23.88–38.57), respectively. These are recorded request-processing durations. They do not measure expert labour, overall implementation time or monetary savings, and they were not subjected to a comparative efficiency claim.

## 4 Discussion

### 4.1 Feasibility of recovering missing healthcare equipment metadata

The two workflows recovered verifiable candidate brands for 308 and 524 of the 1000 selected historical records. These findings support the feasibility of candidate generation from retained equipment names and usable models when original documentation is incomplete. They also show why the number of populated fields is insufficient to describe successful information recovery. Specific outputs included confirmed errors and assignments that could not be verified against the available reference evidence. The information-science contribution is the joint assessment of recoverable metadata and residual assignment uncertainty in a real institutional resource.

Data-quality reviews describe multiple dimensions and substantial variation in their operational definitions [4,5]. Our evaluation applies those distinctions to a specific missing-field task, using explicit denominators and expert assessment. Verified brand identification yield measures supported recovery across all records, whereas specific-output coverage measures the availability of proposed values. Conditional correctness describes the composition of those outputs, and the five outcome categories identify different unresolved problems. This application extends the interpretation of candidate generation without claiming a new general data-quality framework. The observed proportions remain conditional on the study inventory, eligibility criteria and evaluated configurations.

### 4.2 Coverage–reliability trade-offs in AI-assisted metadata completion

Search returned specific brands for 720 records, compared with 373 for reasoning, and produced more verified correct identifications overall. However, conditional correctness was 72.8% for search and 82.6% for reasoning, and search produced more incorrect and unverified assignments. These conditional proportions concern different output-selected populations and were compared descriptively. Higher coverage expanded both the pool of supported candidates and the pool requiring rejection or further investigation. Reporting coverage alongside verified yield and assignment categories makes this trade-off visible without treating every completed field as reliable information [6,7,8].

External retrieval provides a plausible route to product information that is unavailable in an abbreviated equipment description. Almanac evaluated retrieval from medical resources with expert review [10], whereas our search workflow used a provider-operated web facility without an evaluated equipment-source corpus. Retrieval relevance, citation accuracy and source quality were not systematically measured. Furthermore, the workflows differed in provider, model identifier, prompt wording and output budget, and the search condition also enabled thinking. The 21.6-percentage-point difference therefore characterizes the complete workflows; it does not identify the causal benefit of adding retrieval alone. A controlled comparison would hold the model and prompt constant while varying retrieval access.

The combination-weighted difference of 14.0 percentage points was smaller than the record-weighted difference of 21.6 points. This distinction matters when institutional inventories contain many instances of the same equipment description. Record weighting reflects the frequency of those descriptions in the sampled resource, whereas combination weighting describes the average difference across observed name–model combinations. Both estimates are relevant, but neither establishes performance on unseen equipment families or at another hospital. The cluster intervals address observed repetition rather than stochastic variation across repeated model calls.

### 4.3 Evidence uncertainty and human verification

Incorrect assignments and unverified assignments require different interpretations and review actions. An incorrect assignment contradicts a confirmed reference and requires rejection or correction. An unverified assignment lacks sufficient reference confirmation and requires additional evidence before acceptance. Reasoning supplied five specific brands among unresolved reference records, whereas search supplied 75. Some of these candidates might ultimately be correct if better documentation becomes available. Describing all unverified outputs as hallucinations would therefore exceed the evidence available in this study.

Unknown outputs also have different meanings according to reference status. Returning unknown despite a confirmed reference represents missed recovery, while retaining unknown for an unresolved reference preserves visible uncertainty. Research on language-model evaluation has shown how accuracy-based incentives can reward guessing, supporting separate reporting of abstention and correct answers [15]. Here, however, stored unknowns may include parser-normalised empty outputs, so they cannot always be interpreted as intentional model abstention. The expert reference also remained fallible because documentary evidence was incomplete and some public sources could overlap with those available to search.

### 4.4 Implications for health information systems

The findings support a design distinction between candidate metadata and approved registry values. A proposed system would retain candidate brands separately until an authorised reviewer confirms supporting evidence. Candidate records could include the source consulted, evidence status, reviewer, review date and acceptance or rejection decision. Unresolved cases would remain identifiable and could be revisited when further documentation becomes available. These are design recommendations derived from the observed outcome categories, rather than features implemented and evaluated in this study.

Such separation places evidence and accountability within the information-processing workflow. A sociotechnical model emphasises the relationship between health-information technology, people and organisational processes [16]. WHO guidance similarly stresses accountability for health AI, including generative systems [17,18]. DECIDE-AI highlights human factors and evaluation during operational use, although its clinical decision-support scope differs from this equipment-metadata task [19]. These principles support prospective assessment of reviewer decisions and residual errors before AI candidates are incorporated into authoritative information resources.

The exploratory output strata may inform questions for that future assessment. Search correctness was 89.1% when both workflows supplied brands and 55.9% when only search did so. Nevertheless, both supplying a brand did not require agreement, and 40 of the 366 search outputs in the first stratum were not verified correct. The strata were derived and evaluated in the same sample, with no independently validated automatic-acceptance threshold. Future evaluation could assess review prioritisation while preserving verification for all candidates. It should measure approved corrections, residual errors, reviewer workload and actual human time rather than infer benefits from request-processing durations.

### 4.5 Limitations and future evaluation

This study has several limitations. First, it evaluated a selected missing-brand remediation pool at one hospital, restricted by equipment category, price and usable model information. Records lacking usable models may present greater recovery difficulties, but were excluded from this evaluation. The findings therefore do not support a solution for all forms of missing historical asset information. Neither the prevalence of missing brands nor the availability of historical documents in other hospitals can be inferred from this sample. The final workbook does not retain the original brand-field status or registration year. Those upstream restrictions rely on the asset-management team's confirmed source-pool description, rather than a new record-level reconstruction.

Second, each workflow contributed one retained output per record. We did not quantify stochastic variation across repeated calls or compare alternative prompts and retrieval configurations. Provider updates and changing web content limit temporal reproducibility. A brand already present within an equipment name or model field could make identification easier; this was not separately classified. The study therefore combines direct extraction, recognition and inference rather than isolating inference from information-free descriptions.

Third, the reference was expert-based and depended on internet sources and available equipment manuals. Missing historical contracts and acceptance records limited the available documentary evidence. Initial blinding reduced direct incorporation of AI answers into reference formation, but did not make the reference infallible. Experts and the search workflow could consult overlapping public sources. Evidence provenance was not systematically scored per record, and a formal hierarchy of documentary sources was not available for analysis. Initial agreement was high, but no synonym-normalised independent label set was available for estimating a chance-corrected agreement coefficient.

Fourth, repeated equipment descriptions reduced the number of distinct identification problems. Cluster resampling addressed observed name–model repetition, but exact-string grouping may separate synonymous descriptions and cannot capture every dependency between related equipment families. The smaller combination-weighted effect reinforces the need to report both estimands. Bootstrap intervals remain conditional on the observed workflow configuration and do not establish transportability to other hospitals.

Finally, risk strata were derived and evaluated in the same dataset. No safe acceptance threshold, deployed review policy or labour saving was established. Technical failures and retries were not fully characterised by the adjudicated workbook, and recorded unknowns may include parser-normalised empty responses. Future work should prospectively retain source evidence and technical logs, evaluate repeatability, and test review policies on independent inventories before operational adoption.

## 5 Conclusion

Generative AI workflows recovered verifiable candidate brands from selected historical hospital equipment records with retained names and usable models. Broader candidate coverage accompanied more incorrect and unverified assignments, demonstrating the need to distinguish proposed metadata from supported information. The evaluation contributes evidence on recovery and reliability, with explicit treatment of unresolved reference records and repeated equipment descriptions. Expert verification remains necessary before candidate values enter official registries. These workflow comparisons do not isolate retrieval effects or establish applicability to records lacking usable models, workload reductions or benefits after deployment.

## List of abbreviations

AI: artificial intelligence; API: application programming interface; CI: confidence interval; JSON: JavaScript Object Notation; WHO: World Health Organization.

## Statements and Declarations

### Ethics approval and consent to participate

Not applicable. This study analysed de-identified equipment inventory records and did not involve human participants, human biological material or patient-level data. The hospital authorised the research use of the de-identified asset data.

### Consent for publication

Not applicable. The manuscript contains no individual person's data.

### Availability of data and materials

The record-level dataset is not publicly available because access is restricted by the hospital. Requests for access may be addressed to the corresponding author and are subject to institutional approval. Aggregate statistical results and reproduction instructions are provided in Online Resource 2. Analysis, figure and document-generation code, dependency specifications and machine-readable aggregates are available at https://github.com/xuean009/hospital-equipment-metadata-recovery/tree/v1.0.1. Online Resource 1 documents the methods and supplementary results. Reproducing record-level analyses requires authorised access to the adjudicated dataset.

### Competing interests

The authors declare no competing interests.

### Funding

This research received no funding.

### Authors' contributions

YQ: conceptualisation, methodology, investigation, data curation, formal analysis, software, visualisation and writing—original draft. ZZ: conceptualisation, methodology, investigation, project administration and writing—review and editing. All authors approved the submitted version and accept accountability for the work.

### Use of AI assistance

OpenAI Codex (OpenAI) [14] assisted with language editing, manuscript restructuring, document preparation and analysis-code support. The application version reported for the earlier manuscript preparation was 26.1021.31345; it is not asserted to identify the software used for this transfer revision. A complete historical record of application versions and underlying model identifiers was not available for this disclosure. The application version does not identify the underlying model. The authors reviewed the AI-assisted text, references, code and outputs and remain responsible for the accuracy, originality and integrity of the manuscript. DeepSeek was the research intervention described in Methods. Figures were prepared using Python and Matplotlib.

## Supplementary Information

Online Resource 1 (ESM_1.pdf). Supplementary methods and results: outcome definitions, source-pool and sampling details, original prompts and translations, workflow settings, cluster-bootstrap methods, equipment-category results and sensitivity analyses.

Online Resource 2 (ESM_2.pdf). Aggregate statistical results and reproducibility guide: outcome definitions, aggregate tables, paired comparisons, cluster-bootstrap estimates and instructions for accessing the versioned GitHub code repository (https://github.com/xuean009/hospital-equipment-metadata-recovery/tree/v1.0.1). Individual records are not publicly available. Full record-level statistical reproduction requires the separately authorised adjudicated workbook.

## References

1. World Health Organization: Introduction to medical equipment inventory management. World Health Organization, Geneva (2011). https://www.who.int/publications/i/item/9789241501392. Accessed 2 Nov 2026.

2. World Health Organization: Inventory and maintenance management information system for medical devices. World Health Organization, Geneva (2025). https://www.who.int/publications/i/item/9789240111257. Accessed 2 Nov 2026.

3. World Health Organization: Computerized maintenance management system. World Health Organization, Geneva (2011). https://www.who.int/publications/i/item/9789241501415. Accessed 2 Nov 2026.

4. Ghalavand, H., Shirshahi, S., Rahimi, A., Zarrinabadi, Z., Amani, F.: Common data quality elements for health information systems: a systematic review. BMC Med Inform Decis Mak 24, 243 (2024). https://doi.org/10.1186/s12911-024-02644-7

5. Hosseinzadeh, E., Afkanpour, M., Momeni, M., Tabesh, H.: Data quality assessment in healthcare, dimensions, methods and tools: a systematic review. BMC Med Inform Decis Mak 25, 296 (2025). https://doi.org/10.1186/s12911-025-03136-y

6. Wang, R.Y., Strong, D.M.: Beyond accuracy: what data quality means to data consumers. J Manag Inf Syst 12(4), 5–33 (1996). https://doi.org/10.1080/07421222.1996.11518099

7. Weiskopf, N.G., Weng, C.: Methods and dimensions of electronic health record data quality assessment: enabling reuse for clinical research. J Am Med Inform Assoc 20, 144–151 (2013). https://doi.org/10.1136/amiajnl-2011-000681

8. Kahn, M.G., Callahan, T.J., Barnard, J., Bauck, A.E., Brown, J., Davidson, B.N., et al.: A harmonized data quality assessment terminology and framework for the secondary use of electronic health record data. EGEMS (Wash DC) 4, 1244 (2016). https://doi.org/10.13063/2327-9214.1244

9. Li, X., Song, Y., Li, Y., Li, Y., Wu, K., Huang, Y., Zhang, K.: CoT-CC: chain-of-thought reasoning and contrastive correction for zero-shot medical relation extraction. Health Inf Sci Syst 14, 87 (2026). https://doi.org/10.1007/s13755-026-00479-2

10. Zakka, C., Shad, R., Chaurasia, A., Dalal, A.R., Kim, J.L., Moor, M., et al.: Almanac—retrieval-augmented language models for clinical medicine. NEJM AI 1, AIoa2300068 (2024). https://doi.org/10.1056/AIoa2300068

11. Miao, Y., Zhao, Y., Luo, Y., Wang, H., Wu, Y.: Improving large language model applications in the medical and nursing domains with retrieval-augmented generation: scoping review. J Med Internet Res 27, e80557 (2025). https://doi.org/10.2196/80557

12. Benchimol, E.I., Smeeth, L., Guttmann, A., Harron, K., Moher, D., Petersen, I., et al.: The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) statement. PLoS Med 12(10), e1001885 (2015). https://doi.org/10.1371/journal.pmed.1001885

13. Field, C.A., Welsh, A.H.: Bootstrapping clustered data. J R Stat Soc Series B Stat Methodol 69, 369–390 (2007). https://doi.org/10.1111/j.1467-9868.2007.00593.x

14. OpenAI. Codex. https://openai.com/codex/. Accessed 2 Nov 2026.

15. Kalai, A.T., Nachum, O., Vempala, S.S., Zhang, E.: Evaluating large language models for accuracy incentivizes hallucinations. Nature 653, 1047–1051 (2026). https://doi.org/10.1038/s41586-026-10549-w

16. Sittig, D.F., Singh, H.: A new sociotechnical model for studying health information technology in complex adaptive healthcare systems. Qual Saf Health Care 19 Suppl 3, i68–i74 (2010). https://doi.org/10.1136/qshc.2010.042085

17. World Health Organization: Ethics and governance of artificial intelligence for health: WHO guidance. World Health Organization, Geneva (2021). https://www.who.int/publications/i/item/9789240029200. Accessed 2 Nov 2026.

18. World Health Organization: Ethics and governance of artificial intelligence for health: guidance on large multi-modal models. World Health Organization, Geneva (2024). https://www.who.int/publications/i/item/9789240084759. Accessed 2 Nov 2026.

19. Vasey, B., Nagendran, M., Campbell, B., Clifton, D.A., Collins, G.S., Denaxas, S., et al.: Reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI. Nat Med 28, 924–933 (2022). https://doi.org/10.1038/s41591-022-01772-9
