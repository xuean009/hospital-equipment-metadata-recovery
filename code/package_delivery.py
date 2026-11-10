"""Package HISS submission assets using an explicit public-file allowlist."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
def archive(name,files):
    entries={}
    for p in sorted(set(files)):
        assert p.is_file(),p
        rel=p.relative_to(ROOT).as_posix()
        assert '..' not in Path(rel).parts
        assert p.suffix.lower() not in {'.xlsx','.xls','.env','.key','.pem'}
        entries[rel]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    with zipfile.ZipFile(ROOT/name,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in entries:z.write(ROOT/rel,rel)
        z.writestr('FILE_MANIFEST.json',json.dumps(entries,ensure_ascii=False,indent=2))
    with zipfile.ZipFile(ROOT/name) as z:
        assert z.testzip() is None
        for rel,meta in entries.items():assert hashlib.sha256(z.read(rel)).hexdigest()==meta['sha256']
    print(f'{name}: {len(entries)} files plus manifest; integrity PASS')
def main():
    shared=[ROOT/n for n in ['README.md','requirements.txt','reference_verification.csv','PACKAGE_METADATA.json']]
    shared += [ROOT/'code'/n for n in ['analyze.py','figures.py','build_documents.py','build_esm2.py','manuscript.md','package_delivery.py','qa.py','render_qa.ps1']]
    shared += [ROOT/'source_data'/n for n in ['analysis_summary.json','category_results.csv','figure_source_data.csv','original_prompts.json','study_context.json','Table_1.csv','Table_2.csv','Table_3.csv','Table_4.csv','Table_S1.csv','Table_S2.csv','Table_S3.csv','Table_S4.csv','Table_S5.csv']]
    # Code is deposited in GitHub; Online Resource 2 is a PDF.
    complete=shared+[ROOT/n for n in ['Main_Manuscript.docx','Main_Manuscript.md','ESM_1.docx','ESM_1.pdf','ESM_2.docx','ESM_2.pdf','Cover_Letter.docx','Cover_Letter.md','修改说明与核查报告.md','投稿文件清单.md']]
    complete += [p for p in (ROOT/'figures').iterdir() if p.suffix in {'.svg','.pdf','.tiff','.png'}]
    assert len([p for p in complete if p.parent.name=='figures'])==12
    archive('HISS_submission_package.zip',complete)
if __name__=='__main__':main()

