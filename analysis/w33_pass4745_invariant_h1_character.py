#!/usr/bin/env python3
"""Pass 4745 — ordinary H^1 character of the invariant 810-flag orbital graph.

Over characteristic zero the graph cohomology character is

    chi_H1(g) = chi_oriented_edges(g) - chi_vertices(g) + 1,

where a setwise-fixed edge contributes -1 if g reverses orientation. We
reconstruct the 20 PSp conjugacy classes and ordinary character table internally,
decompose H^1, and compute the PGSp outer action on the PSp irreducibles.

Independent execution of the Pass4713 deterministic construction fixes y=173
as the first connected self-paired valency-16 suborbit representative, avoiding
a wasteful rescan of every orbital. The resulting H^1 has no characteristic-zero
trivial constituent, even though Pass4713 gives a nonzero PGSp-fixed mod-2 deck
class. Thus the deck line is intrinsically characteristic two and has no
PGSp-invariant integral/rational lift.
"""
from __future__ import annotations
import itertools,json,math
from collections import defaultdict,deque
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4745_INVARIANT_H1_CHARACTER.json'

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

def build_flag_graph_and_group():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8);apartments=sorted(tuple(map(int,a)) for a in apartments)
    all40=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    rep=lambda x:min(int(x),int(x)^all40)
    def fib(ap):
        z=0
        for i in ap:z^=cols[i]
        return rep(z)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    flag_lifts=defaultdict(list)
    for ap in apartments:
        L=aline(ap);x=fib(ap);flag_lifts[(L,x)].append(ap)
    flags=sorted(flag_lifts);findex={f:i for i,f in enumerate(flags)};assert len(flags)==810
    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    assert len(G)==25920
    def actv(x,g):return rep(pmask(rep(x),g))
    def actL(L,g):return tuple(sorted(actv(x,g) for x in L))
    def afi(i,g):
        L,x=flags[i];return findex[(actL(L,g),actv(x,g))]
    H=[g for g in G if afi(0,g)==0];assert len(H)==32
    O={afi(173,h) for h in H};assert len(O)==16 and min(O)==173
    E={tuple(sorted((afi(0,g),afi(173,g)))) for g in G}
    B=nx.Graph();B.add_nodes_from(range(810));B.add_edges_from(E)
    assert len(E)==6480 and set(dict(B.degree()).values())=={16} and nx.is_connected(B) and nx.diameter(B)==5
    outer=build_line_perm(np.diag([1,2,1,2])%3,pts,pidx,lines,lidx)
    return pts,pidx,lines,lidx,flags,afi,E,G,gens,outer

def character_table(G,gens):
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
    cd.sort(key=lambda z:(z[0],z[1],z[2]));sizes=np.array([z[1] for z in cd],dtype=float)
    cmap={g:i for i,z in enumerate(cd) for g in z[4]};invG={g:invperm(g) for g in G}
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
        ch=d*lam/sizes
        ch=np.array([complex(round(z.real) if abs(z.real-round(z.real))<1e-7 else z.real,round(z.imag) if abs(z.imag-round(z.imag))<1e-7 else z.imag) for z in ch])
        chars.append((int(round(d)),ch))
    assert sorted(d for d,_ in chars)==[1,5,5,6,10,10,15,15,20,24,30,30,30,40,40,45,45,60,64,81]
    bydeg=defaultdict(list)
    for i,(d,ch) in enumerate(chars):
        fp=tuple((round(float(z.real),6),round(float(z.imag),6)) for z in ch);bydeg[d].append((fp,i))
    labels=[None]*20
    for d,rows in bydeg.items():
        for k,(_,i) in enumerate(sorted(rows),1):labels[i]=str(d) if len(rows)==1 else f'{d}{chr(96+k)}'
    return cd,sizes,chars,labels,cmap

