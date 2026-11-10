"""Reproduce paired analyses from the authorized, adjudicated workbook.
Usage: python code/analyze.py --input PATH_TO_WORKBOOK
No individual-level data are exported. Raw inputs are never modified.
"""
from pathlib import Path
import sys, json, csv, argparse, hashlib, platform
ROOT = Path(__file__).resolve().parents[1]
if (ROOT / '.runtime').exists(): sys.path.insert(0, str(ROOT / '.runtime'))
import numpy as np
import scipy
from scipy.stats import binomtest
import openpyxl
from collections import Counter

def main():
    p = argparse.ArgumentParser(); p.add_argument('--input', type=Path, required=True)
    args = p.parse_args()
    w = openpyxl.load_workbook(args.input, read_only=True, data_only=True)
    rows = list(w['合并数据集'].values); heads, rows = rows[0], rows[1:]
    assert len(rows)==1000 and len(set(r[0] for r in rows))==1000
    assert all(r[i] is not None for r in rows for i in [0,1,5,9,10,12,14,15])
    assert all(r[i] in ['是','否','未知'] for r in rows for i in [14,15])
    groups = sorted(set((str(r[1]),str(r[5])) for r in rows))
    lookup = {k:i for i,k in enumerate(groups)}
    g = np.array([lookup[(str(r[1]),str(r[5]))] for r in rows])
    n = len(rows); G=len(groups)
    known=np.array([r[9]!='未知' for r in rows])
    correct=np.array([[r[j]=='是' for j in [14,15]] for r in rows])
    specific=np.array([[r[j]!='未知' for j in [10,12]] for r in rows])
    assert np.all(~correct | (known[:,None]&specific))
    cats=np.zeros((n,2,5),int)
    cats[:,:,0]=correct
    cats[:,:,1]=known[:,None]&specific&~correct
    cats[:,:,2]=~known[:,None]&specific
    cats[:,:,3]=known[:,None]&~specific
    cats[:,:,4]=~known[:,None]&~specific
    assert np.all(cats.sum(axis=2)==1)
    for j,col in enumerate([14,15]):
        expected=np.where(correct[:,j],'是',np.where(cats[:,j,4],'未知','否'))
        assert np.all(expected==np.array([r[col] for r in rows]))
    strata=np.where(specific[:,0]&specific[:,1],0,np.where(~specific[:,0]&specific[:,1],1,np.where(specific[:,0]&~specific[:,1],2,3)))
    # Cluster summaries: n, correct R/S, specific R/S, conditional stratum numerators/denominators.
    X=np.column_stack([np.ones(n),correct,specific]+[v for k in range(4) for v in [(strata==k),(strata==k)&correct[:,1]]]).astype(float)
    cluster=np.zeros((G,X.shape[1])); np.add.at(cluster,g,X)
    diff_group=(cluster[:,2]-cluster[:,1])/cluster[:,0]
    rng=np.random.default_rng(20261029); B=6000
    estimates=[]
    for b in range(B):
        idx=rng.integers(0,G,size=G); z=cluster[idx].sum(axis=0)
        estimates.append([(z[2]-z[1])/z[0],diff_group[idx].mean(),z[1]/z[0],z[2]/z[0],z[1]/z[3],z[2]/z[4]]+[z[6+2*k]/z[5+2*k] if z[5+2*k] else np.nan for k in range(4)])
    boot=np.array(estimates)
    def ci(col): return [float(x) for x in np.nanquantile(boot[:,col],[.025,.975])]
    transitions=Counter((r[14],r[15]) for r in rows)
    discordant=[int(np.sum(correct[:,0]&~correct[:,1])),int(np.sum(~correct[:,0]&correct[:,1]))]
    risk=[]
    for k,label in enumerate(['Both workflows output a brand','Search only outputs a brand','Reasoning only outputs a brand','Neither workflow outputs a brand']):
        m=strata==k; den=int(m.sum()); num=int(correct[m,1].sum())
        risk.append(dict(label=label,n=den,reasoning_correct=int(correct[m,0].sum()),search_correct=num,unresolved=int((m&~known).sum()),search_yield=num/den,ci=ci(6+k) if k<2 else None))
    categories=[]
    for c in sorted(set(r[3] for r in rows)):
        m=np.array([r[3]==c for r in rows]); nn=int(m.sum())
        categories.append(dict(category=c,n=nn,reasoning_correct=int(correct[m,0].sum()),search_correct=int(correct[m,1].sum()),unresolved=int((m&~known).sum())))
    categories.sort(key=lambda x:-x['n'])
    sizes=Counter(g)
    S=dict(n=n,clusters=G,repeated_clusters=sum(v>1 for v in sizes.values()),max_cluster=max(sizes.values()),known=int(known.sum()),unresolved=int((~known).sum()),categories=categories,
           agreement=dict(Counter(r[8] for r in rows)),specific=specific.sum(axis=0).tolist(),correct=correct.sum(axis=0).tolist(),outcomes=cats.sum(axis=0).tolist(),risk=risk,
           paired3=[[transitions.get((a,b),0) for b in ['是','否','未知']] for a in ['是','否','未知']],paired2=[[int(np.sum(correct[:,0]&correct[:,1])),discordant[0]],[discordant[1],int(np.sum(~correct[:,0]&~correct[:,1]))]],
           difference=float((correct[:,1].astype(int)-correct[:,0]).mean()),difference_ci=ci(0),equal_group_difference=float(diff_group.mean()),equal_group_ci=ci(1),yield_ci=[ci(2),ci(3)],conditional_ci=[ci(4),ci(5)],mcnemar_p=float(binomtest(discordant[0],sum(discordant),.5).pvalue),bootstrap_B=B,seed=20261029,
           runtime=[dict(total=float(sum(r[i] for r in rows)),median=float(np.median([r[i] for r in rows])),q1=float(np.quantile([r[i] for r in rows],.25)),q3=float(np.quantile([r[i] for r in rows],.75))) for i in [11,13]],
           input_filename=args.input.name,input_sha256=hashlib.sha256(args.input.read_bytes()).hexdigest(),versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,openpyxl=openpyxl.__version__))
    assert S['correct']==[308,524] and S['specific']==[373,720]
    assert S['outcomes']==[[308,60,5,376,251],[524,121,75,99,181]]
    assert G==418 and S['paired2']==[[294,14],[230,462]]
    (ROOT/'source_data').mkdir(exist_ok=True)
    (ROOT/'source_data'/'analysis_summary.json').write_text(json.dumps(S,ensure_ascii=False,indent=2),encoding='utf-8')
    with (ROOT/'source_data'/'figure_source_data.csv').open('w',newline='',encoding='utf-8-sig') as f:
        cw=csv.writer(f); cw.writerow(['panel','measure','group','numerator_or_estimate','denominator','ci_lower','ci_upper','unit'])
        for j,label in enumerate(['Reasoning','Web-enabled search']):
            cw.writerow(['3a','specific_output',label,S['specific'][j],n,'','','records'])
            cw.writerow(['3a','conditional_correctness',label,S['correct'][j],S['specific'][j],*S['conditional_ci'][j],'proportion'])
            for k,name in enumerate(['Correct','Incorrect','Unverified','Missed identification','Both unknown']):cw.writerow(['3b',name,label,S['outcomes'][j][k],n,'','','records'])
        for label,point,interval in [('Record-weighted',S['difference'],S['difference_ci']),('Combination-weighted',S['equal_group_difference'],S['equal_group_ci'])]:cw.writerow(['2b','paired_difference',label,point,'',*interval,'proportion'])
        for v in risk[:2]:cw.writerow(['3c','search_correctness',v['label'],v['search_correct'],v['n'],*v['ci'],'proportion'])
        for i,a in enumerate(['Correct','Not correct']):
            for j,b in enumerate(['Correct','Not correct']):cw.writerow(['2a',a+' to '+b,'Paired records',S['paired2'][i][j],n,'','','records'])
    print(json.dumps({k:S[k] for k in ['difference','difference_ci','equal_group_difference','equal_group_ci','risk','runtime','versions']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
