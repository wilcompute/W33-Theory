#!/usr/bin/env python3
"""Pass 2951: the isodual map is a four-lane order-four OAM/bin quarter-turn."""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT2951_ISODUAL_OAM_QUARTER_TURN_results.json'
G=np.array([[1,1,0,1,1,0,1,0],[2,1,1,2,0,0,0,0],[1,1,0,1,0,1,0,1],[2,2,2,0,0,1,1,2]],dtype=int)%3
H=np.array([[1,1,1,1,0,0,0,0],[2,0,2,0,1,1,0,0],[2,1,1,0,2,0,1,0],[1,1,0,0,1,0,0,1]],dtype=int)%3
perm=[1,0,3,2,6,7,4,5];sign=[1,2,2,1,1,1,2,2];D=np.zeros((8,8),dtype=int)
for old,new in enumerate(perm):D[new,old]=sign[old]
msgs=np.array(list(itertools.product(range(3),repeat=4)),dtype=int);C={tuple(x) for x in msgs@G%3};dual={tuple(x) for x in msgs@H%3};image={tuple(D@np.array(x)%3) for x in C}
cycles=[];seen=set()
for i in range(8):
 if i not in seen:cycles.append([i,perm[i]]);seen|={i,perm[i]}
Dc=np.where(D==2,-1,D).astype(float);eigs=np.linalg.eigvals(Dc);ev=sorted((round(z.real,9),round(z.imag,9)) for z in eigs)
checks={'maps_code_to_dual':image==dual,'square_is_global_negation':np.array_equal(D@D%3,2*np.eye(8,dtype=int)%3),'fourth_power_identity':np.array_equal(np.linalg.matrix_power(D,4)%3,np.eye(8,dtype=int)),'four_two_mode_lanes':len(cycles)==4,'complex_eigenvalues_four_plus_i_four_minus_i':bool(sum(abs(z-1j)<1e-8 for z in eigs)==4 and sum(abs(z+1j)<1e-8 for z in eigs)==4)}
lanes=[{'lane':i,'coordinates':c,'map':f'out[{c[1]}]={sign[c[0]]}*in[{c[0]}], out[{c[0]}]={sign[c[1]]}*in[{c[1]}]','square':'global ternary negation'} for i,c in enumerate(cycles)]
out={'schema':'w33.pass2951.isodual_oam_quarter_turn.v1','status':'COMPLETE_EXACT_PHYSICAL_MAPPING_PROPOSAL','checks':checks,'check_count':len(checks),'matrix_mod3':D.tolist(),'coordinate_cycles':cycles,'lanes':lanes,'complex_eigenvalues':ev,'algebra':'D^2=-I, D^4=I','interpretation':'The encoder/check duality is a four-lane quarter-turn. Swap two bins in each lane with ternary sign controls; applying it twice gives global inversion, so encode and syndrome networks share one reciprocal mixer topology.','hardware_mapping':'four OAM lanes times two time/frequency bins; ternary negation is a mode-label inversion or calibrated phase-relabel operation','claim_boundary':'Exact finite-field wiring equivalence. Coherent optical implementation, insertion loss, and phase stability are unmeasured.'};assert all(checks.values());OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f"PASS {len(checks)}/{len(checks)}",out['algebra'])
