"""Build manuscript and supplementary DOCX from verified aggregate results.
Requires python-docx and the analysis_summary.json produced by analyze.py.
"""
from pathlib import Path
import sys,json,re,ast,csv
ROOT=Path(__file__).resolve().parents[1]
(ROOT/'qa').mkdir(exist_ok=True)
if (ROOT/'.runtime').exists():sys.path.insert(0,str(ROOT/'.runtime'))
from docx import Document
from docx.shared import Inches,Pt,Mm,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
S=json.loads((ROOT/'source_data'/'analysis_summary.json').read_text(encoding='utf-8'))
C=json.loads((ROOT/'source_data'/'study_context.json').read_text(encoding='utf-8'))
def pct(x):return f'{100*x:.1f}'
def interval(x):return f'{pct(x[0])}–{pct(x[1])}'
def nper(n,d=1000):return f'{n} ({100*n/d:.1f}%)'
CAT=['Ward nursing and hospital equipment','Disinfection and sterilisation equipment','Medical electrophysiological equipment','Radiotherapy equipment','Emergency and life-support equipment','Operating theatre equipment and accessories','Clinical laboratory equipment','Physical therapy, rehabilitation and exercise therapy equipment','Medical radiation monitoring equipment','Medical ultrasound equipment','Other medical equipment','Medical X-ray accessories and components','Medical radiation protection equipment','Medical endoscopes','Medical low-temperature and cryotherapy equipment','Diagnostic X-ray equipment','Magnetic resonance equipment','Magnetic resonance accessories','Pharmacy equipment','Extracorporeal circulation equipment','Medical laser equipment','Surgical instruments','Water pollution control equipment','Epidemic prevention and protective health equipment']
assert len(CAT)==len(S['categories'])==24
def setup(line_numbers=True):
    d=Document();sec=d.sections[0]
    sec.page_width=Mm(210);sec.page_height=Mm(297)
    sec.top_margin=Mm(22);sec.bottom_margin=Mm(22);sec.left_margin=Mm(20);sec.right_margin=Mm(20)
    sec.header_distance=Mm(9);sec.footer_distance=Mm(10)
    for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3']:
        st=d.styles[name];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0)
        st.font.underline=False
        st._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Microsoft YaHei')
    for st in d.styles:
        for border in list(st._element.iter(qn('w:pBdr'))):border.getparent().remove(border)
        if hasattr(st,'paragraph_format'):
            st.paragraph_format.page_break_before=False
    d.styles['Normal'].font.size=Pt(11)
    d.styles['Normal'].paragraph_format.line_spacing=2
    d.styles['Normal'].paragraph_format.space_after=Pt(5)
    for name,sz in [('Title',17),('Heading 1',13),('Heading 2',11)]:
        st=d.styles[name];st.font.size=Pt(sz);st.font.bold=True
        st.paragraph_format.space_before=Pt(10);st.paragraph_format.space_after=Pt(5)
        st.paragraph_format.keep_with_next=True
    if line_numbers:
        ln=OxmlElement('w:lnNumType');ln.set(qn('w:countBy'),'1');ln.set(qn('w:restart'),'continuous');ln.set(qn('w:distance'),'170');sec._sectPr.append(ln)
    footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=footer.add_run();fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');r._r.append(fld)
    d.core_properties.author='Yihan Qi; Zhenqi Zhang'
    return d
def para(d,text,size=None):
    p=d.add_paragraph(text)
    if size:
        for r in p.runs:r.font.size=Pt(size)
    return p
