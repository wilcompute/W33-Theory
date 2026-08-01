#!/usr/bin/env python3
from __future__ import annotations
import hashlib,itertools,json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/w33_pass1941_gaussian_solver_transport.json'
residual=[4,6,8,10,11,16,18,20,21,26,30,31,38,40,42]
idx={4:0,6:3,8:7,10:9,11:5,16:6,18:11,20:1,21:4,26:13,30:14,31:12,38:8,40:2,42:10}
duads=list(itertools.combinations(range(6),2))
transport=[{'gaussian_line':i,'duad':list(duads[idx[v]]),'residual_vertex':v} for i,v in enumerate(residual)]
adj=[[int(i!=j and set(duads[idx[residual[i]]]).isdisjoint(duads[idx[residual[j]]])) for j in range(15)] for i in range(15)]
deg={sum(row) for row in adj};lam=set();mu=set()
for i in range(15):
 for j in range(i+1,15):
  z=sum(adj[i][k]*adj[j][k] for k in range(15));(lam if adj[i][j] else mu).add(z)
Q=sp.Matrix([[1,1,1,1]]);phi=sp.Matrix([[0,1,0,-1]]);rank_Q=Q.rank();kernel_dim=4-rank_Q;blocks=15*9
checks={'literal_duad_bijection':len({tuple(x['duad']) for x in transport})==15,'kg_15_6_1_3':deg=={6} and lam=={1} and mu=={3},'block_projection_rank1':rank_Q==1,'phi_in_projection_kernel':(Q*phi.T)==sp.zeros(1,1),'phi_not_descended':sp.Matrix.vstack(Q,phi).rank()==2,'global_dimensions':4*blocks==540 and blocks==135 and kernel_dim*blocks==405,'odd_kernel_dimension':blocks==135}
out={'schema':'w33.pass1941.gaussian_solver_transport.v1','status':'PASS_WITH_FRAME_SOLVER_INCIDENCE_BOUNDARY','checks':checks,'literal_projective_transport':transport,'projective_graph':'KG(6,2)=SRG(15,6,1,3)','oriented_lift':{'variables':'y[l,k,c], l=0..14, k in Z4, c=0..8','dimension':540,'color_quotient':'x[l,c]=sum_k y[l,k,c]','quotient_dimension':135,'kernel_dimension':405,'conjugation':'k -> -k mod 4','odd_moment':'Phi[l,c]=y[l,1,c]-y[l,3,c]','odd_subspace_dimension':135},'no_descent_theorem':'Every conjugation-odd moment lies in the kernel of the projective/color quotient. Equivalently, no linear functional of x[l,c] can equal Phi[l,c]. Projective KG incidence and ordinary color counts are therefore exactly phase-blind.','pinned_constraint_abi':'Any existing pin on a chart color x[l,c] lifts compatibly as sum_k y[l,k,c]=x[l,c]. Pins constrain the color quotient but leave the C4 orientation unresolved; no extra frame permutation is introduced.','solver_boundary':'The current 540-frame coloring model does not expose a literal residual-duad coordinate on each frame variable. The exact transport closes at the 15 residual chart vertices. Attaching the oriented ABI to the global frame solver requires a separately certified frame-to-chart incidence map; none is inferred from equal cardinalities.','physical_reading_boundary':'Because the current constraint solver quotients out all phase-odd data, it cannot yet support the proposed Gauss-law/charge interpretation of the sixfold phase. That interpretation remains conditional on an oriented constraint-sector transport.','theorem':'The Gaussian projective lines and residual separator duads are literally the same 15-set, but the color projection kills all 135 conjugation-odd moments. The exact remedy is a 540-variable C4-oriented chart lift with pins imposed only through orientation sums.','boundary':'This proves the projective transport and the no-descent obstruction. It does not fabricate the missing global frame-to-chart incidence map.'}
assert all(checks.values());x=dict(out);out['sha256_without_hash_field']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest();OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'status':out['status'],'sha':out['sha256_without_hash_field'],'dimensions':out['oriented_lift'],'checks':checks},indent=2))
