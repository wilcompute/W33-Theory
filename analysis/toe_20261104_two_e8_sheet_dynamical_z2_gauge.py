#!/usr/bin/env python3
"""Dynamical Z2 plaquette and two-E8-glue sheet-exchange no-go.

Four intersheet links around C4 carry qubit-valued Z2 link fields.
H=-K Z0Z1Z2Z3 - g(sum X_i). The local Gauss operator at each
vertex is G_v=X_prev X_next. Check all [H,G_v]=0.
The Gauss-invariant subspace on ONE isolated four-cycle is 2D.
Exact ground flux expectation K/sqrt(K^2+16g^2) for g>0.
No on-link Z expectation permitted; no flux ±1 pinned at nonzero
electric mixing g. Sign(K) explicitly chooses flux; do not hide it.
A two-glue sheet qubit with full H4 sheet-exchange X has
H=-Delta X-h Z; for h0, unique equal-amplitude ground state
at Delta>0, <Z>=0; at Delta0 two degenerate sheets. No
spontaneous symmetry breaking in this finite toy.
"""
from __future__ import annotations
import math,json,itertools
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261104_two_e8_sheet_dynamical_z2_gauge.json"
I=np.eye(2);X=np.array([[0,1],[1,0]],dtype=float);Z=np.diag([1.,-1.])
def op(*args):
 out=np.array([[1.]],dtype=float)
 for a in args:out=np.kron(out,a)
 return out
def main():
 I4=np.eye(16)
 Bs=op(Z,Z,Z,Z)
 Xi=[op(*(X if i==j else I for i in range(4))) for j in range(4)]
 G=[Xi[j]@Xi[(j+1)%4] for j in range(4)]
 projector=I4.copy()
 for g in G:projector=projector@(I4+g)/2
 assert np.linalg.matrix_rank(projector,tol=1e-10)==2
 assert np.max(abs(projector@projector-projector))<1e-12
 assert np.max(abs(projector@Bs-Bs@projector))<1e-12
 assert all(np.max(abs(Bs@g-g@Bs))<1e-12 for g in G)
 assert all(np.max(abs(x@g-g@x))<1e-12 for x in Xi for g in G)
 assert all(np.max(abs(projector@Z-Z@projector))>0 for Z in [op(Z,I,I,I)])
 Q=np.linalg.eigh(projector)[1][:,-2:]
 assert np.max(abs(Q.T@projector@Q-np.eye(2)))<1e-12
 b=Q.T@Bs@Q
 e=Q.T@sum(Xi)@Q
 assert np.max(abs(b@b-np.eye(2)))<1e-12
 assert np.max(abs(e@e-16*np.eye(2)))<1e-12
 assert np.max(abs(b@e+e@b))<1e-12
 assert all(abs(float(np.trace(Q.T@Zi@Q)))<1e-12 for Zi in
            (op(Z,I,I,I),op(I,Z,I,I),op(I,I,Z,I),op(I,I,I,Z)))
 rows=[]
 for K in (-2,-1,.3,1,2):
  for g in (0,.05,.25,.5,1):
   H=-K*Bs-g*sum(Xi)
   assert all(np.max(abs(H@GG-GG@H))<1e-12 for GG in G)
   He=Q.T@H@Q
   vals,vec=np.linalg.eigh(He)
   assert abs(vals[0]+math.sqrt(K*K+16*g*g))<1e-11
   assert abs(vals[1]-math.sqrt(K*K+16*g*g))<1e-11
   psi=Q@vec[:,0]
   flux=float(np.real(psi@Bs@psi))
   if g>0:assert abs(flux-K/math.sqrt(K*K+16*g*g))<1e-10
   assert all(abs(float(psi@Zi@psi))<1e-10 for Zi in
      (op(Z,I,I,I),op(I,Z,I,I),op(I,I,Z,I),op(I,I,I,Z)))
   rows.append(dict(K_plaquette_coupling=K,g_electric_field=g,
      ground_energy=float(vals[0]),physical_gap=float(vals[1]-vals[0]),
      flux_expectation=flux,ground_link_expectation_zero=True,
      ground_flux_for_nonzero_electric_g_is_not_exact_pm_one=bool(g>0)))
 sheets=[]
 for Delta in (0,.02,.25,1):
  for h in (0,.05,.2):
   H=-Delta*X-h*Z
   eig,vec=np.linalg.eigh(H)
   if Delta==0 and h==0:
    mean=None;degenerate=True
   else:
    ground=vec[:,0];mean=float(ground@Z@ground);degenerate=False
    assert abs(mean-h/math.sqrt(Delta*Delta+h*h))<1e-12
   sheets.append(dict(exchange_tunnelling_Delta=Delta,
      explicit_sheet_bias_h=h,sheet_order_parameter_sigma_z=mean,
      ground_level_degenerate=degenerate,gap=float(eig[1]-eig[0])))
 assert all(abs(x["sheet_order_parameter_sigma_z"])<1e-12
    for x in sheets if x["exchange_tunnelling_Delta"]>0 and x["explicit_sheet_bias_h"]==0)
 result=dict(status="PASS_ACTUAL_GAUSS_COVARIANT_Z2_DYNAMICS_NO_AUTOMATIC_E8_GLUE_SELECTION",
    plaquette_edge_qubits=4,gauge_invariant_hilbert_dimension_per_C4=2,
    number_of_intersheet_C4_in_previous_icosian_model=120,
    total_physical_gauge_invariant_dimension_for_120_independent_loops="2^120",
    plaquette_operator="B=Z0*Z1*Z2*Z3",
    Gauss_generators="Gv=X_e_before X_e_after",
    action_hamiltonian="H=-K B-g sum_e X_e",
    all_Gauss_generators_commute_with_hamiltonian_exact=True,
    explicit_local_link_Z_is_gauge_odd_and_expectation_zero=True,
    ground_state_Wilson_flux_expectation_for_g_nonzero="K/sqrt(K^2+16*g^2)",
    ground_state_gap="2*sqrt(K^2+16*g^2) in Gauss+ subspace",
    no_dynamical_uniform_pi_selection_without_negative_K_or_frustration=True,
    sweep_gauge_flux=rows,
    two_glue_exchange_involution="X interchanges E8+ and E8- sheet labels",
    two_glue_sheet_hamiltonian="H=-Delta X-h Z",
    zero_bias_nonzero_Delta_ground_sheet_imbalance=0,
    finite_sheet_qubit_has_spontaneous_symmetry_breaking=False,
    explicit_h_nonzero_breaks_full_H4_sheet_swap=True,
    sheet_sweep=sheets,
    physical_boundaries="A gauge-theory toy on 120 disconnected independent squares and a SINGLE sheet-choice qubit. Not derived from photonic microscopic Hamiltonian or a four-dimensional local lattice action. No Elitzur-violating gauge-odd order parameter; no genuine macroscopic thermodynamic limit or spontaneous symmetry breaking.",
    prior_art="Wegner Z2 lattice gauge theory and Elitzur theorem classical; exact 4-edge plaquette calculation is an operational completion of the 2026-11-04 root-flux scaffold, not a new gauge theory.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(result["status"],"zero-bias symmetric",result["zero_bias_nonzero_Delta_ground_sheet_imbalance"],flush=True)
 return result
if __name__=="__main__":main()
