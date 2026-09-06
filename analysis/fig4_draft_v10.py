import numpy as np, pandas as pd, matplotlib.pyplot as plt, matplotlib as mpl
from matplotlib.lines import Line2D
mpl.rcParams['font.family']='Liberation Sans'; mpl.rcParams['font.size']=7.5; mpl.rcParams['pdf.fonttype']=42
C='#0F6E56'; U='#B3541A'; GREY='#9C9A92'; TXT='#2C2C2A'; ACC='#534AB7'; HL='#c0392b'
ref=pd.read_csv('analysis/fig4_interim.csv',comment='#')
claims=pd.read_csv('analysis/claims_new.csv',comment='#'); claims['sid']=claims.structure_id_resolved.fillna(claims.structure_id); claims=claims[claims.quantity=='deliverable_capacity']
ev=pd.read_csv('analysis/fig2_events.csv',comment='#'); cov=pd.read_csv('analysis/coverage.csv',comment='#')
refval=dict(zip(ref.structure_id,ref.working_capacity)); reported=set(claims[claims.structure_class=='retained'].sid)
tail=ref[ref.segment!='agent_tail'].sort_values('working_capacity',ascending=False).drop_duplicates('structure_id').reset_index(drop=True)
best_ref=tail.working_capacity.max()
# per-agent best retained claim -> reference value, regret
rows=[]
for r in ev.run:
    sub=claims[(claims.run==r)&(claims.structure_class=='retained')]
    if len(sub)==0: rows.append((r,ev[ev.run==r].group.iloc[0],None,np.nan)); continue
    top=sub.sort_values('reported_value',ascending=False).iloc[0]
    rows.append((r,ev[ev.run==r].group.iloc[0],top.sid,refval.get(top.sid,np.nan)))
A=pd.DataFrame(rows,columns=['run','group','best_sid','ref_value']).merge(cov[['run','stated_distinct_structures']],on='run'); A['regret']=best_ref-A.ref_value

fig=plt.figure(figsize=(7.2,5.8))
gs=fig.add_gridspec(2,2,height_ratios=[1,1.05],width_ratios=[1,1.15],hspace=0.4,wspace=0.25,left=0.08,right=0.93,top=0.95,bottom=0.08)
# ---- a: landscape
ax=fig.add_subplot(gs[0,:])
s=ref[ref.segment=='sample'].working_capacity
w=np.ones(len(s))/len(s); ax.hist(s,bins=np.arange(0,215,5),weights=w,color='#C9C7BE',edgecolor='white',lw=0.4)
ax.set_xlabel('Deliverable capacity under the pinned protocol (cm$^3$ cm$^{-3}$)'); ax.set_ylabel(f'Fraction of random sample (n = {len(s):,})')
ax.set_xlim(0,218); ax.set_ylim(0,ax.get_ylim()[1]*1.45)
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ymax=ax.get_ylim()[1]
for _,r in A.dropna(subset=['ref_value']).iterrows(): ax.plot(r.ref_value,ymax*0.66,'v',color=C if r.group=='C' else U,ms=4,clip_on=False)
ax.errorbar(207.17,ymax*0.66,xerr=1.24,fmt='o',mfc='white',mec=GREY,ecolor=GREY,ms=5,clip_on=False); ax.text(210.5,ymax*0.56,'excluded entry\n(pinned protocol)',ha='center',va='top',fontsize=6,color=GREY)
ax.axvline(best_ref,color=ACC,lw=0.8,ls='--'); ax.text(best_ref-1.2,ymax*0.28,'reference best, retained',rotation=90,va='center',ha='right',fontsize=6,color=ACC)
h=[Line2D([],[],marker='v',color=C,ls='',label='checked agent, best retained claim'),Line2D([],[],marker='v',color=U,ls='',label='unchecked agent, best retained claim')]
ax.legend(handles=h,loc='upper left',bbox_to_anchor=(0.0,1.0),fontsize=6,frameon=False)
# inset: tail ranked, colored by whether an agent reported it
ins=ax.inset_axes([0.42,0.44,0.34,0.50])
top=tail.head(30)
cols=[ACC if sid in reported else '#C9C7BE' for sid in top.structure_id]
ins.bar(range(1,len(top)+1),top.working_capacity,color=cols,width=0.8,yerr=top.uncertainty,error_kw=dict(elinewidth=0.5,capsize=1.2,capthick=0.5,ecolor='#444'))
ins.set_ylim(180,203); ins.set_xlim(0.3,len(top)+0.7); ins.set_xlabel('Rank by reference point estimate, all measured structures',fontsize=6); ins.set_ylabel('cm$^3$ cm$^{-3}$',fontsize=6)
ins.tick_params(labelsize=6); ins.set_title(f'top {len(top)} of {len(tail):,} measured; purple = reported by an agent',fontsize=6,loc='left')
for sp in ['top','right']: ins.spines[sp].set_visible(False)
# ---- b: frontier recovery vs search volume
bx=fig.add_subplot(gs[1,0])
top10=set(tail.head(10).structure_id)
rec=[]
for r in ev.run:
    sids=set(claims[(claims.run==r)&(claims.structure_class=='retained')].sid)
    n=len(sids&top10); xv=cov[cov.run==r].stated_distinct_structures.iloc[0]; stated=not np.isnan(xv)
    if not stated: xv=cov[cov.run==r].distinct_any_surviving_output.iloc[0]
    rec.append((r,ev[ev.run==r].group.iloc[0],n,xv,stated))
