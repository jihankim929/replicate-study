import numpy as np, matplotlib.pyplot as plt, matplotlib as mpl
from matplotlib.collections import LineCollection
from render import load, nets
mpl.rcParams['font.family']='Liberation Sans'; mpl.rcParams['font.size']=7; mpl.rcParams['pdf.fonttype']=42
GREY='#8a8a8a'; C='#1b6e5a'; U='#b5521a'; HL='#c0392b'
def project(a,view):
    cell=a.cell.array; ax_i={'a':0,'b':1,'c':2}[view]; o=[k for k in range(3) if k!=ax_i]
    u=cell[o[0]]/np.linalg.norm(cell[o[0]]); w=np.cross(cell[ax_i],u); w/=np.linalg.norm(w); v=np.cross(w,u)
    return lambda X: np.array([X@u,X@v])
def draw(ax,a,rep=(2,2,1),view='c',netcols=None,hl_idx=None,hl_col=HL,lw=0.55,title=None):
    i,j,S,lab,n=nets(a); sizes=np.bincount(lab)
    big=[k for k in np.argsort(-sizes) if sizes[k]>=10]
    netcols=netcols or ['#1f5f9e','#c0392b']
    cols={k:netcols[t%len(netcols)] for t,k in enumerate(big)}
    small=[k for k in range(n) if sizes[k]<10]
    cell=a.cell.array; pos=a.positions; P=project(a,view)
    hl=set(hl_idx or [])
    segs=[];cs=[];lws=[];pts=[];pc=[];ps=[]
    for ra in range(rep[0]):
      for rb in range(rep[1]):
        for rc in range(rep[2]):
            sh=ra*cell[0]+rb*cell[1]+rc*cell[2]
            for ii,jj,ss in zip(i,j,S):
                if ii>jj and (ss==0).all(): continue
                if a[ii].symbol=='H' or a[jj].symbol=='H': continue
                c_=hl_col if (ii in hl or jj in hl or lab[ii] in small) else cols.get(lab[ii],GREY)
                segs.append(np.vstack([P(pos[ii]+sh),P(pos[jj]+ss@cell+sh)])); cs.append(c_); lws.append(lw*(1.8 if c_==hl_col else 1))
            for k in range(len(a)):
                s=a[k].symbol
                if s=='H' and k not in hl and lab[k] not in small: continue
                metal=s not in('C','H','N','O','F','Cl','S','B')
                c_=hl_col if (k in hl or lab[k] in small) else cols.get(lab[k],GREY)
                pts.append(P(pos[k]+sh)); pc.append(c_); ps.append(10 if metal else (4 if c_==hl_col else 1.8))
    ax.add_collection(LineCollection(segs,colors=cs,linewidths=lws,alpha=0.9))
    pts=np.array(pts); ax.scatter(pts[:,0],pts[:,1],s=ps,c=pc,edgecolors='none',zorder=3)
    ax.set_aspect('equal'); ax.autoscale(); ax.axis('off')
    if title: ax.set_title(title,fontsize=7,pad=2)
def diff_atoms(child,parent,tol=0.35):
    # atoms in child with no parent atom within tol (Cartesian, same cell assumed)
    from scipy.spatial import cKDTree
    t=cKDTree(parent.positions); d,_=t.query(child.positions); return [k for k in range(len(child)) if d[k]>tol]

fig=plt.figure(figsize=(7.2,5.6))
gs=fig.add_gridspec(2,2,height_ratios=[1,0.9],hspace=0.2,wspace=0.18,left=0.21,right=0.97,top=0.95,bottom=0.06)

# ---------- a: inventory
ax=fig.add_subplot(gs[0,0])
rows=[('rep02','U','net removal',1713,'retained'),('rep15','U','water removal',251,'retained'),
      ('rep09','U','terminal-group removal',209,'retained'),('rep10','U','methylation',24,'retained'),
      ('rep12','C','methyl / fluoro',7,'mixed'),('rep06','C','net removal',4,'retained'),
      ('rep05','C','lattice scaling',35,'excluded'),('rep17','U','methyl / fluoro',10,'excluded')]
ys=range(len(rows),0,-1)
for y,(run,g,tr,nf,pc_) in zip(ys,rows):
    col=(C if g=='C' else U) if pc_!='excluded' else '#bbbbbb'
    ax.barh(y,nf,color=col,height=0.6)
    ax.text(nf*1.25,y,f'{nf:,}',va='center',fontsize=6.5,color='#333')
    ax.text(0.7,y,f'{run}  {tr}'+('  (parent excluded by audit)' if pc_=='excluded' else ''),va='center',ha='left',fontsize=6.3,color='white' if nf>60 and pc_=='retained' else '#333',
            transform=ax.get_yaxis_transform() if False else ax.transData,clip_on=False) if False else None
