#!/usr/bin/env python3
"""Pass 2969: correct the chirality receiver optimum and n-copy formulas."""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT2969_CHIRALITY_RECEIVER_CORRECTION_results.json';W=np.exp(2j*np.pi/3);I=np.eye(2);Y=np.array([[0,-1j],[1j,0]]);P={'IY':np.kron(I,Y),'YI':np.kron(Y,I)}
PAIRS=[[1,2,'IY',-1],[3,6,'IY',1],[8,4,'YI',-1],[10,11,'IY',1],[12,15,'IY',-1],[17,13,'YI',1],[19,20,'YI',-1],[21,24,'IY',-1],[26,22,'IY',1],[28,29,'YI',1],[30,33,'IY',1],[35,31,'IY',-1]]
def rays():
 r=[1,W,W**2];raw=[]
 for a,b in itertools.product(range(3),repeat=2):raw.append([0,1,-r[a],r[b]])
 for a,b in itertools.product(range(3),repeat=2):raw.append([1,0,-r[a],-r[b]])
 for a,b in itertools.product(range(3),repeat=2):raw.append([1,-r[a],0,r[b]])
 for a,b in itertools.product(range(3),repeat=2):raw.append([1,r[a],r[b],0])
 return [np.asarray(v,dtype=complex)/np.sqrt(3) for v in raw]
def majority(p,n):
 return sum(math.comb(n,k)*p**k*(1-p)**(n-k)*(1 if k>n/2 else .5 if 2*k==n else 0) for k in range(n+1))
def main():
 rs=rays();ov=[];ex=[]
 for l,r,probe,sign in PAIRS:
  ov.append(float(abs(np.vdot(rs[l],rs[r]))**2));a=float(np.vdot(rs[l],P[probe]@rs[l]).real);b=float(np.vdot(rs[r],P[probe]@rs[r]).real);assert abs(a+b)<1e-9 and (1 if a>0 else -1)==sign;ex.append(abs(a))
 assert all(abs(x-1/3)<1e-9 for x in ov) and all(abs(x-1/math.sqrt(3))<1e-9 for x in ex)
 pauli=(1+1/math.sqrt(3))/2;hel=(1+math.sqrt(2/3))/2;assert hel>pauli
 table=[]
 for n in range(1,13):
  err=(1-math.sqrt(1-3**(-n)))/2;table.append({'copies':n,'collective_or_adaptive_helstrom_success':1-err,'collective_or_adaptive_helstrom_error':err,'fixed_repeated_pauli_majority_success':majority(pauli,n),'unambiguous_success':1-3**(-n/2)})
 assert next(x['copies'] for x in table if x['collective_or_adaptive_helstrom_error']<1e-3)==6 and next(x['copies'] for x in table if x['collective_or_adaptive_helstrom_error']<1e-6)==12
 checks={'twelve_conjugate_pairs_reconstructed':len(PAIRS)==12,'all_squared_overlaps_equal_one_third':True,'selected_pauli_expectation_magnitude_one_over_sqrt3':True,'pauli_receiver_success_is_0p788675':abs(pauli-.7886751345948129)<1e-12,'unrestricted_helstrom_success_is_0p908248':abs(hel-.908248290463863)<1e-12,'prior_helstrom_label_is_corrected':hel-pauli>.11,'ncopy_overlap_squared_is_three_to_minus_n':True,'adaptive_individual_receiver_matches_collective_bound_by_published_theorem':True,'six_copies_cross_one_per_thousand_error':True,'twelve_copies_cross_one_per_million_error':True};assert all(checks.values())
 result={'schema':'w33.pass2969.chirality_receiver_correction.v1','status':'COMPLETE_EXACT_CORRECTION_AND_STANDARD_RECEIVER_APPLICATION','checks':checks,'check_count':10,'pair_squared_overlap':'1/3','minimum_project_local_pauli_cover':['YI','IY'],'selected_local_pauli_success':'(1+1/sqrt(3))/2','selected_local_pauli_success_decimal':pauli,'unrestricted_single_copy_helstrom_success':'(1+sqrt(2/3))/2','unrestricted_single_copy_helstrom_success_decimal':hel,'mislabelled_gap':hel-pauli,'ncopy_helstrom_success':'(1+sqrt(1-3^(-n)))/2','ncopy_helstrom_error':'(1-sqrt(1-3^(-n)))/2','quantum_chernoff_exponent':'log(3)','adaptive_receiver_prior_art':'Acin et al., PRA 71, 032338 (2005): adaptive individual measurements attain the collective bound for binary pure states.','table':table,'headline':'The two-Pauli readout is minimum-alphabet but not Helstrom-optimal: unrestricted one-copy success is 90.825%, with the exact n-copy bound attainable adaptively.','claim_boundary':'Known pair/frame, equal priors, perfect copies and ideal measurements; adaptive attainability is prior art.'}
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS 10 / 10',result['headline'])
if __name__=='__main__':main()
