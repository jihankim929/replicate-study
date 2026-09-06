import pandas as pd, numpy as np, matplotlib.pyplot as plt, matplotlib as mpl
from matplotlib.lines import Line2D
mpl.rcParams['font.family']='Liberation Sans'; mpl.rcParams['font.size']=7.5; mpl.rcParams['pdf.fonttype']=42; mpl.rcParams['svg.fonttype']='none'
e=pd.read_csv('analysis/fig2_events.csv',comment='#')
c=pd.read_csv('analysis/claims_new.csv',comment='#')
c['structure_id']=c.structure_id_resolved.fillna(c.structure_id)
c=c[c.quantity=='deliverable_capacity']  # by record: drops rep09's N65 rows and rep03's 'other'
c['unc']=pd.to_numeric(c.reported_uncertainty.astype(str).str.extract(r'([\d.]+)')[0],errors='coerce')
C='#1b6e5a'; U='#b5521a'; GREY='#8a8a8a'
order=list(e[e.group=='C'].run)+list(e[e.group=='U'].run)
ypos={r:len(order)-i for i,r in enumerate(order)}
lo,hi=180,212
def fam(s):
    if 'Cu][pts' in s and s.startswith('2016'): return 'Cu pts'
    if 'V][srs' in s: return 'V srs'
    if 'Yb][nia' in s: return 'Yb nia'
    if 'In][nuc' in s: return 'In nuc'
    if 'Cu][sql' in s: return 'Cu sql'
    return 'other'
famcol={'Cu pts':'#1f5f9e','V srs':'#7b3fa0','Yb nia':'#d19b00','In nuc':'#2a9d8f','other':'#999999','Cu sql':GREY}
# filter: drop low passing mentions and rep09's N65 absolute uptakes (pending quantity column)
cc=c[~((c.reported_value<lo)&(c.structure_class!='excluded'))]


fig=plt.figure(figsize=(7.2,6.0))
gs=fig.add_gridspec(2,2,width_ratios=[1.1,1],height_ratios=[16,6.2],hspace=0.12,wspace=0.12)
ax=fig.add_subplot(gs[0,0]); bx=fig.add_subplot(gs[0,1],sharey=ax); cx=fig.add_subplot(gs[1,1],sharex=bx)
# ---- panel a
for _,r in e.iterrows():
    y=ypos[r.run]; col=C if r.group=='C' else U
    ax.plot([0,max(r.t_session_end,r.t_final_filing)],[y,y],color=col,lw=3.2,alpha=0.28,solid_capstyle='butt',zorder=1)
    ax.plot([r.t_first_job_submitted],[y],'|',color=col,ms=7,mew=1.2,zorder=3)
    if not np.isnan(r.t_first_declared_strategy): ax.plot(r.t_first_declared_strategy,y,'^',color=col,ms=4.5,zorder=3)
    ax.plot(r.t_first_high_accuracy_calc,y,'D',color=col,ms=3.8,zorder=3)
    ax.plot(r.t_first_encounter_cu_sql,y,'o',mfc='white',mec=GREY,ms=4.5,mew=1.0,zorder=3)
    ax.plot(r.t_final_filing,y,'s',color=col,ms=4.5,mfc=col if r.end_reason=='spend_cap' else 'white',mew=1.1,zorder=4)
    ax.text(-2.5,y,r.strategy,ha='right',va='center',fontsize=7,color='#333')
ax.annotate('deadline 168 h',xy=(97,len(order)+0.95),xytext=(84,len(order)+0.95),fontsize=6.5,color='#444',va='center',ha='right',arrowprops=dict(arrowstyle='->',color='#444',lw=0.7))
ax.set_xlim(-6,98); ax.set_xticks([0,24,48,72,96]); ax.set_xlabel('Hours since launch')
ax.set_yticks(list(ypos.values())); ax.set_yticklabels(list(ypos.keys()),fontsize=7); ax.set_ylim(0.3,len(order)+1.3)
ax.axhspan(8.5,len(order)+0.7,color=C,alpha=0.04,lw=0); ax.axhspan(0.4,8.5,color=U,alpha=0.04,lw=0)
ax.text(97,ypos['rep01']+0.1,'checked',ha='right',va='bottom',fontsize=7,color=C,fontweight='bold')
ax.text(97,ypos['rep02']+0.1,'unchecked',ha='right',va='bottom',fontsize=7,color=U,fontweight='bold')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.set_title('a  Course of the sixteen runs',loc='left',fontsize=8.5,fontweight='bold')
h=[Line2D([],[],marker='|',color='#444',ls='',ms=7,mew=1.2,label='first job submitted'),
   Line2D([],[],marker='^',color='#444',ls='',ms=4.5,label='strategy first declared'),
   Line2D([],[],marker='D',color='#444',ls='',ms=3.8,label='first high-accuracy calculation'),
   Line2D([],[],marker='o',mfc='white',mec=GREY,ls='',ms=4.5,label='first encounter, excluded Cu sql entry'),
   Line2D([],[],marker='s',color='#444',ls='',ms=4.5,label='final report (filled: ended at spend cap)')]