R=pd.DataFrame(rec,columns=['run','group','n_top10','screened','stated'])
for g,col in [('C',C),('U',U)]:
    sub=R[(R.group==g)&R.stated]; bx.plot(sub.screened,sub.n_top10,'o',color=col,ms=4.5,alpha=0.85)
    sub=R[(R.group==g)&~R.stated]; bx.plot(sub.screened,sub.n_top10,'o',mfc='white',mec=col,ms=4.5,mew=1.0)
from scipy.stats import spearmanr
print('spearman stated only:',spearmanr(R[R.stated].screened,R[R.stated].n_top10), 'n=',R.stated.sum())
seen={}
for _,r in R.iterrows():
    key=(round(np.log10(r.screened)*4)/4,r.n_top10); k=seen.get(key,0); seen[key]=k+1
    off={'rep01':(1.12,0.35),'rep10':(1.12,-0.45),'rep13':(0.62,-0.45),'rep12':(1.12,0.15),'rep17':(1.12,-0.35)}.get(r.run,(1.12,0.15))
    bx.text(r.screened*off[0],r.n_top10+off[1],r.run,fontsize=5.5,color=TXT)
bx.set_xscale('log'); bx.set_xlabel('Structures screened (stated by the agent; open, surviving outputs)'); bx.set_ylabel('Reference top-10 structures\n(by point estimate) reported by the agent')
bx.set_yticks(range(0,11,2)); bx.set_ylim(-0.5,10.5)
for sp in ['top','right']: bx.spines[sp].set_visible(False)
bx.legend(handles=[Line2D([],[],marker='o',color=C,ls='',ms=4.5,label='checked agent'),Line2D([],[],marker='o',color=U,ls='',ms=4.5,label='unchecked agent')],fontsize=6.5,frameon=False,loc='upper left')
print(R.to_string())
# ---- c: map
cx=fig.add_subplot(gs[1,1])
um=pd.read_csv('analysis/umap_v2.csv').merge(pd.read_csv('analysis/descriptors.csv')[['structure_id','recon_vf_he']],on='structure_id')
cx.scatter(um.x,um.y,s=1.5,c=um.recon_vf_he,cmap='viridis',alpha=0.6,linewidths=0)
r=um[um.structure_id.isin(reported)]; x_=um[um.structure_id.isin(set(claims[claims.structure_class=='excluded'].sid))]
cx.scatter(r.x,r.y,s=22,facecolor='none',edgecolor=U,lw=1.0,zorder=3,label='reported by agents, retained')
cx.scatter(x_.x,x_.y,s=40,facecolor='none',edgecolor='#e0007f',lw=1.4,zorder=4,label='excluded entry')
ylo,yhi=cx.get_ylim(); cx.set_ylim(ylo-0.02*(yhi-ylo), yhi+0.25*(yhi-ylo))
cx.axis('off'); cx.legend(fontsize=6.5,frameon=False,loc='upper left',bbox_to_anchor=(-0.02,1.0),ncol=1)
sm=plt.cm.ScalarMappable(cmap='viridis',norm=plt.Normalize(0,0.8)); cb=plt.colorbar(sm,ax=cx,fraction=0.035,pad=0.02,ticks=[0,0.2,0.4,0.6,0.8]); cb.set_label('Void fraction',fontsize=6.5); cb.ax.tick_params(labelsize=6.5)
for lab,(x,y) in {'a':(0.02,0.965),'b':(0.02,0.45),'c':(0.53,0.45)}.items(): fig.text(x,y,lab,fontsize=9,fontweight='bold')
fig.text(0.5,0.005,'sample 1,495 of 1,500; porous tail 833 of 858',fontsize=6,color=GREY,ha='center')
plt.savefig('/mnt/user-data/outputs/Figure4_draft_v10.png',dpi=220); plt.savefig('/mnt/user-data/outputs/Figure4_draft_v10.pdf')
print(A[['run','group','best_sid','ref_value','regret']].to_string())
print('agent-reported among top-k of tail:', [ (k, sum(sid in reported for sid in tail.head(k).structure_id)) for k in (5,8,10,20)])