def table(d,title,headers,rows,widths,note='',newpage=True):
    rows=[[re.sub(r'(?<=\d),(?=\d{3}(?:\D|$))','',str(v)) for v in row] for row in rows]
    key=title.split('.')[0].replace(' ','_')
    with (ROOT/'source_data'/(key+'.csv')).open('w',newline='',encoding='utf-8-sig') as f:
        cw=csv.writer(f);cw.writerow(headers);cw.writerows(rows)
    cap=d.add_paragraph(title)
    cap.paragraph_format.keep_with_next=True
    cap.paragraph_format.line_spacing=1.15
    for r in cap.runs:r.bold=True;r.font.size=Pt(10)
    t=d.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for c,w in zip(t.columns,widths):c.width=Mm(w)
    for c,v in zip(t.rows[0].cells,headers):c.text=str(v)
    for row in rows:
        for c,v in zip(t.add_row().cells,row):c.text=str(v)
    for i,row in enumerate(t.rows):
        pr=row._tr.get_or_add_trPr();cant=OxmlElement('w:cantSplit');pr.append(cant)
        if i==0:
            repeat=OxmlElement('w:tblHeader');pr.append(repeat)
        for j,c in enumerate(row.cells):
            c.width=Mm(widths[j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcPr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                e=OxmlElement('w:'+side)
                visible=(side=='top' and i==0) or (side=='bottom' and (i==0 or i==len(t.rows)-1))
                e.set(qn('w:val'),'single' if visible else 'nil');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'000000');b.append(e)
            tcPr.append(b)
            mar=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                e=OxmlElement('w:'+side);e.set(qn('w:w'),'75');e.set(qn('w:type'),'dxa');mar.append(e)
            tcPr.append(mar)
            for p in c.paragraphs:
                p.paragraph_format.line_spacing=1.15;p.paragraph_format.space_after=Pt(0);p.paragraph_format.space_before=Pt(0)
                p.paragraph_format.keep_with_next=(i==0)
                if j>0:p.alignment=WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:r.font.size=Pt(10);r.font.bold=(i==0);r.font.color.rgb=RGBColor(0,0,0)
    if note:
        p=para(d,re.sub(r'(?<=\d),(?=\d{3}(?:\D|$))','',note),10);p.paragraph_format.line_spacing=1.15
    return t

FIGLEG=[
('Figure 1. Study design and reference assessment','Figure_1_study_design',
'a, The source was the 2010–2025 historical asset-ledger remediation pool, preselected for missing brand fields. Equipment-category, price and model criteria yielded 1101 eligible records; 1000 were sampled without replacement, representing 418 equipment name–model combinations. b, Both AI workflows received the same equipment name and model and were run in March 2026. In a separate reference pathway, two experts independently reviewed records while blinded to AI outputs, using internet sources and available equipment manuals; 946 initial assessments agreed and 54 disagreements were reconciled. c, Reference brands were confirmed for 744 records and remained unresolved for 256. After reference formation, the experts jointly scored AI outputs using brand equivalence rather than literal string matching. Unresolved means insufficient confirmation, not proven absence of a brand. Expert reference assessment and output evaluation took place in April–May 2026.'),
('Figure 2. Paired identification changes and sensitivity to repeated equipment combinations','Figure_2_paired_effects',
'a, Flow widths are proportional to the number of records in each paired correct/not-correct outcome. All 1,000 records are retained. Not correct includes incorrect or unverified assignments and unknown outputs. b, Points show search-minus-reasoning differences in verified identification yield. Record weighting retains the inventory frequency of each combination; combination weighting averages within-combination differences equally. Error bars are percentile 95% confidence intervals from 6,000 bootstrap replicates sampling all 418 name–model clusters with replacement. The same resampled clusters are used for both estimands; seed 20261029. Intervals quantify sampled-cluster variability, not repeated model runs. The exact record-level McNemar test gave P = 1.57 × 10⁻⁵¹ and does not account for clustering.'),
('Figure 3. Output coverage, assignment risk and exploratory review strata','Figure_3_coverage_risk',
'a, Each point represents one workflow; coverage uses all 1,000 records, whereas conditional correctness uses that workflow’s specific brand outputs. b, Five mutually exclusive categories sum to 1,000 per workflow. Labels show counts; bar lengths show percentages. Incorrect assignments contradict known reference brands; unverified assignments occur when the reference is unresolved. Missed identification denotes unknown output despite a known reference, and both unknown denotes unresolved reference and unknown output. c, Search correctness is stratified by the presence of specific outputs from the two workflows. Both outputting a brand does not imply equivalent brands. Points are observed proportions; bars are cluster-bootstrap percentile 95% confidence intervals (6,000 replicates; 418 clusters; seed 20261029), with denominators recalculated each time. Strata were explored in the same dataset, with no independent validation or automatic-acceptance threshold.')]

def build_tables(d):
    rows=[['Eligible source records','1101'],['Sampled paired records','1000'],['Asset years in source pool',C['asset_years']],['Brand-field status at pool entry','Missing'],['Model execution period',C['model_run_period']],['Expert assessment period',C['expert_review_period']],['Equipment categories','24'],['Distinct name–model combinations','418'],['Combinations occurring more than once','164'],['Initial expert agreement','946/1000 (94.6%)'],['Disagreements reconciled','54/1000 (5.4%)'],['Confirmed reference brand','744/1000 (74.4%)'],['Unresolved reference brand','256/1000 (25.6%)']]
    rows += [[CAT[i],nper(v['n'])] for i,v in enumerate(S['categories'][:5])]
    rows += [['Other 19 categories',nper(sum(v['n'] for v in S['categories'][5:]))]]
    table(d,'Table 1. Inventory characteristics and expert reference assessment',['Characteristic','Value'],rows,[112,58],note='The final six rows give the five largest equipment categories and the remainder. The full 24-category distribution is in Online Resource 1. The source pool was preselected for missing brand fields and the 2010–2025 asset-year window. Years were not inferred from asset identifiers.')
    rows=[['Verified correct brand yield',nper(308),nper(524)],['Specific brand output coverage',nper(373),nper(720)],['Correct among specific outputs',f'308/373 (82.6%)',f'524/720 (72.8%)'],['Correct among confirmed references','308/744 (41.4%)','524/744 (70.4%)'],['Incorrect assignment',nper(60),nper(121)],['Unverified assignment',nper(5),nper(75)],['Missed identification',nper(376),nper(99)],['Both workflow and reference unknown',nper(251),nper(181)],['All unknown outputs',nper(627),nper(280)],['Total recorded processing time, s','36,785.51','32,614.01'],['Median processing time (IQR), s','35.18 (30.20–41.90)','31.27 (23.88–38.57)']]
    table(d,'Table 2. Brand identification and assignment outcomes',['Outcome','Reasoning','Web-enabled search'],rows,[86,42,42],note='Unless another denominator is shown, percentages use all 1,000 records. Correct, incorrect, unverified, missed identification and both unknown partition the sample. Other rows overlap these categories and must not be summed. Conditional correctness compares different output-selected subsets. IQR, interquartile range. Time is not human labour.')
    rows=[[label,*S['paired3'][i],sum(S['paired3'][i])] for i,label in enumerate(['Correct','Not correct','Both unknown'])]
    rows.append(['Total',524,295,181,1000])
    table(d,'Table 3. Paired adjudication outcomes and identification differences',['Reasoning outcome','Search correct','Search not correct','Search both unknown','Total'],rows,[54,29,29,35,23],note='Not correct includes incorrect assignments, unverified assignments and missed identifications; both unknown denotes an unresolved reference and an unknown workflow output. Categories reflect adjudication, not string equality.')
    para(d,f"Record-weighted difference: 21.6 percentage points (cluster-bootstrap 95% CI {interval(S['difference_ci'])}). Combination-weighted difference: 14.0 points (95% CI {interval(S['equal_group_ci'])}).",10)
    para(d,'Correctness-discordant pairs: search only correct, 230; reasoning only correct, 14. Exact two-sided McNemar P = 1.57 × 10⁻⁵¹ (record-level test without cluster adjustment). Bootstrap: 6000 draws of 418 clusters, seed 20261029.',10)
    rows=[]
    for k,v in enumerate(S['risk']):rows.append([v['label'],v['n'],v['reasoning_correct'],v['search_correct'],v['unresolved'],(f"{100*v['search_yield']:.1f}%\n({interval(v['ci'])})" if k<2 else 'Not applicable')])
    table(d,'Table 4. Exploratory review strata defined by output presence',['Output stratum','n','Reasoning correct','Search correct','Reference unresolved','Search correctness\n(95% CI)'],rows,[48,14,25,25,26,32],note='Conditional search correctness is defined only in strata receiving a search brand output. Both workflows outputting brands does not imply agreement. Intervals use name–model cluster bootstrap; all strata are exploratory and were not validated independently.')

def figure(d, number):
    title,name,legend=FIGLEG[number-1]
    p=d.add_paragraph()
    p.paragraph_format.line_spacing=1
    p.paragraph_format.keep_with_next=True
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run();r.add_picture(str(ROOT/'figures'/(name+'.png')),width=Mm(170))
    docpr=d.inline_shapes[-1]._inline.docPr
    docpr.set('descr',title.split('. ',1)[1]+'. '+legend)
    p=d.add_paragraph()
    p.paragraph_format.line_spacing=1.05
    p.paragraph_format.space_after=Pt(8)
    p.paragraph_format.keep_together=True
    r=p.add_run(f'Fig. {number}');r.bold=True;r.font.size=Pt(9)
    r=p.add_run(' '+title.split('. ',1)[1]+'. '+legend.rstrip('.'));r.font.size=Pt(9)

def main_doc():
    src=(ROOT/'code'/'manuscript.md').read_text(encoding='utf-8')
    assert '{{' not in src
    (ROOT/'Main_Manuscript.md').write_text(src,encoding='utf-8')
    # Build editable tables once and move their complete caption/body/note groups.
    td=setup(False);build_tables(td)
    groups={};current=None
    for element in list(td._element.body):
        txt=''.join(element.itertext()) if False else ''.join(element.xpath('.//w:t/text()'))
        if element.tag==qn('w:sectPr'):continue
        match=re.match(r'Table ([1-4])\.',txt)
        if match:current=int(match[1]);groups[current]=[]
        if current:groups[current].append(element)
    # Insert each object at the end of its corresponding subsection.
    before={
      '### 2.4':[('figure',1)],
      '### 3.2':[('table',1)],
      '### 3.3':[('table',2)],
      '### 3.4':[('table',3),('figure',2)],
      '### 3.5':[('figure',3)],
      '## 4 Discussion':[('table',4)],
    }
    d=setup();in_abstract=False;in_refs=False
    for block in src.split('\n\n'):
        block=block.strip()
        if not block:continue
        for prefix,objects in before.items():
            if block.startswith(prefix):
                for typ,n in objects:
                    if typ=='figure':figure(d,n)
                    else:
                        for el in groups[n]:d._element.body.insert(len(d._element.body)-1,el)
        if block.startswith('# '):d.add_paragraph(block[2:],'Title')
        elif block.startswith('## '):
            in_abstract=block=='## Abstract';in_refs=block=='## References'
            d.add_heading(block[3:],level=1)
        elif block.startswith('### '):d.add_heading(block[4:],level=2)
        else:
            p=para(d,block)
            if block.startswith('Acknowledgements:'):
                p.paragraph_format.line_spacing=1.15
                for run in p.runs:run.font.size=Pt(9)
            if in_refs:
                p.paragraph_format.line_spacing=1.15
                p.paragraph_format.space_after=Pt(6)
                p.paragraph_format.keep_together=True
                for run in p.runs:run.font.size=Pt(10)
        if in_abstract:
            d.paragraphs[-1].paragraph_format.space_after=Pt(2)
            if block.startswith('### '):d.paragraphs[-1].paragraph_format.space_before=Pt(4)
    d.core_properties.title=src.splitlines()[0][2:]
    d.save(ROOT/'Main_Manuscript.docx')
    ab=src.split('## Abstract')[1].split('Keywords:')[0]
    ab=re.sub(r'### \w+','',ab)
    wc=len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",ab))
    assert 150<=wc<=250,wc
    (ROOT/'qa'/'word_counts.json').write_text(json.dumps({'abstract_words':wc,'body_words':len(src.split('\n## 1 Introduction\n')[1].split('\n## List of abbreviations')[0].split()),'total_text_words':len(src.split())},indent=2),encoding='utf-8')

def cover_doc():
    source=ROOT/'Cover_Letter.md'
    if not source.exists():return
    d=setup(False)
    d.styles['Normal'].font.size=Pt(10.5)
    d.styles['Normal'].paragraph_format.line_spacing=1.05
    d.styles['Normal'].paragraph_format.space_after=Pt(7)
    for block in source.read_text(encoding='utf-8').strip().split('\n\n'):
        para(d,block)
    d.core_properties.title='Cover letter to Health Information Science and Systems'
    d.save(ROOT/'Cover_Letter.docx')

def prompts():
    stored=ROOT/'source_data'/'original_prompts.json'
    if stored.exists():return json.loads(stored.read_text(encoding='utf-8'))
    project=ROOT.parents[2]
    out={}
    for name,file in [('Reasoning','deepseek_excel_fill_reasoner.py'),('Web-enabled search','tencent_deepseek_excel_search.py')]:
        t=ast.parse((project/'实验'/file).read_text(encoding='utf-8-sig'))
        node=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='build_messages')
        scope={};exec(compile(ast.Module(body=[node],type_ignores=[]),'<prompt extraction>','exec'),scope)
        out[name]=scope['build_messages']('[DEVICE NAME]','[SPECIFICATION/MODEL]')
    return out

