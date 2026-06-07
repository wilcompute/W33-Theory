#!/usr/bin/env python3
"""BT518: Eisenstein-Hurwitz Radial Shell Fold Theorem.

This executes Next Idea 3 from BT515.

Because the uploaded PDF body was inaccessible, this script builds minimal,
standard shell graphs suggested by its title:
  * Eisenstein unit shell: C6, radial quotient by ± gives K3.
  * Hurwitz unit shell / 24-cell: 24 vertices at minimal-distance graph degree 8,
    radial quotient by ± gives a 12-vertex graph with spectrum 8^1,0^9,(-4)^2.
  * Product address shell: Eisenstein C6 x Hurwitz 24-shell gives 144 states.

The point is not to force a match; it is to test what these radial shell folds
actually produce against W33 sectors.  The main useful hit is the 144 state
pre-fold shell and the 12 x 12 address square.  The quotient C3 x H12 has
36 states, a clean toroidal/Clifford address scale.
"""
from __future__ import annotations

import itertools, json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import networkx as nx
import numpy as np


def eig_counter(A)->dict[str,int]:
    vals=np.linalg.eigvalsh(nx.to_numpy_array(A,dtype=float) if isinstance(A,nx.Graph) else A.astype(float))
    return {str(k):int(v) for k,v in sorted(Counter(int(round(x)) for x in vals).items())}

def hurwitz_vertices():
    verts=[]
    for i in range(4):
        for s in (-1,1):
            v=[Fraction(0) for _ in range(4)]; v[i]=Fraction(s); verts.append(tuple(v))
    for signs in itertools.product((-1,1), repeat=4):
        verts.append(tuple(Fraction(s,2) for s in signs))
    assert len(set(verts))==24
    return verts

def dist2(a,b): return sum((a[i]-b[i])**2 for i in range(len(a)))

def main()->dict:
    # Eisenstein shell.
    E=nx.cycle_graph(6)
    assert E.number_of_nodes()==6 and E.number_of_edges()==6
    E_pairs=[(0,3),(1,4),(2,5)]
    E_pair_idx={v:i for i,p in enumerate(E_pairs) for v in p}
    Eq=nx.Graph(); Eq.add_nodes_from(range(3))
    for u,v in E.edges():
        a,b=E_pair_idx[u],E_pair_idx[v]
        if a!=b: Eq.add_edge(a,b)
    assert nx.is_isomorphic(Eq,nx.complete_graph(3))

    # Hurwitz/24-cell shell.
    Hverts=hurwitz_vertices(); idx={v:i for i,v in enumerate(Hverts)}
    H=nx.Graph(); H.add_nodes_from(range(24))
    for i,j in itertools.combinations(range(24),2):
        if dist2(Hverts[i],Hverts[j])==1:
            H.add_edge(i,j)
    assert H.number_of_edges()==96
    assert sorted(dict(H.degree()).values())==[8]*24

    used=set(); Hpairs=[]
    for i,v in enumerate(Hverts):
        if i in used: continue
        neg=tuple(-x for x in v); j=idx[neg]
        Hpairs.append((i,j)); used.add(i); used.add(j)
    assert len(Hpairs)==12
    Hpair_idx={v:i for i,p in enumerate(Hpairs) for v in p}
    Hq=nx.Graph(); Hq.add_nodes_from(range(12))
    mult=np.zeros((12,12),dtype=int)
    for u,v in H.edges():
        a,b=Hpair_idx[u],Hpair_idx[v]
        if a!=b:
            Hq.add_edge(a,b); mult[a,b]+=1; mult[b,a]+=1
    assert Hq.number_of_edges()==48
    assert sorted(dict(Hq.degree()).values())==[8]*12
    assert set(mult.flatten()) <= {0,2}

    # Product shells.
    prod=nx.cartesian_product(E,H)
    prod_q=nx.cartesian_product(Eq,Hq)
    assert prod.number_of_nodes()==144
    assert prod_q.number_of_nodes()==36

    # Tensor product shell for pure simultaneous phase-step coupling.
    tens=nx.tensor_product(E,H)
    assert tens.number_of_nodes()==144

    results={
        'theorem':'BT518 Eisenstein-Hurwitz Radial Shell Fold Theorem',
        'Eisenstein_shell':{'graph':'C6','vertices':6,'edges':6,'spectrum':eig_counter(E),'radial_quotient':'K3','quotient_spectrum':eig_counter(Eq)},
        'Hurwitz_shell':{'graph':'24-cell minimal-distance graph','vertices':24,'edges':96,'degree':8,'spectrum':eig_counter(H),'radial_quotient_vertices':12,'radial_quotient_edges':48,'radial_quotient_spectrum':eig_counter(Hq),'edge_multiplicity_under_quotient':'each quotient edge has multiplicity 2'},
        'product_folds':{
            'Eisenstein_x_Hurwitz_cartesian_vertices':prod.number_of_nodes(),
            'EisensteinQuotient_x_HurwitzQuotient_vertices':prod_q.number_of_nodes(),
            'Eisenstein_x_Hurwitz_tensor_vertices':tens.number_of_nodes(),
            'cartesian_product_spectrum_summary':eig_counter(prod),
            'quotient_cartesian_spectrum_summary':eig_counter(prod_q),
            'tensor_product_spectrum_summary':eig_counter(tens)},
        'comparison_to_W33':{
            'pre_fold_144':'matches BT514 odd/chiral local-axis square rank scale 12^2, but not the actual odd rank after quadrangle incidence','quotient_36':'3 radial Eisenstein directions times 12 Hurwitz antipodal directions','negative_control':'spectra do not directly reproduce W33 1,24,15,81; extra quadrangle/W33 incidence is essential'},
        'substrate_reading':{'6':'Eisenstein unit shell','24':'Hurwitz/24-cell unit shell and tetra flags','144':'6*24 pre-fold shell / 12^2 axis-square scale','36':'radial quotient address shell 3*12','96':'24-cell edge count and local dual-packet 4*24'}
    }
    out=Path('data/PART_BT518_EISENSTEIN_HURWITZ_RADIAL_SHELL_FOLD_results.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))
    return results

if __name__=='__main__': main()
