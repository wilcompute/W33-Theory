#!/usr/bin/env python3
"""BT521: Eisenstein-Hurwitz 144 Filter Theorem.

Executes next-step branch 3.

BT518 built the 144-state Eisenstein x Hurwitz pre-fold shell C6 x H24.
BT514 found the odd/chiral Xmin sector has rank 120 and a rank-24 coupling
bridge.  Here we build a minimal radial-balance filter on R^6 tensor R^24:

Let J6 be the all-ones projection on the Eisenstein shell.  The subspace
constant on the Eisenstein factor has dimension 24.  Its orthogonal complement
has dimension (6-1)*24 = 120.

Thus:
    144 = 120 balanced states + 24 bridge states.

This is a negative-control-compatible filter: it does not claim the raw
Eisenstein-Hurwitz graph spectrum equals W33; it shows the simplest radial
phase-balance constraint that separates exactly the BT514 120 odd/chiral rank
from the 24 even/odd coupling bridge.
"""
from __future__ import annotations

import itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
import networkx as nx
import numpy as np

def hurwitz_vertices():
    verts=[]
    for i in range(4):
        for s in (-1,1):
            v=[Fraction(0) for _ in range(4)]; v[i]=Fraction(s); verts.append(tuple(v))
    for signs in itertools.product((-1,1), repeat=4): verts.append(tuple(Fraction(s,2) for s in signs))
    return verts

def dist2(a,b): return sum((a[i]-b[i])**2 for i in range(4))

def main()->dict:
    E=nx.cycle_graph(6); Hverts=hurwitz_vertices(); H=nx.Graph(); H.add_nodes_from(range(24))
    for i,j in itertools.combinations(range(24),2):
        if dist2(Hverts[i],Hverts[j])==1: H.add_edge(i,j)
    assert H.number_of_edges()==96 and sorted(dict(H.degree()).values())==[8]*24
    n=144
    J6=np.ones((6,6),dtype=float)/6
    I6=np.eye(6); I24=np.eye(24)
    Bridge=np.kron(J6,I24)
    Balanced=np.kron(I6-J6,I24)
    assert np.allclose(Bridge@Bridge,Bridge)
    assert np.allclose(Balanced@Balanced,Balanced)
    assert np.allclose(Bridge@Balanced,0)
    assert np.allclose(Bridge+Balanced,np.eye(n))
    rank_bridge=np.linalg.matrix_rank(Bridge)
    rank_bal=np.linalg.matrix_rank(Balanced)
    assert (rank_bridge,rank_bal)==(24,120)

    # Product graph adjacency and how filter sectors interact.
    A_E=nx.to_numpy_array(E,dtype=float); A_H=nx.to_numpy_array(H,dtype=float)
    A_cart=np.kron(A_E,I24)+np.kron(I6,A_H)
    # J6 commutes with C6, so the filter is invariant for cartesian shell dynamics.
    assert np.allclose(A_cart@Bridge,Bridge@A_cart)
    assert np.allclose(A_cart@Balanced,Balanced@A_cart)

    # Tensor graph also respects the split because J6 commutes with C6.
    A_tensor=np.kron(A_E,A_H)
    assert np.allclose(A_tensor@Bridge,Bridge@A_tensor)
    assert np.allclose(A_tensor@Balanced,Balanced@A_tensor)

    results={
      'theorem':'BT521 Eisenstein-Hurwitz 144 Filter Theorem',
      'pre_fold_shell':{'Eisenstein_vertices':6,'Hurwitz_vertices':24,'product_states':144},
      'radial_balance_filter':{'bridge_projector':'J6 tensor I24','balanced_projector':'(I6-J6) tensor I24','bridge_rank':int(rank_bridge),'balanced_rank':int(rank_bal),'identity':'144 = 24 + 120'},
      'invariance':{'cartesian_product_dynamics_preserves_filter':True,'tensor_product_dynamics_preserves_filter':True},
      'comparison_to_BT514':{'balanced_rank_120':'matches odd/chiral rank','bridge_rank_24':'matches even-odd coupling rank','negative_control':'filter gives dimensions only; W33 quadrangle incidence supplies actual spectra'},
      'substrate_reading':{'144':'Eisenstein x Hurwitz pre-fold shell','24':'Eisenstein-radial constant bridge / tetra flags','120':'Eisenstein-balanced shell / odd chiral rank','6_minus_1':'five nonconstant Eisenstein modes times 24 Hurwitz states'}
    }
    out=Path('data/PART_BT521_EISENSTEIN_HURWITZ_144_FILTER_results.json'); out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