ax.set_yticks(list(ys)); ax.set_yticklabels([f'{r[0]}  {r[2]}' for r in rows],fontsize=6.5)
ax.set_xscale('log'); ax.set_xlim(1,6000); ax.set_xlabel('Structure files built')
for s in ['top','right']: ax.spines[s].set_visible(False)

from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=C,label='checked'),Patch(color=U,label='unchecked'),Patch(color='#bbbbbb',label='parent excluded by audit')],loc='lower right',fontsize=6,frameon=False,handlelength=1.0,bbox_to_anchor=(1.0,0.08))



# ---------- b: de-interpenetration
sub=gs[0,1].subgridspec(2,2,wspace=0.05,hspace=0.35)
p=load('analysis/fig3/rep02/db/2014[Zn][hms]3[ASR]1.cif'); c=load('analysis/fig3/rep02/mod/2014[Zn][hms]3[ASR]1__1of2.cif')
a1=fig.add_subplot(sub[0,0]); draw(a1,p,rep=(2,2,1),view='c',title='2014[Zn][hms]3'); a1.text(0.5,-0.06,'75.4 cm$^3$ cm$^{-3}$',transform=a1.transAxes,ha='center',fontsize=6.5)
a2=fig.add_subplot(sub[0,1]); draw(a2,c,rep=(2,2,1),view='c',title='one net removed'); a2.text(0.5,-0.06,'203.7 cm$^3$ cm$^{-3}$',transform=a2.transAxes,ha='center',fontsize=6.5)
p2=load('analysis/fig3/rep06/db/0000[Lu][lcy]3[ASR]1.cif'); c2=load('analysis/fig3/rep06/work/mod/0000[Lu][lcy]3[ASR]1_DENET.cif')
a3=fig.add_subplot(sub[1,0]); draw(a3,p2,rep=(1,1,1),view='c',title='0000[Lu][lcy]3'); a3.text(0.5,-0.06,'165.8 cm$^3$ cm$^{-3}$',transform=a3.transAxes,ha='center',fontsize=6.5)
a4=fig.add_subplot(sub[1,1]); draw(a4,c2,rep=(1,1,1),view='c',title='one net removed'); a4.text(0.5,-0.06,'175.4 cm$^3$ cm$^{-3}$',transform=a4.transAxes,ha='center',fontsize=6.5)
# ---------- c: terminal water removal
sub=gs[1,0].subgridspec(1,2,wspace=0.05)
p=load('analysis/fig3/rep15/db/2011[FeHo][nan]3[FSR]1.cif'); c=load('analysis/fig3/rep15/cifs/2011[FeHo][nan]3[FSR]1+DEAQ.cif')
lost=[k for k in range(len(p)) if k not in set(range(len(p)))]  # placeholder
from scipy.spatial import cKDTree
t=cKDTree(c.positions); d,_=t.query(p.positions); water=[k for k in range(len(p)) if d[k]>0.35]
a1=fig.add_subplot(sub[0,0]); draw(a1,p,rep=(1,1,1),view='c',hl_idx=water,title='2011[FeHo][nan]3'); a1.text(0.5,-0.06,'23.3 cm$^3$ cm$^{-3}$',transform=a1.transAxes,ha='center',fontsize=6.5)
a2=fig.add_subplot(sub[0,1]); draw(a2,c,rep=(1,1,1),view='c',title='bound water removed'); a2.text(0.5,-0.06,'98.1 cm$^3$ cm$^{-3}$',transform=a2.transAxes,ha='center',fontsize=6.5)


# ---------- d: methylation
sub=gs[1,1].subgridspec(1,2,wspace=0.05)
p=load('analysis/fig3/rep10/db/2013[Yb][nia]3[ASR]1.cif'); c=load('analysis/fig3/rep10/mod/M2013_Yb__nia_3_ASR_1_f25.cif')
added=diff_atoms(c,p)
a1=fig.add_subplot(sub[0,0]); draw(a1,p,rep=(1,1,1),view='c',title='2013[Yb][nia]3'); a1.text(0.5,-0.06,'198.3 cm$^3$ cm$^{-3}$',transform=a1.transAxes,ha='center',fontsize=6.5)
a2=fig.add_subplot(sub[0,1]); draw(a2,c,rep=(1,1,1),view='c',hl_idx=added,title='25% methylated'); a2.text(0.5,-0.06,'187.1 cm$^3$ cm$^{-3}$',transform=a2.transAxes,ha='center',fontsize=6.5)


for lab,(x,y) in {'a':(0.02,0.965),'b':(0.545,0.965),'c':(0.02,0.45),'d':(0.545,0.45)}.items(): fig.text(x,y,lab,fontsize=9,fontweight='bold')
plt.savefig('fig3_draft.png',dpi=220); plt.savefig('/mnt/user-data/outputs/Figure3_draft_v11.pdf')
