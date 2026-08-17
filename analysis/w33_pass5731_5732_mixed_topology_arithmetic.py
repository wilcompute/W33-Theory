#!/usr/bin/env python3
"""Bonkers Pass5731--5732: mixed Z3/Z2 extensions and p=2/p=3 arithmetic bridge."""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT31=ROOT/'data/PART_W33_PASS5731_Z3_Z2_MIXED_EXTENSION_TOPOLOGY.json';OUT32=ROOT/'data/PART_W33_PASS5732_P2_P3_DETERMINANT_ARITHMETIC_BRIDGE.json'
def det3(M):return (int(M[0,0])*int(M[1,1])-int(M[0,1])*int(M[1,0]))%3
def gl23():
 out=[]
 for a,b,c,d in itertools.product(range(3),repeat=4):
  M=np.array([[a,b],[c,d]],int)
  if det3(M):out.append(M)
 return out

def main():
 w=np.exp(2j*np.pi/3);Z=np.diag([1,w,w*w]);assert np.linalg.norm(Z.conj()-np.linalg.matrix_power(Z,2))<1e-8
 out31={'pass':5731,'status':'BONKERS_Z3xZ2_MIXED_TOPOLOGY_NO_GO__CENTRAL_EXTENSION_SPLITS_BUT_COMPLEX_CONJUGATION_CAN_FORM_S3_SEMIDIRECT_SYMMETRY',
  'central_extension_cohomology':{'H2_C3_with_C2_trivial':0,'H2_C2_with_C3_trivial':0,'reason':'For trivial cyclic action H^2(C_n,A)=A/nA; multiplication by3 is invertible on C2 and by2 is invertible on C3.','consequence':'No nontrivial mixed central extension exists. Independent Z3 and Z2 labels give the split product C3 x C2 ~= C6, with no new coupling invariant.'},
  'noncentral_escape':{'Aut_C3':'C2 by inversion','qutrit_K_action':'complex conjugation K sends Z->Z^-1','semidirect_group':'C3:C2 ~= S3','boundary':'Relevant only if the deck/class-D conjugation operation is explicitly identified with qutrit K across a common tensor carrier. Pass5710 alone does not provide that cross-carrier map.'},
  'pfaffian_result':'Pass5710 already gives identical Pfaffian parity for the two deck magnetic rays; adjoining an independent Z3 label does not manufacture a new Pfaffian split.','physics_boundary':'No interacting topological-superconductor/anomaly claim.'}
 G=gl23();hist={1:0,2:0}
 for M in G:hist[det3(M)]+=1
 assert len(G)==48 and hist=={1:24,2:24}
 out32={'pass':5732,'status':'BONKERS_P2_P3_ARITHMETIC_BRIDGE_REDUCES_TO_ORIENTATION_DETERMINANT_HINGE__NO_CANONICAL_CRT_MIXING_OF_COHOMOLOGY_CLASSES',
  'primary_no_go':{'Hom_C2_C3':0,'Hom_C3_C2':0,'CRT':'C6 ~= C2 x C3 canonically splits into primary components; CRT packages independent data but does not create an interaction','consequence':'binary switching classes and ternary torsion do not acquire a canonical additive coupling merely because 6=2*3'},
  'exact_cross_prime_hinge':{'map':'det:GL(2,3)->F3^* ~= C2','kernel':'SL(2,3), order24','fiber_sizes':hist,'geometric_role':'det records preservation/reversal of the torsion alternating form','qutrit_role':'the same bit separates unitary symplectic normalizers from determinant-reversing antiunitary extended-Clifford operations'},
  'ramanujan_boundary':'No canonical repo map currently sends the binary Ramanujan switching/cohomology state space into GL(2,3) or det. The determinant is a genuine p=3 to p=2 orientation hinge, not yet a weld to the 2-lift recursion.','physics_boundary':'Arithmetic/group structure only.'}
 OUT31.write_text(json.dumps(out31,indent=2,sort_keys=True)+'\n');OUT32.write_text(json.dumps(out32,indent=2,sort_keys=True)+'\n');print(json.dumps({'5731':out31,'5732':out32},indent=2,sort_keys=True))
if __name__=='__main__':main()
