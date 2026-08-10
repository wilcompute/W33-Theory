#!/usr/bin/env python3
"""Pass 4747 — derive the cold selected270 spectrum representation-theoretically.

The selected270/residue cold graph is rebuilt as the 1620-edge relation.  Its
PSp vertex permutation character is decomposed with the internally reconstructed
20-class character table from Pass4745.  Each adjacency eigenspace is then given
its exact PSp character by tracing class representatives on the eigenspace.

The irrational 40-dimensional sector is isolated without guessing radicals:
its two 20-dimensional eigenspaces carry the same degree-20 irreducible.  Global
tr(A)=0 and tr(A^2)=270*12 then force the multiplicity-space polynomial
x^2-2x-12, hence eigenvalues 1±sqrt(13).
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
from w33_pass4745_invariant_h1_character import character_table,pmask
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4747_ROUTER_SPECTRAL_REPRESENTATION.json'

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    all40=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    rep=lambda x:min(int(x),int(x)^all40)
    def fib(ap):
        z=0
        for i in ap:z^=cols[i]
        return rep(z)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});assert len(selected)==270
    sidx={L:i for i,L in enumerate(selected)}
    # cold relation: selected lines intersect, but lie in different Petersen fibers;
    # equivalently use Pass4716's exact bundle split.
    from w33_pass4716_selected270_bundle_connection import build_bundle
    X=build_bundle();cold=sorted(X['cold']);A=np.zeros((270,270),dtype=float)
    for u,v in cold:A[u,v]=A[v,u]=1.0
    assert len(cold)==1620 and set(map(int,A.sum(1)))=={12}

    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    assert len(G)==25920
    def actv(x,g):return rep(pmask(rep(x),g))
    def acts(i,g):return sidx[tuple(sorted(actv(x,g) for x in selected[i]))]

    cd,sizes,chars,labels,cmap=character_table(G,gens)
    pc=[sum(acts(i,g)==i for i in range(270)) for _,_,_,g,_ in cd]
    pm=[]
    for d,ch in chars:
        z=sum(sizes[i]*pc[i]*np.conjugate(ch[i]) for i in range(20))/25920
        assert abs(z.imag)<1e-5 and abs(z.real-round(z.real))<1e-5;pm.append(int(round(z.real)))
    assert sum(chars[i][0]*pm[i] for i in range(20))==270

    vals,vecs=np.linalg.eigh(A)
    clusters=[]
    used=np.zeros(270,dtype=bool)
    for i,x in enumerate(vals):
        if used[i]:continue
        I=np.flatnonzero(np.abs(vals-x)<1e-7);used[I]=True;clusters.append((float(np.mean(vals[I])),I))
    assert len(clusters)==8
    eigrows=[]
    for lam,I in clusters:
        Q=vecs[:,I]
        ech=[]
        for _,_,_,g,_ in cd:
            p=np.array([acts(i,g) for i in range(270)],dtype=int)
            ech.append(float(np.sum(Q*Q[p,:])))
        em=[]
        for d,ch in chars:
            z=sum(sizes[k]*ech[k]*np.conjugate(ch[k]) for k in range(20))/25920
            assert abs(z.imag)<2e-4 and abs(z.real-round(z.real))<2e-4;em.append(int(round(z.real)))
        assert sum(chars[i][0]*em[i] for i in range(20))==len(I)
        eigrows.append({'eigenvalue_numeric':lam,'multiplicity':len(I),'PSp':{labels[i]:em[i] for i in range(20) if em[i]}})

    irr=[r for r in eigrows if abs(r['eigenvalue_numeric']-round(r['eigenvalue_numeric']))>1e-5]
    assert len(irr)==2 and all(r['multiplicity']==20 for r in irr)
    irr_support=[next(iter(r['PSp'])) for r in irr]
    assert irr_support[0]==irr_support[1]
    irr_label=irr_support[0]
    irr_idx=labels.index(irr_label);assert chars[irr_idx][0]==20 and pm[irr_idx]==2

    rational=[]
    for r in eigrows:
        if r in irr:continue
        lam=int(round(r['eigenvalue_numeric']));assert abs(r['eigenvalue_numeric']-lam)<1e-6
        rational.append((lam,r['multiplicity']))
    s=-sum(l*m for l,m in rational)//20
    sq=(270*12-sum(l*l*m for l,m in rational))//20
    assert 20*s==-sum(l*m for l,m in rational)
    assert 20*sq==270*12-sum(l*l*m for l,m in rational)
    prod=(s*s-sq)//2
    assert 2*prod==s*s-sq and (s,prod)==(2,-12)
    disc=s*s-4*prod;assert disc==52
    exact_factor=f"(x-12)^1 (x-8)^15 (x-2)^84 (x+1)^64 (x+4)^60 (x+6)^6 (x^2-{s}x{prod:+d})^20"

    out={'pass':4747,
      'vertex_permutation_character':{labels[i]:pm[i] for i in range(20) if pm[i]},
      'cold_graph':{'vertices':270,'edges':1620,'degree':12,'eigenspaces':eigrows},
      'irrational_sector':{'PSp_irrep':irr_label,'degree':20,'multiplicity_in_vertex_module':2,
        'adjacency_multiplicity_space_trace':s,'adjacency_multiplicity_space_determinant':prod,
        'minimal_polynomial':'x^2 - 2 x - 12','discriminant':disc,'eigenvalues':'1 ± sqrt(13)','each_graph_multiplicity':20},
      'exact_characteristic_factorization':exact_factor,
      'derivation':'PSp eigenspace characters identify the two irrational 20-spaces as the same degree-20 irreducible; tr(A)=0 and tr(A^2)=3240 force trace 2 and determinant -12 on its 2x2 multiplicity space.',
      'theorem':'The 1±sqrt(13) router eigenvalues are not an isolated numerical coincidence: they are the two eigenvalues of the cold adjacency operator on the multiplicity-two copy of the unique 20-dimensional PSp constituent. All remaining eigenspaces are decomposed into exact PSp constituents.',
      'boundary':'Exact finite representation/spectral theorem; no physical frequency or mass interpretation is attached to the radicals.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
