#!/usr/bin/env python3
"""Pass5219 (bonkers): q=5 root torus/cross have identical connected-L syndrome.

Pass5217 identifies the 25 P atoms of the canonical chamber star with F5^2
coordinates (a,c). Split them into the 16-atom torus T: a,c nonzero and the
9-atom coordinate cross X: a=0 or c=0. Their apartment supports are disjoint,
|T|=400 and |X|=225, with T xor X equal to the 625-apartment chamber star.
Since a chamber star is an apartment-code word, T and X necessarily have the
same L triangle syndrome. This producer freezes the much sharper local profile.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import roots,mm,mv,norm
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment,atoms
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5219_Q5_ROOT_TORUS_CROSS_L_SYNDROME_DUALITY.json'

def main():
    q=5;G=build_W(q);U,H,F=roots(q);pidx={p:i for i,p in enumerate(G['pts'])};gens=[z for h in H for z in h[1:]]
    fp=[i for i,p in enumerate(G['pts']) if all(pidx[norm(mv(g,p,F),F)]==i for g in gens)];fl=[]
    for li,L in enumerate(G['lines']):
        if all(frozenset(pidx[norm(mv(g,G['pts'][p],F),F)] for p in L)==L for g in gens):fl.append(li)
    fixed=[(p,l) for p in fp for l in fl if p in G['lines'][l]];assert len(fixed)==1;fi=G['flags'].index(fixed[0])
    support=[a for a,es in enumerate(G['apt_edges']) if fi in es];lookup={G['apartments'][a]:a for a in support};base=G['apartments'][support[0]]
    def elem(a,b,c,d):return mm(mm(mm(H[0][a],H[1][b],F),H[2][c],F),H[3][d],F)
    coord_to_ap={}
    for a,b,c,d in itertools.product(range(5),repeat=4):
        g=elem(a,b,c,d);Q=frozenset(pidx[norm(mv(g,G['pts'][p],F),F)] for p in base);coord_to_ap[(a,b,c,d)]=lookup[Q]
    acid,_=p_component_assignment(G);A,meta,_=atoms(G,acid);starset=set(support);SA=[i for i,S in enumerate(A) if S<=starset];assert len(SA)==25
    ap_to_atom={a:i for i in SA for a in A[i]};fib={}
    for x,ap in coord_to_ap.items():fib.setdefault(ap_to_atom[ap],set()).add((x[0],x[2]))
    assert all(len(v)==1 for v in fib.values());atom_ac={u:next(iter(v)) for u,v in fib.items()}
    TA={u for u,z in atom_ac.items() if z[0] and z[1]};XA=set(SA)-TA;assert (len(TA),len(XA))==(16,9)
    T=set().union(*(A[u] for u in TA));X=set().union(*(A[u] for u in XA));assert len(T)==400 and len(X)==225 and not(T&X) and T|X==starset
    Lcharts=[loc for t,loc in G['charts'] if t=='L']
    def profile(S):
        wh=Counter();sh=Counter();synbits=[]
        for ci,loc in enumerate(Lcharts):
            w=sum(a in S for a in loc.values());wh[w]+=1;z=0
            for i,j in itertools.combinations(range(1,6),2):z+=((loc[(0,i)] in S)^(loc[(0,j)] in S)^(loc[(i,j)] in S))
            if z:sh[z]+=1
            synbits.append(z)
        return wh,sh,sum(synbits)
    th,ts,tw=profile(T);xh,xs,xw=profile(X);sh,ss,sw=profile(starset)
    assert th==Counter({0:9530,4:140,3:80})
    assert xh==Counter({0:9500,1:140,2:80,5:30})
    assert sh==Counter({0:9500,5:250})
    assert ts==xs==Counter({4:100,3:64,1:40,2:16}) and tw==xw==664 and not ss and sw==0
    out={'pass':5219,'status':'THEOREM_Q5_ROOT_TORUS_CROSS_CONNECTEDL_SYNDROME_DUALITY',
      'torus_atoms':16,'cross_atoms':9,'torus_apartments':400,'cross_apartments':225,
      'partition':'T is a,c nonzero in the F5^2 P-atom grid; X is a=0 or c=0; T xor X is the chamber star.',
      'L_restriction_weight_histograms':{
        'torus':{'0':9530,'3':80,'4':140},
        'cross':{'0':9500,'1':140,'2':80,'5':30},
        'star':{'0':9500,'5':250}},
      'fundamental_L_triangle_syndrome_weight':{'torus':664,'cross':664,'star':0},
      'syndrome_active_chart_profile':{'weight1':40,'weight2':16,'weight3':64,'weight4':100},
      'connection':'The 16/9 root-metric torus/cross split is not merely an atom count: the two complementary P-atom sectors carry exactly the same connected-L syndrome. The 30 extra cross charts of local weight five are already L-cut-valid and syndrome silent.',
      'boundary':'This exact syndrome identity follows within one canonical chamber-star carrier and does not identify T or X separately as apartment-code words; neither sector has zero L syndrome.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
