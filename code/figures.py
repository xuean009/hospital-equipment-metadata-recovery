"""HISS figures: a restrained, editable 170-mm-wide publication system.

Figure 1: study-design schematic; independent reference precedes AI scoring.
Figure 2: paired alluvial evidence plus cluster-bootstrap effect estimates.
Figure 3: coverage/reliability, all-record outcomes and exploratory review strata.
All quantitative marks use verified aggregates; no observations are omitted.
All drawing, previews and vector/raster exports use Python/matplotlib.
"""
from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[1]
(ROOT/'figures').mkdir(exist_ok=True)
if (ROOT/'.runtime').exists(): sys.path.insert(0, str(ROOT/'.runtime'))
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Ellipse, PathPatch
from matplotlib.path import Path as MPath

mpl.rcParams.update({
    'font.family':'sans-serif', 'font.sans-serif':['Arial','DejaVu Sans'],
    'font.size':8, 'axes.labelsize':8, 'xtick.labelsize':7.5, 'ytick.labelsize':7.5,
    'svg.fonttype':'none', 'pdf.fonttype':42, 'axes.linewidth':.6,
    'axes.spines.top':False, 'axes.spines.right':False,
    'lines.linewidth':.9, 'hatch.linewidth':.45, 'legend.frameon':False, 'savefig.facecolor':'white',
    'text.color':'#273445', 'axes.labelcolor':'#273445',
    'xtick.color':'#657385', 'ytick.color':'#657385',
})
S = json.loads((ROOT/'source_data'/'analysis_summary.json').read_text(encoding='utf-8'))
C = json.loads((ROOT/'source_data'/'study_context.json').read_text(encoding='utf-8'))
INK='#273445'; MUTED='#657385'; LINE='#AEB9C5'; PALE='#F3F5F8'
REASON='#536C9B'; SEARCH='#98638F'; GREEN='#6D9F93'; LOSS='#BE737E'
OC=['#76A59A','#CC8586','#D6B16D','#BBC8DB','#E6E9ED']

def canvas(height):
    fig=plt.figure(figsize=(6.692913386,height/25.4))
    ax=fig.add_axes([0,0,1,1]); ax.set(xlim=(0,170),ylim=(0,height)); ax.axis('off')
    return fig,ax

def tx(ax,x,y,text,size=8,color=INK,weight='normal',ha='left',va='center',**kw):
    return ax.text(x,y,text,fontsize=max(7.5,size),color=color,fontweight=weight,ha=ha,va=va,
                   linespacing=1.32,**kw)

def heading(ax,x,y,letter,title):
    tx(ax,x,y,letter,10,weight='bold'); tx(ax,x+6,y,title,9,weight='bold')

def line(ax,points,color=LINE,lw=.65,**kw):
    ax.plot(*zip(*points),color=color,lw=lw,solid_capstyle='round',**kw)

def arrow(ax,points,color=LINE,lw=.75):
    if len(points)>2: line(ax,points[:-1],color,lw)
    ax.annotate('',xy=points[-1],xytext=points[-2],
        arrowprops=dict(arrowstyle='-|>',color=color,lw=lw,mutation_scale=7,
                        shrinkA=0,shrinkB=0))

def card(ax,x,y,w,h,fill,edge='none'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=1.5',
                               fc=fill,ec=edge,lw=.65))

def ledger(ax,x,y,w=12,h=14,color=LINE):
    """A vector record-stack encoding the inventory/paired output data."""
    for dx,dy in [(2,2),(1,1),(0,0)]:
        ax.add_patch(Rectangle((x+dx,y+dy),w,h,fc='white',ec=color,lw=.55))
    for r in [3,6,9]:
        line(ax,[(x+2,y+r),(x+w-2,y+r)],color,.5)
    line(ax,[(x+4,y+1),(x+4,y+h-2)],color,.45)

def network(ax,x,y,color):
    pts=[(x-3,y+2),(x+3,y+3),(x,y-1),(x+4,y-4),(x-4,y-4)]
    for a,b in [(0,1),(0,2),(1,2),(2,3),(2,4)]: line(ax,[pts[a],pts[b]],color,.65)
    for px,py in pts: ax.add_patch(Circle((px,py),.85,fc='white',ec=color,lw=.65))

def globe(ax,x,y,color):
    ax.add_patch(Circle((x,y),4,fc='none',ec=color,lw=.65))
    ax.add_patch(Ellipse((x,y),3.3,8,fc='none',ec=color,lw=.55))
    line(ax,[(x-3.9,y),(x+3.9,y)],color,.55)
    line(ax,[(x-3.4,y+2),(x+3.4,y+2)],color,.45)
    line(ax,[(x-3.4,y-2),(x+3.4,y-2)],color,.45)

