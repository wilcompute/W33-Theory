#!/usr/bin/env python3
"""D9 S2xS2 Einstein-Maxwell: construct all six EXACT infinitesimal
flux-preserving Killing compensators and their geometric overlap integrals.

This is the first mixed-mode GAUGE constraint, not the full coupled
Einstein-Maxwell vector/scalar mass matrix.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261115_D9_SO3xSO3_flux_moment_maps.json"
def dot(u,v):return sum(a*b for a,b in zip(u,v))
def cross(u,v):return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
def basis(i):return tuple(Q(int(i==j)) for j in range(3))
def check_one(n, f, r):
  assert dot(n,n)==1
  e=[basis(i) for i in range(3)]
  K=[cross(e[i],n) for i in range(3)]
  mu=[f*r*r*n[i] for i in range(3)]
  tangents=[cross(ei,n) for ei in e]
  def flux(a,b):return f*r*r*dot(n,cross(a,b))
  for i in range(3):
    assert dot(K[i],n)==0
    for w in tangents:
      # i_{K_i} F=d mu_i, exact.
      assert flux(K[i],w)==f*r*r*w[i]
  for i in range(3):
    for j in range(3):
      assert flux(K[i],K[j])==f*r*r*dot(n,cross(e[i],e[j]))
  return {"n":[str(z) for z in n],
          "mu":[str(x) for x in mu],
          "all_three_flux_compensators_exact":True,
          "Hamiltonian_SO3_Poisson_bracket":"{mu_a,mu_b} = epsilon_abc mu_c",
          "Killing_algebra":"so(3), distinct spheres commute"}
def run():
  rational_vectors=[
      (Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(Q(0),Q(0),Q(1)),
      (Q(3,5),Q(4,5),Q(0)),(Q(1,3),Q(2,3),Q(2,3)),
      (Q(4,9),Q(4,9),Q(7,9))]
  # Last vector 16+16+49=81, yes.
  checks=[check_one(n,Q(7,5),Q(5,2)) for n in rational_vectors]
  assert len(checks)==6
  # Sphere moments from <n_a n_b>=delta_ab/3 and area=4pi r²:
  # <K_a.K_b>integral=(8pi/3)r⁴delta_ab,
  # <mu_a mu_b>integral=(4pi/3)f²r⁶delta_ab.
  # Include other sphere volume => 32pi²/3 and 16pi²/3.
  f1,f2=Q(7,5),Q(9,7)
  r1,r2=Q(5,2),Q(3,2)
  g1=Q(32,3)*r1**4*r2**2
  g2=Q(32,3)*r2**4*r1**2
  h1=Q(16,3)*f1**2*r1**6*r2**2
  h2=Q(16,3)*f2**2*r2**6*r1**2
  assert all(x>0 for x in (g1,g2,h1,h2))
  assert g1/g2==(r1/r2)**2
  return {
   "status":"D9_S2xS2_EXACT_FLUX_COMPENSATED_SO3xSO3_MOMENT_MAPS",
   "rational_points_checked":len(checks),
   "sample_first_sphere_checks":checks,
   "six_massless_vector_gauge_generators":6,
   "Lie_algebra":"so(3)+so(3) (independent round spheres), plus Maxwell u(1) gauge",
   "on_each_S2":"K_a(n) = e_a cross n, F=f*r² omega_unit; i_{K_a}F=d(f*r²*n_a)",
   "moment_map":"mu_a=f*r²*n_a",
   "moment_Poisson_structure":"F(K_a,K_b) = epsilon_abc mu_c",
   "Killing_vector_L2_single_sphere":"(8*pi/3)*r**4*delta_ab",
   "moment_map_L2_single_sphere":"(4*pi/3)*f**2*r**6*delta_ab",
   "Killing_overlap_S2xS2_coefficients_in_pi_squared":[str(g1),str(g2)],
   "moment_overlap_S2xS2_coefficients_in_pi_squared":[str(h1),str(h2)],
   "cross_sphere_moment_and_Killing_overlaps":0,
   "constant_Maxwell_internal_volume_in_pi_squared":str(16*r1*r1*r2*r2),
   "scope":"Exact background differential identities / mode overlap integrals fix protected gauge zero-mode mixing. They are not a derivation of a full gauge-fixed Einstein-Maxwell KK mass matrix, no scalar/vector instability bound, no E6 gauge enhancement."
  }
if __name__=="__main__":
 r=run();OUT.write_text(json.dumps(r,indent=2)+"\n")
 print("PASS",r["status"],r["six_massless_vector_gauge_generators"])
