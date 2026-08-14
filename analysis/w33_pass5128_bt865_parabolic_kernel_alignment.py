#!/usr/bin/env python3
"""Pass5128: BT865 torsor groups are the canonical q=3 parabolic kernels.

The point and line parabolics both have order 648 but their local actions are
not the same in odd symplectic type.  The point parabolic acts on the four
lines through its fixed point through A4; its 54-element kernel has derived
subgroup H27 of order 27.  The quotient by H27 is SL(2,3).  The line
parabolic acts on the four points of its fixed line through S4 with kernel
F3^3 of order 27.  The positive-root subgroups from Pass5105 agree exactly
with these canonical subgroups.  Thus the BT865 group-level torsor gauge is
closed; only its free rank-three H1 cycle-seed basis remains noncanonical.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5128_BT865_PARABOLIC_ALIGNMENT.json'
P=3

def canon(v):
    for x in v:
        if x%3:
            s=1 if x%3==1 else 2; return tuple((s*y)%3 for y in v)
    raise ValueError
def symp(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3
def comp(a,b): return tuple(a[b[i]] for i in range(len(b)))
def invp(g):
    z=[0]*len(g)
    for i,j in enumerate(g):z[j]=i
    return tuple(z)
def closure(gens,n=40):
    I=tuple(range(n));S={I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);Q.append(z)
    return S
def order(g):
    I=tuple(range(len(g)));x=I
    for n in range(1,100):
        x=comp(g,x)
        if x==I:return n
    raise RuntimeError
def derived(G):
    G=list(G);cs=[]
    for a in G:
      ai=invp(a)
      for b in G: cs.append(comp(comp(comp(a,b),ai),invp(b)))
    return closure(cs)
def center(G):
    G=list(G);return {g for g in G if all(comp(g,h)==comp(h,g) for h in G)}

def main():
    pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)}
    adj=[[False]*40 for _ in range(40)]
    for i,j in itertools.combinations(range(40),2):
        if symp(pts[i],pts[j])==0:adj[i][j]=adj[j][i]=True
    lines=[frozenset(c) for c in itertools.combinations(range(40),4) if all(adj[i][j] for i,j in itertools.combinations(c,2))];li={L:i for i,L in enumerate(lines)}
    assert len(pts)==len(lines)==40 and 0 in lines[0]
    def lperm(g):return tuple(li[frozenset(g[x] for x in L)] for L in lines)
    def trans(v):
        out=[]
        for x in pts:
            w=symp(x,v);out.append(pi[canon(tuple((x[t]+w*v[t])%3 for t in range(4)))])
        return tuple(out)
    PSp=closure([trans(v) for v in pts]);assert len(PSp)==25920
    pstab={g for g in PSp if g[0]==0};lstab={g for g in PSp if lperm(g)[0]==0};assert len(pstab)==len(lstab)==648
    pencil=sorted(l for l,L in enumerate(lines) if 0 in L);online=sorted(lines[0]);assert len(pencil)==len(online)==4
    I4=tuple(range(4));pimg={};limg={}
    for g in pstab:
        lp=lperm(g);pimg[g]=tuple(pencil.index(lp[l]) for l in pencil)
    for g in lstab:limg[g]=tuple(online.index(g[p]) for p in online)
    Pimage=set(pimg.values());Limage=set(limg.values())
    Pker={g for g,s in pimg.items() if s==I4};Lker={g for g,s in limg.items() if s==I4}
    assert len(Pimage)==12 and Counter(order(s) for s in Pimage)==Counter({3:8,2:3,1:1}) # A4
    assert len(Limage)==24 and Counter(order(s) for s in Limage)==Counter({2:9,3:8,4:6,1:1}) # S4
    assert len(Pker)==54 and len(Lker)==27
    # Standard C2 positive-root U, aligned to the BT865 chamber (point0,line0).
    I=np.eye(4,dtype=int)%3
    def E(i,j):M=np.zeros((4,4),dtype=int);M[i,j]=1;return M
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)]
    def mperm(M):return tuple(pi[canon(tuple(map(int,(M@np.array(x,dtype=int))%3)))] for x in pts)
    rg0=[mperm((I+Z)%3) for Z in X];U0=closure(rg0);assert len(U0)==81
    fixedp=[p for p in range(40) if all(g[p]==p for g in U0)];fixedl=[l for l in range(40) if all(lperm(g)[l]==l for g in U0)];assert fixedp==fixedl==[13]
    gmap=next(g for g in PSp if g[13]==0 and lperm(g)[13]==0);gi=invp(gmap);conj=lambda h:comp(comp(gmap,h),gi)
    r=[conj(x) for x in rg0];Hstate=closure([r[0],r[2]]);Hflat=closure([r[1],r[2],r[3]])
    assert len(Hstate)==len(Hflat)==27
    assert Hflat==Lker
    assert Hstate==derived(Pker)
    assert Hstate < Pker and len(Pker)//len(Hstate)==2
    assert len(center(Pker))==3 and center(Pker)==center(Hstate)
    assert Counter(order(g) for g in Hstate)==Counter({3:26,1:1})
    assert Counter(order(g) for g in Hflat)==Counter({3:26,1:1})
    # Exact quotient order census identifies pstab/Hstate as SL(2,3).
    unseen=set(pstab);cosets=[]
    while unseen:
        g=next(iter(unseen));C={comp(g,h) for h in Hstate};cosets.append(C);unseen-=C
    def qorder(C):
        g=next(iter(C));x=tuple(range(40))
        for n in range(1,20):
            x=comp(g,x)
            if x in Hstate:return n
        raise RuntimeError
    qc=Counter(qorder(C) for C in cosets)
    assert qc==Counter({6:8,3:8,4:6,2:1,1:1})
    out={'pass':5128,'status':'THEOREM_BT865_TORSOR_GROUP_GAUGE_CLOSED',
         'point_parabolic':{'order':648,'pencil_image':'A4','image_order':12,'image_order_census':dict(Counter(order(s) for s in Pimage)),
                            'pencil_kernel_order':54,'kernel_derived_order':27,'kernel_derived_equals_root_H27':True,
                            'kernel_center_order':3,'quotient_by_H27':'SL(2,3)','quotient_order_census':dict(qc)},
         'line_parabolic':{'order':648,'line_point_image':'S4','image_order':24,'image_order_census':dict(Counter(order(s) for s in Limage)),
                           'kernel_order':27,'kernel_equals_root_F3_3':True},
         'synthesis':'After the common BT865/Pass5105 chamber alignment, the flat line-program torsor is literally the S4 local-action kernel. The curved point-state H27 is literally the derived/O3 subgroup of the 54-element A4 pencil kernel; the hidden central C2 is the center of the SL(2,3) Levi factor and is invisible on the four pencil directions.',
         'boundary':'The torsor subgroups are now canonical at group level. BT865 still uses three deterministic cycle seeds to choose a free rank-3 group-algebra basis of H1; this pass does not make those three seed copies canonical.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
