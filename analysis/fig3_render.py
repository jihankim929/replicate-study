import re, numpy as np, matplotlib.pyplot as plt, matplotlib as mpl, pandas as pd
from ase.io import read
from ase.neighborlist import neighbor_list
from ase.data import covalent_radii, atomic_numbers
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
mpl.rcParams['font.family']='Liberation Sans'
def load(p):
    txt=open(p).read()
    txt=re.sub(r'\b([A-Z][a-z]?)_\b',r'\1',txt)
    open('/tmp/x.cif','w').write(txt)
    a=read('/tmp/x.cif'); a.set_pbc(True); return a
def nets(a):
    cut={s:covalent_radii[atomic_numbers[s]]*1.2 for s in set(a.get_chemical_symbols())}
    i,j,S=neighbor_list('ijS',a,{(x,y):cut[x]+cut[y] for x in cut for y in cut})
    g=coo_matrix((np.ones(len(i)),(i,j)),shape=(len(a),len(a)))
    n,lab=connected_components(g,directed=False)
    return i,j,S,lab,n
def draw(ax,a,rep=(2,2,1),view='c',title=''):
    i,j,S,lab,n=nets(a)
    sizes=np.bincount(lab); big=[k for k in range(n) if sizes[k]>=10]
    cols={k:c for k,c in zip(big,['#1f5f9e','#c0392b','#2a9d8f','#d19b00'])}
    cell=a.cell.array; pos=a.positions
    # projection basis: view along axis 'view'
    ax_i={'a':0,'b':1,'c':2}[view]; others=[k for k in range(3) if k!=ax_i]
    u=cell[others[0]]/np.linalg.norm(cell[others[0]]); w=np.cross(cell[ax_i],u); w/=np.linalg.norm(w); v=np.cross(w,u)
    P=lambda X: np.array([X@u, X@v])
    segs=[];cs=[];pts=[];pc=[];ps=[]
    for ra in range(rep[0]):
      for rb in range(rep[1]):
        for rc in range(rep[2]):
            sh=ra*cell[0]+rb*cell[1]+rc*cell[2]
            for ii,jj,ss in zip(i,j,S):
                if lab[ii] not in cols or ii>jj and (ss==0).all(): continue
                p1=pos[ii]+sh; p2=pos[jj]+ss@cell+sh
                segs.append(np.vstack([P(p1),P(p2)])); cs.append(cols[lab[ii]])
            for k in range(len(a)):
                if lab[k] in cols:
                    pts.append(P(pos[k]+sh)); pc.append(cols[lab[k]]); ps.append(9 if a[k].symbol not in('C','H','N','O','F','Cl','S') else (0 if a[k].symbol=='H' else 2.5))
    from matplotlib.collections import LineCollection
    ax.add_collection(LineCollection(segs,colors=cs,linewidths=0.6,alpha=0.85))
    pts=np.array(pts); ax.scatter(pts[:,0],pts[:,1],s=ps,c=pc,edgecolors='none',zorder=3)
    ax.set_aspect('equal'); ax.autoscale(); ax.axis('off'); ax.set_title(title,fontsize=7)
    return n,sizes
if __name__=='__main__':
    m=pd.read_csv('fig3/MANIFEST.csv',comment='#')
    pairs=[(m[(m.structure_id==p)].local_path.iloc[0], m[(m.parent_structure_id==p)&(m.role.str.startswith('child'))].local_path.iloc[0], p) for p in m.parent_structure_id.unique()]
    fig,axes=plt.subplots(len(pairs),2,figsize=(6,3*len(pairs)))
    for r,(pp,cp,name) in enumerate(pairs):
        for c_,(path,lab) in enumerate([(pp,'parent'),(cp,'child')]):
            a=load(path); n,sz=draw(axes[r,c_],a); axes[r,c_].set_title(f'{name} {lab}  nets={int((sz>=10).sum())} atoms={len(a)}',fontsize=7)
    plt.tight_layout(); plt.savefig('fig3_contact.png',dpi=110)
