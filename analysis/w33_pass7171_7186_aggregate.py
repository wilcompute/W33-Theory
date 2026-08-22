#!/usr/bin/env python3
"""Aggregate/freeze Pass7171--7186.

This producer replays the previously interactive 7171--7178 statements that are
not already frozen elsewhere, reads the exact 7179--7186 sub-certificates, and
writes a compact canonical frontier certificate.  All claims are finite.  The
q=9 global 48-clique question remains open.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
import w33_pass7163_7170_e8_hexagonal_lift as b
import w33_pass7182_d4_glue_spread_code as d

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7171_7186_AGGREGATE.json'

def load(name):return json.loads((ROOT/'data'/name).read_text())
def gf2rank(rows):
    P={}
    for x0 in rows:
        x=int(x0)
        while x:
            k=x.bit_length()-1
            if k in P:x^=P[k]
            else:P[k]=x;break
    return len(P)

def root_scheme(R):
    A=np.zeros((240,240),dtype=np.int64)
    for i in range(240):
        h=Counter()
        for j in range(240):
            z=b.dot(R[i],R[j])//4;h[z]+=1
            if z==1:A[i,j]=1
        assert h==Counter({0:126,1:56,-1:56,2:1,-2:1})
    I=np.eye(240,dtype=np.int64);Z=A-56*I
    for lam in (28,8,-2,-4):Z=Z@(A-lam*I)
    assert not np.any(Z)
    return {'relations':['2','1','0','-1','-2'],'valencies':[1,56,126,56,1],
      'A_plus_spectrum':{'56':1,'28':8,'8':35,'-2':112,'-4':84},
      'eigenmatrix_P':[[1,56,126,56,1],[1,28,0,-28,-1],[1,8,-18,8,1],[1,-2,0,2,-1],[1,-4,6,-4,1]],
      'multiplicities':[1,8,35,112,84],'Bose_Mesner_dimension':5,'A_plus_generates_full_algebra':True}

def phase_firewall(e8hist):
    def canon(v):
        for x in v:
            if x%3:
                z=1 if x==1 else 2;return tuple(z*y%3 for y in v)
    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    def B(u,v):return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3
    h=Counter()
    for i,j,k in itertools.combinations(range(40),3):
        if B(P[i],P[j]) and B(P[j],P[k]) and B(P[k],P[i]):
            z=(4*B(P[i],P[j])+4*B(P[j],P[k])+4*B(P[k],P[i]))%12;h[z]+=1
    assert sum(h.values())==3240 and set(h)<={0,4,8}
    assert all(int(k)%2==1 for k,v in e8hist.items() if v)
    return {'canonical_projective_section_Pauli_triangle_histogram':{str(k):v for k,v in sorted(h.items())},
      'section_independent_obstruction':'Every Pauli/Weyl commutator edge phase is in 4*Z/12, hence every triangle holonomy is 0,4,8 mod12; E8 triangle holonomies are odd (1,3,9,11). Therefore the two cocycles cannot differ by a coboundary.',
      'correction':'The detailed 4-versus-8 multiplicities depend on the chosen projective Pauli representative section; only the subgroup/parity obstruction is promoted as canonical.'}

def center_data(adj):
    Q,partner=d.cqs(adj);P=d.pairs(partner);return Q,partner,P

def d4_micro(R,fib,Q):
    I={r:i for i,r in enumerate(R)};neg={i:I[tuple(-x for x in R[i])] for i in range(240)}
    frames=Counter();one_per=True;degree=Counter()
    for q in Q:
        roots=sorted({v for f in q for v in fib[f]});assert len(roots)==24
        degree.update([sum(1 for w in roots if b.dot(R[v],R[w])==4) for v in roots])
        lines=sorted({min(v,neg[v]) for v in roots});F=[]
        for C in itertools.combinations(lines,4):
            if all(b.dot(R[a],R[c])==0 for a,c in itertools.combinations(C,2)):F.append(C)
        frames[len(F)]+=1
        for C in F:
            owners=[]
            for line in C:
                hit=[f for f in q if line in fib[f] or neg[line] in fib[f]];assert len(hit)==1;owners+=hit
            one_per &= len(set(owners))==4
    assert frames==Counter({3:90}) and one_per and set(degree)=={8}
    # Exact spectrum on one representative D4 root graph.
    roots=sorted({v for f in Q[0] for v in fib[f]});M=sp.zeros(24)
    for i,j in itertools.combinations(range(24),2):
        if b.dot(R[roots[i]],R[roots[j]])==4:M[i,j]=M[j,i]=1
    ev={str(int(x)):int(m) for x,m in M.eigenvals().items()};assert ev=={'8':1,'4':4,'0':9,'-2':8,'-4':2}
    return {'root_graph_spectrum':ev,'positive_inner_product_degree':8,'triality_frames_per_D4':3,
      'each_triality_frame_uses_one_antipodal_pair_from_each_of_four_C6_fibres':True}

def main():
    # New subcertificates must have been generated first by the replay workflow.
    names={p:f'PART_W33_PASS{p}_'+s for p,s in [
      (7179,'D4_SCHEME_KREIN.json'),(7180,'Q9_LOCAL_EDIT_RADIUS.json'),(7181,'E6_MINUSCULE_FIBER_VOLTAGE.json'),
      (7182,'D4_GLUE_SPREAD_CODE.json'),(7183,'C3_AFFINE_AREA_COCYCLE.json'),(7184,'SPREAD_CODE_V20_V24_MODULE.json'),
      (7185,'E8_D4_CHART_ATLAS.json'),(7186,'E8_MATTER_H27_CAYLEY.json')]}
    sub={str(p):load(n) for p,n in names.items()};assert all(x['status']=='PASS' for x in sub.values())
    old=load('PART_W33_PASS7163_7170_E8_HEXAGONAL_LIFT.json');fourier=load('PART_W33_PASS7164_E8_FOURIER_ADDENDUM.json')
    R,fib,phase,radj,adj,zero,twelve,diff=b.e8_fibers();Q,partner,pairs=center_data(adj)
    # Re-freeze the two binary support ranks from the old interactive 7177 result.
    qrows=[sum(1<<x for x in q) for q in Q];prows=[sum(1<<x for x in (Q[i]|Q[j])) for i,j in pairs]
    assert gf2rank(qrows)==39 and gf2rank(prows)==15
    e8hist=old['pass_7168_z12_holonomy']['z12_holonomy_histogram']
    out={'schema':'w33.pass7171_7186.aggregate.v1','status':'PASS',
      'boundary':'Exact finite geometry/root-system/coding/local-q9 statements. The global q9 target-48 problem remains open; no physics claim follows from shared finite groups or phases.',
      'pass7171_full_E8_root_association_scheme':root_scheme(R),
      'pass7172_D4_subsystem_geometry':{'selected_D4':90,'all_E8_D4':sub['7182']['all_E8_D4'],'selected90_scheme':sub['7179']},
      'pass7173_q9_local_closure':sub['7180'],
      'pass7174_Z12_phase_firewall':phase_firewall(e8hist),
      'pass7175_E6_A2_matter_reconstruction':sub['7181'],
      'pass7176_D4_micro_triality':d4_micro(R,fib,Q),
      'pass7177_support_codes':{'90_D4_support_rank':39,'90_D4_support_code':'[40,39,2]_2 full even-weight code','45_pair_support_rank':15,'45_pair_support_code':'[40,15,8]_2'},
      'pass7178_ten_D4_spreads':{'spreads':sub['7182']['ten_D4_spreads'],'spread_pair_pattern':sub['7182']['spread_pair_pattern'],'spread_code':sub['7182']['spread_incidence_code']},
      'pass7179_7186_sources':{str(p):names[p] for p in names},
      'pass7183_affine_area':sub['7183']['theorem'],'pass7184_module_dictionary':sub['7184']['module_dictionary'],
      'pass7185_chart_atlas':sub['7185']['theorem'],'pass7186_H27_bridge':sub['7186']['E8_bridge'],
      'fourier_interface':{'full_E8_root_graph_spectrum':fourier['full_root_graph_spectrum'],'antipodal_parity':fourier['antipodal_parity']}}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','aggregate':'7171-7186','q9_global':'OPEN','H27':True}))
if __name__=='__main__':main()
