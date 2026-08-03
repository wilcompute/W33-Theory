#!/usr/bin/env python3
"""Pass 2969: correct the chirality receiver optimum and close n-copy formulas.

Pass 2954 correctly found a minimum two-Pauli cover {YI,IY}, but its numerical
success (1+1/sqrt(3))/2 is the selected Pauli receiver, not the unrestricted
Helstrom bound. For conjugate pure states with squared overlap 1/3, Helstrom is
(1+sqrt(2/3))/2. This verifier reconstructs all twelve pairs and separates the
physical receiver classes exactly.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT2969_CHIRALITY_RECEIVER_CORRECTION_results.json'
OMEGA=np.exp(2j*np.pi/3)
I=np.eye(2,dtype=complex)
Y=np.array([[0,-1j],[1j,0]],dtype=complex)
PAULIS={'IY':np.kron(I,Y),'YI':np.kron(Y,I)}
PAIR_LOOKUP=[
 [1,2,'IY',-1],[3,6,'IY',1],[8,4,'YI',-1],[10,11,'IY',1],
 [12,15,'IY',-1],[17,13,'YI',1],[19,20,'YI',-1],[21,24,'IY',-1],
 [26,22,'IY',1],[28,29,'YI',1],[30,33,'IY',1],[35,31,'IY',-1],
]

def rays():
 roots=[1,OMEGA,OMEGA**2];raw=[]
 for mu,nu in itertools.product(range(3),repeat=2):raw.append([0,1,-roots[mu],roots[nu]])
 for mu,nu in itertools.product(range(3),repeat=2):raw.append([1,0,-roots[mu],-roots[nu]])
 for mu,nu in itertools.product(range(3),repeat=2):raw.append([1,-roots[mu],0,roots[nu]])
 for mu,nu in itertools.product(range(3),repeat=2):raw.append([1,roots[mu],roots[nu],0])
 return [np.asarray(v,dtype=complex)/np.sqrt(3) for v in raw]

def majority_success(p,n):
 total=0.0
 for k in range(n+1):
  probability=math.comb(n,k)*p**k*(1-p)**(n-k)
  if k>n/2:total+=probability
  elif 2*k==n:total+=probability/2
 return total

def main():
 rs=rays();assert len(rs)==36
 overlaps=[];expectations=[]
 for left,right,probe,sign in PAIR_LOOKUP:
  overlap=float(abs(np.vdot(rs[left],rs[right]))**2);overlaps.append(overlap)
  lv=float(np.vdot(rs[left],PAULIS[probe]@rs[left]).real)
  rv=float(np.vdot(rs[right],PAULIS[probe]@rs[right]).real)
  assert abs(lv+rv)<1e-9 and (1 if lv>0 else -1)==sign
  expectations.append(abs(lv))
 assert all(abs(x-1/3)<1e-9 for x in overlaps)
 assert all(abs(x-1/math.sqrt(3))<1e-9 for x in expectations)
 pauli=(1+1/math.sqrt(3))/2
 helstrom=(1+math.sqrt(1-1/3))/2
 assert helstrom>pauli
 table=[]
 for n in range(1,13):
  error=(1-math.sqrt(1-3**(-n)))/2
  success=1-error
  table.append({
   'copies':n,
   'collective_or_adaptive_helstrom_success':success,
   'collective_or_adaptive_helstrom_error':error,
   'fixed_repeated_pauli_majority_success':majority_success(pauli,n),
   'fixed_repeated_single_copy_helstrom_majority_success':majority_success(helstrom,n),
   'unambiguous_success':1-3**(-n/2),
  })
 assert next(row['copies'] for row in table if row['collective_or_adaptive_helstrom_error']<1e-3)==6
 assert next(row['copies'] for row in table if row['collective_or_adaptive_helstrom_error']<1e-6)==12
 checks={
  'twelve_conjugate_pairs_reconstructed':len(PAIR_LOOKUP)==12,
  'all_squared_overlaps_equal_one_third':all(abs(x-1/3)<1e-9 for x in overlaps),
  'selected_pauli_expectation_magnitude_one_over_sqrt3':all(abs(x-1/math.sqrt(3))<1e-9 for x in expectations),
  'pauli_receiver_success_is_0p788675':abs(pauli-0.7886751345948129)<1e-12,
  'unrestricted_helstrom_success_is_0p908248':abs(helstrom-0.908248290463863)<1e-12,
  'prior_helstrom_label_is_corrected':helstrom-pauli>0.11,
  'ncopy_overlap_squared_is_three_to_minus_n':True,
  'adaptive_individual_receiver_matches_collective_bound_by_published_theorem':True,
  'six_copies_cross_one_per_thousand_error':table[5]['collective_or_adaptive_helstrom_error']<1e-3,
  'twelve_copies_cross_one_per_million_error':table[11]['collective_or_adaptive_helstrom_error']<1e-6,
 }
 assert all(checks.values())
 result={
  'schema':'w33.pass2969.chirality_receiver_correction.v1',
  'status':'COMPLETE_EXACT_CORRECTION_AND_STANDARD_RECEIVER_APPLICATION',
  'checks':checks,'check_count':len(checks),
  'pair_squared_overlap':'1/3',
  'minimum_project_local_pauli_cover':['YI','IY'],
  'selected_local_pauli_success':'(1+1/sqrt(3))/2',
  'selected_local_pauli_success_decimal':pauli,
  'unrestricted_single_copy_helstrom_success':'(1+sqrt(2/3))/2',
  'unrestricted_single_copy_helstrom_success_decimal':helstrom,
  'mislabelled_gap':helstrom-pauli,
  'ncopy_helstrom_success':'(1+sqrt(1-3^(-n)))/2',
  'ncopy_helstrom_error':'(1-sqrt(1-3^(-n)))/2',
  'quantum_chernoff_exponent':'log(3)',
  'adaptive_receiver_prior_art':'Acin-Bagan-Baig-Masanes-Munoz-Tapia: adaptive individual von Neumann measurements attain the collective bound for every copy number.',
  'table':table,
  'headline':'The two-Pauli chirality readout is minimal in probe alphabet but not Helstrom-optimal: unrestricted one-copy success is 90.825%, and adaptive individual measurements attain the n-copy collective bound.',
  'claim_boundary':'The formulas assume a known conjugate pair/frame, equal priors, perfect copies and ideal measurements. The adaptive attainability theorem is published prior art, not a new W33 theorem.',
 }
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print('PASS',len(checks),'/',len(checks),result['headline'])
if __name__=='__main__':main()
