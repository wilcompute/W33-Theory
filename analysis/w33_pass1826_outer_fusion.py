#!/usr/bin/env python3
from __future__ import annotations
import sys,itertools,json,hashlib
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from w33_pass1801_1805_common import build_geometry,rank_mod,nullspace,basis_columns,inv_mod
P=1000003
D=build_geometry(); edges=D['edges']; eidx=D['eidx']; lines=D['lines']
bd=np.zeros((40,240),dtype=np.int64)
for j,(a,b) in enumerate(edges): bd[a,j]=-1; bd[b,j]=1
tri=[]
for line in lines:
    for a,b,c in itertools.combinations(line,3):
        row=np.zeros(240,dtype=np.int64)
        row[eidx[(a,b)]]=1; row[eidx[(b,c)]]=1; row[eidx[(a,c)]]=-1
        tri.append(row)
tri=np.array(tri,dtype=np.int64); assert tri.shape==(160,240)
pp,ep=D['outer'][0],D['outer'][1]
sign=np.array([1 if pp[a]<pp[b] else -1 for a,b in edges],dtype=np.int64)
def act_rows(B):
    Y=np.zeros_like(B); Y[:,np.array(ep)]=(B*sign)%P; return Y%P
def rep_trace(B):
    rows=basis_columns(B.T,P); BB=B[rows,:]%P
    cols=basis_columns(BB,P); C=BB[:,cols]%P; Ci=inv_mod(C,P)
    Y=act_rows(BB); R=(Y[:,cols]@Ci)%P
    assert np.array_equal((R@BB)%P,Y%P)
    tr=int(np.trace(R)%P); tr=tr if tr<P//2 else tr-P
    plus=len(BB)-rank_mod((R-np.eye(len(BB),dtype=np.int64))%P,P)
    minus=len(BB)-rank_mod((R+np.eye(len(BB),dtype=np.int64))%P,P)
    return {'dimension':len(BB),'trace':tr,'plus':plus,'minus':minus,'determinant':(-1)**minus}
A=np.zeros((40,40),dtype=np.int64)
for a,b in edges: A[a,b]=A[b,a]=1
E15=nullspace((A+4*np.eye(40,dtype=np.int64))%P,P)
E24=nullspace((A-2*np.eye(40,dtype=np.int64))%P,P)
G15=(E15@bd)%P; G24=(E24@bd)%P
s=np.zeros((45,40),dtype=np.int64); u=np.zeros((45,240),dtype=np.int64)
for o,(left,right) in enumerate(D['octets']):
    s[o,list(left)]=1; s[o,list(right)]=-1
    for a in left:
        for b in right: u[o,eidx[tuple(sorted((a,b)))]]=1 if a<b else -1
V=(4*u+s@bd)%P
H=nullspace(np.vstack([bd,tri])%P,P)
assert (rank_mod(bd,P),rank_mod(V,P),rank_mod(G15,P),rank_mod(G24,P),len(H))==(39,30,15,24,81)
blocks={'15':rep_trace(G15),'24':rep_trace(G24),'30':rep_trace(V),'81':rep_trace(H)}
Gens=[tuple(a[0]) for a in D['acts']]+[tuple(D['outer'][0])]
out=Gens[-1]; I=tuple(range(40))
def comp(p,q): return tuple(p[q[i]] for i in range(40))
seen={I}; queue=[I]
for x in queue:
    for g in Gens:
        y=comp(g,x)
        if y not in seen: seen.add(y); queue.append(y)
cent=sum(comp(g,out)==comp(out,g) for g in seen)
fp=sum(out[i]==i for i in range(40)); fl=sum(tuple(sorted(out[x] for x in l))==l for l in lines)
ff=sum(i==D['outer'][3][i] for i in range(540)); fo=sum(i==D['outer'][4][i] for i in range(45))
res={'schema':'w33.pass1826.outer_fusion.v1','status':'PASS','group_order':len(seen),'canonical_outer':{'order':2,'centralizer':cent,'class_size':len(seen)//cent,'fixed_points':fp,'fixed_lines':fl,'fixed_frames':ff,'fixed_octets':fo,'atlas_class':'2D','atlas_reason':'ATLAS U4(2):2 has outer involutions 2C (centralizer 1440) and 2D (centralizer 96); the canonical multiplier-minus-one involution has centralizer 96.'},'chiral_block_2D_traces':blocks,'sign_twist_traces':{k:-v['trace'] for k,v in blocks.items()},'four_bit_reconciliation':'The four chiral characters are globally independent functions, while evaluation at the canonical geometric outer involution is the single 2D column shown here. The coexact trace +2 is therefore the degree-30 coordinate of the four-bit vector, not a universal scalar handedness bit.'}
raw=json.dumps(res,sort_keys=True,separators=(',',':')); res['sha256']=hashlib.sha256(raw.encode()).hexdigest()
assert res['sha256']=='733db25929c469107b9f178a626a4a4c45c020261c1b28f1613b53af1a15cac4'
(ROOT/'data'/'w33_pass1826_outer_fusion.json').write_text(json.dumps(res,sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps(res,indent=2))
