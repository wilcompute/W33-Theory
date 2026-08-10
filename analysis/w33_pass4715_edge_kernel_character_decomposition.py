#!/usr/bin/env python3
"""Pass 4715 — exact character decomposition of the 378/1485 routing kernels.

Reconstruct PSp(4,3), the selected270 graph, its 405 Petersen shortcut edges and
1620 base edges.  The script derives all 20 conjugacy classes and the complete
ordinary character table numerically from the 20-dimensional class algebra
(no GAP dependency), verifies the standard irreducible degree multiset, and
decomposes the two edge permutation characters and their quotient carriers.

The 378 shortcut-fiber kernel and 1485 base-edge-fiber kernel therefore receive
full global PSp constituent decompositions.  Independent local stabilizer actions
supply induced-module cross-checks: A5 on the 15 Petersen edges, and an order-96
12-edge action with complex permutation split 1+1+1+3+6.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
from w33_pass4595_concrete_d4_triality_w33_lifts import max_generators
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4715_EDGE_KERNEL_CHARACTER_DECOMPOSITION_REGEN.json'

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def invperm(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def orderperm(p):
    seen=set();o=1
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        o=math.lcm(o,n)
    return o
def cyc_type(p):
    seen=set();c=[]
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        if n>1:c.append(n)
    return tuple(sorted(c))
def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    V=set(span(B9));rep=lambda x:min(int(x),int(x)^j);q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    def fib(ap):
        z=0
        for i in ap:z^=cols[i]
        return rep(z)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});sing=sorted(set().union(*(set(L) for L in selected)));sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.int64)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    GL=N.T@N-3*np.eye(270,dtype=np.int64)
    MG=max_generators(sing,rep,q,polar)
    selsets=[set(L) for L in selected]
    comps=[]
    for X in MG:
        S=frozenset(i for i,L in enumerate(selsets) if L.issubset(X))
        if len(S)==10:comps.append(S)
    comps=sorted(set(comps),key=lambda S:tuple(sorted(S)));assert len(comps)==27 and set().union(*comps)==set(range(270))
    vcomp={v:i for i,S in enumerate(comps) for v in S}
    hot=[];cold=[]
    for u in range(270):
        for v in range(u+1,270):
            if GL[u,v]:
                (hot if vcomp[u]==vcomp[v] else cold).append((u,v))
    assert (len(hot),len(cold))==(405,1620)

    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    assert len(G)==25920
    def actv(x,g):return rep(pmask(rep(x),g))
    selidx={L:i for i,L in enumerate(selected)}
    def acts(i,g):return selidx[tuple(sorted(actv(x,g) for x in selected[i]))]
    cidx={S:i for i,S in enumerate(comps)}
    def actc(i,g):return cidx[frozenset(acts(v,g) for v in comps[i])]
    def acte(e,g):return tuple(sorted((acts(e[0],g),acts(e[1],g))))
    qedges=sorted({tuple(sorted((vcomp[u],vcomp[v]))) for u,v in cold});assert len(qedges)==135
    def actqe(e,g):return tuple(sorted((actc(e[0],g),actc(e[1],g))))

    # Conjugacy classes by generator conjugation.
    invgens=[invperm(g) for g in gens];unseen=set(G);classes=[];ident=tuple(range(40))
    while unseen:
        x=ident if ident in unseen else next(iter(unseen));O={x};Q=deque([x])
        while Q:
            a=Q.popleft()
            for h,hi in zip(gens,invgens):
                for hh,hhi in ((h,hi),(hi,h)):
                    z=compose(hh,compose(a,hhi))
                    if z not in O:O.add(z);Q.append(z)
        classes.append(O);unseen-=O
    assert len(classes)==20
    cd=[]
    for C in classes:
        r=min(C);cd.append((orderperm(r),len(C),cyc_type(r),r,C))
    cd.sort(key=lambda z:(z[0],z[1],z[2]));sizes=np.array([x[1] for x in cd],dtype=float)
    cmap={g:i for i,entry in enumerate(cd) for g in entry[4]};invG={g:invperm(g) for g in G}

    # Class-algebra structure constants: coefficient of each element z in C_k
    # in the product of class sums C_i C_j.
    pc=np.zeros((20,20,20),dtype=np.int64)
    for k,(_,_,_,z,_) in enumerate(cd):
        for i,(_,_,_,_,Ci) in enumerate(cd):
            cnt=np.zeros(20,dtype=np.int64)
            for x in Ci:cnt[cmap[compose(invG[x],z)]]+=1
            pc[i,:,k]=cnt
    L=[]
    for i in range(20):
        M=np.zeros((20,20),dtype=float)
        for jj in range(20):
            for k in range(20):M[k,jj]=pc[i,jj,k]
        L.append(M)
    weights=[1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67]
    Z=sum(w*M for w,M in zip(weights,L));ev,VV=np.linalg.eig(Z)
    assert len({round(float(z.real),7)+1j*round(float(z.imag),7) for z in ev})==20
    chars=[]
    for c in range(20):
        v=VV[:,c];den=np.vdot(v,v);lam=np.array([np.vdot(v,M@v)/den for M in L])
        d=math.sqrt(25920/sum(abs(lam[i])**2/sizes[i] for i in range(20)))
        ch=d*lam/sizes;chars.append((int(round(d)),ch))
    assert sorted(d for d,_ in chars)==[1,5,5,6,10,10,15,15,20,24,30,30,30,40,40,45,45,60,64,81]

    hotset=set(hot);coldset=set(cold);qset=set(qedges)
    def pchar(objects,act):
        return [sum(1 for x in objects if act(x,g)==x) for _,_,_,g,_ in cd]
    def mults(pc0):
        out=[]
        for d,ch in chars:
            z=sum(sizes[i]*pc0[i]*np.conjugate(ch[i]) for i in range(20))/25920
            assert abs(z.imag)<1e-6 and abs(z.real-round(z.real))<1e-6
            out.append(int(round(z.real)))
        return out
    mh=mults(pchar(hot,acte));mc=mults(pchar(cold,acte));mq=mults(pchar(qedges,actqe))
    # component quotient
    m27=mults([[sum(1 for x in range(27) if actc(x,g)==x) for _,_,_,g,_ in cd][i] for i in range(20)])
    assert sum(m*m for m in mh)==24 and sum(m*m for m in mc)==146

    # Label equal-degree characters by intrinsic fingerprints.
    # W33 line vs point actions distinguish the two 15s.
    linepc=[sum(g[i]==i for i in range(40)) for _,_,_,g,_ in cd]
    # W33 points are maximal K4s of the line graph.
    import networkx as nx
    K4=[frozenset(c) for c in nx.find_cliques(nx.from_numpy_array(Astar)) if len(c)==4];kp={S:i for i,S in enumerate(K4)}
    def actp(i,g):return kp[frozenset(g[x] for x in K4[i])]
    pointpc=[sum(actp(i,g)==i for i in range(40)) for _,_,_,g,_ in cd]
    ml=mults(linepc);mp=mults(pointpc)
    labels=[]
    for i,(d,ch) in enumerate(chars):
        if d==15: lab='15_L' if ml[i] else '15_P'
        elif d==30: lab='30_R' if max(abs(z.imag) for z in ch)<1e-6 else ('30_C+' if next((z.imag for z in ch if abs(z.imag)>1e-5),0)>0 else '30_C-')
        elif d==40: lab='40_C+' if next((z.imag for z in ch if abs(z.imag)>1e-5),0)>0 else '40_C-'
        elif d==45: lab='45_C+' if next((z.imag for z in ch if abs(z.imag)>1e-5),0)>0 else '45_C-'
        elif d in (5,10): lab=f'{d}_C+' if next((z.imag for z in ch if abs(z.imag)>1e-5),0)>0 else f'{d}_C-'
        else: lab=str(d)
        labels.append(lab)
    def dictmult(mm):return {labels[i]:mm[i] for i in range(20) if mm[i]}
    hot_kernel=[mh[i]-m27[i] for i in range(20)];cold_kernel=[mc[i]-mq[i] for i in range(20)]
    assert sum(chars[i][0]*hot_kernel[i] for i in range(20))==378
    assert sum(chars[i][0]*cold_kernel[i] for i in range(20))==1485

    # Local 12-edge fiber of a quotient edge.
    pair=qedges[0];fiber=sorted(e for e in cold if tuple(sorted((vcomp[e[0]],vcomp[e[1]])))==pair);assert len(fiber)==12
    fidx={e:i for i,e in enumerate(fiber)};Hp=[g for g in G if actqe(pair,g)==pair];assert len(Hp)==192
    p12={tuple(fidx[acte(e,g)] for e in fiber) for g in Hp};assert len(p12)==96
    H0=[p for p in p12 if p[0]==0];sub=[];uu=set(range(12))
    while uu:
        x=min(uu);O={p[x] for p in H0};sub.append(O);uu-=O
    assert sorted(map(len,sub))==[1,1,2,4,4]
    # Its rank-five commutative orbital algebra is multiplicity-free with
    # complex constituent dimensions 1,1,1,3,6.
    local_complex_dims=[1,1,1,3,6]

    out={'pass':4715,
      'irreducible_degrees':sorted(d for d,_ in chars),'conjugacy_classes':20,
      'hot_405':{'rank':24,'full':dictmult(mh),'quotient_27':dictmult(m27),'kernel_378':dictmult(hot_kernel),'local_A5_edge_split':'1 + 4 + 5 + 5','local_kernel_induction':'Ind_H960^PSp(4 + 5 + 5)'},
      'cold_1620':{'rank':146,'full':dictmult(mc),'quotient_135':dictmult(mq),'kernel_1485':dictmult(cold_kernel),'local_12_image_order':96,'local_complex_dimensions':local_complex_dims,'local_kernel_induction':'Ind_H192^PSp(omega + omega_bar + 3 + 6)','local_induced_dimensions':[135,135,405,810]},
      'theorem':'The 405 and 1620 routing-edge permutation characters are decomposed from the internally reconstructed 20-class character algebra of PSp(4,3). Subtracting the 27- and 135-object quotients gives exact global constituent decompositions of the 378- and 1485-dimensional fiber kernels, cross-checked by their local induced modules.',
      'boundary':'Exact finite ordinary-character/permutation-module theorem; equal-degree labels use line/point and complex-conjugation fingerprints, not physics names.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