leg1=ax.legend(handles=h,loc='upper left',bbox_to_anchor=(0.0,-0.10),fontsize=6.5,frameon=False,ncol=1,handletextpad=0.5,title='Panel a',title_fontsize=6.5,alignment='left')
# ---- panel b
bx.axvspan(190,200,color='#dddddd',alpha=0.45,lw=0,zorder=0)
for _,r in cc.iterrows():
    y=ypos[r.run]; v=r.reported_value
    if r.structure_class=='excluded':
        bx.plot(v,y,'o',mfc='white',mec=GREY,ms=5.5 if r.rank_in_run==1 else 4,mew=1.0,zorder=3); continue
    if r.structure_class=='agent_modified':
        bx.plot(v,y,'*',color='#c0392b',ms=6,zorder=3); continue
    col=famcol[fam(r.structure_id)]
    bx.errorbar(v,y,xerr=r.unc if not np.isnan(r.unc) else 0,fmt='o',color=col,ms=5.5 if r.rank_in_run==1 else 3.8,
                mec='black' if r.rank_in_run==1 else col,mew=0.8,elinewidth=0.7,capsize=0,zorder=3)
bx.set_xlim(lo,hi); plt.setp(bx.get_xticklabels(),visible=False); plt.setp(bx.get_yticklabels(),visible=False)
bx.axhspan(8.5,len(order)+0.7,color=C,alpha=0.04,lw=0); bx.axhspan(0.4,8.5,color=U,alpha=0.04,lw=0)
for s in ['top','right']: bx.spines[s].set_visible(False)
bx.set_title('b  Materials reported by each run',loc='left',fontsize=8.5,fontweight='bold')
bx.text(195,len(order)+0.9,'literature band',ha='center',fontsize=6.5,color='#555')
bx.tick_params(axis='y',length=0)
h2=[Line2D([],[],marker='o',color=famcol[k],ls='',ms=4,label=k) for k in ['Cu pts','V srs','Yb nia','In nuc','other']]
h2+=[Line2D([],[],marker='*',color='#c0392b',ls='',ms=6,label='agent-modified'),
     Line2D([],[],marker='o',mfc='white',mec=GREY,ls='',ms=4.5,label='excluded by audit'),
     Line2D([],[],marker='o',mfc='#bbb',mec='black',ls='',ms=5.5,label='black edge: claimed best')]
# ---- panel c: per-material aggregate
rows=[('Cu sql (excluded)','excluded'),('built by rep02','agent_modified'),('Cu pts','Cu pts'),('V srs','V srs'),('Yb nia','Yb nia'),('In nuc','In nuc')]
cx.axvspan(190,200,color='#dddddd',alpha=0.45,lw=0,zorder=0)
for i,(lab,key) in enumerate(rows):
    y=len(rows)-i
    if key in ('excluded','agent_modified'): sub=cc[cc.structure_class==key]
    else: sub=cc[(cc.structure_class=='retained')&(cc.structure_id.map(fam)==key)]
    nruns=sub.run.nunique()
    col=famcol.get(key,GREY)
    if key=='excluded':
        cx.plot(sub.reported_value,[y]*len(sub),'o',mfc='white',mec=GREY,ms=4,mew=0.9,zorder=3)
    elif key=='agent_modified':
        cx.plot(sub.reported_value,[y]*len(sub),'*',color='#c0392b',ms=5.5,zorder=3)
    else:
        cx.plot(sub.reported_value,[y]*len(sub),'o',color=col,ms=4,alpha=0.85,zorder=3)
    cx.plot([sub.reported_value.min(),sub.reported_value.max()],[y,y],color=col,lw=1.0,alpha=0.5,zorder=2)
    cx.text(211.6,y,f'{nruns} run' + ('s' if nruns!=1 else ''),ha='right',va='center',fontsize=6.5,color='#333')
cx.set_yticks(range(1,len(rows)+1)); cx.set_yticklabels([r[0] for r in rows][::-1],fontsize=7); cx.set_ylim(0.4,len(rows)+0.7)
cx.set_xlabel('Reported deliverable capacity (cm$^3$ cm$^{-3}$)')
for s in ['top','right']: cx.spines[s].set_visible(False)
cx.set_title('c  Agreement across runs, by material',loc='left',fontsize=8.5,fontweight='bold')
ax.add_artist(leg1)
ax.legend(handles=h2,loc='upper left',bbox_to_anchor=(0.0,-0.46),fontsize=6.5,frameon=False,ncol=2,handletextpad=0.5,columnspacing=1.2,title='Panels b and c',title_fontsize=6.5,alignment='left')
fig.subplots_adjust(left=0.08,right=0.98,top=0.95,bottom=0.2)
plt.savefig('fig2_draft.png',dpi=220,bbox_inches='tight'); plt.savefig('/mnt/user-data/outputs/Figure2_draft_v9.pdf',bbox_inches='tight')
