"""Validate HISS structure, aggregate invariants and exported Word proofs."""
from pathlib import Path
import sys,json,re,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/'.runtime').exists():sys.path.insert(0,str(ROOT/'.runtime'))
import pymupdf
from PIL import Image,ImageDraw
from docx import Document
S=json.loads((ROOT/'source_data'/'analysis_summary.json').read_text(encoding='utf-8'))
report={}
src=(ROOT/'Main_Manuscript.md').read_text(encoding='utf-8')
body,refs=src.split('\n## References\n\n')
abstract=body.split('\n## Abstract\n\n')[1].split('Keywords:')[0]
assert re.findall(r'^### (\w+)',abstract,re.M)==['Purpose','Methods','Results','Conclusion']
nums=[int(n) for n in re.findall(r'(?m)^(\d+)\.',refs)]
assert nums==list(range(1,len(nums)+1)) and len(nums)==19
seen=[]
for m in re.finditer(r'\[(\d+(?:,\d+)*)\]',body):
    for n in map(int,m[1].split(',')):
        if n not in seen:seen.append(n)
assert seen==nums
assert len(re.findall(r'^## [1-5] ',body,re.M))==5
assert len(re.findall(r'^### 2\.\d ',body,re.M))==6
assert len(re.findall(r'^### 3\.\d ',body,re.M))==5
assert len(re.findall(r'^### 4\.\d ',body,re.M))==5
assert list(dict.fromkeys(re.findall(r'Figure (\d)',body)))==['1','2','3']
assert list(dict.fromkeys(re.findall(r'Table (\d)',body)))==['1','2','3','4']
assert len(body.split('Keywords: ')[1].split('\n')[0].split(';'))==6
assert not re.search('Additional.file|BMC Health Services Research|TODO|TBD|TBC',src)
assert '## Statements and Declarations' in body
assert S['paired2']==[[294,14],[230,462]]
assert list(S['outcomes'][0])==[308,60,5,376,251]
assert list(S['outcomes'][1])==[524,121,75,99,181]
assert S['n']==1000 and S['known']==744 and S['unresolved']==256
assert sum(c['n'] for c in S['categories'])==1000
assert sum(v['n'] for v in S['risk'])==1000
counts=json.loads((ROOT/'qa'/'word_counts.json').read_text())
assert 150<=counts['abstract_words']<=250
report.update(structure='PASS',aggregate_invariants='PASS',references=len(nums),word_counts=counts)
for name in ['Main_Manuscript','ESM_1','ESM_2','Cover_Letter']:
    path=ROOT/(name+'.docx')
    if not path.exists() and name=='Cover_Letter':continue
    d=Document(path);text='\n'.join(p.text for p in d.paragraphs)
    assert '{{' not in text
    assert not re.search(r'Additional.file|BMC Health Services Research|\b(TODO|TBC|TBD)\b',text)
    assert 'ESM_2.zip' not in text
    assert 'https://github.com/xuean009/hospital-equipment-metadata-recovery/tree/v1.0.0' in text
    if name=='ESM_2':
        assert len(d.tables)==9 and len(d.inline_shapes)==0
        assert S['input_sha256'] in text and '9xuean@gmail.com' in text
        originals=Document(ROOT/'Main_Manuscript.docx').tables+Document(ROOT/'ESM_1.docx').tables
        for actual,expected in zip(d.tables,originals):
            assert [[c.text for c in r.cells] for r in actual.rows]==[[c.text for c in r.cells] for r in expected.rows]
    if name=='Main_Manuscript':
        assert len(d.tables)==4 and len(d.inline_shapes)==3
        assert d.element.xpath('.//w:lnNumType[@w:restart="continuous"]')
        h=[p.text for p in d.paragraphs if p.style.name=='Heading 1']
        assert h.count('2 Methods')==1 and h.count('3 Results')==1
    if name=='ESM_1':
        assert len(d.tables)==5 and len(d.inline_shapes)==0
        assert S['input_sha256'] in text and '9xuean@gmail.com' in text
        assert 'Health Information Science and Systems' in text
    proof=ROOT/'qa'/(name+'.pdf')
    if not proof.exists():continue
    assert proof.stat().st_mtime>=path.stat().st_mtime,'Stale proof: '+name
    pdf=pymupdf.open(proof)
    if name=='Cover_Letter':assert len(pdf)==1
    out=ROOT/'qa'/name;out.mkdir(exist_ok=True)
    pages=[];thumbs=[]
    for i,page in enumerate(pdf):
        png=out/f'page-{i+1}.png'
        page.get_pixmap(matrix=pymupdf.Matrix(1.8,1.8)).save(png)
        txt=page.get_text();assert '\ufffd' not in txt
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for sp in line['spans']:
                    x0,y0,x1,y1=sp['bbox']
                    assert x0>=0 and y0>=0 and x1<=page.rect.width+1 and y1<=page.rect.height+1,(name,i,sp)
        pages.append(dict(page=i+1,words=len(txt.split()),images=len(page.get_images()),first=txt.replace('\n',' ')[:90]))
        im=Image.open(png).convert('RGB');im.thumbnail((298,422))
        t=Image.new('RGB',(318,450),'#dddddd');t.paste(im,(10,23));ImageDraw.Draw(t).text((10,4),f'{name} {i+1}',fill='black');thumbs.append(t)
    for st in range(0,len(thumbs),9):
        panel=Image.new('RGB',(954,1350),'white')
        for j,t in enumerate(thumbs[st:st+9]):panel.paste(t,((j%3)*318,(j//3)*450))
        panel.save(ROOT/'qa'/f'{name}_contact_{st//9+1}.png')
    report[name]=pages
for path in (ROOT/'figures').glob('*.pdf'):
    pdf=pymupdf.open(path);page=pdf[0]
    assert abs(page.rect.width/72*25.4-170)<.01
    assert all(pdf.extract_font(f[0])[3] for f in page.get_fonts(full=True))
report['figure_fonts']='embedded'
(ROOT/'qa'/'final_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if not isinstance(v,list)},ensure_ascii=False,indent=2))