def save(fig,name):
    # Fixed journal dimensions; tight cropping would alter the specified width.
    fig.savefig(ROOT/'figures'/f'{name}.svg')
    fig.savefig(ROOT/'figures'/f'{name}.pdf')
    fig.savefig(ROOT/'figures'/f'{name}.tiff',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
    fig.savefig(ROOT/'figures'/f'{name}.png',dpi=300)
    plt.close(fig)

def fig1():
    f,a=canvas(132)
    heading(a,5,124,'a','Inventory sample')
    heading(a,56,124,'b','Parallel AI workflows')
    heading(a,123,124,'c','Paired assessment')
    for x,w in [(5,39),(56,54),(123,42)]: line(a,[(x,119),(x+w,119)],'#DCE2E8',.5)

    ledger(a,7,97,11,12)
    tx(a,24,108,'1,101',17,weight='bold')
    tx(a,24,99,'eligible records',7.3,MUTED)
    tx(a,7,89,'Legacy-ledger work pool\n2010–2025 · Missing brand field',7.5,MUTED)
    arrow(a,[(24,83),(24,74)])
    tx(a,28,79,'Random\nsampling',7.1,MUTED)
    card(a,5,45,39,27,PALE)
    tx(a,9,62,f"{S['n']:,}",22,weight='bold')
    tx(a,9,50,'sampled asset records',8)
    tx(a,7,38,f"{S['clusters']} name–model\ncombinations",7.7,MUTED)

    # The two workflows receive the same inputs; expert review has its own branch.
    line(a,[(44,59),(49,59),(49,101)],LINE,.7)
    arrow(a,[(49,101),(56,101)],REASON)
    arrow(a,[(49,59),(56,59)],SEARCH)
    a.add_patch(Circle((49,59),.7,fc=LINE,ec='none'))
    tx(a,56,78,'Same equipment name and model',7.2,MUTED)

    card(a,56,85,54,29,'#EEF2F9')
    network(a,103,104,REASON)
    tx(a,60,108,'Reasoning',9.5,REASON,'bold')
    tx(a,60,100,'DeepSeek API',7.6)
    tx(a,60,94,'deepseek-reasoner',8)
    tx(a,60,88,'No search tool configured',7.1,MUTED)
    card(a,56,45,54,29,'#F5EFF5')
    globe(a,103,64,SEARCH)
    tx(a,60,68,'Web-enabled search',9,SEARCH,'bold')
    tx(a,60,60,'Tencent Cloud',7.6)
    tx(a,60,54,'deepseek-v3.2',8)
    tx(a,60,48,'Search + thinking enabled',7.1,MUTED)

    tx(a,128,110,'Two output sets',8.5,weight='bold')
    ledger(a,130,91,10,12,REASON); ledger(a,143,91,10,12,SEARCH)
    tx(a,144,85,'1,000 paired records',7.5,MUTED,ha='center')
    arrow(a,[(110,101),(125,101)],REASON)
    arrow(a,[(110,59),(117,59),(117,91),(125,91)],SEARCH)
    arrow(a,[(144,80),(144,72)])
    card(a,124,54,41,18,'#EDF4F1')
    tx(a,144.5,66,'Joint expert scoring',8.3,weight='bold',ha='center')
    tx(a,144.5,59,'Brand equivalence',7.6,ha='center')

    # Independent reference is established while reviewers are blinded to AI.
    arrow(a,[(5,56),(2,56),(2,17),(52,17)],LINE)
    tx(a,6,26,'Blinded to\nAI outputs',7.2,MUTED)
    line(a,[(56,37),(110,37)],'#DCE2E8',.5)
    tx(a,56,31,'Independent reference',8.5,weight='bold')
    tx(a,56,24,'2 experts; each >8 years’ experience',7.1,MUTED)
    tx(a,56,17,'946 agreed · 54 reconciled',8,weight='bold')
    tx(a,56,10,'Discussion and source rechecking',7.1,MUTED)
    arrow(a,[(110,17),(123,17)],LINE)
    tx(a,124,38,'Reference established',7.8,weight='bold')
    tx(a,124,28,str(S['known']),14,GREEN,'bold')
    tx(a,147,28,str(S['unresolved']),14,MUTED,'bold')
    tx(a,124,21,'confirmed',7,MUTED)
    tx(a,147,21,'unresolved',7,MUTED)
    a.add_patch(Rectangle((124,11),41*S['known']/S['n'],3,fc=GREEN,ec='none'))
    a.add_patch(Rectangle((124+41*S['known']/S['n'],11),41*S['unresolved']/S['n'],3,fc=OC[4],ec='none'))
    arrow(a,[(144,42),(144,54)],GREEN)
    tx(a,148,47,'Reference\nfirst',7,MUTED)
    tx(a,5,3,f"AI runs: {C['model_run_period']} · Expert assessment: {C['expert_review_period']}",7.5,MUTED)
    save(f,'Figure_1_study_design')

def ribbon(ax,x0,x1,y0,y1,h,color):
    mid=(x0+x1)/2
    vs=[(x0,y0),(mid,y0),(mid,y1),(x1,y1),(x1,y1+h),
        (mid,y1+h),(mid,y0+h),(x0,y0+h),(x0,y0)]
    codes=[MPath.MOVETO,MPath.CURVE4,MPath.CURVE4,MPath.CURVE4,MPath.LINETO,
           MPath.CURVE4,MPath.CURVE4,MPath.CURVE4,MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(vs,codes),fc=color,ec='white',lw=.45))