def supp_doc():
    d=setup(False);d.styles['Normal'].paragraph_format.line_spacing=1.5
    d.add_paragraph('Online Resource 1\nSupplementary methods and results','Title')
    para(d,'Reliability of generative AI workflows for recovering missing hospital equipment metadata: an expert-verified paired evaluation')
    para(d,'Health Information Science and Systems')
    para(d,'Yihan Qi and Zhenqi Zhang')
    para(d,'Sichuan Cancer Hospital & Institute, Sichuan Clinical Research Center for Cancer, Sichuan Cancer Center, Affiliated Cancer Hospital of University of Electronic Science and Technology of China, Chengdu 610041, China')
    para(d,'Corresponding author: Zhenqi Zhang; Email: 9xuean@gmail.com')
    d.add_heading('S1 Outcome definitions and data integrity',level=1)
    para(d,'The adjudicated dataset contains 1000 unique record identifiers. Equipment name, specification/model, reference brand, both AI brands and both adjudication labels are complete. No records were removed from analysis. Correctness comes from joint expert judgement, not exact matching of brand strings.')
    table(d,'Table S1. Mutually exclusive classification rules',['Category','Reference','Workflow output and assessment'],[
        ['Correct assignment','Known brand','Specific brand accepted by the experts'],['Incorrect assignment','Known brand','Specific brand rejected by the experts'],['Unverified assignment','Unresolved','Specific brand supplied'],['Missed identification','Known brand','Unknown output'],['Both unknown','Unresolved','Unknown output']],[42,35,93],newpage=False,note='Unresolved means not reliably confirmed, not confirmed absence of a brand. The latter four categories are not verified correct identifications. No missing outcome imputation is used.')
    d.add_heading('S2 Eligibility and sampling',level=1)
    para(d,'The hospital asset-management team had preselected a 2010–2025 historical ledger remediation pool for missing brand fields before export. Subsequent selection required classification code A023*, unit price ≥ CNY 1000, and a valid specification/model. The eligible frame contained 1101 records; 1000 were sampled without replacement with seed 20260416. Only equipment name and specification/model were input to the models. Both workflows ran in March 2026, and expert reference assessment, reconciliation and output scoring took place in April–May 2026.')
    para(d,'The year window and missing-brand restriction describe upstream selection confirmed by the asset-management team. The final analysis workbook does not retain these original fields, so the present analysis cannot independently reconstruct that selection. The retained sample matched the five fields in the original sampling workbook. Results should not be extrapolated to all hospital assets or records with missing models. Counts excluded from the entire hospital inventory by each condition were unavailable.')
    para(d,'Historical extraction detail: the original script additionally restricted the asset-identifier prefix to ZCKP02000–ZCKP02025. This is recorded as an implementation detail for provenance only; identifier codes were not used to infer asset registration years. The original extraction script is not retrospectively rewritten to imply that it performed the upstream selection. Sampling seed 20260416 and bootstrap seed 20261029 are random-generator parameters, not study dates.')
    para(d,'Two experts with more than eight years of fixed-asset management experience independently queried internet sources and consulted available equipment manuals while blinded to AI answers. Historical procurement contracts and acceptance records were often unavailable. Their 946 agreements and 54 reconciled disagreements established the reference; they then jointly scored outputs using brand equivalence. Evidence strength and source provenance were not systematically graded per record.')
    table(d,'Table S2. Request settings for the evaluated workflows',['Setting','Reasoning','Web-enabled search'],[
        ['Provider','DeepSeek API','Tencent Cloud'],['Model identifier','deepseek-reasoner','deepseek-v3.2'],['Search','No search tool configured','enable_search = true'],['Thinking','Reasoner model endpoint','thinking.type = enabled'],['Streaming','Not requested','true'],['Maximum output token setting','64,000','8,192'],['Timeout','120 seconds','30-second connect; 180-second read'],['Maximum attempts','5','5'],['Temperature / top-p','Not explicitly supplied','Not explicitly supplied'],['Input fields','Equipment name and model','Equipment name and model'],['Structured fields','brand; generic_name; confidence; reason','brand; generic_name; confidence; reason']],[48,61,61],note='Settings were extracted from the scripts used with their default configurations. Provider defaults and underlying model snapshots were not independently recovered. Maximum token settings do not indicate actual token consumption. The comparison is between workflows, not an isolated search toggle.')
    d.add_heading('S3 Exact original prompts',level=1)
    pp=prompts()
    for name,msgs in pp.items():
        d.add_heading(name,level=2)
        for m in msgs:
            para(d,m['role'].capitalize()+' message').paragraph_format.keep_with_next=True
            for line in m['content'].splitlines():
                p=para(d,line,9);p.paragraph_format.line_spacing=1.1;p.paragraph_format.space_after=Pt(2)
    d.add_heading('S4 English translations of the prompts',level=1)
    para(d,'The translations below document the original Chinese instructions; they were not used for model calls. [DEVICE NAME] and [SPECIFICATION/MODEL] mark substituted record fields.')
    translations=[('Reasoning system','You are a medical and general equipment asset standardisation assistant. Based on the equipment name and specification/model, infer the most likely brand and a generic standardised name suitable for consistent asset-ledger naming. Think as concisely as possible, then output only JSON. You must output only JSON, with no additional explanation.'),('Reasoning user','Output JSON with brand (use unknown if unknown), generic_name (a standardised equipment name suitable for a fixed-asset ledger, as standardised and concise as possible), confidence (0.0), and reason (a one-sentence explanation of the basis for the judgement). Requirements: (1) prioritise the specification/model when identifying the brand; (2) return unknown for brand if it cannot be reliably determined; (3) generic_name must not simply copy the model and should be a standardised equipment name; (4) confidence ranges from 0 to 1. Input: equipment name [DEVICE NAME]; specification/model [SPECIFICATION/MODEL].'),('Search system','You are a medical and general equipment asset standardisation assistant. Combine web-search results with the equipment name and specification/model to infer the most likely brand and a generic standardised name suitable for consistent asset-ledger naming. You must output only JSON, with no additional explanation.'),('Search user','Output JSON with brand (use unknown if unknown), generic_name (a standardised equipment name suitable for a fixed-asset ledger, as standardised and concise as possible), confidence (0.0), and reason (briefly explain the basis for the judgement; web-search clues may be cited). Requirements: (1) prioritise the specification/model and supplement with web search if needed; (2) return unknown for brand if it cannot be reliably determined; (3) generic_name must not simply copy the model and should be a standardised equipment name; (4) output must be valid JSON. Input: equipment name [DEVICE NAME]; specification/model [SPECIFICATION/MODEL].')]
    for name,t in translations:d.add_heading(name,level=2);para(d,t)
    d.add_heading('S5 Processing and technical limitations',level=1)
    para(d,'Both scripts extract the returned brand and normalise an empty brand to 未知. The reasoning script parses returned JSON directly; the search script first extracts a JSON block from streaming content. Request or parsing failures can trigger another attempt, with a maximum of five attempts. Exhausted attempts raise an error. The adjudicated file contains complete retained outputs, but does not provide a complete attempt-level failure log. Unknown-output counts therefore describe stored output behaviour and cannot always be equated with intentional semantic abstention.')
    para(d,'The retained runtime is a processing-duration field, not a measurement of expert activity. The evaluation did not systematically audit the search corpus, retrieval relevance, citation validity or evidence strength. Model-generated confidence was not calibrated against outcomes. Neither generic equipment naming nor rationale quality was evaluated as an endpoint.')
    d.add_heading('S6 Cluster resampling and estimands',level=1)
    para(d,'Let d_ig = y_search,ig − y_reasoning,ig, where y is 1 for a verified correct brand and 0 otherwise. The record-weighted difference is Σ_gΣ_i d_ig / Σ_g n_g. The combination-weighted difference is (1/G)Σ_g[(Σ_i d_ig)/n_g], with G = 418. In every replicate, G clusters are sampled with replacement and their full record sets retained. Confidence intervals are the 2.5th and 97.5th percentiles of 6000 replicates. NumPy default_rng is seeded with 20261029; exact name–model keys are sorted before sampling.')
    para(d,'For conditional proportions, both numerator and denominator are recomputed within each resample. This includes the specific-output subsets and the two search-output strata. Clusters with no member in a stratum contribute zero to its numerator and denominator; they are not excluded before resampling. Exact-string clusters preserve the supplied grouping without inventing synonymous equipment relationships. No finite-population correction or between-run model variability is included.')
    table(d,'Table S3. Cluster-bootstrap estimates',['Measure','Estimate (%) or points','95% CI'],[
        ['Reasoning verified yield',pct(308/1000),interval(S['yield_ci'][0])],['Search verified yield',pct(524/1000),interval(S['yield_ci'][1])],['Reasoning conditional correctness',pct(308/373),interval(S['conditional_ci'][0])],['Search conditional correctness',pct(524/720),interval(S['conditional_ci'][1])],['Record-weighted difference, points','21.6',interval(S['difference_ci'])],['Combination-weighted difference, points','14.0',interval(S['equal_group_ci'])],['Search correctness when both output brands','89.1',interval(S['risk'][0]['ci'])],['Search correctness when only search outputs a brand','55.9',interval(S['risk'][1]['ci'])]],[90,40,40],note='All intervals account for exact name–model clusters. Conditional metrics use different output-selected populations. No subgroup significance tests or multiplicity-adjusted comparisons are reported.')
    rows=[]
    for c,name in zip(S['categories'],CAT):
        rows.append([name,c['n'],nper(c['reasoning_correct'],c['n']),nper(c['search_correct'],c['n']),c['unresolved']])
    table(d,'Table S4. Descriptive performance by equipment category',['Equipment category','n','Reasoning correct','Search correct','Unresolved reference'],rows,[70,15,28,28,29],note='Percentages use the category count. These exploratory descriptive strata may be small and contain repeated models; no category-specific significance claims are made. English labels are translations of stored category names, not independent reclassification.')
    table(d,'Table S5. Literal string agreement within dual-output records',['Dual-output subset','n','Reasoning correct','Search correct'],[['Identical brand strings',186,175,175],['Different brand strings',180,130,151]],[80,20,35,35],note='These are descriptive literal-string subsets only. Different strings can be equivalent brands, including Chinese/English aliases. They must not be interpreted as a synonym-normalised disagreement analysis.')
    d.add_heading('S7 Reproduction and data access',level=1)
    para(d,'Online Resource 2 provides aggregate statistical results and a reproducibility guide. Code, dependencies, study context and machine-readable aggregates are available at https://github.com/xuean009/hospital-equipment-metadata-recovery/tree/v1.0.0. Run code/analyze.py with --input pointing to the authorised workbook, followed by code/figures.py and code/build_documents.py. The latter two scripts also rebuild outputs directly from supplied aggregates. Only aggregate results are exported; individual records and API credentials are excluded. Record access requires hospital authorisation.')
    para(d,'Software versions: '+', '.join(f'{k} {v}' for k,v in S['versions'].items())+'. Figure and document dependencies are pinned in requirements.txt. The source workbook is read-only.')
    para(d,'Canonical source workbook: '+S['input_filename']+' (worksheet: 合并数据集).',10)
    para(d,'Source workbook SHA-256: '+S['input_sha256'],8)
    d.add_heading('S8 Reporting boundaries',level=1)
    para(d,'This evaluation is retrospective and single-centre, with one retained result per workflow and record. It has no training/test split because the workflows were applied without task-specific fitting. Review strata were explored on the evaluated sample, not validated independently. Bootstrap draws are statistical resamples, not technical replicates of AI inference. No patient outcomes, deployed correction rate, human time saving or economic benefit were measured.')
    d.save(ROOT/'ESM_1.docx')
    (ROOT/'source_data'/'original_prompts.json').write_text(json.dumps(pp,ensure_ascii=False,indent=2),encoding='utf-8')
    with (ROOT/'source_data'/'category_results.csv').open('w',newline='',encoding='utf-8-sig') as f:
        cw=csv.writer(f);cw.writerow(['category_original','category_english','n','reasoning_correct','search_correct','unresolved'])
        for c,name in zip(S['categories'],CAT):cw.writerow([c['category'],name,c['n'],c['reasoning_correct'],c['search_correct'],c['unresolved']])

if __name__=='__main__':
    main_doc();supp_doc();cover_doc();print('Created manuscript and supplementary DOCX files.')
