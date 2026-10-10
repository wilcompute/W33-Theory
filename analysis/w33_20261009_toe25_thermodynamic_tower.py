"""Round25 controlled thermodynamic W(3,q) Bose-Hubbard tower:
prove fixed-density attractive unscaled model energy density diverges;
state scaled-coupling alternatives and finite-volume vacuum uniqueness.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe25_thermodynamic_tower.json'
def params(q):
 v=2*(q+1)*(q*q+1);k=q+1
 rho=0.5;N=int(rho*v)
 # -t adjacency hopping: one-body minimum -t*k; N-boson
 # operator bound >= -t*k*N.
 # -U doublon: min >=-U*N*(N-1)/2.
 # all-on-one-site trial gives exactly -U*N*(N-1)/2.
 # Uniform N-boson Bose condensate E=-t k N-U*N(N-1)/(2v).
 threshold=2*k/((N-1)*(1-1/v))
 return dict(q=q,sites=v,degree=k,bosons=N,density=N/v,
  zero_field_PF_ground_unique=True,
  two_variational_branch_U_over_t_crossing=threshold,
  normalized_levi_nonzero_spectral_gap=1-math.sqrt(2*q)/(q+1),
  adjacency_norm_upper=k,
  fixed_U1_E0_over_v_upper=-N*(N-1)/(2*v),
  fixed_U1_E0_over_v_lower=-N*(N-1)/(2*v)-k*N/v,
  hopping_bound_ratio_to_binding=(k*N)/(N*(N-1)/2))
def run():
 table=[params(q) for q in (2,3,5,7,11,31,101)]
 assert all(r['sites']==2*(r['q']+1)*(r['q']**2+1) for r in table)
 assert all(r['two_variational_branch_U_over_t_crossing']>0 for r in table)
 assert table[-1]['two_variational_branch_U_over_t_crossing']<.001
 assert table[-1]['hopping_bound_ratio_to_binding']<.001
 for r in table:print('Q-TOWER',r['q'],'v',r['sites'],'N',r['bosons'],
   'U/t crossing',round(r['two_variational_branch_U_over_t_crossing'],6),
   'E/v bracket',round(r['fixed_U1_E0_over_v_lower'],4),
   round(r['fixed_U1_E0_over_v_upper'],4),flush=True)
 rec=dict(status='PASS',symplectic_family='classical W(3,q), q prime power',
  selected_density='rho=1/2',exact_family=table,
  binding_energy_theorem='For N bosons at fixed density N/v->rho>0, hopping t>0, attraction U>0 fixed, -U*N*(N-1)/2 -t*k*N <= E0 <= -U*N*(N-1)/2, where k=q+1, v=2(q+1)(q^2+1). Since k/v->0, E0/v^2 -> -U*rho^2/2 and E0/v -> -infinity. The unscaled attractive model has no finite extensive thermodynamic energy density.',
  comparison='Uniform N-particle condensate has E=-t*k*N-U*N*(N-1)/(2v). Localized single-vertex trial E=-U*N*(N-1)/2. The localized trial beats the uniform condensate if U/t > 2*k/((N-1)*(1-1/v)). At fixed density the threshold tends to zero since k/v->0. This trial comparison does not prove unique ordered phase or spontaneous symmetry breaking.',
  salvage_scaling='Choosing t_q=t0/k and U_q=u/v makes both kinetic O(v) and collapse energy O(v); then two trial energy densities are -t0*rho vs -u*rho^2/2, crossing near u*rho=2t0. This normalized family is an ADDITIONAL dynamical assumption, not derived from W33, and still lacks a 4D heat-kernel continuum.',
  finite_size_status='Every fixed finite q,N with t>0 has a unique symmetric ground state by Perron-Frobenius; a broken thermodynamic vacuum requires specifying external h->0 after q,N->infinity and verifying nonzero order parameter. This pass proves instability of the naive unscaled thermodynamic limit, not such a vacuum.',
  originality='Uses analytic q-family generalized quadrangle counts and a rigorous many-boson operator energy sandwich; Round21 had q-family normalized heat no-go and Round22-24 finite N=2/3 computations.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