def fig2():
    f,a=canvas(105)
    heading(a,5,98,'a','Paired identification')
    heading(a,108,98,'b','Effect robustness')
    tx(a,9,87,'Reasoning',8.5,REASON,'bold')
    tx(a,99,87,'Search',8.5,SEARCH,'bold',ha='right')
    y=19; k=.06; gap=2.5; x0=12; x1=96
    both,loss,gain,neither=S['paired2'][0][0],S['paired2'][0][1],S['paired2'][1][0],S['paired2'][1][1]
    for x,c,col in [(9,S['correct'][0],REASON),(96,S['correct'][1],SEARCH)]:
        nc=S['n']-c
        a.add_patch(Rectangle((x,y),3,nc*k,fc='#CDD5DF',ec='none'))
        a.add_patch(Rectangle((x,y+nc*k+gap),3,c*k,fc=col,ec='none'))
    ribbon(a,x0,x1,y,y,neither*k,'#E5E9EE')
    ribbon(a,x0,x1,y+neither*k,y+(neither+loss)*k+gap,gain*k,'#9CBEB4')
    ribbon(a,x0,x1,y+(neither+gain)*k+gap,y+neither*k,loss*k,LOSS)
    ribbon(a,x0,x1,y+(neither+gain+loss)*k+gap,y+(neither+loss+gain)*k+gap,both*k,'#B3C2D8')
    tx(a,54,74,str(both),16,weight='bold',ha='center')
    tx(a,54,68.5,'Both correct',8,ha='center')
    tx(a,42,54.5,str(gain),16,weight='bold',ha='center')
    tx(a,42,50,'Search only correct',8,ha='center')
    tx(a,54,34,str(neither),16,weight='bold',ha='center')
    tx(a,54,28.5,'Neither correct',8,ha='center')
    tx(a,80,42.5,str(loss),10,LOSS,'bold',ha='center')
    tx(a,80,38.5,'Reasoning only correct',6.9,MUTED,ha='center')
    line(a,[(81,44.5),(86,47.5)],LOSS,.6)
    tx(a,9,13,'Correct: 308/1,000',7.4,REASON)
    tx(a,99,13,'524/1,000',7.4,SEARCH,ha='right')
    b=f.add_axes([112/170,25/105,49/170,57/105])
    ps=np.array([S['difference'],S['equal_group_difference']])*100
    cis=np.array([S['difference_ci'],S['equal_group_ci']])*100
    for j,(p,ci) in enumerate(zip(ps,cis)):
        yy=1-j
        b.errorbar(p,yy,xerr=[[p-ci[0]],[ci[1]-p]],fmt=['o','s'][j],color=GREEN,
                   markersize=4.5,capsize=2.5,lw=1.2)
        b.text(0,yy+.36,['Record weighted','Combination weighted'][j],fontsize=7.7,color=INK)
        b.text(p,yy-.25,f'{p:.1f} ({ci[0]:.1f}–{ci[1]:.1f})',fontsize=7.5,ha='center',color=INK)
    b.axvline(0,color=LINE,lw=.65,ls=(0,(3,3)))
    b.set(xlim=(-1,35),ylim=(-.48,1.65),xticks=[0,10,20,30],yticks=[])
    b.spines['left'].set_visible(False); b.tick_params(axis='x',length=3,pad=3)
    tx(a,138,13,'Search minus reasoning\n(percentage points; 95% CI)',7.8,ha='center')
    tx(a,5,3,'All 1,000 pairs retained · Intervals resample 418 name–model combinations',7,MUTED)
    save(f,'Figure_2_paired_effects')