def main():
    pts,pidx,lines,lidx,flags,afi,edges,G,gens,outer=build_flag_graph_and_group();cd,sizes,chars,labels,cmap=character_table(G,gens)
    edge_list=sorted(edges);cv=[];ce=[]
    for _,_,_,g,_ in cd:
        pflag=[afi(i,g) for i in range(810)];cv.append(sum(pflag[i]==i for i in range(810)));tr=0
        for u,v in edge_list:
            a,b=pflag[u],pflag[v]
            if a==u and b==v:tr+=1
            elif a==v and b==u:tr-=1
        ce.append(tr)
    ch1=[ce[i]-cv[i]+1 for i in range(20)];mult=[]
    for d,ch in chars:
        z=sum(sizes[i]*ch1[i]*np.conjugate(ch[i]) for i in range(20))/25920
        assert abs(z.imag)<1e-5 and abs(z.real-round(z.real))<1e-5;mult.append(int(round(z.real)))
    assert sum(chars[i][0]*mult[i] for i in range(20))==5671
    got={labels[i]:mult[i] for i in range(20) if mult[i]}
    expected={'5a':1,'5b':1,'10a':3,'10b':3,'15a':4,'20':1,'24':4,'30a':7,'30b':4,'30c':4,'40a':10,'40b':10,'45a':12,'45b':12,'60':11,'64':14,'81':19}
    assert got==expected
    u,v=edge_list[0];Est=[g for g in G if {afi(u,g),afi(v,g)}=={u,v}];rev=[g for g in Est if afi(u,g)==v and afi(v,g)==u]
    assert len(Est)==4 and len(rev)==2
    triv=next(i for i,(d,ch) in enumerate(chars) if d==1 and all(abs(z-1)<1e-6 for z in ch));assert mult[triv]==0
    oi=invperm(outer);classperm=[cmap[compose(outer,compose(g,oi))] for _,_,_,g,_ in cd];irouter=[]
    for i,(d,ch) in enumerate(chars):
        twisted=np.array([ch[classperm[k]] for k in range(20)]);hits=[j for j,(e,cj) in enumerate(chars) if e==d and np.max(np.abs(twisted-cj))<1e-5]
        assert len(hits)==1;irouter.append(hits[0])
    assert all(mult[i]==mult[irouter[i]] for i in range(20))
    orbits=[];seen=set()
    for i in range(20):
        if i in seen:continue
        O=sorted({i,irouter[i]});seen|=set(O)
        if any(mult[j] for j in O):orbits.append([labels[j] for j in O])
    out={'pass':4745,'graph':{'vertices':810,'edges':6480,'valency':16,'H1_dimension':5671,'deterministic_orbital_seed':173},
      'ordinary_PSp':{'irreducibles':[{'label':k,'degree':next(chars[i][0] for i in range(20) if labels[i]==k),'multiplicity':v} for k,v in sorted(got.items())],'trivial_multiplicity':0,'dimension_check':5671},
      'PGSp_outer_on_nonzero_PSp_constituents':orbits,
      'characteristic_two_boundary':{'edge_stabilizer_order':4,'endpoint_reversers':2,'H1_Q_PSp_invariants':0,'H1_Q_PGSp_invariants':0,'H1_F2_has_PGSp_fixed_deck_line':True,'deck_line_has_PGSp_invariant_integral_or_rational_lift':False,'reason':'the mod-2 orientation sign disappears; over characteristic zero the self-paired edge orbital has no invariant oriented 1-chain'},
      'theorem':'The full ordinary PSp character of the invariant-flag H^1 is 5a+5b+3(10a+10b)+4(15a)+20+4(24)+7(30a)+4(30b+30c)+10(40a+40b)+12(45a+45b)+11(60)+14(64)+19(81). It contains no trivial constituent, while the nonzero PGSp-fixed apartment deck class exists over F2. Hence that deck line is an intrinsically characteristic-two invariant with no PGSp-invariant integral/rational lift.',
      'boundary':'Exact graph/cohomology/ordinary-character statement. Modular indecomposable structure beyond the fixed deck line is not claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
