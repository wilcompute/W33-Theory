#!/usr/bin/env python3
"""Pass5697 bonkers: the internal Ramanujan network gives a uniform adjoint Laplacian gap.

For a 4-regular Ramanujan graph, every nontrivial adjacency eigenvalue satisfies
|lambda|<=2 sqrt(3). Thus the combinatorial Laplacian L=4I-A has nonconstant gap
lambda_1(L) >= 4-2 sqrt(3). For the affine su(3) site field,
L_adj = L tensor I_8. Eight global constant directions are zero modes; every
nonconstant graph mode is repeated eight times and inherits the graph gap.

This is a finite internal routing/gauge-Laplacian statement, not the Yang--Mills
mass gap or confinement theorem.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
import w33_pass5683_balanced_ramanujan_levi_lifts as p5683
import w33_pass5693_explicit_ramanujan_levels23 as p5693
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5697_RAMANUJAN_ADJOINT_LAPLACIAN_GAP.json'
RAM=2*math.sqrt(3);LOWER=4-RAM

def main():
    # Preserve the Pass5683 producer order because NEG indexes that exact edge list.
    E0=p5683.levi();neg0=set(p5683.NEG)
    E1=p5693.lift_edges(E0,80,neg0)
    best1,_=p5693.best_two_matching_signing(E1,160);E2=p5693.lift_edges(E1,160,best1[3])
    best2,_=p5693.best_two_matching_signing(E2,320);E3=p5693.lift_edges(E2,320,best2[3])
    levels=[]
    for E,n in [(E0,80),(E1,160),(E2,320),(E3,640)]:
      A=p5693.unsigned_adj(E,n);ev=np.linalg.eigvalsh(4*np.eye(n)-A)
      pos=[float(x) for x in ev if x>1e-7];gap=min(pos)
      assert gap>=LOWER-1e-7
      levels.append({'vertices':n,'scalar_laplacian_gap':gap,'adjoint_zero_modes':8,'first_positive_adjoint_eigenvalue':gap,'first_positive_adjoint_multiplicity_at_least':8})
    L0=4*np.eye(80)-p5693.unsigned_adj(E0,80);Ladj=np.kron(L0,np.eye(8))
    ev=np.linalg.eigvalsh(Ladj);assert np.sum(abs(ev)<1e-7)==8
    first=float(min(x for x in ev if x>1e-7));assert abs(first-levels[0]['scalar_laplacian_gap'])<1e-8
    out={
      'pass':5697,'status':'RAMANUJAN_INTERNAL_ADJOINT_LAPLACIAN_HAS_UNIFORM_FINITE_GRAPH_GAP_NOT_YANG_MILLS_MASS_GAP',
      'universal_bound':{'adjacency_nontrivial_radius_max':RAM,'laplacian_gap_min':LOWER},
      'operator':'L_adj=(4I-A_graph) tensor I_8 on su3-valued site fields',
      'explicit_W33_levels':levels,
      'zero_sector':'eight constant su3 directions are exact zero modes before gauge fixing; every nonconstant scalar graph mode is copied across the eight adjoint components',
      'routing_interpretation':'The expander suppresses slowly varying nonconstant internal site modes by a level-independent dimensionless graph gap.',
      'mass_gap_no_go':'A finite expander Laplacian gap is not the Yang-Mills mass gap or confinement. It has no energy units until a kinetic/metric scale is supplied and does not establish the required infinite-volume interacting gauge-theory statement.',
      'physics_boundary':'Promoted only as a finite internal graph-spectrum theorem for the linearized adjoint field.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