def fig3():
    f,a=canvas(140)
    heading(a,5,132,'a','Coverage and reliability')
    heading(a,85,132,'b','Outcome composition')
    b=f.add_axes([17/170,83/140,54/170,39/140])
    for j,(col,marker) in enumerate([(REASON,'o'),(SEARCH,'s')]):
        x=S['specific'][j]/S['n']*100; y=S['correct'][j]/S['specific'][j]*100
        b.plot([x,x],[50,y],color=col,lw=.65,ls=(0,(2,3)),alpha=.45)
        b.plot(x,y,marker=marker,color=col,ms=5.5,ls='none')
        label=f"{['Reasoning','Search'][j]}  {y:.1f}%\n{S['correct'][j]}/{S['specific'][j]} correct"
        b.annotate(label,(x,y),xytext=(-4,12) if j==0 else (-5,-29),textcoords='offset points',
                   ha='left' if j==0 else 'right',fontsize=7.5,color=col,linespacing=1.35)
        b.text(x,51.2,f"{S['specific'][j]}/1,000\n{x:.1f}%",ha='center',va='bottom',fontsize=7.5,color=col,
               bbox=dict(facecolor='white',edgecolor='none',pad=.8))
    b.set(xlim=(20,90),ylim=(50,100),xticks=[25,50,75],yticks=[50,75,100],
          xlabel='Specific brand outputs (%)',ylabel='Correct among brand outputs (%)')
    b.grid(axis='y',color='#E9EDF2',lw=.5); b.set_axisbelow(True)
    b.tick_params(length=3,pad=3)

    bx=88; bw=76; h=8
    for j,yy in enumerate([107,85]):
        tx(a,bx,yy+13,['Reasoning','Search'][j],8,[REASON,SEARCH][j],'bold')
        left=bx
        for q,n in enumerate(S['outcomes'][j]):
            w=bw*n/S['n']
            a.add_patch(Rectangle((left,yy),w,h,fc=OC[q],ec='white',lw=.5,
                                  hatch={1:'..',2:'///'}.get(q)))
            if n>=90: tx(a,left+w/2,yy+h/2,str(n),7.6,ha='center')
            else:
                shift=-2 if j==0 and q==1 else (4 if j==0 and q==2 else 0)
                line(a,[(left+w/2,yy-.4),(left+w/2+shift,yy-2.2)],MUTED,.5)
                tx(a,left+w/2+shift,yy-4,str(n),7.3,ha='center')
            left+=w
    labels=['Correct assignment','Incorrect assignment','Unverified assignment','Missed identification','Both unknown']
    for q,label in enumerate(labels):
        lx=88+(q%2)*40; ly=75-(q//2)*5.7
        a.add_patch(Rectangle((lx,ly-1.2),3,2.5,fc=OC[q],ec='white',lw=.4,hatch={1:'..',2:'///'}.get(q)))
        tx(a,lx+4.3,ly,label,6.8)
    tx(a,88,59,'Counts shown; each bar totals 1,000 records',7,MUTED)

    line(a,[(5,54),(165,54)],'#DCE2E8',.5)
    heading(a,5,47,'c','Exploratory review strata')
    tx(a,165,47,'Not independently validated',7,MUTED,ha='right')
    c=f.add_axes([70/170,14/140,91/170,26/140])
    for j,st in enumerate(S['risk'][:2]):
        p=st['search_yield']*100; ci=np.array(st['ci'])*100; yy=1-j
        c.errorbar(p,yy,xerr=[[p-ci[0]],[ci[1]-p]],fmt=['o','s'][j],color=SEARCH,
                   markersize=5,capsize=3,lw=1.2)
        c.text(p,yy+.27,f'{p:.1f}%',fontsize=8,ha='center',color=INK)
        physical_y=14+(yy+.65)/(1.65+.65)*26
        tx(a,10,physical_y+1.8,['Both output a brand','Only search outputs a brand'][j],8)
        tx(a,10,physical_y-3.3,f"{st['search_correct']}/{st['n']} search outputs correct",7.3,MUTED)
    c.set(xlim=(0,100),ylim=(-.65,1.65),xticks=[0,25,50,75,100],yticks=[])
    c.spines['left'].set_visible(False); c.grid(axis='x',color='#E9EDF2',lw=.5); c.set_axisbelow(True)
    c.tick_params(length=3,pad=3)
    tx(a,115.5,4.5,'Search outputs correct (%, cluster-bootstrap 95% CI)',7.7,ha='center')
    save(f,'Figure_3_coverage_risk')

if __name__=='__main__':
    fig1(); fig2(); fig3()
    print('Three figures exported as editable SVG/PDF, 600 dpi TIFF and 300 dpi PNG.')

